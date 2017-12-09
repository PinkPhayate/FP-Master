from Model import stub
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler
import random
from lib import statistic as st
from lib.report_analyzer import AUCAnalyzer
from lib.report_analyzer import Analyzer
from tqdm import tqdm
from Model.metrics import Metrics
from Model import model_creator as mc
import configparser
import pandas as pd
from sklearn.model_selection import GridSearchCV
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
EXECUTION_MODE = inifile.get('env', 'mode')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

def create_dataset(model):
    ver, predict_ver = model.previous_version, model.final_version
    pre_model = mc.retrieve_model(model.sw_name, model.final_version)
    training_m = Metrics(ver, METRICS_DIR, pre_model)
    evaluate_m = Metrics(predict_ver, METRICS_DIR, model)
    return training_m, evaluate_m

def find_best_param(training_m, evaluate_m):
    sm = RandomOverSampler(ratio='auto', random_state=random.randint(1,100))
    X_resampled, y_resampled = sm.fit_sample( training_m.product_df, training_m.fault )

    clf = RandomForestClassifier()


    params = {
              'n_estimators': [3, 5, 10, 50, 100],
              'max_depth': list(range(1, 10)),
              'class_weight': ['balanced', None],
              'max_features': [None, 'auto'],
              'min_samples_split': [3, 5, 10, 20, 30]
    }

    from sklearn.metrics import f1_score
    from sklearn.metrics import make_scorer
    f1_scorer = make_scorer(f1_score, pos_label=1)

    grid_search = GridSearchCV(clf,  # 分類器を渡す
                               param_grid=params,  # 試行してほしいパラメータを渡す
                               cv=5,  # 10-Fold CV で汎化性能を調べる
                               scoring=f1_scorer
                               )
    grid_search.fit(X_resampled, y_resampled)
    return grid_search.best_score_, grid_search.best_params_

if __name__ == '__main__':
    model = stub.get_hive_model()
    # model = stub.get_derby_model()
    training_m, evaluate_m = create_dataset(model)
    find_best_param(training_m, evaluate_m)
