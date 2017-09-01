import pandas as pd
from lib.auc import AUC

class Analyzer(object):
    COLUM_NAMES = ['predict', 'actual', 'isNew', 'isModified']
    accum_val1 = None   #   FPモジュールの上位何%が新モジュールなのか
    accum_val2 = None   #   変更のなかったモジュールに絞ったところ、どれくらいの精度なのか
    accum_val3 = None   #   変更があったモジュールに絞ったところ、どれくらいの精度なのか
    accum_val4 = None   #   新モジュールに絞ったところ、どれくらいの精度なのか

    def set_report_df(self, report):
        self.report_df = report
        self.report_df.columns = [self.COLUM_NAMES]

    def analyze(self):
        self.calculate_0()
        self.calculate_1()
        self.calculate_2()
        self.calculate_3()
        self.calculate_4()

    def calculate_diagram(self, actual, pred):
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
        print(msg)
        return diagram_value

    def calculate_1(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['actual'] == 1, axis=1)]
        total_num = len(__df)
        new_mods = __df.apply(lambda x: x['isNew'] == 1, axis=1)
        new_num = len(new_mods)
        value = new_num / float(total_num)
        rep_msg = "[report] value01: {}".format(value)
        print(rep_msg)
        return value

    def calculate_2(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 0, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value2: {}'.format(diagram_value)
        print(msg)
        return diagram_value

    def calculate_3(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isModified'] == 1, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value3: {}'.format(diagram_value)
        print(msg)
        return diagram_value

    def calculate_4(self):
        __df = self.report_df[self.report_df.apply(
            lambda x: x['isNew'] == 1, axis=1)]
        diagram_value = self.calculate_diagram(
            __df[['predict']], __df[['actual']])
        msg = '[result] diagram_value4: {}'.format(diagram_value)
        print(msg)
        return diagram_value
