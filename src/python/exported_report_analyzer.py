import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
EXECUTION_MODE = inifile.get('env', 'mode')
ENV = inifile.get('env', 'locale')
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'

import pandas as pd
def measure_prediction_actual_value(model):
    def __count_specified_area(df, probability):
        # df.apply(lambda x: print(x[['predict']].values[0]), axis=1)
        tmp = df[df.apply(lambda x: x[['predict']].values[0] >= probability, axis=1)].dropna()
        # tmp.apply(lambda x: print(x[['predict']].values[0]), axis=1)
        tmp = tmp[tmp.apply(lambda x: probability+0.1 > x[['predict']].values[0], axis=1)].dropna()
        # print('probability {}: {}'.format(probability, len(tmp)))
        return len(tmp)

    version = model.final_version
    filename = '{}{}ITG-report.csv'.format(REPORT_DIR, version)
    try:
        df = pd.read_csv(filename, index_col=0, header=0).dropna()
    except Exception:
        return
    print('version: {}'.format(version))
    # 確率別の予測数
    fault_df = df[df['actual'].apply(lambda x: x == 1)]
    # predicts = df[['predict']]
    prob_list = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    for p in prob_list:
        # print('fp count / probabilities', end='')
        fp_num = __count_specified_area(df, p)
        # print('corrected fp count / probabilities', end='')
        tf_num = __count_specified_area(fault_df, p)
        if fp_num==0:
            print('probability{}: precision: 0 ({}/{})'.format(p, tf_num, fp_num))
        else:
            print('probability{}: precision: {} ({}/{})'.format(p, float(tf_num)/fp_num, tf_num, fp_num))
