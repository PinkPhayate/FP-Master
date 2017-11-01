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
