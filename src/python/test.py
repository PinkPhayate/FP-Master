
def test_calculate_accum_fault():
    from lib.fopt import Fopt
    import pandas as pd
    d1 = pd.DataFrame([3,0,3,1,2,2,1,2,3,4])
    fopt = Fopt(d1, d1)
    print(fopt.calculate_accum_fault(d1))

test_calculate_accum_fault()
