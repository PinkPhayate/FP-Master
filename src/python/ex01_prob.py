# from lib import metrics as me
from lib.metrics import Metrics_Origin
from lib import statistic as st
from lib import ex_randf as rf
import configparser
import sys
import random
from imblearn.over_sampling import RandomOverSampler
from lib.report_analyzer import Analyzer
from lib.report_analyzer import AUCAnalyzer
from lib.repository import PredictorRepository
import pandas as pd
from tqdm import tqdm
REPORT_COLUMNS = ['predict', 'actual', 'isNew', 'isModified']
# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'
# METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'


EXECUTION_MODE = inifile.get('env', 'mode')
TARGET = ''

args = sys.argv
ITER = int(args[2]) if (len(args)>2) else (2000)
PRED_TYPE = str(args[3]) if (len(args)>3) else (2000)


def predict(ver, predict_ver,  alike_metrics):
    predictor_rep = PredictorRepository(predict_ver, ver)
    # if TARGET == 'Derby':
    #     #  Apache-Derby
    #     training_m = Metrics_Origin(ver, METRICS_DIR)
    #     evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)
    # else:
    #     # NO SERVUCE
    #     return

    training_m = Metrics_Origin(ver, METRICS_DIR)
    evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)

    # nml_analyzer = AUCAnalyzer(predict_ver, 'NML', TARGET)
    # rfn_analyzer = AUCAnalyzer(predict_ver, 'RFN', TARGET)
    # itg_analyzer = AUCAnalyzer(predict_ver, 'ITG', TARGET)
    nml_analyzer = Analyzer(predict_ver, 'NML')
    rfn_analyzer = Analyzer(predict_ver, 'RFN')
    itg_analyzer = Analyzer(predict_ver, 'ITG')

    for i in tqdm(range(ITER)):
        # NML MODEL
        predictor = predictor_rep.get_predictor('NML', PRED_TYPE)
        if predictor is None:
            print(' predictor has not found, type: ' + PRED_TYPE)
            return
        sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
        model = predictor.train_model( X_resampled, y_resampled )
        nml_value, importance = predictor.predict_proba(model, evaluate_m.product_df, evaluate_m.fault, TARGET + "-ex1nml.csv")
        predictor.set_is_new_df(evaluate_m.isNew)
        predictor.set_is_modified_df(evaluate_m.isModified)
        report_df = predictor.export_report(predict_ver)
        if report_df is not None:
            nml_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            nml_analyzer.calculate()


        # RFN MODEL
        predictor = predictor_rep.get_predictor('RFN', PRED_TYPE)
        sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
        model = predictor.train_model( X_resampled, y_resampled )
        rfn_value, importance = predictor.predict_proba(model, evaluate_m.mrg_df, evaluate_m.fault, TARGET + "-ex1rfn.csv")
        predictor.set_is_new_df(evaluate_m.isNew)
        predictor.set_is_modified_df(evaluate_m.isModified)
        report_df = predictor.export_report(predict_ver)
        if report_df is not None:
            rfn_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            rfn_analyzer.calculate()

        # INTELLIGENCE MODEL
        predictor = predictor_rep.get_predictor('ITG', PRED_TYPE)
        sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        alike_df = training_m.get_specific_df(alike_metrics)
        X_resampled, y_resampled = sm.fit_sample( alike_df, training_m.fault )
        model = predictor.train_model( X_resampled, y_resampled )
        alike_df = evaluate_m.get_specific_df(alike_metrics)
        rfn_value, importance = predictor.predict_proba(model, alike_df, evaluate_m.fault, TARGET + "-ex1itg.csv")
        predictor.set_is_new_df(evaluate_m.isNew)
        predictor.set_is_modified_df(evaluate_m.isModified)
        report_df = predictor.export_report(predict_ver)
        if report_df is not None:
            itg_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            itg_analyzer.calculate()

    # export report
    nml_df = nml_analyzer.calculate_average(ITER)
    rfn_df = rfn_analyzer.calculate_average(ITER)
    itg_df = itg_analyzer.calculate_average(ITER)
    df = pd.concat([nml_df, rfn_df, itg_df], ignore_index=True)

    nml_analyzer.export_accum_df(target_sw=TARGET)
    rfn_analyzer.export_accum_df(target_sw=TARGET)
    itg_analyzer.export_accum_df(target_sw=TARGET)

    nml_analyzer.export(target_sw=TARGET, df=df, predictor_type=PRED_TYPE)    # どのanalyzerクラスでも良い

def exp(v1, v2):
    version1 = Metrics_Origin(v1, METRICS_DIR)
    version2 = Metrics_Origin(v2, METRICS_DIR)
    print(v1+'-'+v2)
    alike_metrics = st.compare_two_versions(version1,version2)
    print(alike_metrics)
    predict(v1, v2, alike_metrics)

def __remove_report_files():
    report_file_name = REPORT_DIR + TARGET+'-aucreport.csv'
    import os
    if os.path.exists(report_file_name):
        os.remove(report_file_name)


def exp_derby():
    __remove_report_files()
    exp('10.8','10.9')
    exp('10.9','10.10')

def exp_solr():
    __remove_report_files()
    exp('4.1.0', '4.2.0')
    exp('4.2.0', '4.3.0')
    exp('4.3.0', '4.4.0')
    exp('4.4.0', '4.5.0')

if __name__ == '__main__':
    print('TARGET')
    if args[1] == "derby":
        TARGET = 'Derby'
        METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
        exp_derby()
    if args[1] == "solr":
        TARGET = 'Solr'
        METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
        exp_solr()
