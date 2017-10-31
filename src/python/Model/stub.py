from Model.exp_model import EXP_MODEL
def get_derby_model():
    model = EXP_MODEL(sw='derby',
                      fv='10.9',
                      bvs=['10.8'],
                      pv='10.8',
                      cv='10.9',
                      dn='ApacheDerby')
    return model
