from ex01_class import Ex01
from Model.metrics import Metrics
import configparser
from lib import statistic as st
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics'

class Ex01_additional(Ex01):
    def __init__(self, model, METRICS_DIR):
        super(Ex01_additional, self).__init__(model, METRICS_DIR)
        self.model = model
        self.TARGET = model.sw_name
        self.METRICS_DIR = METRICS_DIR


    def invest_distribution(self, model1, model2):
        # ver, predict_ver = self.model.previous_version, self.model.final_version
        # pre_model = mc.retrieve_model(self.model.sw_name, self.model.final_version)
        # predictor_rep = PredictorRepository(predict_ver, self.model)
        training_m = Metrics(model1.final_version, self.METRICS_DIR, model1)
        evaluate_m = Metrics(model2.final_version, self.METRICS_DIR, model2)
        alike_metrics = st.compare_two_versions(training_m, evaluate_m)
        msg = "Sw: {}:{}-{}:{}, alike_metrics: {}"\
            .format(model1.sw_name, model1.final_version, model2.sw_name, model2.final_version, alike_metrics)
        print(msg)

def create_all_models():
    from Model import model_creator
    import version_operator as vo
    model_dict = model_creator.get_model_dictionary()
    jobs = []
    # model_dict = retrieb_models(model_dict)
    all_models = []
    for _, models in model_dict.items():
        # models = retrieb_model_specified_versions(models)
        for model in models:
            all_models.append(model)
    return all_models

def main():
    from itertools import combinations

    models = create_all_models()
    for i,j in combinations(models, 2):
        ex01 = Ex01_additional(i, METRICS_DIR)
        ex01.invest_distribution(i, j)

if __name__ == '__main__':
    main()
