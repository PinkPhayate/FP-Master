import pandas as pd

class AUC:
    def __init__(self,df):
        self.df = df

    def save_ev_values( self, filename ):
        self.df.to_csv("../Data/Research/"+filename)

    @property
    def circulate_auc(self):

        # sorting
        self.df =self.df.sort_values(by='ev_value',ascending=False)
        # Indicator about num of existed fault
        NumF = self.df['fault'].sum(axis=0)
        # Size of DataFrame
        size = len(self.df)
        # size =self.df.size/len(df)

        # count: Indicator count predicted Fault
        count = 0
        list = []

        for i, row in self.df.iterrows():
            fault = row['fault']
            if int(fault) != 0:
                count += 1
            list.append( count )
        under = sum(list) - NumF/2.0
        # print 'size: ' + str(size)
        # print 'NumF: ' + str(NumF)
        # print 'under: ' + str(under)
        auc = under / float(size * NumF)
        return auc
