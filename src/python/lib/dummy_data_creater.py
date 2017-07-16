from imblearn.over_sampling import SMOTE
import pandas as pd
import random
from lib import metrics as me
"""
This module creates dummy data
elder_df -> seed version
later_m -> target version

"""

def create_dummy_negative_data(elder_m, later_m):
    smote = SMOTE(kind='regular')
    # create negative data
    # elder_m = me.Metrics_Adam(elder)
    # later_m = me.Metrics_Adam(later)
    dummy_df = pd.DataFrame([])
    origin_num = len( later_m.mrg_df[ later_m.fault > 0 ] )
    k = 0
    N = len( elder_m.mrg_df[ elder_m.fault > 0 ] )
    while k<N :
        X_resampled, y_resampled = smote.fit_sample(later_m.mrg_df, later_m.fault)
        neg_df = pd.DataFrame( X_resampled[ y_resampled > 0 ] )
        tmp_df = neg_df.ix[origin_num+1:,:]
        # tmp_df.loc[:, 'fault'] = 1
        tmp_df.loc.__setitem__((slice(None), ('fault')), 1)
        dummy_df = pd.concat([dummy_df, tmp_df],axis=0)
        k = len(dummy_df)
    dummy_df = dummy_df.reset_index( drop = True )
    dummy_df = dummy_df.ix[ :N-1 , : ]
    return dummy_df

def create_dummy_positive_data(elder, later):
    smote = SMOTE(kind='regular')
    # create negative data
    # elder_m = me.Metrics_Adam(elder)
    reduced_m = _reduce_positive_df(later)
    later_m = _create_metrics_module(reduced_m)

    dummy_df = pd.DataFrame([])
    origin_num = len( later_m.mrg_df[ later_m.fault < 1 ] )
    k = 0
    N = len( elder.mrg_df[ elder.fault < 1 ] )
    while k<N :
        X_resampled, y_resampled = smote.fit_sample(later_m.mrg_df, later_m.fault)
        pos_df = pd.DataFrame( X_resampled[ y_resampled < 1 ] )
        tmp_df = pos_df.ix[origin_num+1:,:]
        tmp_df.loc[:, 'fault'] = 0
        dummy_df = pd.concat([dummy_df, tmp_df],axis=0)
        k = len(dummy_df)
    dummy_df = dummy_df.reset_index( drop = True )
    dummy_df = dummy_df.ix[ :N-1 , : ]

    return dummy_df


def _reduce_positive_df(metrics):
    neg_df = metrics.mrg_df[ metrics.fault > 0]
    N = len( neg_df )
    pos_df = metrics.mrg_df[ metrics.fault < 1]
    pos_df = pos_df.loc[ random.sample(list(pos_df.index), int(N/2)) ]
    df = pd.concat([neg_df, pos_df], axis=0)
    df = pd.concat([df, metrics.fault], axis=1, join_axes=[df.index])
    return df

def _create_metrics_module(df):
    metrics = me.Metrics_Adam("v2")     # v2 is CHANGEABLE
    metrics.put_metrics(df.iloc[:,:-1])
    metrics.put_fault(df.iloc[:,-1])
    return metrics

def create_dummy_metrics(m1,m2):
    pos_dummy_df = create_dummy_positive_data(m1,m2)
    neg_dummy_df = create_dummy_negative_data(m1,m2)
    df = pd.concat([pos_dummy_df, neg_dummy_df], axis=0)
    return _create_metrics_module(df)

# elder_m = me.Metrics_Adam('v1')
# later_m = me.Metrics_Adam('v2')
# metrics = create_dummy_negative_data(elder_m, later_m)
# print(metrics.product_df)
