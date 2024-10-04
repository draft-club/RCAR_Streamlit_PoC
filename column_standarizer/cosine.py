# cosine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .core import Distance

class CosineDistance(Distance):
    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer(analyzer='char')

    def calculate(self, input_col, ref_col):
        """
        Calculate the cosine similarity between two columns.

        Args:
        - input_col (str): The input column name.
        - ref_col (str): The reference column name.

        Returns:
        - float: The cosine similarity between the input and reference column.
        """
        vectors = self.vectorizer.fit_transform([input_col, ref_col])
        return cosine_similarity(vectors[0], vectors[1])[0][0]
