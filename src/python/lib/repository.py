from lib.predictor import RFPredictor, LGPredictor, SVCPredictor
from lib.predictor import TreePredictor, SVRPredictor, BoostingPredictor, XGBPredictor
class PredictorRepository(object):
    def __init__(self, predict_ver, ver_model):
        self.predict_ver = predict_ver
        self.ver_model = ver_model

    def get_predictor(self, model_type, predictor_type):
        if predictor_type == 'rf':
            return RFPredictor(self.predict_ver, self.ver_model, model_type)
        if predictor_type == 'log':
            return LGPredictor(self.predict_ver, self.ver_model, model_type)
        if predictor_type == 'svc':
            return SVCPredictor(self.predict_ver, self.ver_model, model_type)
        if predictor_type == 'dt':
            return TreePredictor(self.predict_ver, self.ver_model, model_type)
        if predictor_type == 'svr':
            return SVRPredictor(self.predict_ver, self.ver_model, model_type)
        if predictor_type == 'bst':
            return BoostingPredictor(self.predict_ver, self.ver_model, model_type)

        return None
