import configparser
import json, csv
from logging import getLogger
from Model.exp_model import EXP_MODEL

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
config_file = METRICS_DIR + '/exp_config.json'

def get_logger():
    mode = inifile.get('env', 'mode')
    logger = 'debug' if mode == 'debug' else 'report'
    error_logger = getLogger("error_log")
    report_logger = getLogger(logger+"_log")
    return report_logger, error_logger

def get_exp_versions():
    raise Exception
    '''Model/models_creator.pyに移動'''
    # f = open(config_file, 'r')
    # jsonData = json.load(f)
    # f.close()
    # version_data = json.dumps(jsonData)
    # version_datas = json.loads(version_data)
    # return version_datas

def models_creator():
    raise Exception
    '''Model/models_creator.pyに移動'''
    # version_datas = get_exp_versions()
    # model_dictionary = {}
    # for version_data in version_datas:
    #     models = []
    #     for version in version_data:
    #         model = EXP_MODEL(sw=version_data["sw"],
    #                           fv=version["v"],
    #                           bvs=version["bugv"],
    #                           pv=version["diffv"][0],
    #                           cv=version["diffv"][1],
    #                           dn=version_data["dirname"])
    #         models.append(model)
    #     model_dictionary[ version_data["sw"] ] = models
    # return model_dictionary

def get_bug_list(bug_filename):
    '''
    引数のファイルにあるバグレポートに合ったファイル名を
    リストにして返すメソッド
    '''
    bug_list = []
    with open(bug_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            bug_list.append(row[0])
        return bug_list
def transform_sol1(bug_module, sw_name):
    beginning_str = "/{}/".format(sw_name)
    soluted_bug_module = bug_module.split(beginning_str)[-1]
    return soluted_bug_module

def transform_sol3(bug_module, sw_name):
    beginning_str = "/"
    li = bug_module.split(beginning_str)
    return li[-1]

def get_bug_list_sol1(bug_filename, sw_name):
    '''
    sol1でバグリストを整形する
    sol1: そのソフトウェア名以下のパスから最後までをパスとする手法
    '''
    report_logger, error_logger = get_logger()
    bug_list = get_bug_list(bug_filename)
    beginning_str = "/{}/".format(sw_name)
    soluted_bug_list = []
    exc_bug_list = []
    for bug_module in bug_list:
        if beginning_str in bug_module:
            soluted_bug_module = bug_module.split(beginning_str)[-1]
            soluted_bug_list.append(soluted_bug_module)
        else:
            exc_bug_list.append(bug_module)
    report_logger.info('reduction of numbug module via soli1 {}/{}'.format(len(bug_list), len(soluted_bug_list)))
    return soluted_bug_list, exc_bug_list

def get_bug_list_sol2(bug_filename, sw_name):
    '''
    sol1でバグリストを整形する
    sol1: そのソフトウェア名以下のパスから最後までをパスとする手法
    '''
    report_logger, error_logger = get_logger()
    bug_list = get_bug_list(bug_filename)
    beginning_str = "java/".format(sw_name)
    soluted_bug_list = []
    exc_bug_list = []
    for bug_module in bug_list:
        if beginning_str in bug_module:
            soluted_bug_module = bug_module.split(beginning_str)[-1]
            soluted_bug_list.append(soluted_bug_module)
        else:
            exc_bug_list.append(bug_module)
    report_logger.info('reduction of numbug module via soli2 {}/{}'.format(len(bug_list), len(soluted_bug_list)))
    return soluted_bug_list, exc_bug_list

def get_bug_list_sol3(bug_filename, sw_name):
    '''
    sol3でバグリストを整形する
    sol3: そのファイル名のみ
    '''
    report_logger, error_logger = get_logger()
    bug_list = get_bug_list(bug_filename)
    beginning_str = "java/"
    soluted_bug_list = []
    exc_bug_list = []
    soluted_bug_list = [x.split('/')[-1] for x in bug_list]
    # print(soluted_bug_list)
    # raise Exception
    # soluted_bug_list = map(lambda x: x.split('/')[-1], bug_list)
    report_logger.info('reduction of numbug module via soli2 {}/{}'.format(len(bug_list), len(soluted_bug_list)))
    return soluted_bug_list, None

def adjust_bug_list(model):
    '''
    対象のバージョンに対応するバグリストを作成するモジュール
    '''
    def __put_bug_list(ad_bug_filename,ad_bug_list):
        with open(ad_bug_filename, 'w') as f:
            for x in ad_bug_list:
                f.write(str(x) + "\n")

    def __merge_bug_list(sw_name, versions):
        ad_bug_list = []
        for version in versions:
            bug_filename = "{0}/{1}/bug/{1}_{2}_bgmd.csv".format(METRICS_DIR,sw_name,version)
            bug_list = get_bug_list(bug_filename)
            ad_bug_list.extend(bug_list)
        return ad_bug_list

    versions = model.bug_versions
    sw_name = model.sw_name
    ad_bug_list = __merge_bug_list(sw_name, versions)
    ad_bug_filename = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
                      .format(METRICS_DIR, sw_name, model.final_version)
    __put_bug_list(ad_bug_filename, ad_bug_list)
