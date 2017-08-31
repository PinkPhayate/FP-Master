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

def train_rf (ev_data, dv_data):
    # normalize
    # ev_data = (ev_data - ev_data.mean()) / ev_data.std()

    model = RandomForestClassifier()
    model.fit(ev_data, column_or_1d(dv_data))

    return model

def predict_rf(model, ev_data, dv_data):
    paramater = ev_data.copy()
    # normalize
    # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
    output = model.predict_proba(ev_data)
    actual = pd.DataFrame(output).ix[:, 1:]
    actual.columns = [['predict']]
    return actual


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
    ev_data = pd.concat([paramater, dv_data],axis=1)
    actual = pd.DataFrame(output).ix[:,1:]
    actual.columns = [[ 'predict']]
    df = pd.concat([paramater, actual],axis=1)
    df =df.sort_values(by='predict',ascending=False)
    importance = pd.DataFrame(model.feature_importances_)
    # importance
    if EXECUTION_MODE == 'debug':
        # print(importance)
        df = pd.concat([df, importance], axis=0)
        df.to_csv("../Data/Research/Investigation/"+filename)
        return calculate_diagram_saver(dv_data, actual, filename), model.feature_importances_
    else:
        return calculate_auc_score(dv_data, actual), model.feature_importances_
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
