from ex02_class import Ex02
from itertools import combinations
import configparser
from multiprocessing import Process
import exp_execution_ex02

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'



def retrieb_models(sw_name, version):
    models = exp_execution_ex02.__create_all_models()
    for model in models:
        if model.sw_name == sw_name and model.final_version == version:
            return model
    else:
        print('could not find this model:{}{}'.format(sw_name, version))
    raise Exception

def test_ex02_class_predict():
    model1 = retrieb_models('velocity', '1.6')
    model2 = retrieb_models('solr', '6.6.0')
    ex02 = Ex02(model1, model2, METRICS_DIR)
    ex02.predict()


test_ex02_class_predict()
