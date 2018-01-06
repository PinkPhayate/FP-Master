from ex02_class import Ex02
from itertools import combinations
from itertools import permutations
import configparser
from multiprocessing import Process

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
    # model_dict = retrieb_models(model_dict)
    for _, models in model_dict.items():
        # models = retrieb_model_specified_version(models)
        for model in models:
            """
            ここに実行する実験メソッドを書けば良い
            """
            print(model.sw_name, model.final_version, model.previous_version)
            # ex1.execute_ex01(model)
            ex1.execute_ex01_prob(model)
            ex1.count_fp_numsv(model)

            # job = Process(target=ex1.execute_ex01, args=(model,))
            # jobs.append(job)
            # job.start()
    # [jb.join() for jb in jobs]

if __name__ == '__main__':
    # main()
    _main()
