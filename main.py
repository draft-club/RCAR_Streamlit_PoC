from utils import read_pdfs_from_folder, convert_pdf_to_images, extract_text_from_images, save_extracted_text
from paths import INPUT_PDFS_PATH, OUTPUT_IMAGES_PATH, OUTPUT_TEXT_PATH
from config import load_config


def main():
    # Load configuration settings from config.yaml
    config = load_config()
    print(config)

    # Step 1: Read PDF files from the input folder
    pdf_files = read_pdfs_from_folder(INPUT_PDFS_PATH)

    # Step 2: Process each PDF file
    for pdf_file in pdf_files:
        # Convert each PDF to images using PyMuPDF
        image_files = convert_pdf_to_images(pdf_file, INPUT_PDFS_PATH, OUTPUT_IMAGES_PATH)

        # Extract text from the generated images using Tesseract OCR
        extracted_text = extract_text_from_images(image_files, OUTPUT_IMAGES_PATH, config)

        # Save the extracted text to a file
        save_extracted_text(pdf_file, extracted_text, OUTPUT_TEXT_PATH)


if __name__ == "__main__":
    main()
