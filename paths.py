import os

# Define the base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'datafiles')

# Input and output paths
INPUT_PDFS_PATH = os.path.join(DATA_DIR, 'input_pdfs')
OUTPUT_IMAGES_PATH = os.path.join(DATA_DIR, "output_images/" )
OUTPUT_TEXT_PATH = os.path.join(DATA_DIR, 'extracted_text')
