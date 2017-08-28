from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import column_or_1d
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np
from lib import auc
# set environment lab or home
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
EXECUTION_MODE = inifile.get('env', 'mode')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'

def train_rf (ev_data, dv_data):
    # normalize
    # ev_data = (ev_data - ev_data.mean()) / ev_data.std()

    model = RandomForestClassifier(
        oob_score=True,
        class_weight='balanced',
        max_depth=3,
        n_estimators=100,
        min_samples_leaf=3
    )
    model.fit(ev_data, column_or_1d(dv_data))

    return model

def predict_rf(model, ev_data, dv_data):

    # normalize
    # ev_data = (ev_data - ev_data.mean()) / ev_data.std()

    output = model.predict_proba(ev_data)
    pred = pd.DataFrame( output ).ix[:,1:1]
    print(model.feature_importances_)
    return calculate_diagram(dv_data, pred)

def predict_rf_saver(model, ev_data, dv_data, filename):
    # save for write file about metrics and predict and actualy
    paramater = ev_data.copy()
    # normalize
    # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
    output = model.predict_proba(ev_data)
    # ev_data = pd.concat([paramater, dv_data],axis=1)
    predict = pd.DataFrame(output).ix[:,1:]
    predict.columns = [['predict']]
    df = pd.concat([paramater, predict],axis=1)
    dv_data.columns = [['actual']]
    df = pd.concat([df, dv_data.to_frame(name='actual')],axis=1)
    df['predict'] = df.apply(lambda x: float(x['predict']), axis=1)
    # df['predict'] = df[['predict']].apply(lambda x: float(x.values[0]))
    df =df.sort_values(by='predict',ascending=False)

    importance = pd.DataFrame(model.feature_importances_)
    # importance
    if EXECUTION_MODE == 'Investigation':
        # print(importance)
        # df = pd.concat([df, importance], axis=0)
        df.to_csv(METRICS_DIR+filename)
        return calculate_auc_score(dv_data, predict), model.feature_importances_
    else:
        return calculate_auc_score(dv_data, predict), model.feature_importances_
        # return calculate_diagram(dv_data, actual), model.feature_importances_


def get_random_ev(size):
    np.random.seed(seed=2019)
    rev = np.random.rand( size )
    return rev


def calculate_diagram(actual, pred):
    df = pd.concat([ actual, pred ], axis=1)
    df.columns = ['fault', 'ev_value']
    diagram_value = auc.AUC(df). circulate_auc
    return diagram_value

def calculate_auc_score(actual, pred):
    df = pd.concat([ actual, pred ], axis=1)
    df.columns = ['fault', 'ev_value']
    auc_score = roc_auc_score(df['fault'], df['ev_value'])
    return auc_score

def calculate_diagram_saver(actual, pred, filename):
    df = pd.concat([ actual, pred ], axis=1)
    df.columns = ['fault', 'ev_value']
    evaluater = auc.AUC(df)
    diagram_value = evaluater. circulate_auc
    # evaluater.save_ev_values( filename=filename )
    return diagram_value
