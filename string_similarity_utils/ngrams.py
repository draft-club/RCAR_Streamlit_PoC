# ngrams.py
import nltk
from nltk.util import ngrams
from column_standarizer.core import Distance

class NgramDistance(Distance):
    def calculate(self, input_col, ref_col):
        n = self.hyperparameters['ngrams_n']
        input_ngrams = set(ngrams(input_col, n))
        ref_ngrams = set(ngrams(ref_col, n))
        return len(input_ngrams.intersection(ref_ngrams)) / max(len(input_ngrams), len(ref_ngrams))
