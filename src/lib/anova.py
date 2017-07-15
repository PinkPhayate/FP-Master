import pandas as  pd
import scipy.stats as stats
import random
ROOT_DIR = '/Users/phayate/Documents/FP-Predict3/Data/Diagram_list/'

def compare_3model( filename ):
    df = pd.read_csv(filename, header=0, index_col=0)
    df.columns = [['nml','rfn','chr','rnd']]
    # random sampling
    # df = df.loc[ random.sample(list(df.index), 10) ]
    rfn = df['rfn']
    nml = df['nml']
    chr = df['chr']
    print(stats.f_oneway(nml,rfn,chr))

def _select_10sample(df):
    return df.loc[ random.sample(list(df.index), 10) ]

def get_list_from_3line(filename):
    df = pd.read_csv(filename, header=0, index_col=0)
    df.columns = [['nml','rfn','chr','rnd']]
    # random sampling
    # df = df.loc[ random.sample(list(df.index), 10) ]
    return df

def get_list_one(filename):
    df = pd.read_csv(filename, header=0, index_col=0)
    df.columns = [['rfn']]
    df = df.loc[ random.sample(list(df.index), 10) ]
    return df['rfn']


def main():
    print('experiment1 - Adam')
    filename = ROOT_DIR + 'Adamv2-v3ex01-diagram.csv'
    compare_3model(filename)

    print('experiment1 - Derby')
    filename = ROOT_DIR + 'Derby10.9-10.10ex01-diagram.csv'
    compare_3model(filename)

    print('experiment2 - Adam')
    filename = ROOT_DIR + 'Adamv3ex02-diagram.csv'
    compare_3model(filename)

    print('experiment2 - Derby')
    filename = ROOT_DIR + 'Derby10.10ex02-diagram.csv'
    compare_3model(filename)
    #
    #
    #
    print('compare1-2 - Adam')
    filename = ROOT_DIR + 'Adamv2-v3ex01-diagram.csv'
    df1 = get_list_from_3line(filename)
    filename = ROOT_DIR + 'Adamv3ex02-diagram.csv'
    df2 = get_list_from_3line(filename)
    print(stats.f_oneway(df1['nml'],df2['nml']))
    print(stats.f_oneway(df1['rfn'],df2['rfn']))
    print(stats.f_oneway(df1['chr'],df2['chr']))
    #
    #
    #
    print('compare1-2 - Derby')
    filename = ROOT_DIR + 'Derby10.9-10.10ex01-diagram.csv'
    df1 = get_list_from_3line(filename)
    filename = ROOT_DIR + 'Derby10.10ex02-diagram.csv'
    df2 = get_list_from_3line(filename)
    print(stats.f_oneway(df1['nml'],df2['nml']))
    print(stats.f_oneway(df1['rfn'],df2['rfn']))
    print(stats.f_oneway(df1['chr'],df2['chr']))


    # print('compare2-4 - Adam')
    # filename = ROOT_DIR + 'Adamv3ex04-diagram.csv'
    # df4 = get_list_one(filename)
    # filename = ROOT_DIR + 'Adamv3ex02-diagram.csv'
    # df2 = get_list_from_3line(filename)['rfn']
    # print(stats.f_oneway(df2,df4))
if __name__ == '__main__':
    main()
