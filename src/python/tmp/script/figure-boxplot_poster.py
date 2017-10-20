import sys,os
import pandas as pd

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import configparser
import matplotlib.pyplot as plt
from lib.metrics import Metrics_Origin

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')


def __create_boxplot_seaborn(g1, g2, save_name, title=None):
    # create graph just one version
    # import seaborn as sns
    # hige = pd.concat([g1, g2], axis=1)
    hige = (g1, g2)
    # hige.columns = [['org', 'dst']]
    fig = plt.figure()

    ax = fig.add_subplot(111)
    bp = ax.boxplot(hige)
    ax.set_xticklabels(['org', 'dst'])
    # sns.boxplot(data=hige)
    # flatui = ["#3498db", "#95a5a6"]
    # sns.set_palette(flatui)
    # ax.set_xticklabels(['pre', 'cre'])
    plt.grid()
    plt.xlabel('model')
    plt.ylabel('f1 value')
    plt.savefig(save_name)

if __name__ == '__main__':
    """
    メトリクスの分布を箱ひげ図で表すスクリプト
    """
    args = sys.argv
    sw = args[1] if 1 < len(args) else 'solr'
    versions = inifile.get('version', sw).split(',')
    types = inifile.get('model', 'model').split(',')
    METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'
    for version in versions:
        # filename = 'Solr4.5.0-ITG-all_values'
        filename_org = '{}{}-RFN-all_values.csv'.format(sw, version)
        filename_dst = '{}{}-ITG-all_values.csv'.format(sw, version)
        try:
            df_org = pd.read_csv(METRICS_DIR + filename_org, index_col=0, header=0)
            df_dst = pd.read_csv(METRICS_DIR + filename_dst, index_col=0, header=0)
            save_name = 'compare-wisky-'+version+'.png'
            __create_boxplot_seaborn(df_org.ix[:,2], df_dst.ix[:,2], save_name)
            save_name = 'compare-wisky-'+version+'_mdf.png'
            __create_boxplot_seaborn(df_org.ix[:,8], df_dst.ix[:,8], save_name)
        except Exception as e:
            print(e)
