import pandas as pd
from lib import metrics_operator as mp
from lib import over_sampling as ovs


class Metrics:
    def __init__(self, dir):
        self.__dir = dir
        self.smote = ovs.SMOTE(1000)


    def get_merged_metrics( self, versions ):
        merged_df = pd.DataFrame([])
        for ver in versions:
            df = self.get_metrics(ver[0])
            merged_df = pd.concat([merged_df, df])
        return merged_df


    # label   : -> 0 or
    # df      : seed of random samplig
    # size    : number of dumy DataFrame size
    def create_dummy_data(self, label, df, size):
        dummy_df = pd.DataFrame([])
        smp=df.ix[:,:-1].as_matrix()
        cv=df.ix[:,-1].as_matrix()

        while len(dummy_df) < size :
            self.smote = ovs.SMOTE(1000)
            sampled_np = self.smote.oversampling(smp=smp, cv=cv, label=label)
            # print(len(sampled_np))
            _tmp = pd.DataFrame( sampled_np )
            _tmp = _tmp.ix[:,4:9]
            _tmp['fault'] = label
            dummy_df = pd.concat( [dummy_df, _tmp])
        dummy_df = dummy_df.reset_index( drop = True )
        return dummy_df.ix[:size-1,:]

    def get_metrics( self, version ):
        df =  pd.read_csv (self.__dir+ version +'_dataframe.csv', header=0)
        df = df.ix[:,2:]
        # return df

    def get_all_metrics( self, versions):
        all_metrics = pd.DataFrame([])
        for ver in versions:
            df = self.get_metrics(ver[0])
            all_metrics = pd.concat([all_metrics, df])
        return all_metrics
