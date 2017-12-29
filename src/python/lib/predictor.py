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
EXECUTION_MODE = inifile.get('env', 'mode')
class Predictor(object):
    model_type = None
    is_new_df = None
    report_df = None

    def __init__(self, pv, v_model, model_type):
        self.predict_ver = pv
        self.ver = v_model
        self.model_type = model_type
        self.report_df = None

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
        # print(df['fault'])
        evaluater = auc.AUC(df)
        diagram_value = evaluater. circulate_auc
        # evaluater.save_ev_values( filename=filename )
        return diagram_value

    def set_is_new_df(self, df):
        self.is_new_df = pd.DataFrame(df)
        self.is_new_df.columns = ['isNew']

    def set_is_modified_df(self, df):
        self.is_modified_df = pd.DataFrame(df)
        self.is_modified_df.columns = ['isModified']

    def export_report(self, version, sorting=True):
        if self.is_new_df is not None and\
           self.is_modified_df is not None and\
           self.report_df is not None:
            self.report_df = pd.concat([self.report_df, self.is_new_df], axis=1)
            self.report_df = pd.concat([self.report_df, self.is_modified_df], axis=1)
            if sorting:
                self.report_df = self.report_df.sort_values(by='predict', ascending=False)
            if EXECUTION_MODE == 'logging':
                self.report_df.to_csv(METRICS_DIR+version+self.model_type+'-report.csv')
            return self.report_df

    def predict_test_data(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        # output = model.predict(ev_data)
        output = model.predict(ev_data)

        # ev_data = pd.concat([paramater, dv_data],axis=1)
        predict = pd.DataFrame(output)
        predict.columns = [['predict']]
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict), None

    def predict_ensemble_test_data(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        output = model.predict(ev_data)

        predict = pd.DataFrame(output)
        predict.columns = [['predict']]
        predict.index = paramater.index
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = pd.concat([self.report_df, df], axis=0)\
                         if self.report_df is not None else df
        # return self.calculate_auc_score(dv_data, predict), None
        return None, None

    def predict_ensemble_proba(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        output = model.predict_proba(ev_data)

        predict = pd.DataFrame(output).ix[:,1:]
        predict.columns = [['predict']]
        predict.index = paramater.index
        df = pd.concat([paramater, predict],axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')],axis=1)
        self.report_df = pd.concat([self.report_df, df], axis=0)\
                         if self.report_df is not None else df

        # return self.calculate_auc_score(dv_data, predict),\
        #                                 model.feature_importances_
        return None, None

class RFPredictor(Predictor):
    def __init__(self, pv, v_model, model_type):
        super(RFPredictor, self).__init__(pv, v_model, model_type)

    def __get_optimized_model(self):
        param_d = self.predict_ver.param_dictionary
        if param_d is not None:
            model = RandomForestClassifier(
                oob_score=False,
                class_weight=None if param_d["class_weight"]=='None' else param_d['class_weight'],
                max_features=None if param_d["max_features"]=='None' else param_d['max_features'],
                max_depth=param_d['max_depth'],
                n_estimators=param_d['n_estimators'],
                min_samples_split=param_d['min_samples_split'],
                # min_samples_leaf=3
            )
            return model
        # print('this version {} does not have paramaters file.'.format(self.ver.final_version))
        model = RandomForestClassifier(
            oob_score=False,
            class_weight=None,
            # max_features="auto",
            max_depth=9,
            n_estimators=50,
            min_samples_split=3,
            # min_samples_leaf=3
        )
        return model

    def train_model(self, ev_data, dv_data):
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = self.__get_optimized_model()
        model.fit(ev_data, column_or_1d(dv_data))

        return model

    def predict_proba(self, model, ev_data, dv_data, filename):
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
        df.loc[:, 'predict'] = df.apply(lambda x: float(x['predict']), axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict),\
                                            model.feature_importances_

    def predict_test_data(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        output = model.predict(ev_data)

        # ev_data = pd.concat([paramater, dv_data],axis=1)
        predict = pd.DataFrame(output)
        predict.columns = [['predict']]
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict),\
                                        model.feature_importances_

class LGPredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(LGPredictor, self).__init__(pv, v, model_type)

    def train_model(self, ev_data, dv_data):
        from sklearn.linear_model import SGDClassifier
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = SGDClassifier(loss="log",
                              penalty="l2",
                              class_weight="balanced",
                              max_iter=1000)
        model.fit(ev_data, column_or_1d(dv_data))

        return model

    def predict_proba(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        # output = model.predict(ev_data)
        output = model.predict_proba(ev_data)

        # ev_data = pd.concat([paramater, dv_data],axis=1)
        predict = pd.DataFrame(output[:,1])
        predict.columns = [['predict']]
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict), None

class SVCPredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(SVCPredictor, self).__init__(pv, v, model_type)

    def train_model(self, ev_data, dv_data):
        from sklearn.svm import SVC
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = SVC()
        model.fit(ev_data, column_or_1d(dv_data))

        return model

class SVRPredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(SVRPredictor, self).__init__(pv, v, model_type)

    def train_model(self, ev_data, dv_data):
        from sklearn.svm import SVR
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = SVR(kernel='poly',
                    degree=len(ev_data[0]),
                    max_iter=-1)    # no limit
        print('model fitting')
        model.fit(ev_data, column_or_1d(dv_data))
        print('model fitted')

        return model

class TreePredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(TreePredictor, self).__init__(pv, v, model_type)

    def train_model(self, ev_data, dv_data):
        from sklearn.tree import DecisionTreeRegressor
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = DecisionTreeRegressor()
        model.fit(ev_data, column_or_1d(dv_data))

        return model

class BoostingPredictor(Predictor):
    def __init__(self, pv, v, model_type):
        super(BoostingPredictor, self).__init__(pv, v, model_type)

    def train_model(self, ev_data, dv_data):
        from sklearn.ensemble import GradientBoostingClassifier
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        model = GradientBoostingClassifier()
        model.fit(ev_data, column_or_1d(dv_data))

        return model

    def predict_ensemble_test_data(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        output = model.predict(ev_data)

        predict = pd.DataFrame(output)
        predict.columns = [['predict']]
        predict.index = paramater.index
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = pd.concat([self.report_df, df], axis=0)\
                         if self.report_df is not None else df
        # return self.calculate_auc_score(dv_data, predict), None
        return None, None

    def predict_proba(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        # output = model.predict(ev_data)
        output = model.predict_proba(ev_data)

        # ev_data = pd.concat([paramater, dv_data],axis=1)
        predict = pd.DataFrame(output[:,1])
        predict.columns = [['predict']]
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict), None

    def predict_ensemble_proba(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        output = model.predict_proba(ev_data)

        predict = pd.DataFrame(output).ix[:,1:]
        predict.columns = [['predict']]
        predict.index = paramater.index
        df = pd.concat([paramater, predict],axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')],axis=1)
        self.report_df = pd.concat([self.report_df, df], axis=0)\
                         if self.report_df is not None else df

        # return self.calculate_auc_score(dv_data, predict),\
        #                                 model.feature_importances_
        return None, None

class XGBPredictor(Predictor):
    def __init__(self, pv, v_model, model_type):
        super(XGBPredictor, self).__init__(pv, v_model, model_type)

    def __get_optimized_model(self):
        from xgboost import XGBClassifier
        param_d = self.ver.param_dictionary
        if param_d is not None:
            model = XGBClassifier(
                colsample_bytree=param_d["colsample_bytree"],
                learning_rate=param_d["learning_rate"],
                max_depth=param_d["max_depth"],
                subsample=param_d['subsample'],
            )
            return model
        model = XGBClassifier()
        return model

    def train_model(self, ev_data, dv_data):
        model = self.__get_optimized_model()
        model.fit(ev_data, column_or_1d(dv_data))
        return model

    def predict_proba(self, model, ev_data, dv_data, filename):
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
        df.loc[:, 'predict'] = df.apply(lambda x: float(x['predict']), axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict),\
                                            model.feature_importances_

    def predict_test_data(self, model, ev_data, dv_data, filename):
        # save for write file about metrics and predict and actualy
        paramater = ev_data.copy()
        # normalize
        # ev_data = (ev_data - ev_data.mean()) / ev_data.std()
        output = model.predict(ev_data)

        # ev_data = pd.concat([paramater, dv_data],axis=1)
        predict = pd.DataFrame(output)
        predict.columns = [['predict']]
        df = pd.concat([paramater, predict], axis=1)
        dv_data.columns = [['actual']]
        df = pd.concat([df, dv_data.to_frame(name='actual')], axis=1)
        self.report_df = df

        return self.calculate_auc_score(dv_data, predict),\
                                        None
