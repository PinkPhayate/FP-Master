# from lib import metrics as me
from lib.metrics import Metrics_Origin
from lib import statistic as st
from lib import ex_randf as rf
from lib.predictor import RFPredictor
import configparser
import sys
import random
from imblearn.over_sampling import RandomOverSampler
from lib.report_analyzer import Analyzer
import pandas as pd
REPORT_COLUMNS = ['predict', 'actual', 'isNew', 'isModified']
# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
# METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'

REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'
EXECUTION_MODE = inifile.get('env', 'mode')
TARGET = ''

args = sys.argv
ITER = int(args[2]) if (len(args)>2) else (2000)

def analyze_report(report_df):
    analyzer.analyze()

def predict(ver, predict_ver,  alike_metrics):
    # if TARGET == 'Derby':
    #     #  Apache-Derby
    #     training_m = Metrics_Origin(ver, METRICS_DIR)
    #     evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)
    # else:
    #     # NO SERVUCE
    #     return

    training_m = Metrics_Origin(ver, METRICS_DIR)
    evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)
    # initialize
    acum_nml_value=0
    acum_rfn_value=0
    acum_intel_value=0

    nml_analyzer = Analyzer(predict_ver, 'NML')
    rfn_analyzer = Analyzer(predict_ver, 'RFN')
    itg_analyzer = Analyzer(predict_ver, 'ITG')


    # acum_nml_report= pd.DataFrme([])
    # acum_rfn_report= pd.DataFrme([])
    # acum_intel_report= pd.DataFrme([])

    for i in range(ITER):
        if i%500 == 0:
            print('iteration: ' +str(i))

        # NML MODEL
        rf = RFPredictor(predict_ver, ver, 'NML')
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        nml_value, importance = rf.predict_rf_saver(model, evaluate_m.product_df, evaluate_m.fault, TARGET + "-ex1nml.csv")
        acum_nml_value += nml_value
        rf.set_is_new_df(evaluate_m.isNew)
        rf.set_is_modified_df(evaluate_m.isModified)
        report_df = rf.export_report(predict_ver)
        if report_df is not None:
            nml_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            nml_analyzer.calculate()



        # RFN MODEL
        rf = RFPredictor(predict_ver, ver, 'RFN')
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        rfn_value, importance = rf.predict_rf_saver(model, evaluate_m.mrg_df, evaluate_m.fault, TARGET + "-ex1rfn.csv")
        acum_rfn_value += rfn_value
        rf.set_is_new_df(evaluate_m.isNew)
        rf.set_is_modified_df(evaluate_m.isModified)
        report_df = rf.export_report(predict_ver)
        if report_df is not None:
            rfn_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            rfn_analyzer.calculate()

        # INTELLIGENCE MODEL
        rf = RFPredictor(predict_ver, ver, 'ITG')
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        alike_df = training_m.get_specific_df(alike_metrics)
        X_resampled, y_resampled = sm.fit_sample( alike_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        alike_df = evaluate_m.get_specific_df(alike_metrics)
        rfn_value, importance = rf.predict_rf_saver(model, alike_df, evaluate_m.fault, TARGET + "-ex1itg.csv")
        acum_intel_value += rfn_value
        rf.set_is_new_df(evaluate_m.isNew)
        rf.set_is_modified_df(evaluate_m.isModified)
        report_df = rf.export_report(predict_ver)
        if report_df is not None:
            itg_analyzer.set_report_df(report_df[REPORT_COLUMNS])
            itg_analyzer.calculate()

    # export report
    report_file_name = REPORT_DIR + TARGET+'-report.csv'
    import os
    if os.path.exists(report_file_name):
        report_df = pd.read_csv(report_file_name,header=0, index_col=0)
    else:
        report_df = pd.DataFrame([])
    nml_df = nml_analyzer.calculate_average(ITER)
    rfn_df = rfn_analyzer.calculate_average(ITER)
    itg_df = itg_analyzer.calculate_average(ITER)
    df = pd.concat([nml_df, rfn_df, itg_df], ignore_index=True, axis=0)
    report_df = pd.concat([report_df, df], axis=1, ignore_index=True,)
    report_df.to_csv(report_file_name)

def exp(v1, v2):
    version1 = Metrics_Origin(v1, METRICS_DIR)
    version2 = Metrics_Origin(v2, METRICS_DIR)
    print(v1+'-'+v2)
    alike_metrics = st.compare_two_versions(version1,version2)
    print(alike_metrics)
    predict(v1, v2, alike_metrics)



def exp_derby():
    exp('10.8','10.9')
    exp('10.9','10.10')

def exp_solr():
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
