import metrics as me
# import figure as fig
import configparser

# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/JR/metrics-data/Apache-Derby'
EXECUTION_MODE = inifile.get('env', 'mode')

# バージョンのメトリクスを比較する
def compare_each_metrics():
    # version1 = me.Metrics_Derby('10.9', METRICS_DIR)
    # print(version1.mrg_df.ix[:,1])
    version2 = me.Metrics_Derby('10.8', METRICS_DIR)
    print(version2.mrg_df)
    version2.export_df()

    # fig.compare_metrics(filename=)

compare_each_metrics()
