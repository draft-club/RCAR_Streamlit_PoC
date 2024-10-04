import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from datetime import datetime
import io
import cv2
import numpy as np
from textify_docs.tables.table_extracter import extract_tables_from_image_as_dict


def read_pdfs_from_folder(pdf_path):
    """
    Reads PDF filenames from the input folder.

    Returns a list of PDF filenames.
    """
    pdf_files = [f for f in os.listdir(pdf_path) if f.lower().endswith('.pdf')]
    return pdf_files


def extract_tables_from_image(image):
    """
    Extracts tables as list of dictionaries from an image.

    Parameters:
    - image: The image from which to extract tables.

    Returns:
    - table_dicts: The list of extracted dictionaries from the image.
    """
    tables = extract_tables_from_image_as_dict(image,language='ara')
    table_dicts = [table['table_dict'] for table in tables]
    return table_dicts

def _get_table_meta_data(table_dict):
    columns = table_dict[0]
    num_rows, num_columns = len(table_dict), len(columns)
    meta_data = {"columns":columns, "num_row":num_rows, "num_columns": num_columns}
    return meta_data

def convert_pdf_to_images(pdf_file, pdf_path, output_path):
    """
    Converts a single PDF file to images and saves them to the output path using PyMuPDF.

    Returns a list of generated image filenames.
    """
    doc = fitz.open(os.path.join(pdf_path, pdf_file))
    image_files = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        img = _preprocess_image(img)

        image_filename = f"{os.path.splitext(pdf_file)[0]}_page_{page_number + 1}.png"
        image_path = os.path.join(output_path, image_filename)
        img.save(image_path)
        image_files.append(image_filename)
    return image_files


def _preprocess_image(image):
    """
    Preprocesses an image before OCR.

    Returns the preprocessed image.
    """
    # Convert image to openCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Convert back to PIL image
    image = Image.fromarray(gray)
    return image

def extract_text_from_images(image_files, images_path, config):
    """
    Extracts text from a list of images.

    Returns the extracted text as a string.
    """
    full_text = ""
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        text = pytesseract.image_to_string(Image.open(image_path), lang=config['language'], config=config['tesseract_config'])
        full_text += text + "\n"
    return full_text


def save_extracted_text(pdf_file, text, output_text_path):
    """
    Saves the extracted text to a file in the output path.
    The file is named based on the original PDF filename and a timestamp.
    """
    # Create a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Generate output filename with original PDF name, timestamp, and "extracted"
    output_filename = f"{os.path.splitext(pdf_file)[0]}_{timestamp}_extracted.txt"

    # Save the extracted text in the test folder
    output_file = os.path.join(output_text_path, output_filename)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
