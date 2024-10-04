# setup.py
from setuptools import setup, find_packages

setup(
    name='column_standarizer',
    version='1.0.0',
    description='A module to standardize Arabic columns based on different distance metrics.',
    author='Amine Lahouani',
    author_email='amin.mba@iuj.ac.jp',
    packages=find_packages(),
    install_requires=[
        'Levenshtein',  # For Levenshtein and Damerau-Levenshtein distances
        'scikit-learn',  # For Cosine similarity
        'nltk',  # For N-grams
        'PyYAML',  # For configuration handling
    ],
    python_requires='>=3.7',
)
