import configparser
import json, csv
from Model.exp_model import EXP_MODEL

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
config_file = METRICS_DIR

def get_exp_versions(exp_num=1):
    if exp_num ==1:
        config_file = METRICS_DIR + '/exp_config.json'
    elif exp_num ==2:
        config_file = METRICS_DIR + '/exp2_config.json'
    f = open(config_file, 'r')
    jsonData = json.load(f)
    f.close()
    version_data = json.dumps(jsonData)
    version_datas = json.loads(version_data)
    return version_datas


def get_model_dictionary(exp_num=1):
    """exp_test.pyにテスト書いた"""
    version_datas = get_exp_versions(exp_num)
    model_dictionary = {}
    for version_data in version_datas:
        models = []
        for version in version_data['versions']:
            model = EXP_MODEL(sw=version_data["sw"],
                              fv=version["v"],
                              bvs=version["bugv"],
                              pv=version["diffv"][0],
                              cv=version["diffv"][1],
                              dn=version_data["dirname"])
            prev = version['prev'] if 'prev' in version.keys() else ''
            model.set_previous_version(prev)
            models.append(model)
        model_dictionary[version_data["sw"]] = models
    return model_dictionary

def retrieve_model(sw_name, version):
    model_dict = get_model_dictionary()
    for sw, models in model_dict.items():
        for model in models:
            if model.final_version == version and\
               sw_name == sw:
               return model
    else:
        print('could not find model sw_name: {},version: {}'\
              .format(sw_name, version))
        raise Exception
