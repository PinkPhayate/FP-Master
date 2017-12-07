from Model.exp_model import EXP_MODEL
def get_derby_model():
    model = EXP_MODEL(sw='derby',
                      fv='10.13.1.1',
                      bvs=['10.14.1.0'],
                      pv='10.12.1.1',
                      cv='10.13.1.1',
                      dn='ApacheDerby')
    model.previous_version = "10.12.1.1"
    return model

def get_poi_model():
    model = EXP_MODEL(sw='poi',
                      fv='3.17',
                      bvs=['4.0.0-SNAPSHOT'],
                      pv='3.16',
                      cv='3.17-beta1',
                      dn='ApachePoi')
    model.previous_version = "3.16"
    return model

def get_derby_bug_adjust_model():
    model = EXP_MODEL(sw='derby',
                      fv='10.9',
                      bvs=['10.8.2.2', '10.8.3.0'],
                      pv='10.8',
                      cv='10.9',
                      dn='ApacheDerby')
    return model

def get_bug_process_merge_stub():
    model = EXP_MODEL(sw='hive',
                      fv='2.2.0',
                      bvs=["2.3.1"],
                      pv="2.3.0",
                      cv="2.2.0",
                      dn='ApacheHive')
    model.previous_version = "2.1.0"
    return model
def get_hive_model():
    model = EXP_MODEL(sw='hive',
                      fv='2.2.0',
                      bvs=["2.3.0"],
                      pv="2.3.0",
                      cv="2.2.0",
                      dn='ApacheHive')
    model.previous_version = "2.1.0"
    return model

def get_pdt_prs_merge_stub():
    model = EXP_MODEL(sw='velocity',
                      fv='1.6',
                      bvs=None,
                      pv=None,
                      cv=None,
                      dn='ApacheVelocity')
    return model
