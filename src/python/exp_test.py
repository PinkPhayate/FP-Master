from Model import stub
import subprocess

SRC_DIR = "/Users/phayate/src"
METRICS_DIR = "/Users/phayate/Dropbox/STUDY/Metrics"
DIMA_PATH = METRICS_DIR + "/DIMA-2.4.jar"
MO_PATH = METRICS_DIR + "/MO-1.1.jar"

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
    # バグレポート名
    arg1 = "{0}/{1}/bug/ad_{1}_{2}_bgmd.csv"\
            .format(METRICS_DIR, model.sw_name, model.final_version)
    # プロセスメトリクスレポート名
    arg2 = "{0}/{1}/process/ProcessMetrics-{2}.csv"\
            .format(METRICS_DIR, model.sw_name, model.final_version)
    # 出力ファイル名
    arg3 = "{0}/{1}/process-bug/process-bug-{2}.csv"\
            .format(METRICS_DIR, model.sw_name, model.final_version)
    query = """python ./tmp/script/bug_process_merger.py {} {} {}"""\
            .format(arg1, arg2, arg3)
    res = subprocess.check_output(query, shell=True)
    print(res)

def merge_process_product(model):
    arg1 = "{}/{}/product/product-{}.csv".format(METRICS_DIR, model.sw_name, model.final_version)
    arg2 = "{}/{}/process-bug/process-bug-{}.csv".format(METRICS_DIR, model.sw_name, model.final_version)
    arg3 = model.final_version
    arg4 = "{}/{}/all/".format(METRICS_DIR, model.sw_name)
    query = """java -jar {} {} {} {} {}"""\
            .format(MO_PATH, arg1, arg2, arg3, arg4)
    print(query)
    res = subprocess.check_output(query, shell=True)
    print(res)

model = stub.get_derby_model()
# test_export_process_metrics(model)
# test_export_process_bug_report(model)
merge_process_product(model)
