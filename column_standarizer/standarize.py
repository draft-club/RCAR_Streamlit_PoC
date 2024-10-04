# standardize.py
from .cosine import CosineDistance
from .constants import REFERENCE_COLUMNS
from .utils import clean_text


def standardize_columns(input_columns):
    """
    Standardizes a list of input columns based on the closest matches from the reference columns.
    Only the top N matches (where N is the length of the reference list) are renamed.
    The remaining columns stay the same.
    """
    # Initialize CosineDistance class
    cosine = CosineDistance()

    # Clean input columns and reference columns
    cleaned_input_columns = [clean_text(col) for col in input_columns]
    cleaned_reference_columns = [clean_text(col) for col in REFERENCE_COLUMNS]

    # Store matches along with their scores
    matches = []

    # Calculate the cosine similarity for each input column to all reference columns
    for input_col, cleaned_input_col in zip(input_columns, cleaned_input_columns):
        for ref_col, cleaned_ref_col in zip(REFERENCE_COLUMNS, cleaned_reference_columns):
            score = cosine.calculate(cleaned_input_col, cleaned_ref_col)
            matches.append([input_col, ref_col, score])

    # Sort all matches by cosine similarity score in descending order
    sorted_matches = sorted(matches, key=lambda x: -x[2])  # Sort by score descending

    # Prepare a list to track renamed columns and leave the rest unchanged
    renamed_columns = input_columns.copy()

    # Keep track of how many columns have been renamed
    renamed_count = 0

    # Loop through sorted matches and rename only the top N columns
    for input_col, ref_col, score in sorted_matches:
        if renamed_count < len(REFERENCE_COLUMNS):  # Only rename top N matches
            index = input_columns.index(input_col)
            renamed_columns[index] = ref_col
            renamed_count += 1
        else:
            break

    return renamed_columns

def write_matches_to_file(input_columns, renamed_columns, file_path):
    """
    Writes the matching columns to a text file in the format:
    "This list of cols [INPUT COLS HERE] matches this list of cols [OUTPUT COLS HERE]"
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("This list of cols [INPUT COLS HERE] matches this list of cols [OUTPUT COLS HERE]\n")
        for input_col, renamed_col in zip(input_columns, renamed_columns):
            file.write(f"{input_col} matches {renamed_col}\n")


