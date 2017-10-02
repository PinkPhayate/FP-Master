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
PRED_TYPE2 = str(args[4]) if (len(args)>4) else PRED_TYPE

def predict(ver, predict_ver,  alike_metrics):

    training_m = Metrics_Origin(ver, METRICS_DIR)
    evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)
    ens_analyzer = AUCAnalyzer(predict_ver, 'ENS', TARGET)

    predictor_rep = PredictorRepository(predict_ver, ver)

    for i in tqdm(range(ITER)):
        # NML MODEL
        predictor = predictor_rep.get_predictor('ENS', PRED_TYPE)
        if predictor is None:
            print(' predictor has not found, type: ' + PRED_TYPE)
            return
        sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample(training_m.product_df, training_m.fault)
        model = predictor.train_model(X_resampled, y_resampled)
        ev_data, dv_data = evaluate_m.get_not_modified_df()
        nml_value, _ = predictor.predict_ensemble_test_data(model, ev_data, dv_data, None)
        predictor.set_is_new_df(evaluate_m.isNew)
        predictor.set_is_modified_df(evaluate_m.isModified)
        report_df = predictor.export_report(predict_ver)
        report_df.dropna(inplace=True)

        # DST MODEL
        predictor2 = predictor_rep.get_predictor('ENS', PRED_TYPE2)
        if predictor2 is None:
            print(' predictor has not found, type: ' + PRED_TYPE2)
            return
        sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
        model = predictor2.train_model( X_resampled, y_resampled )
        ev_data, dv_data = evaluate_m.get_modified_df()
        mrg_value, _ = predictor2.predict_ensemble_test_data(model, ev_data, dv_data, None)
        predictor2.set_is_new_df(evaluate_m.isNew)
        predictor2.set_is_modified_df(evaluate_m.isModified)
        report_df2 = predictor2.export_report(predict_ver)
        report_df2.dropna(inplace=True)
        if report_df is not None and report_df2 is not None:
            report_df = pd.concat([report_df, report_df2], axis=0)
            # report_df.to_csv('test.csv')
            # raise Exception
            ens_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            ens_analyzer.calculate()
            ens_analyzer.analyze_predict_result()
        else:
            raise Exception



    # export report
    predictor_type_name = "{0}{1}".format(PRED_TYPE, PRED_TYPE2)
    ens_df = ens_analyzer.calculate_average(ITER)
    ens_analyzer.export(target_sw=TARGET, df=ens_df, predictor_type=predictor_type_name)
    ens_analyzer.export_accum_df(target_sw=TARGET)

    ens_df = ens_analyzer.calculate_num_report_averge(ITER)
    ens_analyzer.export_count_report(target_sw=TARGET, df=ens_df, predictor_type=predictor_type_name)

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
