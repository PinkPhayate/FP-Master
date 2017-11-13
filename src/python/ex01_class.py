from lib.repository import PredictorRepository
from lib.report_analyzer import AUCAnalyzer
from tqdm import tqdm
from lib.metrics import Metrics_Origin
import configparser
import pandas as pd
class Ex01(object):
    REPORT_COLUMNS = ['predict', 'actual', 'isNew', 'isModified']
    ITER = 3
    PRED_TYPE = 'rf'
    model = None
    METRICS_DIR = None
    TARGET = None

    def __init__(self, model, METRICS_DIR):
        self.model = model
        self.TARGET = self.sw_name
        self.METRICS_DIR = METRICS_DIR


def predict(self):
    ver, predict_ver = self.model.pre_version, self.model.curr_version
    predictor_rep = PredictorRepository(predict_ver, ver)

    training_m = Metrics_Origin(ver, self.METRICS_DIR)
    evaluate_m = Metrics_Origin(predict_ver, self.METRICS_DIR)

    nml_analyzer = AUCAnalyzer(predict_ver, 'NML', self.TARGET)
    rfn_analyzer = AUCAnalyzer(predict_ver, 'RFN', self.TARGET)
    itg_analyzer = AUCAnalyzer(predict_ver, 'ITG', self.TARGET)
    # nml_analyzer = Analyzer(predict_ver, 'NML')
    # rfn_analyzer = Analyzer(predict_ver, 'RFN')
    # itg_analyzer = Analyzer(predict_ver, 'ITG')


    # acum_nml_report= pd.DataFrme([])
    # acum_rfn_report= pd.DataFrme([])
    # acum_intel_report= pd.DataFrme([])

    for i in tqdm(range(self.ITER)):
        # NML MODEL
        predictor = predictor_rep.get_predictor('NML', self.PRED_TYPE)
        assert predictor is not None,\
            print(' predictor has not found, type: ' + self.PRED_TYPE)
        # sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        # X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
        X_resampled, y_resampled = training_m.product_df.as_matrix(),\
            training_m.fault.as_matrix()
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
        # sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        # X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
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

        # INTELLIGENCE MODEL
        predictor = predictor_rep.get_predictor('ITG', self.PRED_TYPE)
        assert predictor is not None,\
            print(' predictor has not found, type: ' + self.PRED_TYPE)
        alike_df = training_m.get_specific_df(alike_metrics)
        # sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        # X_resampled, y_resampled = sm.fit_sample(alike_df, training_m.fault)
        X_resampled, y_resampled = training_m.mrg_df.as_matrix(),\
            training_m.fault.as_matrix()
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
