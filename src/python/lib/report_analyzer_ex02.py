import pandas as pd
from lib.auc import AUC
from lib.report_analyzer import AUCAnalyzer
import sklearn.metrics as skm
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.utils import column_or_1d
import configparser
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')
REPORT_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Result2/'


class AUCAnalyzer_Ex02(AUCAnalyzer):
    COLUMNS = ['MODEL', 'recall0', 'precision0', 'accuracy0', 'recall2',
               'precision2', 'accuracy2', 'recall3', 'precision3', 'accuracy3',
               'recall4', 'precision4', 'accuracy4']
    NUM_REPORT_COLUMNS = ['MODEL', 'avg_fp_num', 'avg_crrct_num','avg_fp_num_nml',
                    'avg_crrct_num_nml', 'avg_fp_num_rfn', 'avg_crrct_num_rfn']

    accum_accuracy0 = []
    accum_recall0 = []
    accum_precision0 = []
    accum_accuracy2 = []
    accum_recall2 = []
    accum_precision2 = []
    accum_accuracy3 = []
    accum_recall3 = []
    accum_precision3 = []
    accum_accuracy4 = []
    accum_recall4 = []
    accum_precision4 = []

    accum_fp_num = []
    accum_corrct_num = []
    accum_fp_num_not_modified = []
    accum_corrct_num_not_modified = []
    accum_fp_num_modified = []
    accum_corrct_num_modified = []

    def __init__(self, version, model_type, target_sw):
        self.predict_version = version
        self.model_type = model_type
        self.target_sw = target_sw
        self.report_file_name = REPORT_DIR + target_sw+'-aucreport.csv'
        # self.__remove_report_files()

        if self.accum_recall0 is not None:
            self.accum_recall0 = []
        if self.accum_precision0 is not None:
            self.accum_precision0 = []
        if self.accum_accuracy0 is not None:
            self.accum_accuracy0 = []
        if self.accum_recall2 is not None:
            self.accum_recall2 = []
        if self.accum_precision2 is not None:
            self.accum_precision2 = []
        if self.accum_accuracy2 is not None:
            self.accum_accuracy2 = []
        if self.accum_recall3 is not None:
            self.accum_recall3 = []
        if self.accum_precision3 is not None:
            self.accum_precision3 = []
        if self.accum_accuracy3 is not None:
            self.accum_accuracy3 = []
        if self.accum_recall4 is not None:
            self.accum_recall4 = []
        if self.accum_precision4 is not None:
            self.accum_precision4 = []
        if self.accum_accuracy4 is not None:
            self.accum_accuracy4 = []

        if self.accum_fp_num is not None:
            self.accum_fp_num = []
        if self.accum_corrct_num is not None:
            self.accum_corrct_num = []
        if self.accum_fp_num_not_modified is not None:
            self.accum_fp_num_not_modified = []
        if self.accum_corrct_num_not_modified is not None:
            self.accum_corrct_num_not_modified = []
        if self.accum_fp_num_modified is not None:
            self.accum_fp_num_modified = []
        if self.accum_corrct_num_modified is not None:
            self.accum_corrct_num_modified = []


    def export(self, target_sw, df, predictor_type):
        report_file_name = '{0}{1}-{2}-auc.csv'\
            .format(REPORT_DIR, target_sw, predictor_type)
        df.columns = self.COLUMNS
        if 3 < len(df):
            df = df.ix[[1, 3], :]
        if 2 == len(df):
            df = df.ix[[1], :]
        import os
        if os.path.exists(report_file_name):
            report_df = pd.read_csv(report_file_name, header=0, index_col=0)
            report_df.columns = self.COLUMNS
        else:
            report_df = pd.DataFrame([])
        report_df = pd.concat([report_df, df], axis=0, ignore_index=True,)
        report_df.to_csv(report_file_name)
