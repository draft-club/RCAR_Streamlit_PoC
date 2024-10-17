# jaccard.py
from column_standarizer.core import Distance

class JaccardDistance(Distance):
    def calculate(self, input_col, ref_col):
        set1 = set(input_col)
        set2 = set(ref_col)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return 1 - intersection / union
