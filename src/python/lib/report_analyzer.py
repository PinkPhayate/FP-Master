import pandas as pd
from lib.auc import AUC
import sklearn.metrics as skm
from sklearn.exceptions import UndefinedMetricWarning
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'


class Analyzer(object):
    COLUM_NAMES = ['predict', 'actual', 'isNew', 'isModified']
    COLUMNS = ['MODEL', 'value0', 'value1', 'value2', 'value3', 'value4']
    accum_val0 = []  # 通常の値
    accum_val1 = []  # FPモジュールの上位何%が新モジュールなのか
    accum_val2 = []  # 変更のなかったモジュールに絞ったところ、どれくらいの精度なのか
    accum_val3 = []  # 変更があったモジュールに絞ったところ、どれくらいの精度なのか
    accum_val4 = []  # 新モジュールに絞ったところ、どれくらいの精度なのか
    values_list = []



    def __init__(self, version, model_type):
        self.predict_version = version
        self.model_type = model_type
        if self.accum_val0 is not None:
            self.accum_val0 = []
        if self.accum_val1 is not None:
            self.accum_val1 = []
        if self.accum_val2 is not None:
            self.accum_val2 = []
        if self.accum_val3 is not None:
            self.accum_val3 = []
        if self.accum_val4 is not None:
            self.accum_val4 = []

    def set_report_repository(self, dir_name):
        """
        レポートの保存先を変えたい時に呼ぶ
        """
        global REPORT_DIR
        REPORT_DIR = dir_name

    def set_report_df(self, report):
        self.report_df = report
        self.report_df.columns = [self.COLUM_NAMES]

    def calculate(self):
        v0 = self.calculate_0()
        self.accum_val0.append(v0)
        v1 = self.calculate_1()
        self.accum_val1.append(v1)
        v2 = self.calculate_2()
        self.accum_val2.append(v2)
        v3 = self.calculate_3()
        self.accum_val3.append(v3)
        v4 = self.calculate_4()
        self.accum_val4.append(v4)

    def calculate_diagram(self, pred, actual):
        actual.reset_index(drop=True, inplace=True)
        pred.reset_index(drop=True, inplace=True)
        df = pd.concat([actual, pred], axis=1)
        df.columns = ['fault', 'ev_value']
        diagram_value = AUC(df). circulate_auc
        return diagram_value

    def calculate_0(self):
        __df = self.report_df.copy()
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value0: {}'.format(diagram_value)
        # print(msg)
        return diagram_value

    def calculate_1(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['actual'] == 1, axis=1)]
        total_num = len(__df)
        new_mods = __df[__df.apply(lambda x: x['isNew'] == 1, axis=1)]
        new_num = len(new_mods)
        value = new_num / float(total_num)
        rep_msg = "[report] value01: {}".format(value)
        # print(rep_msg)
        return value

    def calculate_2(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 0, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value2: {}'.format(diagram_value)
        # print(msg)
        return diagram_value

    def calculate_3(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 1, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value3: {}'.format(diagram_value)
        # print(msg)
        return diagram_value

    def calculate_4(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isNew'] == 1, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value4: {}'.format(diagram_value)
        # print(msg)
        return diagram_value

    def calculate_average(self, iter_num):
        df = pd.DataFrame([self.model_type, self.predict_version])
        itnm = float(iter_num)
        print('model: {}, version: {}'.format(
            self.model_type, self.predict_version))
        s = sum(self.accum_val0)
        msg = "[report] value0: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['value0', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_val1)
        msg = "[report] value1: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['value1', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_val2)
        msg = "[report] value2: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['value2', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_val3)
        msg = "[report] value3: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['value3', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_val4)
        msg = "[report] value4: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['value4', s/itnm])], axis=1)
        print(msg)
        return df

    def export(self, target_sw, df, predictor_type):
        report_file_name = REPORT_DIR + target_sw+'-' +predictor_type+'.csv'
        df.columns = self.COLUMNS
        df = df.ix[[1,3,5], :]
        import os
        if os.path.exists(report_file_name):
            report_df = pd.read_csv(report_file_name, header=0, index_col=0)
            report_df.columns = self.COLUMNS
        else:
            report_df = pd.DataFrame([])
        report_df = pd.concat([report_df, df], axis=0, ignore_index=True,)
        report_df.to_csv(report_file_name)

class AUCAnalyzer(Analyzer):
    COLUMNS = ['MODEL', 'recall0', 'precision0', 'accuracy0', 'recall2',
               'precision2', 'accuracy2', 'recall3', 'precision3', 'accuracy3',
               'recall4', 'precision4', 'accuracy4']
    report_file_name = ''

    accum_accuracy0 = []
    accum_recall0 = []
    accum_precision0 = []
    accum_accuracy2 = []
    accum_recall2 = []
    accum_precision2 = []
    accum_accuracy3 = []
    accum_recall3 = []
    accum_precision3 = []
    accum_accuracy4 = []
    accum_recall4 = []
    accum_precision4 = []

    def __init__(self, version, model_type, target_sw):
        self.predict_version = version
        self.model_type = model_type
        self.target_sw = target_sw
        self.report_file_name = REPORT_DIR + target_sw+'-aucreport.csv'
        # self.__remove_report_files()

        if self.accum_recall0 is not None:
            self.accum_recall0 = []
        if self.accum_precision0 is not None:
            self.accum_precision0 = []
        if self.accum_accuracy0 is not None:
            self.accum_accuracy0 = []
        if self.accum_recall2 is not None:
            self.accum_recall2 = []
        if self.accum_precision2 is not None:
            self.accum_precision2 = []
        if self.accum_accuracy2 is not None:
            self.accum_accuracy2 = []
        if self.accum_recall3 is not None:
            self.accum_recall3 = []
        if self.accum_precision3 is not None:
            self.accum_precision3 = []
        if self.accum_accuracy3 is not None:
            self.accum_accuracy3 = []
        if self.accum_recall4 is not None:
            self.accum_recall4 = []
        if self.accum_precision4 is not None:
            self.accum_precision4 = []
        if self.accum_accuracy4 is not None:
            self.accum_accuracy4 = []

    def __remove_report_files(self):
        import os
        if os.path.exists(self.report_file_name):
            os.remove(self.report_file_name)

    def calculate(self):
        self.calculate_0()
        self.calculate_2()
        self.calculate_3()
        self.calculate_4()

    def calculate_2indict(self, __df):
        recall = skm.recall_score(y_true=__df[['actual']],
                                  y_pred=__df[['predict']])
        accuracy = skm.accuracy_score(y_true=__df[['actual']],
                                      y_pred=__df[['predict']])
        precision = skm.precision_score(y_true=__df[['actual']],
                                      y_pred=__df[['predict']])
        return recall, accuracy, precision

    def calculate_0(self):
        __df = self.report_df.copy()
        recall, accuracy, precision = self.calculate_2indict(__df)
        self.accum_recall0.append(recall)
        self.accum_accuracy0.append(accuracy)
        self.accum_precision0.append(precision)

    def calculate_2(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 0, axis=1)]
        recall, accuracy, precision = self.calculate_2indict(__df)
        self.accum_recall2.append(recall)
        self.accum_accuracy2.append(accuracy)
        self.accum_precision2.append(precision)

    def calculate_3(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 1, axis=1)]
        recall, accuracy, precision = self.calculate_2indict(__df)
        self.accum_recall3.append(recall)
        self.accum_accuracy3.append(accuracy)
        self.accum_precision3.append(precision)

    def calculate_4(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isNew'] == 1, axis=1)]
        recall, accuracy, precision = self.calculate_2indict(__df)
        self.accum_recall4.append(recall)
        self.accum_accuracy4.append(accuracy)
        self.accum_precision4.append(precision)

    def calculate_average(self, iter_num):
        df = pd.DataFrame([self.model_type, self.predict_version])
        itnm = float(iter_num)
        print('model: {}, version: {}'.format(
            self.model_type, self.predict_version))
        s = sum(self.accum_recall0)
        msg = "[report] recall0: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['recall0', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_precision0)
        msg = "[report] precision0: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['precision0', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_accuracy0)
        msg = "[report] accuracy0: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['accuracy0', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_recall2)
        msg = "[report] recall2: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['recall2', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_precision2)
        msg = "[report] precision2: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['precision2', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_accuracy2)
        msg = "[report] accuracy2: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['accuracy2', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_recall3)
        msg = "[report] recall3: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['recall3', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_precision3)
        msg = "[report] precision3: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['precision3', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_accuracy3)
        msg = "[report] accuracy3: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['accuracy3', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_recall4)
        msg = "[report] recall4: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['recall4', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_precision4)
        msg = "[report] precision4: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['precision4', s/itnm])], axis=1)
        print(msg)
        s = sum(self.accum_accuracy4)
        msg = "[report] accuracy4: {}".format(s/itnm)
        df = pd.concat([df, pd.DataFrame(['accuracy4', s/itnm])], axis=1)
        print(msg)
        return df

    def export(self, target_sw, df, predictor_type):
        report_file_name = REPORT_DIR + target_sw+'-' +predictor_type+'-auc.csv'
        df.columns = self.COLUMNS
        df = df.ix[[1,3,5], :]
        print(df)
        import os
        if os.path.exists(self.report_file_name):
            report_df = pd.read_csv(self.report_file_name, header=0, index_col=0)
            report_df.columns = self.COLUMNS
        else:
            report_df = pd.DataFrame([])
        report_df = pd.concat([report_df, df], axis=0, ignore_index=True,)
        report_df.to_csv(report_file_name)
