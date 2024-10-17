# core.py
import yaml
from .constants import REFERENCE_COLUMNS

class Distance:
    def __init__(self, config_file='config.yaml'):
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        #self.thresholds = config['thresholds']
        #self.hyperparameters = config['hyperparameters']

    def calculate(self, input_col, ref_col):
        """ This should be implemented in each subclass """
        raise NotImplementedError("This method should be implemented by subclasses")

    def standardize(self, input_cols):
        """ Standardizes the columns based on distance calculation. """
        standardized_cols = []
        for col in input_cols:
            best_match = None
            best_score = float('inf')
            for ref in REFERENCE_COLUMNS:
                score = self.calculate(col, ref)
                if score < best_score:
                    best_score = score
                    best_match = ref
            standardized_cols.append(best_match)
        return standardized_cols


columns_with_errors = ["رقم القطع الاضية في التصميم", "مساحتها متر مربع", "اسماء المالكين", "تعويض المستحق بالدرهم"]
