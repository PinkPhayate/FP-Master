# directory 造り
import subprocess
from Model import stub
import configparser
from logging import getLogger
import version_operator
from multiprocessing import Process

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
SRC_DIR = "/Users/phayate/src"
LOG_DIR = METRICS_DIR

def get_logger():
    error_logger = getLogger("error_log")
    report_logger = getLogger("report_log")
    return report_logger, error_logger

def exe_DIMA(model):
    """
    プロセスメトリクスを取得するモジュール
    """
    DIMA_PATH = METRICS_DIR + "/DIMA-2.4.jar"
    report_logger, error_logger = get_logger()
    report_logger.info('execute DIMA.jar.')
    report_logger.info('[sw_name]: {}'.format(model.sw_name))
    report_logger.info('[crt version]: {}'.format(model.curr_version))
    report_logger.info('[pre version]: {}'.format(model.pre_version))


    arg1 = "{}/{}/{}".format(SRC_DIR, model.dir_name, model.curr_version)
    arg2 = "{}/{}/{}".format(SRC_DIR, model.dir_name, model.pre_version)
    arg3 = model.final_version
    try:
        query = """java -jar {} {} {} {} java"""\
                .format(DIMA_PATH, arg1, arg2, arg3)
        report_logger.info('execute this query: {}'.format(query))
        res = subprocess.check_output(query, shell=True)
        report_logger.info(res)
        report_logger.info('execution has done collectly: {}'.format(query))

        query = """mv ProcessMetrics-{}.csv {}/{}/process_test/"""\
                .format(model.final_version, METRICS_DIR, model.sw_name)
        report_logger.info('execute this query: {}'.format(query))
        subprocess.check_call(query, shell=True)
        report_logger.info('execution has done collectly: {}'.format(query))
    except:
        report_logger.info('could not executed collectly')


def config_logger():
    import logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    error_logger = logging.getLogger("error_log")
    error_logger.addHandler(sh)
    error_logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(filename=LOG_DIR+"error.log")
    fh.setFormatter(formatter)
    error_logger.addHandler(fh)

    report_logger = logging.getLogger("report_log")
    report_logger.addHandler(sh)
    report_logger.setLevel(logging.INFO)
    fh = logging.FileHandler(filename=LOG_DIR+"report.log")
    fh.setFormatter(formatter)
    report_logger.addHandler(fh)

def restrict_models(model_dict):
    skip_array = []
    model_dict_copy = model_dict.copy()
    for version in model_dict.keys():
        if version in skip_array:
            del model_dict_copy[version]
    return model_dict_copy


def main():
    from Model import model_creator
    import version_operator as vo
    config_logger()
    model_dict = model_creator.get_model_dictionary()
    jobs = []
    # model_dict = restrict_models(model_dict)
    for sw_name, models in model_dict.items():
        print(sw_name)
        for model in models:
            """
            ここに実行する実験メソッドを書けば良い
            """
            # vo.adjust_bug_list(model)
            job = Process(target=exe_DIMA, args=(model))
            jobs.append(job)
            job.start()
            """
            このインデントを維持する。
            """
    [jb.join() for jb in jobs]


if __name__ == '__main__':
    main()
