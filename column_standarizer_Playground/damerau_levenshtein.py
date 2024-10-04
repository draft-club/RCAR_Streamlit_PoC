# damerau_levenshtein.py
from Levenshtein import damerau_levenshtein_distance
from column_standarizer.core import Distance

class DamerauLevenshteinDistance(Distance):
    def calculate(self, input_col, ref_col):
        return damerau_levenshtein_distance(input_col, ref_col)
