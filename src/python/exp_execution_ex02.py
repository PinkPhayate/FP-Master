from ex02_class import Ex02
from itertools import combinations
from itertools import permutations
import configparser
from multiprocessing import Process
from lib import statistic as st

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

def __create_all_models():
    from Model import model_creator
    import version_operator as vo
    model_dict = model_creator.get_model_dictionary()
    jobs = []
    # model_dict = retrieb_models(model_dict)
    all_models = []
    for _, models in model_dict.items():
        # models = retrieb_model_specified_versions(models)
        for model in models:
            all_models.append(model)
    return all_models

def execute_ex02(i, j):
    ex02 = Ex02(i, j, METRICS_DIR)
    ex02.predict()

def conduct_mh_with_another_version(rfn_analyzer_list, itg_analyzer_list):
    # XXX this module has function only apache derby for version comparing.
    rfn_analyzer0 = rfn_analyzer_list[0]
    rfn_analyzer2 = rfn_analyzer_list[2]
    pvalue = st.conduct_m_whitney_test(rfn_analyzer0.accum_accuracy0, rfn_analyzer2.accum_accuracy0)
    msg = 'sw: {}, predictv: {}, learnv: 10.10.1.1 p-value of mann whitney u test: {}'\
        .format(rfn_analyzer0.target_sw,
                rfn_analyzer0.predict_version,
                pvalue)
    print(msg)

    itg_analyzer0 = itg_analyzer_list[0]
    itg_analyzer2 = itg_analyzer_list[2]
    pvalue = st.conduct_m_whitney_test(itg_analyzer0.accum_accuracy0, itg_analyzer2.accum_accuracy0)
    msg = 'sw: {}, predictv: {}, learnv: 10.10.1.1 p-value of mann whitney u test: {}'\
        .format(itg_analyzer0.target_sw,
                itg_analyzer0.predict_version,
                pvalue)
    print(msg)

def main():
    models = __create_all_models()
    jobs = []
    for i, j in combinations(models, 2):
        try:
            execute_ex02(i, j)
        except Exception as e:
            msg = 'model1: {}{}, model2: {}{} has error caused below reasons.'.format(i.sw_name, i.final_version, j.sw_name, j.final_version)
            print(msg)
            print(e)

        # job = Process(target=execute_ex02, args=(i, j,))
        # jobs.append(job)
        # job.start()
        """
        このインデントを維持する。
        """
    [jb.join() for jb in jobs]

def _main():
    from Model import model_creator
    import version_operator as vo
    import exp_execution as ex1
    model_dict = model_creator.get_model_dictionary(exp_num=2)
    jobs = []
    rfn_analyzer_list = []
    itg_analyzer_list = []
    # model_dict = retrieb_models(model_dict)
    for _, models in model_dict.items():
        # models = retrieb_model_specified_version(models)
        for model in models:
            """
            ここに実行する実験メソッドを書けば良い
            """
            # job = Process(target=ex1.execute_ex01, args=(model,))
            # jobs.append(job)
            # job.start()
            if model.previous_version == '':
                continue

            print(model.sw_name, model.final_version, model.previous_version)
            rfn_analyzer, itg_analyzer = ex1.execute_ex01(model)
            rfn_analyzer_list.append(rfn_analyzer)
            itg_analyzer_list.append(itg_analyzer)
        conduct_mh_with_another_version(rfn_analyzer_list, itg_analyzer_list)
    # [jb.join() for jb in jobs]

if __name__ == '__main__':
    # main()
    _main()
