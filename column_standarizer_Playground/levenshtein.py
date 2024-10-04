# levenshtein.py
import Levenshtein
from core import Distance

class LevenshteinDistance(Distance):
    def calculate(self, input_col, ref_col):
        return Levenshtein.distance(input_col, ref_col)
