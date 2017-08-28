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

class Predictor(object):
    model_type = None
    is_new_df = None
    report_df = None

    def __init__(self, pv, v, model_type):
        self.predict_ver = pv
        self.ver = v
        self.model_type = model_type


    def predict_rf(self, model, ev_data, dv_data):

        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()

        output = model.predict_proba(ev_data)
        pred = pd.DataFrame( output ).ix[:,1:1]
        print(model.feature_importances_)
        return self.calculate_diagram(dv_data, pred)

    def predict_rf_saver(self, model, ev_data, dv_data, filename):
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
        self.report_df = df

        importance = pd.DataFrame(model.feature_importances_)
        # importance
        if EXECUTION_MODE == 'Investigation':
            return self.calculate_auc_score(dv_data, predict), model.feature_importances_
        else:
            return self.calculate_auc_score(dv_data, predict), model.feature_importances_
            # return calculate_diagram(dv_data, actual), model.feature_importances_


    def get_random_ev(self, size):
        np.random.seed(seed=2019)
        rev = np.random.rand( size )
        return rev


    def calculate_diagram(self, actual, pred):
        df = pd.concat([ actual, pred ], axis=1)
        df.columns = ['fault', 'ev_value']
        diagram_value = auc.AUC(df). circulate_auc
        return diagram_value

    def calculate_auc_score(self, actual, pred):
        df = pd.concat([ actual, pred ], axis=1)
        df.columns = ['fault', 'ev_value']
        auc_score = roc_auc_score(df['fault'], df['ev_value'])
        return auc_score

    def calculate_diagram_saver(self, actual, pred, filename):
        df = pd.concat([ actual, pred ], axis=1)
        df.columns = ['fault', 'ev_value']
        evaluater = auc.AUC(df)
        diagram_value = evaluater. circulate_auc
        # evaluater.save_ev_values( filename=filename )
        return diagram_value

    def set_is_new_df(self, df):
        self.is_new_df = df

    def export_report(self):
        if self.is_new_df is not None and\
            self.report_df is not None:
            __report_df = pd.concat([self.report_df, self.is_new_df], axis=1)
            __report_df = __report_df.sort_values(by='predict', ascending=False)
            __report_df.to_csv(METRICS_DIR + self.model_type + '-report.csv')

class RFPredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(RFPredictor, self).__init__(pv, v, model_type)

    def train_rf(self, ev_data, dv_data):
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
