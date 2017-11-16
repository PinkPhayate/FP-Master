from Model.exp_model import EXP_MODEL
def get_derby_model():
    model = EXP_MODEL(sw='derby',
                      fv='10.9',
                      bvs=['10.8'],
                      pv='10.8',
                      cv='10.9',
                      dn='ApacheDerby')
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
    model = EXP_MODEL(sw='velocity',
                      fv='1.7',
                      bvs=["2.0"],
                      pv="1.6.4",
                      cv="1.7-beta1",
                      dn='ApacheVelocity')
    model.previous_version = "1.6"
    return model

def get_pdt_prs_merge_stub():
    model = EXP_MODEL(sw='velocity',
                      fv='1.6',
                      bvs=None,
                      pv=None,
                      cv=None,
                      dn='ApacheVelocity')
    return model
