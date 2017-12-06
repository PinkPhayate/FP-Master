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
    mode = inifile.get('env', 'mode')
    logger = 'debug' if mode == 'debug' else 'report'
    report_logger = getLogger(logger+"_log")
    error_logger = getLogger("error_log")
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

        query = """mv ProcessMetrics-{}.csv {}/{}/process/"""\
                .format(model.final_version, METRICS_DIR, model.sw_name)
        report_logger.info('execute this query: {}'.format(query))
        subprocess.check_call(query, shell=True)
        report_logger.info('execution has done collectly: {}'.format(query))
    except:
        report_logger.info('could not executed collectly')

def export_process_bug_report(model):
    """
    ファイナルバージョンに対してバグリストをまとめる（ファイナライズ）するモジュール
    """
    import pandas as pd
    report_logger, error_logger = get_logger()
    version_list = model.bug_versions
    bug_list = pd.DataFrame([])
    for version in version_list:
        # バグレポート名
        arg1 = "{0}/{1}/bug/{1}_{2}_bgmd.csv"\
            .format(METRICS_DIR, model.sw_name, version)
        print(arg1)
        try:
            df = pd.read_csv(arg1, header=None)
        except:
            error_logger.error('this file couldnt find: {}'.format(arg1))
            return
        bug_list = pd.concat([bug_list, df], axis=0)
    arg1 = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    bug_list.to_csv(arg1, index=False, header=None)
    # print(bug_list)

def merge_process_bug(model):
    '''
    プロセスメトリクスとバグレポートをマージする
    sol1: 全体的にうまくいく？
    sol2: derbyとvelocityがうまく行かない
    '''
    import pandas as pd
    import version_operator as vo
    report_logger, error_logger = get_logger()
    # バグレポート名
    arg1 = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # プロセスメトリクスレポート名
    arg2 = "{0}/{1}/process/ProcessMetrics-{2}.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # 出力ファイル名
    arg3 = "{0}/{1}/process-bug/process-bug-{2}.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # バグモジュールの書かれたリストを取得
    bug_list, exc_bug_list = vo.get_bug_list_sol1(arg1, model.sw_name)
    # bug_list, exc_bug_list = vo.get_bug_list_sol2(arg1, model.sw_name)
    error_str = '{} {}, excepted bug modules: {}'\
        .format(model.sw_name, model.final_version, exc_bug_list)
    if 0 < len(exc_bug_list):
        error_logger.error(error_str)
    # プロセスメトリクスのcsvを読み込み
    df = pd.read_csv(arg2, header=0)
    df['fileName'] = df.apply(lambda x: x['fileName'].split("/")[9:], axis=1)
    df['fileName'] = df.apply(lambda x: "/".join(x['fileName']), axis=1)
    df['fileName'] = df.apply(lambda x: vo.transform_sol1(x['fileName'], model.sw_name), axis=1)
    # df['fileName'] = df.apply(lambda x: vo.transform_sol2(x['fileName'], model.sw_name), axis=1)
    # df['fileName'] = df.apply(lambda x: x['fileName'].split("/")[-1], axis=1)
    df['bug'] = df.apply(lambda x: 1 if(x['fileName'] in bug_list) else 0, axis=1)
    # bug number is integer
    # df['bug'] = df.apply(lambda x: bug_list.count(x['fileName']), axis=1)
    found = df['bug'].sum()
    result_str = '{} {}, bef/after {}/{}'\
        .format(model.sw_name, model.final_version, len(bug_list), found)
    print(result_str)
    report_logger.info(result_str)
    df.to_csv(arg3)

def merge_process_bug_derby(model):
    '''
    プロセスメトリクスとバグレポートをマージする
    sol1: 全体的にうまくいく？
    sol2: derbyとvelocityがうまく行かない
    '''
    import pandas as pd
    import version_operator as vo
    report_logger, error_logger = get_logger()
    # バグレポート名
    arg1 = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # プロセスメトリクスレポート名
    arg2 = "{0}/{1}/process/ProcessMetrics-{2}.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # 出力ファイル名
    arg3 = "{0}/{1}/process-bug/process-bug-{2}.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    # バグモジュールの書かれたリストを取得
    bug_list, exc_bug_list = vo.get_bug_list_sol3(arg1, model.sw_name)
    # プロセスメトリクスのcsvを読み込み
    df = pd.read_csv(arg2, header=0)
    df['fileName'] = df.apply(lambda x: x['fileName'].split("/")[7:], axis=1)
    df['fileName'] = df.apply(lambda x: "/".join(x['fileName']), axis=1)
    df['fileName'] = df.apply(lambda x: vo.transform_sol3(x['fileName'], model.sw_name), axis=1)
    df['bug'] = df.apply(lambda x: 1 if(x['fileName'] in bug_list) else 0, axis=1)
    # bug number is integer
    # df['bug'] = df.apply(lambda x: bug_list.count(x['fileName']), axis=1)
    found = df['bug'].sum()
    result_str = '{} {}, bef/after {}/{}'\
        .format(model.sw_name, model.final_version, len(bug_list), found)
    report_logger.info(result_str)
    df.to_csv(arg3)

