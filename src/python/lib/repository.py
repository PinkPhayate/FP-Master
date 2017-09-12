from lib.predictor import RFPredictor, LGPredictor, SVCPredictor
from lib.predictor import TreePredictor, SVRPredictor

class PredictorRepository(object):
    def __init__(self, predict_ver, ver):
        self.predict_ver = predict_ver
        self.ver = ver

    def get_predictor(self, model_type, predictor_type):
        if predictor_type == 'rf':
            return RFPredictor(self.predict_ver, self.ver, model_type)
        if predictor_type == 'log':
            return LGPredictor(self.predict_ver, self.ver, model_type)
        if predictor_type == 'svc':
            return SVCPredictor(self.predict_ver, self.ver, model_type)
        if predictor_type == 'dt':
            return TreePredictor(self.predict_ver, self.ver, model_type)
        if predictor_type == 'svr':
            return SVRPredictor(self.predict_ver, self.ver, model_type)
        return None
