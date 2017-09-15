import pandas as pd
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result/'

def analye_pred_value():
    df = pd.read_csv(REPORT_DIR + '4.4.0nml_values.csv')
    status_df = df.ix[:, :3]
    df = df.ix[:, 4:]
    modified_df = status_df.loc[:, 'isModified']
    d = modified_df[df.applymap(lambda x: if x==1)]
