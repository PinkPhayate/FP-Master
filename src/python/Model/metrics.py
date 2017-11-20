import pandas as pd
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

class Metrics(object):
    def __init__(self, version, metrics_dir, model):
        self.version = model.final_version
        self.metrics_dir = metrics_dir
        self.model = model
        __filename = '{}/{}/all/mergedMetrics{}.csv'.format(metrics_dir, model.sw_name, version)
        df = pd.read_csv(__filename, header=None)
        self.process_df = df.ix[:, 4:6]
        self.process_df.columns = ['pc1','pc2','pc3']
        self.product_df = df.ix[:, 12:17]
        self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']

        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
        self.faults = df.ix[:, 9]
        self.loc = df.ix[:, 8]
        self.fault = self.faults.apply(lambda x: 1 if 0 < x else 0)
        self.isNew = df.ix[:, 3]
        self.__consider_modification()
        self.__name_columns()

    def put_metrics(self, df):
        self.product_df = df.ix[:, :6]
        self.product_df = df.ix[:, 6:9]
        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
        self.__name_columns()

    def put_fault(self, f):
        self.fault = f

    def __name_columns(self):
        self.process_df.columns = ['pc1','pc2','pc3']
        self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']
        self.fault.columns = ['fault']
        self.isNew.columns = ['isNew']
        self.isModified.columns = ['isModified']

    def export_df(self):
        df = pd.concat([self.mrg_df, self.fault], axis=1)
        df.to_csv("export_metrics" + self.version + ".csv")

    def get_specific_df(self, specific_metrics):
        return self.mrg_df[specific_metrics]

    def __consider_modification(self):
        # sum_df = self.process_df[self.process_df.sum(axis=1)]
        self.isModified = self.process_df.apply(
            lambda x: 1 if 0 < x.sum() else 0, axis=1)

    def get_modified_df(self):
        return self.mrg_df[self.isModified.apply(lambda x: x == 1)],\
               self.fault[self.isModified.apply(lambda x: x == 1)]

    def get_not_modified_df(self):
        return self.product_df[self.isModified.apply(lambda x: x == 0)],\
               self.fault[self.isModified.apply(lambda x: x == 0)]
