from lib import statistic as st
from lib.metrics import Metrics_Origin
from multiprocessing import Process
from ex01_class import Ex01
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
config_logger()

def exp(model, metrics_dir):
    metrics_dir = '/Users/{}/Dropbox/STUDY/{}/Derby/all'\
    .format(ENV, model.dir_name)
    ex01 = Ex01(model, metrics_dir)

    ex01.METRICS_DIR = metrics_dir

    v1 = model.curr_version
    v2 = model.pre_version
    version1 = Metrics_Origin(v1, metrics_dir)
    version2 = Metrics_Origin(v2, metrics_dir)
    print(v1+'-'+v2)
    alike_metrics = st.compare_two_versions(version1, version2)
    print(alike_metrics)
    ex01.predict(v1, v2, alike_metrics)


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
    # TODO arg value
    # ex01.ITER = 10
    # ex01.PRED_TYPE = 'rf'

    model_dict = model_creator.get_model_dictionary()
    jobs = []
    # model_dict = restrict_models(model_dict)
    for sw_name, models in model_dict.items():
        print(sw_name)
        for model in models:
            ex01.TARGET = model.dir_name
            metrics_dir = '/Users/{}/Dropbox/STUDY/{}/Derby/all'\
                .format(ENV, model.dir_name)
            ex01.METRICS_DIR = metrics_dir

            """
            ここに実行する実験メソッドを書けば良い
            """
            # vo.adjust_bug_list(model)
            job = Process(target=exp, args=(model, metrics_dir))
            jobs.append(job)
            job.start()
            """
            このインデントを維持する。
            """
    [jb.join() for jb in jobs]


if __name__ == '__main__':
    main()
