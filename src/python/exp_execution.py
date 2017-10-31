# directory 造り
import subprocess
from Model import stub

def create_module_directory():
    model = stub.get_derby_model()
    query = """mkdir -p {}/{}"""\
            .format(METRICS_DIR, model.sw_name)
    res = subprocess.check_call(query, shell=True)


create_module_directory()
