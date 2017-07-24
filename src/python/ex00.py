from lib import metrics as me
from lib import writer as w
import pandas as pd
from lib import ex_randf as rf, anova
import random
from imblearn.over_sampling import RandomOverSampler
# set environment lab or home
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'
EXECUTION_MODE = inifile.get('env', 'mode')

# set iterative number
import sys
args = sys.argv
ITER = int(args[1]) if (len(args)>1) else (2000)
list = ["Experiment1\n"]
TARGET = ''
DEBUG_MODE = False



def ex01(ver, predict_ver):
    global list
    global TARGET

    if TARGET == 'Derby':
        #  Apache-Derby
        training_m = me.Metrics_Derby(ver, METRICS_DIR)
        evaluate_m = me.Metrics_Derby(predict_ver, METRICS_DIR)

    elif TARGET == 'Adam':
        # Adam
        training_m = me.Metrics_Adam(ver)
        evaluate_m = me.Metrics_Adam(predict_ver)



    # initialize
    acum_nml_value=0
    acum_rfn_value=0
    acum_chrn_value=0
    acum_rand_value=0

    nml_importance_df = pd.DataFrame([])
    rfn_importance_df = pd.DataFrame([])
    chr_importance_df = pd.DataFrame([])

    diagram_value_list = []
    for i in range(ITER):
        if i%500 == 0:
            print('iteration: ' +str(i))
        diagram_list = []
        # NML MODEL
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        # model = rf.train_rf( training_m.product_df, training_m.fault )
        nml_value, importance = rf.predict_rf_saver(model, evaluate_m.product_df, evaluate_m.fault, TARGET + "-ex1nml.csv")
        acum_nml_value += nml_value
        diagram_list.append(nml_value)

        # RFN MODEL
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.mrg_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        rfn_value, importance = rf.predict_rf_saver(model, evaluate_m.mrg_df, evaluate_m.fault, TARGET + "-ex1rfn.csv")
        acum_rfn_value += rfn_value
        diagram_list.append(rfn_value)

        # CHRN MODEL
        sm = RandomOverSampler(ratio=0.2, random_state=random.randint(1,100))
        X_resampled, y_resampled = sm.fit_sample( training_m.process_df, training_m.fault )
        model = rf.train_rf( X_resampled, y_resampled )
        chrn_value, importance = rf.predict_rf_saver(model, evaluate_m.process_df, evaluate_m.fault, TARGET + "-ex1chn.csv")
        acum_chrn_value += chrn_value
        diagram_list.append(chrn_value)

        # RND MODEL
        size = len(evaluate_m.process_df)
        rand_df = pd.DataFrame( rf.get_random_ev(size) )
        rand_value = rf.calculate_diagram( evaluate_m.fault, rand_df )
        acum_rand_value += rand_value
        diagram_list.append(rand_value)
        diagram_value_list.append(diagram_list)

        # importance
        if EXECUTION_MODE == 'debug':
            nml_importance_df = pd.concat([nml_importance_df, pd.DataFrame(importance).T])
            rfn_importance_df = pd.concat([rfn_importance_df, pd.DataFrame(importance).T])
            chr_importance_df = pd.concat([chr_importance_df, pd.DataFrame(importance).T])

    list.append( str(acum_nml_value/ITER) )
    list.append( str(acum_rfn_value/ITER) )
    list.append( str(acum_chrn_value/ITER) )
    list.append( str(acum_rand_value/ITER) )
    list.append( '\n' )


    # save section
    df = pd.DataFrame(diagram_value_list)
    df.to_csv('../Data/Diagram_list/'+TARGET+ver+'-'+predict_ver+'ex01-diagram.csv')
    # importance save
    if EXECUTION_MODE == 'debug':
        nml_importance_df.to_csv('../Data/Research/Importance/ex01/importance-nml'+TARGET+ver+'-'+predict_ver+'ex01.csv')
        rfn_importance_df.to_csv('../Data/Research/Importance/ex01/importance-rfn'+TARGET+ver+'-'+predict_ver+'ex01.csv')
        chr_importance_df.to_csv('../Data/Research/Importance/ex01/importance-chr'+TARGET+ver+'-'+predict_ver+'ex01.csv')



if __name__ == '__main__':
    TARGET = "Derby"
    # list.append('TARGET: ' + TARGET + " with over-sampling\n")
    list.append('Derby, NML, RFN, CHR\n')
    list.append('ex01 10.9 -> 10.10')
    ex01('10.9','10.10')

    list.append('ex01 10.8 -> 10.9')
    ex01('10.8','10.9')

    list.append('ex01 10.8 -> 10.10')
    ex01('10.8','10.10')

    TARGET = "Adam"
    # list.append('TARGET: ' + TARGET + " with over-sampling\n")
    list.append('Adam, NML, RFN, CHR\n')
    list.append('ex01 v2 -> v3')
    ex01('v2','v3')

    list.append('ex01 v1 -> v2')
    ex01('v1','v2')

    list.append('ex01 v1 -> v3')
    ex01('v1','v3')
    print("done.")
    w.write_report(list)
    #
    # anova.main()