def merge_process_product(model):
    # プロダクトメトリクスとプロセスメトリクスをマージするモジュール
    MO_PATH = METRICS_DIR + "/MO-1.1.jar"
    report_logger, error_logger = get_logger()
    arg1 = "{}/{}/product/product-{}.csv".format(METRICS_DIR, model.sw_name, model.final_version)
    arg2 = "{}/{}/process-bug/process-bug-{}.csv".format(METRICS_DIR, model.sw_name, model.final_version)
    arg3 = model.final_version
    arg4 = "{}/{}/all/".format(METRICS_DIR, model.sw_name)
    query = """java -jar {} {} {} {} {}"""\
            .format(MO_PATH, arg1, arg2, arg3, arg4)
    try:
        res = subprocess.check_output(query, shell=True)
    except Exception:
        error_logger.error('could not execute properly query: {}'.format(query))
    report_logger.info(res)

def execute_ex01(model):
    from ex01_class import Ex01
    report_logger, error_logger = get_logger()
    if model.previous_version == '':
        return
    report_logger.info('sw name: {}, predict version: {}, previousversion: {}'
        .format(model.sw_name, model.final_version, model.previous_version))
    ex01 = Ex01(model, METRICS_DIR)
    ex01.predict()

def execute_ex01_prob(model):
    from ex01_class import Ex01
    report_logger, error_logger = get_logger()
    if model.previous_version == '':
        return
    report_logger.info('sw name: {}, predict version: {}, previousversion: {}'
        .format(model.sw_name, model.final_version, model.previous_version))
    ex01 = Ex01(model, METRICS_DIR)
    ex01.predict_prob()

def draw_metrics_distribution(model, specific_metrics=None):
    from Model.metrics import Metrics
    from Model import model_creator as mc
    from lib import figure
    metrics = Metrics(model.final_version, METRICS_DIR, model)
    pre_model = mc.retrieve_model(model.sw_name, model.final_version)
    pre_metrics = Metrics(model.previous_version, METRICS_DIR, pre_model)

    for column in metrics.mrg_df.columns:
        print('col: {}'.format(column))
        if specific_metrics is not None:
            column = specific_metrics
        fileName = '{}/{}-{}-{}.png'.format(METRICS_DIR, model.sw_name, model.final_version, column)
        # figure.draw_violin_plot(metrics.mrg_df.ix[:, column],
        #                         pre_metrics.mrg_df.ix[:, column],
        #                         fileName=fileName)
        figure.draw_histgram(metrics.mrg_df.ix[:, column],
                                pre_metrics.mrg_df.ix[:, column],
                                fileName=fileName)

def config_logger():
    import logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    error_logger = logging.getLogger("error_log")
    error_logger.addHandler(sh)
    error_logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(filename=LOG_DIR+"/error.log")
    fh.setFormatter(formatter)
    error_logger.addHandler(fh)

    report_logger = logging.getLogger("report_log")
    report_logger.addHandler(sh)
    report_logger.setLevel(logging.INFO)
    fh = logging.FileHandler(filename=LOG_DIR+"/report.log")
    fh.setFormatter(formatter)
    report_logger.addHandler(fh)

def restrict_models(model_dict):
    skip_array = []
    model_dict_copy = model_dict.copy()
    for version in model_dict.keys():
        if version in skip_array:
            del model_dict_copy[version]
    return model_dict_copy

def retrieb_models(model_dict):
    target_array = ['log4j', 'velocity']
    model_dict_copy = {}
    for version in model_dict.keys():
        if version in target_array:
            model_dict_copy[version] = model_dict[version]
    return model_dict_copy

def main():
    from Model import model_creator
    import version_operator as vo
    config_logger()
    model_dict = model_creator.get_model_dictionary()
    jobs = []
    # model_dict = retrieb_models(model_dict)
    for sw_name, models in model_dict.items():
        for model in models:
            """
            ここに実行する実験メソッドを書けば良い
            """
            # vo.adjust_bug_list(model)
            # job = Process(target=exe_DIMA, args=(model,))
            # job = Process(target=retrieb_bug_list, args=(model,))
            # job = Process(target=merge_process_bug, args=(model,))
            # job = Process(target=merge_process_bug_derby, args=(model,))
            # job = Process(target=merge_process_product, args=(model,))
            # job = Process(target=execute_ex01, args=(model,))
            job = Process(target=draw_metrics_distribution, args=(model,))
            jobs.append(job)
            job.start()
            """
            このインデントを維持する。
            """
    [jb.join() for jb in jobs]


if __name__ == '__main__':
    main()
