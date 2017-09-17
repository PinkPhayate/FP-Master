import pandas as pd
import configparser
import matplotlib.pyplot as plt

report_df = pd.read_csv('/Users/phayate/Dropbox/STUDY/Result/4.5.0nml_values.csv', header=0, index_col=0)
def calculate_modified_fp(report_df):
    """
    FPと予測したモジュールのうち、修正のあったモジュールがどのくらいあったかを調査するスクリプト
    50回試行したうち、修正モジュール数とFP数が異なっていたかをカウントする。
    つまり、カウントが多いほど、修正モジュールがFPになっている可能性が高く、
    """
    #修正されたかつ、FPだったモジュールの数
    modified_df = report_df[report_df['isModified'].apply(lambda x: x == 1)]
    value_df = modified_df.ix[:, 3:]
    s = value_df.apply(lambda x: sum(x))

    # FPと予測したモジュールの個数
    value_df = report_df.ix[:, 3:]
    all_sum = value_df.apply(lambda x: sum(x))

    d = pd.concat([s, all_sum], axis=1)
    d = d.apply(lambda x: x[0]/x[1], axis=1)
    return d, len(d[d.apply(lambda x: x < 1.0)])

def calc_rate_fp_modified():
    for version in versions:
        for model_type in types:
            filename = '/Users/phayate/Dropbox/STUDY/Result/{0}{1}_values.csv'\
                                            .format(version, model_type)
            try:
                df = pd.read_csv(filename, header=0, index_col=0)
                sr, num = calculate_modified_fp(report_df=df)
                print('{0}-{1} {2}'.format(version, model_type, num))
                lab = "{0}{1}".format(version, model_type)
                left = range(len(sr))
                height = sr.tolist()
                plt.plot(left, height, label=lab)
            except Exception as e:
                print(e)
    plt.legend()
    plt.show()

def count_bug_in_modified_df():
    def count_bugs(report_df):
        bug_df = report_df[report_df['actual'].apply(lambda x: x == 1)]
        modified_df = bug_df[bug_df['isModified'].apply(lambda x: x == 1)]
        print('{0} / {1}'.format(len(modified_df), len(bug_df)))

    for version in versions:
        for model_type in types:
            filename = '/Users/phayate/Dropbox/STUDY/Result/{0}{1}_values.csv'\
                                            .format(version, model_type)
            try:
                df = pd.read_csv(filename, header=0, index_col=0)
                print('{0}-{1}: '.format(version, model_type), end='')
                count_bugs(report_df=df)
            except Exception as e:
                print(e)


# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
versions = inifile.get('version', 'derby').split(',')
# versions = inifile.get('version', 'solr').split(',')
versions.extend(inifile.get('version', 'solr').split(','))
types = inifile.get('model', 'model').split(',')

# calc_rate_fp_modified()
count_bug_in_modified_df()
