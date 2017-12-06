from Model import stub
import subprocess
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'

SRC_DIR = "/Users/phayate/src"
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'
LOG_DIR = METRICS_DIR

def test_export_process_metrics(model):
    arg1 = "{}/{}/{}".format(SRC_DIR, model.dir_name, model.curr_version)
    arg2 = "{}/{}/{}".format(SRC_DIR, model.dir_name, model.pre_version)
    arg3 = model.final_version
    query = """java -jar {} {} {} {} java"""\
            .format(DIMA_PATH, arg1, arg2, arg3)
    res = subprocess.check_output(query, shell=True)
    print(res)

    query = """mv ProcessMetrics-{}.csv {}/{}/process_test/"""\
            .format(model.final_version, METRICS_DIR, model.sw_name)
    try:
        subprocess.check_call(query, shell=True)
    except:
        print("exception handler")
        #  TODO; exxception handler

def test_merge_process_bug(model):
    import exp_execution
    exp_execution.merge_process_bug(model)

def test_merge_process_bug_derby(model):
    import exp_execution
    exp_execution.merge_process_bug_derby(model)

def test_merge_process_product(model):
    import exp_execution
    exp_execution.merge_process_product(model)

def test_get_exp_versions():
    from Model import model_creator
    model_dict = model_creator.get_model_dictionary()
    print(model_dict)

def test_execute_ex01(model):
    from ex01_class import Ex01
    from lib import statistic as st
    ex01 = Ex01(model, METRICS_DIR)
    ex01.ITER = 5
    # alike_metrics = st.compare_two_versions(model.final_version, model.prev)
    ex01.predict()

def test_execute_ex01_prob(model):
    from ex01_class import Ex01
    from lib import statistic as st
    ex01 = Ex01(model, METRICS_DIR)
    # alike_metrics = st.compare_two_versions(model.final_version, model.prev)
    ex01.predict_prob()

def test_get_bug_list_sol1(model):
    import version_operator as vo
    arg1 = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
        .format(METRICS_DIR, model.sw_name, model.final_version)
    bug_list, exc_bug_list = vo.get_bug_list_sol2(arg1, model.sw_name)
    print(len(bug_list))
    print(exc_bug_list)

def test_retrieb_bug_list(model):
    import exp_execution
    exp_execution.retrieb_bug_list(model)

def test_draw_metrics_distribution(model, specific_metrics=None):
    import exp_execution
    exp_execution.draw_metrics_distribution(model, specific_metrics)

# model = stub.get_derby_model()
# test_export_process_metrics(model)
# merge_process_product(model)

def config_logger():
    import logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    debug_logger = logging.getLogger("debug_log")
    debug_logger.addHandler(sh)
    debug_logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename=LOG_DIR+"debug.log")
    fh.setFormatter(formatter)
    debug_logger.addHandler(fh)

config_logger()
# test_get_exp_versions()

# model = stub.get_bug_process_merge_stub()
# model = stub.get_derby_bug_adjust_model()
# model = stub.get_derby_model()
model = stub.get_hive_model()
# print(model.final_version)
# test_export_process_bug_report(model)
# test_merge_process_product(model)
# test_get_bug_list_sol1(model)
# test_export_process_bug_report(model)
# test_retrieb_bug_list(model)
# test_get_bug_list_sol1(model)
# test_merge_process_bug(model)
# test_merge_process_bug_derby(model)
test_execute_ex01(model)
# test_execute_ex01_prob(model)
# test_draw_metrics_distribution(model)
# test_draw_metrics_distribution(model, )
