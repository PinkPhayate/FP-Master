import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns
args = sys.argv
def __get_graph_data(filename):
    def __get_accum_list(df):
        list = []
        count = 0
        for i, row in df.iterrows():
            fault = row['fault']
            if int(fault) != 0:
                count += 1
                list.append( count )
                return list
    df = pd.read_csv(filename, header=0)
    list = __get_accum_list(df)
    X = df.index
    y = list
    return X,y

def compare_models(exNum):
    filename = './../Data/Research/'+str(exNum)+'nml.csv'
    X,y = __get_graph_data(filename)
    plt.plot(X, y, label='nml', color = 'blue')

    filename = './../Data/Research/'+str(exNum)+'rfn.csv'
    X,y = __get_graph_data(filename)
    plt.plot(X, y, label='ex3', color = 'red')

    filename = './../Data/Research/'+str(exNum)+'chn.csv'
    X,y = __get_graph_data(filename)
    plt.plot(X, y, label='chn', color = 'green')

    # plt.show()
    filename = './../data/Research/'+str(exNum)+'.png'
    plt.legend(loc='lower right')
    plt.savefig(filename)

def compare_two_models(file1,file2,svfile):
    X,y = __get_graph_data(file1)
    plt.plot(X, y, label='nml', color = 'blue')

    X,y = __get_graph_data(file2)
    plt.plot(X, y, label='ex3', color = 'red')

    # plt.show()
    filename = './../data/Research/'+svfile+'.png'
    plt.legend(loc='lower right')
    plt.savefig(filename)

def _get_diagram_df ( filename ):
    df = pd.read_csv(filename, header=0, index_col=0)
    df.columns = [['NML','RFN','CHR','RND']]
    return df

def _create_boxplot_diagram(df, save_name, title):
    # create graph just one version
    hige = ( df['NML'], df['RFN'], df['CHR'])
    fig = plt.figure()
    ax = fig.add_subplot(111)

    bp = ax.boxplot(hige)
    ax.set_xticklabels(df.columns)

    plt.grid()
    plt.xlabel('MODEL')
    plt.ylabel('DIAGRAM VALUE')
    # plt.title(title)
    plt.savefig(save_name)

def _create_compare_boxplot_diagram(df, save_name, title):
    # create graph just one version
    hige = ( df['ex1-NML'], df['ex2-NML'],df['ex1-RFN'], df['ex2-RFN'],df['ex1-CHN'], df['ex2-CHN'])
    fig = plt.figure()
    ax = fig.add_subplot(111)

    bp = ax.boxplot(hige)
    ax.set_xticklabels(['ex1-NML', 'ex2-NML','ex1-RFN', 'ex2-RFN','ex1-CHN', 'ex2-CHN'])

    plt.grid()
    plt.xlabel('MODEL')
    plt.ylabel('AUC VALUE')
    # plt.title(title)
    plt.savefig(save_name)


def draw_boxplot_diagram(exp_nm):
    df = _get_diagram_df( './../Data/Diagram_list/'+exp_nm+'.csv')
    filename = './../Data/Diagram_list/figure/boxdig-'+exp_nm+'.png'
    _create_boxplot_diagram(df, filename,exp_nm)

def compare_metrics(save_name, popu_a, popu_b):
    hige = (popu_a, popu_b)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    bp = ax.boxplot(hige)
    ax.set_xticklabels(df.columns)

    plt.grid()
    plt.xlabel('VERSION')
    plt.ylabel('METRICS VALUE')
    # plt.title(title)
    plt.savefig(save_name)

def draw_compare_boxplot_diagram(exp_nm):
    if exp_nm == "derby":
        ex1 = _get_diagram_df( './../Data/Diagram_list/'+exp_nm+'10.9-10.10ex01-diagram.csv')
        ex2 = _get_diagram_df( './../Data/Diagram_list/'+exp_nm+'10.10ex02-diagram.csv')
    elif exp_nm == "Adam":
        ex1 = _get_diagram_df( './../Data/Diagram_list/'+exp_nm+'v2-v3ex01-diagram.csv')
        ex2 = _get_diagram_df( './../Data/Diagram_list/'+exp_nm+'v3ex02-diagram.csv')

    ex1.columns = ['ex1-NML','ex1-RFN','ex1-CHN', 'rnd']
    ex2.columns = ['ex2-NML','ex2-RFN','ex2-CHN', 'rnd']
    df = pd.concat([ex1, ex2], axis=1)
    filename = './../Data/Diagram_list/figure/boxdig-'+exp_nm+'.png'
    _create_compare_boxplot_diagram(df, filename,exp_nm)

