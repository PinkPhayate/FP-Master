import sys,os

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import configparser
import matplotlib.pyplot as plt
from lib.metrics import Metrics_Origin

inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')


def _create_boxplot_diagram(g1, g2, save_name, title=None):
    # create graph just one version
    hige = (g1, g2)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    bp = ax.boxplot(hige)
    ax.set_xticklabels(['pre', 'cre'])
    plt.grid()
    plt.xlabel('VERSION')
    plt.ylabel('METRICS VALUE')
    # plt.title(title)
    plt.savefig(save_name)


if __name__ == '__main__':
    """
    メトリクスの分布を箱ひげ図で表すスクリプト
    """
    v1 = '4.1.0'
    v2 = '4.2.0'
    METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
    version1 = Metrics_Origin(v1, METRICS_DIR)
    version2 = Metrics_Origin(v2, METRICS_DIR)
    metrics = 'pc1'
    _v1 = version1.mrg_df[[metrics]]
    _v2 = version2.mrg_df[[metrics]]
    save_name = 'compare-wisky-'+metrics+'.png'
    _create_boxplot_diagram(_v1, _v2, save_name)
