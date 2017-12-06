from lib.repository import PredictorRepository
from imblearn.over_sampling import RandomOverSampler
import random
from lib import statistic as st
from lib.report_analyzer import AUCAnalyzer
from lib.report_analyzer import Analyzer
from tqdm import tqdm
from Model.metrics import Metrics
from Model import model_creator as mc
import configparser
from logging import getLogger
import pandas as pd
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

class Ex01(object):
    REPORT_COLUMNS = ['predict', 'actual', 'isNew', 'isModified']
    ITER = 50
    PRED_TYPE = 'rf'
    model = None
    METRICS_DIR = None
    TARGET = None
    alike_metrics = None
    report_logger = None
    error_logger = None

    def __init__(self, model, METRICS_DIR):
        self.model = model
        self.TARGET = model.sw_name
        self.METRICS_DIR = METRICS_DIR

    def __get_logger(self):
        inifile = configparser.SafeConfigParser()
        inifile.read('./config.ini')
        mode = inifile.get('env', 'mode')
        logger = 'debug' if mode == 'debug' else 'report'
        self.report_logger, self.error_logger = getLogger(logger+"_log"), getLogger("error_log")


    def __draw_result_boxplot(self, analyzer_a, analyzer_b, index=0):
        from lib import figure
        try:
            version_a = analyzer_a.predict_version
            version_b = analyzer_b.predict_version
            assert version_a == version_b
        except:
            self.error_logger.error('predict version was different: {}:{}'.format(version_a, version_b)); return

        REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/figure/'
        figure_name = '{}/result_wisky-{}^{}{}.png'.format(REPORT_DIR, version_a, self.PRED_TYPE, index)

        if index ==0:
            g1 = pd.DataFrame([analyzer_a.accum_accuracy0]).T
            g2 = pd.DataFrame([analyzer_b.accum_accuracy0]).T
        elif index == 2:
            g1 = pd.DataFrame([analyzer_a.accum_accuracy2]).T
            g2 = pd.DataFrame([analyzer_b.accum_accuracy2]).T
        elif index == 3:
            g1 = pd.DataFrame([analyzer_a.accum_accuracy3]).T
            g2 = pd.DataFrame([analyzer_b.accum_accuracy3]).T
        else:
            print('designated incollect index: {}'.format(index))
            return

        g1.columns = [['ORG']]
        g2.columns = [['DST']]
        hige = pd.concat([g1, g2], axis=1)
        figure.create_boxplot_seaborn(hige, figure_name)

    def predict(self):
        self.__get_logger()
        ver, predict_ver = self.model.previous_version, self.model.final_version
        pre_model = mc.retrieve_model(self.model.sw_name, self.model.final_version)
        predictor_rep = PredictorRepository(predict_ver, ver)
        training_m = Metrics(ver, self.METRICS_DIR, pre_model)
        evaluate_m = Metrics(predict_ver, self.METRICS_DIR, self.model)
        self.alike_metrics = st.compare_two_versions(training_m, evaluate_m)
        msg = "Sw: {}, version: {}, alike_metrics: {}"\
            .format(self.model.sw_name, predict_ver, self.alike_metrics)
        self.report_logger.info(msg)

        if predict_ver is None or self.TARGET is None:
            self.error_logger.error('could not create AUCAnalyzer instance.\
            predict_ver: {}, target: {}'.format(predict_ver, self.TARGET))
            return
        nml_analyzer = AUCAnalyzer(predict_ver, 'NML', self.TARGET)
        rfn_analyzer = AUCAnalyzer(predict_ver, 'RFN', self.TARGET)
        itg_analyzer = AUCAnalyzer(predict_ver, 'ITG', self.TARGET)
        # nml_analyzer = Analyzer(predict_ver, 'NML')
        # rfn_analyzer = Analyzer(predict_ver, 'RFN')
        # itg_analyzer = Analyzer(predict_ver, 'ITG')


        # acum_nml_report= pd.DataFrme([])
        # acum_rfn_report= pd.DataFrme([])
        # acum_intel_report= pd.DataFrme([])

        # for i in tqdm(range(self.ITER)):
        for i in range(self.ITER):
            # NML MODEL
            predictor = predictor_rep.get_predictor('NML', self.PRED_TYPE)
            if predictor is None:
                print(' predictor has not found, type: ' + self.PRED_TYPE)
                return
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
            # X_resampled, y_resampled = training_m.product_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            nml_value, importance = predictor.predict_test_data(model, evaluate_m.product_df, evaluate_m.fault, self.TARGET + "-ex1nml.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                nml_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                nml_analyzer.calculate()
                nml_analyzer.analyze_predict_result()

            # RFN MODEL
            predictor = predictor_rep.get_predictor('RFN', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
            # X_resampled, y_resampled = training_m.mrg_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            rfn_value, importance = predictor.predict_test_data(model, evaluate_m.mrg_df, evaluate_m.fault, self.TARGET + "-ex1rfn.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                rfn_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                rfn_analyzer.calculate()
                rfn_analyzer.analyze_predict_result()

            # INTELLIGENCE MODEL
            predictor = predictor_rep.get_predictor('ITG', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            alike_df = training_m.get_specific_df(self.alike_metrics)
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample(alike_df, training_m.fault)
            # X_resampled, y_resampled = alike_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            alike_df = evaluate_m.get_specific_df(self.alike_metrics)
            rfn_value, importance = predictor.predict_test_data(model, alike_df, evaluate_m.fault, self.TARGET + "-ex1itg.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                itg_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                itg_analyzer.calculate()
                itg_analyzer.analyze_predict_result()

        # conducy mann whitneyu test
        pvalue = st.conduct_m_whitney_test(rfn_analyzer.accum_precision0, itg_analyzer.accum_precision0)
        msg = 'sw: {}, version: {}, p-value 0 of mann whitney u test: {}'.format(self.model.sw_name, self.model.final_version, pvalue)
        self.report_logger.info(msg)
        print(msg)
        pvalue = st.conduct_m_whitney_test(rfn_analyzer.accum_precision2, itg_analyzer.accum_precision2)
        msg = 'sw: {}, version: {}, p-value 2 of mann whitney u test: {}'.format(self.model.sw_name, self.model.final_version, pvalue)
        self.report_logger.info(msg)
        print(msg)
        pvalue = st.conduct_m_whitney_test(rfn_analyzer.accum_precision3, itg_analyzer.accum_precision3)
        msg = 'sw: {}, version: {}, p-value 3 of mann whitney u test: {}'.format(self.model.sw_name, self.model.final_version, pvalue)
        self.report_logger.info(msg)
        print(msg)

        # draw voxplot graph
        self.__draw_result_boxplot(rfn_analyzer, itg_analyzer)


        # export report
        nml_df = nml_analyzer.calculate_average(self.ITER)
        rfn_df = rfn_analyzer.calculate_average(self.ITER)
        itg_df = itg_analyzer.calculate_average(self.ITER)
        df = pd.concat([nml_df, rfn_df, itg_df], ignore_index=True)
        nml_analyzer.export(target_sw=self.TARGET, df=df, predictor_type=self.PRED_TYPE)    # どのanalyzerクラスでも良い

        nml_df = nml_analyzer.calculate_num_report_averge(self.ITER)
        nml_analyzer.export_count_report(target_sw=self.TARGET, df=nml_df,
                                         predictor_type=self.PRED_TYPE)
        rfn_df = rfn_analyzer.calculate_num_report_averge(self.ITER)
        rfn_analyzer.export_count_report(target_sw=self.TARGET, df=rfn_df,
                                         predictor_type=self.PRED_TYPE)
        itg_df = itg_analyzer.calculate_num_report_averge(self.ITER)
        itg_analyzer.export_count_report(target_sw=self.TARGET, df=itg_df,
                                         predictor_type=self.PRED_TYPE)

    def predict_prob(self):
        self.__get_logger()
        ver, predict_ver = self.model.previous_version, self.model.final_version
        predictor_rep = PredictorRepository(predict_ver, ver)
        training_m = Metrics(ver, self.METRICS_DIR, self.model)
        evaluate_m = Metrics(predict_ver, self.METRICS_DIR, self.model)
        self.alike_metrics = st.compare_two_versions(training_m, evaluate_m)
        msg = "Sw: {}, version: {}, alike_metrics: {}"\
            .format(self.model.sw_name, predict_ver, self.alike_metrics)
        self.report_logger.info(msg)

        if predict_ver is None or self.TARGET is None:
            self.error_logger.error('could not create AUCAnalyzer instance.\
            predict_ver: {}, target: {}'.format(predict_ver, self.TARGET))
            return
        nml_analyzer = Analyzer(predict_ver, 'NML')
        rfn_analyzer = Analyzer(predict_ver, 'RFN')
        itg_analyzer = Analyzer(predict_ver, 'ITG')

        # for i in tqdm(range(self.ITER)):
        for i in range(self.ITER):
            # NML MODEL
            predictor = predictor_rep.get_predictor('NML', self.PRED_TYPE)
            if predictor is None:
                print(' predictor has not found, type: ' + self.PRED_TYPE)
                return
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
            # X_resampled, y_resampled = training_m.product_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            nml_value, importance = predictor.predict_proba(model, evaluate_m.product_df, evaluate_m.fault, self.TARGET + "-ex1nml.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                nml_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                nml_analyzer.calculate()
                # nml_analyzer.analyze_predict_result()

            # RFN MODEL
            predictor = predictor_rep.get_predictor('RFN', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
            # X_resampled, y_resampled = training_m.mrg_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            rfn_value, importance = predictor.predict_proba(model, evaluate_m.mrg_df, evaluate_m.fault, self.TARGET + "-ex1rfn.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                rfn_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                rfn_analyzer.calculate()
                # rfn_analyzer.analyze_predict_result()

            # INTELLIGENCE MODEL
            predictor = predictor_rep.get_predictor('ITG', self.PRED_TYPE)
            assert predictor is not None,\
                print(' predictor has not found, type: ' + self.PRED_TYPE)
            alike_df = training_m.get_specific_df(self.alike_metrics)
            sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
            X_resampled, y_resampled = sm.fit_sample(alike_df, training_m.fault)
            # X_resampled, y_resampled = alike_df.as_matrix(),\
            #     training_m.fault.as_matrix()
            model = predictor.train_model(X_resampled, y_resampled)
            alike_df = evaluate_m.get_specific_df(self.alike_metrics)
            rfn_value, importance = predictor.predict_proba(model, alike_df, evaluate_m.fault, self.TARGET + "-ex1itg.csv")
            predictor.set_is_new_df(evaluate_m.isNew)
            predictor.set_is_modified_df(evaluate_m.isModified)
            report_df = predictor.export_report(predict_ver)
            if report_df is not None:
                itg_analyzer.set_report_df(report_df[self.REPORT_COLUMNS])
                itg_analyzer.calculate()
                # itg_analyzer.analyze_predict_result()

        # export report
        nml_df = nml_analyzer.calculate_average(self.ITER)
        rfn_df = rfn_analyzer.calculate_average(self.ITER)
        itg_df = itg_analyzer.calculate_average(self.ITER)
        df = pd.concat([nml_df, rfn_df, itg_df], ignore_index=True)
        nml_analyzer.export(target_sw=self.TARGET, df=df, predictor_type=self.PRED_TYPE)    # どのanalyzerクラスでも良い

        # nml_df = nml_analyzer.calculate_num_report_averge(self.ITER)
        # nml_analyzer.export_count_report(target_sw=self.TARGET, df=nml_df,
        #                                  predictor_type=self.PRED_TYPE)
        # rfn_df = rfn_analyzer.calculate_num_report_averge(self.ITER)
        # rfn_analyzer.export_count_report(target_sw=self.TARGET, df=rfn_df,
        #                                  predictor_type=self.PRED_TYPE)
        # itg_df = itg_analyzer.calculate_num_report_averge(self.ITER)
        # itg_analyzer.export_count_report(target_sw=self.TARGET, df=itg_df,
        #                                  predictor_type=self.PRED_TYPE)