def _draw_ks_linear_glaph(filename):
    plt.figure()
    df=pd.read_csv(filename, header=0, index_col=0)
    # print(df)
    derby = df.ix[0,:]
    adam = df.ix[1,:]
    X = df.columns.tolist()
    y = derby.tolist()
    # print(y)
    # print(X)
    plt.plot(range(0,10), y, label='derby', color = 'blue')
    y = adam.tolist()
    plt.plot(range(0,10), y, label='adam', color = 'red')
    # filename = './../data/Research/prob-factor.png'
    # filename = './../data/Research/ex2-prob-factor.png'
    filename = './../data/Research/ex3-prob-factor.png'
    plt.legend(loc='lower right')
    plt.xticks(range(0,10), df.columns)
    # ax = plt.figure().add_subplot(1,1,1)
    plt.ylim(0, 1.2)

    plt.savefig(filename)

def draw_violin_plot(data1, data2, fileName):
    sns.violinplot(data =[data1,data2])
    sns.despine(offset=10, trim=True)
    plt.ylim(0, 200)
    plt.savefig(fileName)

def draw_histgram(data1, data2, fileName):
    def __remove_out_data(s):
        q1 = s.describe()['25%']
        q3 = s.describe()['75%']
        return q1, q3

    # sns.distplot(data1
    q1, q3 = __remove_out_data(data1)
    _q1, _q3  = __remove_out_data(data2)
    min_value = _q1 if q1<_q1 else q1
    max_value = q3 if _q3<q3 else _q3
    print(min_value, max_value)
    # print(max_value)
    # raise Exception
    plt.figure()
    # plt.xlim(0, max_value)
    plt.hist(data1, color='red', normed=True, alpha=0.5)
    plt.hist(data2, color='blue', normed=True, alpha=0.5)
    # plt.hist(data1, color='red', normed=True, alpha=0.5, range=(min_value, max_value))
    # plt.hist(data2, color='blue', normed=True, alpha=0.5, range=(min_value, max_value))
    # plt.ylim(0, 200)
    plt.savefig(fileName)
    # raise Exception

# def create_boxplot_seaborn(hige, save_name, title=None):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.set_xticklabels(hige.columns)
#     print(hige)
#     bp = ax.boxplot(hige)
#     # sns.boxplot(data=hige)
#     # ax.set_xticklabels(['pre', 'cre'])
#     plt.grid()
#     plt.xlabel('model')
#     plt.ylabel('p-value')
#     plt.savefig(save_name)
def create_boxplot_seaborn(df, save_name, title=None):
    # create graph just one version
    hige = ( df['ORG'], df['DST'])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticklabels(['ORG', 'DST'])

    bp = ax.boxplot(hige)

    plt.grid()
    plt.xlabel('MODEL')
    plt.ylabel('DIAGRAM VALUE')
    # plt.title(title)
    plt.savefig(save_name)


if __name__ == '__main__':
    # mode = 2 if args[1]=="2" else  3
    # if mode == 2:
    #     compare_two_models(args[2], args[3], arg[4])
    # elif mode == 3
    #     compare_models(args[2])

    ''' box plot diagram  about AUC value'''
    # ''' Derby'''
    draw_boxplot_diagram('Derby10.9-10.10ex01-diagram')
    # draw_boxplot_diagram('Derby10.8-10.9ex01-diagram')
    # draw_boxplot_diagram('Derby10.8-10.10ex01-diagram')
    draw_boxplot_diagram('Derby10.10ex02-diagram')
    draw_compare_boxplot_diagram('derby')
    #
    # '''Adam'''
    # draw_boxplot_diagram('Adamv1-v3ex01-diagram')
    # draw_boxplot_diagram('Adamv1-v2ex01-diagram')
    draw_boxplot_diagram('Adamv2-v3ex01-diagram')
    draw_boxplot_diagram('Adamv3ex02-diagram')
    draw_compare_boxplot_diagram('Adam')

    ''' linear graph about KS-probability'''
    # filename = '/Users/phayate/Dropbox/STUDY/Euromicro/ks-value2.csv'
    # filename = '/Users/phayate/Dropbox/STUDY/Euromicro/ks-value3.csv'
    # _draw_ks_linear_glaph(filename)
