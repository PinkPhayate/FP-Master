
def test_calculate_accum_fault():
    from lib.fopt import Fopt
    import pandas as pd
    d1 = pd.DataFrame([3,0,3,1,2,2,1,2,3,4])
    fopt = Fopt(d1, d1)
    print(fopt.calculate_accum_fault(d1))

def test_calculate_RUC():
    import pandas as pd
    from lib.fopt import Fopt
    d1 = pd.DataFrame([3,0,3,1,2,2,1,2,3,4])
    fopt = Fopt(d1, d1)
    d2 = fopt.calculate_accum_fault(d1)
    dlines = pd.DataFrame([10,10,10,10,10,10,10,10,10,10])
    print(fopt.calculate_auc(d2['accum_fault'], dlines))

# test_calculate_accum_fault()
test_calculate_RUC()
