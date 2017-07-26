# from lib import metrics as me
from lib.metrics import Metrics_Origin
from lib import statistic as st
from lib import ex_randf as rf
import configparser
import sys
import random
from imblearn.over_sampling import RandomOverSampler

# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
# METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'

EXECUTION_MODE = inifile.get('env', 'mode')
TARGET = ''

args = sys.argv
ITER = int(args[2]) if (len(args)>2) else (2000)

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
    acum_rfn_value=0
    acum_intel_value=0

    for i in range(ITER):
        if i%500 == 0:
            print('iteration: ' +str(i))

        # RFN MODEL
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        rfn_value, importance = rf.predict_rf_saver(model, evaluate_m.mrg_df, evaluate_m.fault, TARGET + "-ex1rfn.csv")

        acum_rfn_value += rfn_value
        # diagram_list.append(rfn_value)

        # INTELLIGENCE MODEL
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        alike_df = training_m.get_specific_df(alike_metrics)
        X_resampled, y_resampled = sm.fit_sample( alike_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        alike_df = evaluate_m.get_specific_df(alike_metrics)
        rfn_value, importance = rf.predict_rf_saver(model, alike_df, evaluate_m.fault, TARGET + "-ex1rfn.csv")
        acum_intel_value += rfn_value
        # diagram_list.append(rfn_value)

    print(acum_rfn_value/ITER)
    print(acum_intel_value/ITER)


def exp_derby():
    version1 = Metrics_Origin('4.1.0', METRICS_DIR)
    version2 = Metrics_Origin('4.2.0', METRICS_DIR)
    version3 = Metrics_Origin('10.10', METRICS_DIR)
    print('4.1.0-4.2.0')
    alike_metrics = st.compare_two_versions(version1,version2)
    print(alike_metrics)
    predict('4.1.0', '4.2.0', alike_metrics)
    print('4.1.0-10.10')
    alike_metrics = st.compare_two_versions(version1,version3)
    print(alike_metrics)
    predict('4.1.0', '10.10', alike_metrics)
    print('4.2.0-10.10')
    alike_metrics = st.compare_two_versions(version2,version3)
    print(alike_metrics)
    predict('4.2.0', '10.10', alike_metrics)

def exp_solr():
    version1 = Metrics_Origin('4.1.0', METRICS_DIR)
    version2 = Metrics_Origin('4.2.0', METRICS_DIR)
    version3 = Metrics_Origin('4.3.0', METRICS_DIR)
    version3 = Metrics_Origin('4.4.0', METRICS_DIR)
    version3 = Metrics_Origin('4.5.0', METRICS_DIR)
    print('4.1.0-4.2.0')
    alike_metrics = st.compare_two_versions(version1,version2)
    print(alike_metrics)
    predict('4.1.0', '4.2.0', alike_metrics)

    print('4.2.0-4.3.0')
    alike_metrics = st.compare_two_versions(version1,version3)
    print(alike_metrics)
    predict('4.2.0', '4.3.0', alike_metrics)

    print('4.3.0-4.4.0')
    alike_metrics = st.compare_two_versions(version2,version3)
    print(alike_metrics)
    predict('4.3.0', '4.4.0', alike_metrics)

    print('4.4.0-4.5.0')
    alike_metrics = st.compare_two_versions(version2,version3)
    print(alike_metrics)
    predict('4.4.0', '4.5.0', alike_metrics)

if args[1] == "derby":
    TARGET = 'Derby'
    METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
    exp_derby()
if args[1] == "solr":
    TARGET = 'Solr'
    METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
    exp_solr()
