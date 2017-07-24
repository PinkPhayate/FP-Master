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
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
EXECUTION_MODE = inifile.get('env', 'mode')
TARGET = ''

args = sys.argv
ITER = int(args[2]) if (len(args)>2) else (2000)

def predict(ver, predict_ver,  alike_metrics):
    global TARGET
    if TARGET == 'Derby':
        #  Apache-Derby
        training_m = Metrics_Origin(ver, METRICS_DIR)
        evaluate_m = Metrics_Origin(predict_ver, METRICS_DIR)
    else:
        # NO SERVUCE
        return

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



if args[1] == "derby":
    TARGET = 'Derby'

version1 = Metrics_Origin('10.8', METRICS_DIR)
version2 = Metrics_Origin('10.9', METRICS_DIR)
version3 = Metrics_Origin('10.10', METRICS_DIR)
print('10.8-10.9')
alike_metrics = st.compare_two_versions(version1,version2)
print(alike_metrics)
predict('10.8', '10.9', alike_metrics)
print('10.8-10.10')
alike_metrics = st.compare_two_versions(version1,version3)
print(alike_metrics)
predict('10.8', '10.10', alike_metrics)
print('10.9-10.10')
alike_metrics = st.compare_two_versions(version2,version3)
print(alike_metrics)
predict('10.9', '10.10', alike_metrics)
