from lib.auc import AUC
import pandas as pd
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

def test_circulate_auc():
    df = pd.read_csv('/Users/phayate/Dropbox/STUDY/Result/4.2.0ITG-report.csv',
        header=0,
        index_col=0)
    df = df[['actual', 'predict']]
    df.columns = ['fault', 'ev_value']
    diagram_value = AUC(df). circulate_auc
    print(diagram_value)

# test_circulate_auc()

import pandas as pd
class Hoge(object):
    li = []
    df = pd.DataFrame([0,0])
    def __init__(self, name):
        self.name = name
    def append(self, x):
        self.li.append(x)

    def set(self, x):
        self.x = x

    def add_el(self, df):
        self.df = pd.concat([self.df, df])

def test_hoge():
    h1 = Hoge('1taro')
    h2 = Hoge('2taro')
    h3 = Hoge('3taro')

    h1.append(1)
    h2.append(2)
    h3.append(3)
    print(h1.li)
    print(h2.li)
    print(h3.li)

    h1.set(1)
    h2.set(2)
    h3.set(3)
    print(h1.x)
    print(h2.x)
    print(h3.x)

    h1.add_el(pd.DataFrame([1,1]))
    h2.add_el(pd.DataFrame([2,2]))
    h3.add_el(pd.DataFrame([3,3]))
    print(h1.df)
    print(h2.df)
    print(h3.df)

def test_retrieve_model():
    from Model import model_creator as mc
    model = mc.retrieve_model('derby', '10.13.1.1')
    print(model.sw_name, model.final_version)
def test_exp_model_set_param_dict():
    from Model import model_creator
    models = []
    model_dict = model_creator.get_model_dictionary()
    [models.extend(ms) for _, ms in model_dict.items()]
    for model in models:
        print(model.param_dictionary)

# test_hoge()
# test_retrieve_model()
test_exp_model_set_param_dict()
