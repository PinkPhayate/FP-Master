from Model import stub
import subprocess

SRC_DIR = "/Users/phayate/src"
METRICS_DIR = "/Users/phayate/Dropbox/STUDY/Metrics"
DIMA_PATH = METRICS_DIR + "/DIMA-2.4.jar"
MO_PATH = METRICS_DIR + "/MO-1.1.jar"
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

def test_export_process_bug_report(model):
    import exp_execution
    exp_execution.export_process_bug_report(model)

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
    # alike_metrics = st.compare_two_versions(model.final_version, model.prev)
    ex01.predict()

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

model = stub.get_bug_process_merge_stub()
# print(model.final_version)
# test_export_process_bug_report(model)
# test_merge_process_product(model)
test_execute_ex01(model)
