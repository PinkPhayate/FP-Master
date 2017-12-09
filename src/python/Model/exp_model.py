import configparser
import json, csv

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
param_file = METRICS_DIR + '/paramater.json'


class EXP_MODEL(object):
    sw_name = None
    c = None
    bug_versions = None
    pre_version = None
    curr_version = None
    dir_name = None
    alike_metrics = None
    previous_version = None
    param_dictionary = None

    def __init__(self, sw, fv, bvs, pv, cv, dn):
        self.sw_name = sw
        self.final_version = fv
        self.bug_versions = bvs
        self.pre_version = pv
        self.curr_version = cv
        self.dir_name = dn
        self.set_param_dict()

    def set_alike_metrics_list(self, alike_metrics):
        self.alike_metrics = alike_metrics

    def set_previous_version(self, previous_version):
        self.previous_version = previous_version

    def __get_param_dict(self):
        f = open(param_file, 'r')
        jsonData = json.load(f)
        f.close()
        version_data = json.dumps(jsonData)
        version_datas = json.loads(version_data)
        return version_datas

    def set_param_dict(self):
        try:
            param_dict = self.__get_param_dict()
        except:
            return
        for pd in param_dict:
            if self.sw_name == pd['sw'] and self.final_version == pd['version']:
                self.param_dictionary = pd['best-params']
