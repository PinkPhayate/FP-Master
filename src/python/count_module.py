"""
- 各バージョンのバグ個数
- 変更モジュール数、
- 変更モジュールのうちの欠陥数
    を取得するスクリプト
"""
from Model import model_creator
import pandas as pd
import configparser
from lib.metrics import Metrics_Origin
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

# def get_metrics_count(df):


def main():
    import csv
    f = open('sw_indecies.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    model_dict = model_creator.get_model_dictionary()
    indecies_list = []
    col_list = ['total modules', 'modified modules', 'bug modules',
                'modified bug modules']
    writer.writerow(col_list)
    for sw_name, models in model_dict.items():
        for model in models:
            print(sw_name, model.final_version)
            metrics_dir = "/Users/{}/Dropbox/STUDY/Metrics/".format(ENV)
            version = model.final_version
            metrics = Metrics_Origin(version, metrics_dir, model)
            modified_df, modified_fault = metrics.get_modified_df()
            df = pd.concat([modified_df, modified_fault], axis=1)
            modified_df = df.rename(columns = {df.columns[-1]:'fault'})

            mrg_df, fault = metrics.mrg_df, metrics.fault
            df = pd.concat([mrg_df, fault], axis=1)
            df = df.rename(columns = {df.columns[-1]:'fault'})
            # print(df)
            li = ['{} {}'.format(sw_name, model.final_version)]
            # 総モジュール数
            print('total modules, {}'.format(len(df)))
            li.append(len(df))
            # 変更モジュール数
            print('modified modules, {}'.format(len(modified_df)))
            li.append(len(modified_df))

            #  総欠陥数
            d = df[fault.apply(lambda x: x==1)]
            print('bug modules, {}'.format(len(d)))
            li.append(len(d))

            #  変更が合ったうちの総欠陥数
            d = modified_df[fault.apply(lambda x: x==1)]
            print('modified bug modules, {}'.format(len(d)))
            li.append(len(d))
            writer.writerow(li)

main()
