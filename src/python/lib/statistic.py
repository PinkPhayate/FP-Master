import metrics as me
from scipy import stats
# import figure as fig
import configparser
import sys

# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'
EXECUTION_MODE = inifile.get('env', 'mode')

args = sys.argv
v1 = args[1]
v2 = args[2]

# バージョンのメトリクスを比較する
def compare_each_metrics():
    # version1 = me.Metrics_Derby(v1, METRICS_DIR)
    # print(version1.mrg_df.ix[:,1])
    version2 = me.Metrics_Derby(v2, METRICS_DIR)
    print(version2.mrg_df)
    version2.export_df()

    # fig.compare_metrics(filename=)

def ks_2samp(m1, m2):
    ks_result = stats.ks_2samp(m1, m2)
    print(ks_result.pvalue)
    # print(stats.ks_2samp(m1, m2))




def compare_two_versions(version1, version2):
    metrics = ['pd1','pd2','pd3','pd4','pd5','pd6','pc1','pc2','pc3','pc4']
    for m in metrics:
        print(m+': ',end='')
        m1 = version1.mrg_df[m]
        m2 = version2.mrg_df[m]
        ks_2samp(m1, m2)

# compare_each_metrics()

version1 = me.Metrics_Derby(v1, METRICS_DIR)
version2 = me.Metrics_Derby(v2, METRICS_DIR)
# version3 = me.Metrics_Derby('10.10', METRICS_DIR)
print(v1+'-'+v2)
compare_two_versions(version1,version2)
