import pandas as pd
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

class Metrics_Origin(object):
    def __init__(self, version, metrics_dir):
        self.version = version
        self.metrics_dir = metrics_dir
        df = pd.read_csv(metrics_dir + '/mergedMetrics'+version+'.csv', header=None)
        self.process_df = df.ix[:, 4:7]
        self.process_df.columns = ['pc1','pc2','pc3','pc4']

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
        self.product_df = df.ix[:,:6]
        self.product_df = df.ix[:,6:9]
        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
        self.__name_columns()

    def put_fault(self, f):
        self.fault = f

    def __name_columns(self):
        self.process_df.columns = ['pc1','pc2','pc3','pc4']
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
               self.faults[self.isModified.apply(lambda x: x == 1)]

    def get_not_modified_df(self):
        return self.product_df[self.isModified.apply(lambda x: x == 0)],\
               self.faults[self.isModified.apply(lambda x: x == 0)]


# class Metrics_Derby:
#     def __init__(self,version, metrics_dir):
#         # metrics_dir = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
#         self.version  = version
#         df = pd.read_csv(metrics_dir + '/mergedMetrics'+version+'.csv', header = None)
#         self.process_df = df.ix[:,4:7]
#         self.process_df.columns = ['pc1','pc2','pc3','pc4']
#
#         self.product_df = df.ix[:,11:16]
#         self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']
#
#         self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
#
#         self.fault = df[8]
#         # self.fault.columns = ['fault']
#         self.__name_columns()
#
#     def put_metrics(self, df):
#         self.product_df = df.ix[:,:6]
#         self.product_df = df.ix[:,6:9]
#         self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
#         self.__name_columns()
#
#     def put_fault(self,f):
#         self.fault = f
#
#     def __name_columns(self):
#         self.process_df.columns = ['pc1','pc2','pc3','pc4']
#         self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']
#         self.fault.columns = ['fault']
#
#     def export_df(self):
#         df = pd.concat([self.mrg_df, self.fault], axis=1)
#         df.to_csv("export_metrics" + self.version + ".csv")
#
#     def get_alike_df(self, alike_metrics):
#         return self.mrg_df[alike_metrics]

class Metrics_Adam:
    def __init__(self,version):
        METRICS_DIR = "/Users/"+ENV+"/Dropbox/STUDY/JR/metrics-data/Adam"
        self.version  = version
        df = pd.read_csv(METRICS_DIR + '/mergedMetrics'+version+'.csv', header = None)
        self.process_df = df.ix[:,3:6]
        # self.process_df.columns = ['pc1','pc2','pc3','pc4']

        self.product_df = df.ix[:,10:16]
        # self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']

        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)

        self.fault = df[7]
        self.__name_columns()
        # self.fault.columns = ['fault']
    def put_metrics(self, df):
        self.product_df = df.iloc[:,:6]
        self.process_df = df.iloc[:,6:]
        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
        self.__name_columns()

    def put_fault(self,f):
        self.fault = f

    def __name_columns(self):
        self.process_df.columns = ['pc1','pc2','pc3','pc4']
        self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']
        self.fault.columns = ['fault']
        self.faults.columns = ['faults']
