import pandas as pd
class Fopt(object):
    # df.columns = [prob, actual]
    def __init__(self,predict, actual):
        self.predict = predict
        self.predict.columns = [['prob']]
        self.actual = actual
        self.actual.columns = [['actual']]


    def calculate_fopt_delta(self):
        df = pd.concat(self.predict, self.actual, axis=1)
        sorted_df = df.sort_values(by='prob',ascending=False)
        # accum_fault_prob = self.ccalculate_auc(sorted_df['actual','loc'])

        sorted_df = df.sort_values(by='actual',ascending=False)
        # accum_fault_actual = self.calculate_auc(sorted_df['actual','loc'])

    def calculate_accum_fault(self, df):
        ac = 0
        list = []
        for i, v in df.iterrows():
            # print(v)
            ac += v[0]
            list.append(ac)
        df['accum_fault'] = pd.DataFrame(list)
        return df

    def calculate_auc(self, accums, line_df):
        S = 0
        total_line = line_df.sum()
        line_df = line_df / total_line[0]
        df = pd.concat([accums, line_df], axis=1)
        d = df.apply(lambda x: x[0] * x[1])
        return d.sum()
