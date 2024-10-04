from utils import (
    read_pdfs_from_folder,
    convert_pdf_to_images,
    extract_text_from_images,
    save_extracted_text,
)
from paths import INPUT_PDFS_PATH, OUTPUT_IMAGES_PATH, OUTPUT_TEXT_PATH
from config import load_config
from PIL import Image, ImageEnhance
from textify_docs.tables.table_extracter import extract_tables_from_image_as_dict
import pandas as pd
import openai


def enhance_arabic_text(text):
    """Enhances and corrects Arabic text using GPT-4."""
    openai.api_key = ''  # Add your OpenAI API key here
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Enhance and correct the following Arabic text: {text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Extract enhanced text from the GPT response
    return response['choices'][0]['text'].strip()


def process_pdf(pdf_file, config):
    """
    Processes a single PDF file: converts it to images,
    extracts tables, and applies enhancements.
    """
    output = {"text": "to implement later", "table": []}
    first_table_found = False
    page_number = 1

    # Convert the PDF into images
    image_files = convert_pdf_to_images(pdf_file, INPUT_PDFS_PATH, OUTPUT_IMAGES_PATH)

    for image_file in image_files:
        image_path = OUTPUT_IMAGES_PATH + image_file
        print(f"Processing page {page_number} from {pdf_file}")

        # Open and enhance the image
        image = Image.open(image_path)
        image = preprocess_image(image, config)

        # Extract tables from the image
        tables = extract_tables_from_image_as_dict(image, language="ara")
        table_found = bool(tables)

        # Check for new table structure or end of table
        if table_found:
            num_columns = len(tables[0]["table_dict"][0])
            if not first_table_found:
                first_table_found = True
                num_columns_first = num_columns
            elif num_columns != num_columns_first:
                print("New table structure found, stopping further extraction.")
                break  # A new table structure indicates the end of the previous table
        elif first_table_found:
            print("Page without table, stopping further extraction.")
            break  # No table after the first indicates the end of extraction
        else:
            print("No table detected yet.")
            continue

        # Append the table data to the output
        for table in tables:
            table_dict = table["table_dict"]
            output["table"].extend(table_dict.values())

        page_number += 1
        if page_number == 8:  # Limit processing to 8 pages for now
            break

    return output


def preprocess_image(image, config):
    """
    Preprocesses the image by enhancing contrast and removing header/footer.
    """
    # Enhance image contrast
    enhancer = ImageEnhance.Contrast(image)
    contrast_factor = 1.5
    image = enhancer.enhance(contrast_factor)

    # Crop image to remove header and footer
    header_margin = config["header_margin"]
    footer_margin = config["footer_margin"]
    image = image.crop((0, header_margin, image.width, image.height - footer_margin))

    return image


def enhance_dataframe(df):
    """
    Enhances the Arabic text in the DataFrame using GPT-4.
    """
    for col in df.columns:
        # Apply the enhancement to each cell in Arabic columns
        df[col] = df[col].apply(lambda text: enhance_arabic_text(text) if isinstance(text, str) else text)
    return df


def main():
    # Load configuration settings from config.yaml
    config = load_config()
    print("Configuration loaded:", config)

    # Step 1: Read PDF files from the input folder
    pdf_files = read_pdfs_from_folder(INPUT_PDFS_PATH)

    # Step 2: Process each PDF file and extract data
    all_data = {"text": "to implement later", "table": []}
    for pdf_file in pdf_files:
        output = process_pdf(pdf_file, config)
        all_data["table"].extend(output["table"])

    # Step 3: Convert extracted table data to DataFrame
    if all_data["table"]:
        df = pd.DataFrame(all_data["table"][1:], columns=all_data["table"][0])
        print("Original DataFrame:")
        print(df)

        # Step 4: Enhance Arabic text in the DataFrame
        df = enhance_dataframe(df)

        # Step 5: Save the enhanced DataFrame to Excel
        output_file = 'enhanced_test.xlsx'
        df.to_excel(output_file, index=False)
        print(f"DataFrame has been saved to '{output_file}'.")
    else:
        print("No tables found to process.")


if __name__ == "__main__":
    main()
