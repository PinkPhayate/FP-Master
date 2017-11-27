from lib import metrics as me
from scipy import stats
# import figure as fig
import configparser
import sys

THRESOLD = 0.05
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
EXECUTION_MODE = inifile.get('env', 'mode')

# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'
EXECUTION_MODE = inifile.get('env', 'mode')

# args = sys.argv
# v1 = args[1]
# v2 = args[2]


# バージョンのメトリクスを比較する
def compare_each_metrics():
    # version1 = me.Metrics_Derby(v1, METRICS_DIR)
    # print(version1.mrg_df.ix[:,1])
    version2 = me.Metrics_Derby('10.8', METRICS_DIR)
    if EXECUTION_MODE == 'debug':
        print(version2.mrg_df)
    version2.export_df()

    # fig.compare_metrics(filename=)

def ks_2samp(m1, m2):
    ks_result = stats.ks_2samp(m1, m2)
    if EXECUTION_MODE == 'debug':
        print(ks_result.pvalue)
    return ks_result.pvalue
    # print(stats.ks_2samp(m1, m2))




def compare_two_versions(version1, version2):
    metrics = version1.mrg_df.columns
    alike_metrics = []
    for m in metrics:
        if EXECUTION_MODE == 'debug':
            print(m+': ',end='')
        m1 = version1.mrg_df[m]
        m2 = version2.mrg_df[m]
        pvalue = ks_2samp(m1, m2)
        print(str(pvalue)+', ', end='')
        if (THRESOLD < pvalue):
            alike_metrics.append(m)
    return alike_metrics

def conduct_m_whitney_test(result1, result2):
    from scipy import stats
    result = stats.mannwhitneyu(result1, result2)
    return result.pvalue
