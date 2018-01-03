from lib.repository import PredictorRepository
from imblearn.over_sampling import RandomOverSampler
import random
from lib import statistic as st
from lib.report_analyzer_ex02 import AUCAnalyzer_Ex02 as AUCAnalyzer
from tqdm import tqdm
from Model.metrics import Metrics
from Model import model_creator as mc
import configparser
from logging import getLogger
import pandas as pd
from ex01_class import Ex01
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

class Ex02(Ex01):
    REPORT_COLUMNS = ['predict', 'actual', 'isNew', 'isModified']
    ITER = 10
    PRED_TYPE = 'xgb'
    model1 = None
    model2 = None
    METRICS_DIR = None
    TARGET = None
    alike_metrics = None
    report_logger = None
    error_logger = None

    def __get_logger(self):
        inifile = configparser.SafeConfigParser()
        inifile.read('./config.ini')
        mode = inifile.get('env', 'mode')
        logger = 'debug' if mode == 'debug' else 'report'
        self.report_logger, self.error_logger = getLogger(logger+"_log"), getLogger("error_log")

    def __init__(self, model1, model2, METRICS_DIR):
        '''
        model1: 学習バージョン
        model2: 予測バージョン
        '''
        self.model1 = model1
        self.model2 = model2
        self.METRICS_DIR = METRICS_DIR
        self.TARGET = self.model2.sw_name

    def predict(self, box_plotting=False, result_exporting=False):
        self.model2.set_param_dict(self.PRED_TYPE)
        self.__get_logger()
        # (sw_name, version)を２つ受け取り、それぞれの全てのメトリクスを取得する。
        training_m = Metrics(self.model1.final_version, self.METRICS_DIR, self.model1)
        evaluate_m = Metrics(self.model2.final_version, self.METRICS_DIR, self.model2)

        # alike_metricsを取得する。
        self.alike_metrics = st.compare_two_versions(training_m, evaluate_m)
        # alike_metricsでフィルターしたメトリクスを作成する。
        # フィルターをかけないモデルとかけるモデルで予測精度を比較する。

        ver, predict_ver = self.model1.final_version, self.model2.final_version
        # pre_model = mc.retrieve_model(self.model.sw_name, self.model.final_version)
        predictor_rep = PredictorRepository(predict_ver, self.model1)
        # training_m = Metrics(ver, self.METRICS_DIR, pre_model)
        # evaluate_m = Metrics(predict_ver, self.METRICS_DIR, self.model)
        # self.alike_metrics = st.compare_two_versions(training_m, evaluate_m)
        msg = "Sw: {}:{}-{}:{}, alike_metrics: {}"\
            .format(self.model1.sw_name, self.model1.final_version, self.model2.sw_name, self.model2.final_version, self.alike_metrics)
        self.report_logger.info(msg)
        print(msg)

        if predict_ver is None or self.TARGET is None:
            self.error_logger.error('could not create AUCAnalyzer instance.\
            predict_ver: {}, target: {}'.format(predict_ver, self.TARGET))
            return
        # nml_analyzer = AUCAnalyzer(predict_ver, 'NML', self.TARGET)
        rfn_analyzer = AUCAnalyzer(predict_ver, 'RFN', self.TARGET)
        dst_analyzer = AUCAnalyzer(predict_ver, 'DST', self.TARGET)

        for i in range(self.ITER):

            # RFN MODEL
            predictor = predictor_rep.get_predictor('RFN', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            # sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            # X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
            X_resampled, y_resampled = training_m.mrg_df.as_matrix(),\
                training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            rfn_value, importance = predictor.predict_test_data(model, evaluate_m.mrg_df, evaluate_m.fault, self.TARGET + "-ex1rfn.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                rfn_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                rfn_analyzer.calculate()
                rfn_analyzer.analyze_predict_result()

            # DSTRIBUTION MODEL
            predictor = predictor_rep.get_predictor('DST', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            alike_df = training_m.get_specific_df(self.alike_metrics)
            # sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            # X_resampled, y_resampled = sm.fit_sample(alike_df, training_m.fault)
            X_resampled, y_resampled = alike_df.as_matrix(),\
                training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            alike_df = evaluate_m.get_specific_df(self.alike_metrics)
            itg_value, importance = predictor.predict_test_data(model, alike_df, evaluate_m.fault, self.TARGET + "-ex1itg.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                dst_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                dst_analyzer.calculate()
                dst_analyzer.analyze_predict_result()

        # print('feature inportance: {}'.format(importance))

        # conducy mann whitneyu test
        self.conduct_mh_test(rfn_analyzer, dst_analyzer, index=0)
        self.conduct_mh_test(rfn_analyzer, dst_analyzer, index=2)
        self.conduct_mh_test(rfn_analyzer, dst_analyzer, index=3)

        # draw voxplot graph
        if box_plotting:
            # self.draw_result_boxplot(rfn_analyzer, itg_analyzer)
            pass


        # export report
        # nml_df = nml_analyzer.calculate_average(self.ITER)
        rfn_df = rfn_analyzer.calculate_average(self.ITER)
        itg_df = dst_analyzer.calculate_average(self.ITER)
        df = pd.concat([rfn_df, itg_df], ignore_index=True)
        rfn_analyzer.export(target_sw=self.TARGET, df=df, predictor_type=self.PRED_TYPE)    # どのanalyzerクラスでも良い

        # nml_df = nml_analyzer.calculate_num_report_averge(self.ITER)
        # rfn_df = rfn_analyzer.calculate_num_report_averge(self.ITER)
        # itg_df = dst_analyzer.calculate_num_report_averge(self.ITER)

        # if result_exporting:
        #     nml_analyzer.export_count_report(target_sw=self.TARGET, df=nml_df,
        #                                      predictor_type=self.PRED_TYPE)
        #     rfn_analyzer.export_count_report(target_sw=self.TARGET, df=rfn_df,
        #                                      predictor_type=self.PRED_TYPE)
        #     itg_analyzer.export_count_report(target_sw=self.TARGET, df=itg_df,
        #                                      predictor_type=self.PRED_TYPE)
