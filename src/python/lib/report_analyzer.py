import pandas as pd
from lib.auc import AUC

class Analyzer(object):
    COLUM_NAMES = ['predict', 'actual', 'isNew', 'isModified']
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
        new_mods = __df.apply(lambda x: x['isNew'] == 1, axis=1)
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
        itnm = float(iter_num)
        print('model: {}, version: {}'.format(
            self.model_type, self.predict_version))
        s = sum(self.accum_val0)
        msg = "[report] value0: {}".format(s/itnm)
        print(msg)
        s = sum(self.accum_val1)
        msg = "[report] value1: {}".format(s/itnm)
        print(msg)
        s = sum(self.accum_val2)
        msg = "[report] value2: {}".format(s/itnm)
        print(msg)
        s = sum(self.accum_val3)
        msg = "[report] value3: {}".format(s/itnm)
        print(msg)
        s = sum(self.accum_val4)
        msg = "[report] value4: {}".format(s/itnm)
        print(msg)
