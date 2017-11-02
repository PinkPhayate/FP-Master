from Model import stub
import configparser
import json, csv
from Model.exp_model import EXP_MODEL
import version_operator as vo

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
config_file = METRICS_DIR + '/exp_config.json'

def test_adjust_bug_list(model):
    vo.adjust_bug_list(model)

METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

def get_process_metrics(model):
    import pandas as pd
    bug_filename = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
            .format(METRICS_DIR, model.sw_name, model.final_version)
    process_m_filename = "{0}/{1}/process/ProcessMetrics-{2}.csv"\
            .format(METRICS_DIR, model.sw_name, model.final_version)
    df = pd.read_csv(process_m_filename, header=0)
    bug_list = vo.get_bug_list(bug_filename)
    df['fileName'] = df.apply(lambda x: x['fileName'].split("/")[9:], axis=1)
    df['fileName'] = df.apply(lambda x: "/".join(x['fileName']), axis=1)
    print(df['fileName'])

def test_get_bug_list():
    filename = "{0}/{1}/bug/ad_derby_10.9_bgmd.csv".format(METRICS_DIR, 'derby')
    bug_list = vo.get_bug_list(filename)
    print(bug_list)

def test_get_bug_list_sol1(model):
    # TODO: 全Swでテストする
    sw_name = model.sw_name
    final_version = model.final_version
    filename = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
        .format(METRICS_DIR, sw_name, final_version)
    bug_list, exc_bug_list = vo.get_bug_list_sol1(filename, sw_name)
    print('{}   {}').format(sw_name, final_version)
    print(exc_bug_list)

def test_merge_bug_process():
    # TODO: 実装
    pass

model = stub.get_derby_bug_adjust_model()
# test_adjust_bug_list(model)
# test_get_bug_list()
get_process_metrics(model)
