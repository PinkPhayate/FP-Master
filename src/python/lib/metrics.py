import pandas as pd
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')

class Metrics_Derby:
    def __init__(self,version, metrics_dir):
        metrics_dir = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
        self.version  = version
        df = pd.read_csv(metrics_dir + '/mergedMetrics'+version+'.csv', header = None)
        self.process_df = df.ix[:,4:7]
        self.process_df.columns = ['pc1','pc2','pc3','pc4']

        self.product_df = df.ix[:,11:16]
        self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']

        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)

        self.fault = df[8]
        # self.fault.columns = ['fault']
        self.__name_columns()

    def put_metrics(self, df):
        self.product_df = df.ix[:,:6]
        self.product_df = df.ix[:,6:9]
        self.mrg_df = pd.concat([self.product_df, self.process_df], axis=1)
        self.__name_columns()

    def put_fault(self,f):
        self.fault = f

    def __name_columns(self):
        self.process_df.columns = ['pc1','pc2','pc3','pc4']
        self.product_df.columns = ['pd1','pd2','pd3','pd4','pd5','pd6']
        self.fault.columns = ['fault']

    def export_df(self):
        df = pd.concat([self.mrg_df, self.fault], axis=1)
        df.to_csv("export_metrics" + self.version + ".csv")

    def get_alike_df(self, alike_metrics):
        return self.mrg_df[alike_metrics]

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
