import version
import pandas as pd

def removePath(df):
    list = map(lambda x: x[x.rfind('\\')+1:-1]+'a', df['filename'])
    df = df.ix[:,1:]
    df = pd.DataFrame(list).join(df)
    df.rename(columns={0: 'filename'}, inplace=True)
    return df



def create_df(ver):

    # product metrics
    productM = pd.read_csv('./../../Data/metrics/prdctM/productMetricsByMyTool_v' + ver + '.csv', header=None)
    productM.columns = ['filename', 'TCchar', 'LOC2','N1','N2','eta1','eta2','N','NN','NF']
    productM = removePath(productM)

    #  import metcis by understand
    df = pd.read_csv('./../../Data/metrics/prdctM/solr' + ver + '.csv', header=0)
    df = df.ix[df['Kind']=='File',:]
    # metrics_und = df[['Name','AvgCyclomatic','CountLineCode','SumCyclomatic']]
    metrics_und = df[['Name','AvgCyclomatic','CountLineCode','SumCyclomatic', 'CountLineComment']]
    metrics_und.rename(columns={'Name': 'filename'}, inplace=True)
    # 'filename','AvgCyclomatic','CountLineCode','SumCyclomatic','CountLineComment'

    #  merge productM by my tool and by understand
    productM = pd.merge(productM, metrics_und, on='filename')
    productM = productM.dropna()
    productM = productM.drop_duplicates(subset=['filename'])
        # [u'filename', u'TCchar', u'LOC2', u'N1', u'N2', u'eta1', u'eta2', u'N', u'NN', u'NF', u'AvgCyclomatic', u'CountLineCode', u'SumCyclomatic', 'CountLineComment']

    # process metrics
    processM = pd.read_csv('./../../Data/metrics/prcssM/processMetrics_v' + ver + '.csv', header=None)
    processM.columns = ['filename', 'NumOfBug', 'LOC','chum','relatedChum','delectChum','ncdChum', 'isNewModule']
    processM['filename'] = processM['filename'].str.replace('/', '\\')
    # processM.rename(columns={0: 'filename'}, inplace=True)
    processM = removePath(processM)

    #  merge productM and processM
    df = pd.merge(productM, processM, on='filename', how='outer')
    metrics = df.dropna()
    # [u'filename', u'TCchar', u'LOC2', u'N1', u'N2', u'eta1', u'eta2', u'N',u'NN', u'NF', u'AvgCyclomatic', u'CountLineCode', u'SumCyclomatic', 'CountLineComment', u'NumOfBug', u'LOC', u'chum', u'relatedChum', u'delectChum', u'ncdChum',u'isNewModule'],
    # metrics = metrics[['filename', 'TCchar', 'CountLineCode','N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule']]
    metrics = metrics[['filename', 'TCchar', 'CountLineCode', 'CountLineComment', 'N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule']]

    # create bug module list
    df = pd.read_csv('./../../Data/metrics/numBug/slr_'+ver+'_bgmd.csv', header=0)
    bug_modules = df.apply(lambda x: x.str.replace('/', '\\'))
    bug_modules.columns = ['filename']
    bug_modules_list = map(lambda x: x[x.rfind('\\')+1:-1]+'a', bug_modules['filename'])

    metrics['fault'] = metrics['filename'].isin(bug_modules_list)
    # tmp['fault'] = metrics['filename'].isin(bug_modules_list)
    tmp = metrics['filename'].isin(bug_modules_list)
    # metrics = metrics[['filename', 'TCchar', 'CountLineCode','N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule']]
    metrics = metrics[['filename', 'TCchar', 'CountLineCode', 'CountLineComment', 'N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule']]

    tmp = tmp.apply(lambda x: 1 if x else 0)
    tmp.columns = ['tmp']

    metrics = pd.concat([metrics, tmp], axis=1)
    # metrics.columns = ['filename', 'TCchar', 'CountLineCode','N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule', 'fault']
    metrics.columns = ['filename', 'TCchar', 'CountLineCode', 'CountLineComment','N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'isNewModule', 'fault']
    metrics = metrics[['filename', 'TCchar', 'CountLineCode', 'CountLineComment','N','NN','NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum', 'fault']]
    # nml_metrics =  metrics[['filename', 'TCchar', 'CountLineCode', 'CountLineComment', 'N', 'NN', 'NF', 'SumCyclomatic', 'fault']]
    # [u'filename', u'TCchar', u'LOC2', u'N1', u'N2', u'eta1', u'eta2', u'N',u'NN', u'NF', u'AvgCyclomatic_x', u'CountLineCode_x',u'SumCyclomatic_x', u'AvgCyclomatic_y', u'CountLineCode_y',u'SumCyclomatic_y', u'NumOfBug', u'LOC', u'chum', u'relatedChum',u'delectChum', u'ncdChum', u'isNewModule'],

    # pd.DataFrame(metrics).to_csv( './../../Data/metrics/rfn/solr_ex1_rfn_' + ver +'.csv', index=False, cols=None)
    # pd.DataFrame(nml_metrics).to_csv( './../../Data/metrics/nml/solr_ex1_nml_' + ver +'.csv', index=False, cols=None)
    return metrics

def get_merged_merrics( versions ):
    merged_df = pd.DataFrame([])
    for ver in versions:
        df =  pd.read_csv ('/Users/phayate/Documents/FP-Predict/Data/'+ ver[0] +'_dataframe.csv', header=0)
        df = df.ix[:,2:]
        merged_df = pd.concat([merged_df, df])
    return merged_df


if __name__ == '__main__':
    vers = version.get_version_short_list()
    for ver in vers :
        print ver
        df = create_df(ver)
        df.to_csv('./../../Data/'+ver+'_dataframe.csv')
