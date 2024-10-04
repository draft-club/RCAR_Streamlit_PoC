import streamlit as st
import time
import pandas as pd
from PIL import Image, ImageEnhance
from utils import (
    read_pdfs_from_folder,
    convert_pdf_to_images,
    extract_text_from_images,
    save_extracted_text,
)
from paths import OUTPUT_IMAGES_PATH, OUTPUT_TEXT_PATH, INPUT_PDFS_PATH
from config import load_config
from textify_docs.tables.table_extracter import extract_tables_from_image_as_dict
from openai import OpenAI, APIConnectionError, RateLimitError
import json
import os

# Load configuration
config = load_config()

# Initialize OpenAI client with API key from config.yaml
client = OpenAI(api_key=config['openai_api_key'])

# App name
st.title("RCAR E-Consignation Proof of Concept")

# Progress stages
STAGES = [
    "Converting PDF to images",
    "Enhancing image quality and contrast",
    "Removing header and footer",
    "Detecting tables",
    "Merging tables",
    "Normalizing columns",
    "Extracting text",
    "Converting output to JSON",
    "Extracting fields",
]


def enhance_arabic_text(text, max_retries=5):
    """Enhances and corrects Arabic text using GPT-4, with rate limit and connection error handling."""
    retries = 0
    while retries < max_retries:
        try:
            # Call OpenAI API using the correct format
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in Arabic grammar and spelling. Your task is to correct any spelling errors in the provided Arabic text accurately. Follow these specific rules:"
                                                  "If the input is entirely in Arabic, correct any spelling mistakes and return only the corrected text.Example:Input: اللغت العربيه جميله جداOutput: اللغة العربية جميلة جدًا"
                                                  "If the input is not Arabic, return it exactly as it is, without changes."
                                                  "Example:"
                                                  "Input: This is not Arabic."
                                                  "Output: This is not Arabic."
                                                  "If the input is a number, return the number as it is."
                                                  "Example:"
                                                  "Input: 12345"
                                                  "Output: 12345"
                                                  "If the input is a mix of Arabic and another language, correct only the Arabic part and return the rest unchanged."
                                                  "Example:"
                                                  "Input: I love اللغت العربيه."
                                                  "Output: I love اللغة العربية."
                                                  "In all cases, return only the corrected content without any additional comments or explanations."},
                    {"role": "user", "content": f"Enhance and correct the following Arabic text: {text}"}
                ]
            )
            # Access the response content correctly
            return response.choices[0].message.content

        except RateLimitError:
            # Handle rate limit errors by waiting and retrying
            retries += 1
            wait_time = 2 ** retries  # Exponential backoff (2, 4, 8, 16, 32 seconds)
            st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        except APIConnectionError:
            # Handle API connection errors and retry
            retries += 1
            wait_time = 2 ** retries
            st.warning(f"Connection error. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    raise Exception("Maximum retries reached. Failed to enhance text due to rate limits or connection issues.")


# File upload control
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    # Validate file type
    if uploaded_file.type != "application/pdf":
        st.error("Please upload a valid PDF file.")
    else:
        # Start the process
        st.success("File uploaded successfully! Processing will start now.")

        # Progress bar initialization
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Save uploaded file locally and convert PDF to images
        status_text.text(STAGES[0])
        pdf_file_name = uploaded_file.name
        pdf_file_path = os.path.join(INPUT_PDFS_PATH, pdf_file_name)

        with open(pdf_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Save uploaded file locally

        image_files = convert_pdf_to_images(pdf_file_name, INPUT_PDFS_PATH, OUTPUT_IMAGES_PATH)
        progress_bar.progress(1 / len(STAGES))

        # Step 2: Enhance image quality and contrast
        status_text.text(STAGES[1])
        enhanced_images = []
        for image_file in image_files:
            image = Image.open(os.path.join(OUTPUT_IMAGES_PATH, image_file))
            enhancer = ImageEnhance.Contrast(image)
            enhanced_image = enhancer.enhance(1.5)  # Adjust contrast
            enhanced_images.append(enhanced_image)
        progress_bar.progress(2 / len(STAGES))

        # Step 3: Remove header and footer
        status_text.text(STAGES[2])
        cropped_images = []
        for image in enhanced_images:
            header = config["header_margin"]
            footer = config["footer_margin"]
            cropped_image = image.crop((0, header, image.width, image.height - footer))
            cropped_images.append(cropped_image)
        progress_bar.progress(3 / len(STAGES))

        # Step 4: Detect tables
        status_text.text(STAGES[3])
        output = {"text": "To implement later", "table": []}
        first_table_found = False
        for page, image in enumerate(cropped_images):
            tables = extract_tables_from_image_as_dict(image, language="ara")
            if tables:
                num_columns = len(tables[0]["table_dict"][0])
                if not first_table_found:
                    first_table_found = True
                    num_columns_first = num_columns
                elif num_columns != num_columns_first:
                    break  # New table detected
                for table in tables:
                    table_dict = table["table_dict"]
                    for row in table_dict.values():
                        output["table"].append(row)
            else:
                if first_table_found:
                    break
        progress_bar.progress(4 / len(STAGES))

        # Step 5: Merge tables
        status_text.text(STAGES[4])
        if output["table"]:
            df = pd.DataFrame(output["table"][1:], columns=output["table"][0])
        else:
            df = pd.DataFrame()
        progress_bar.progress(5 / len(STAGES))

        # Step 6: Normalize columns
        """status_text.text(STAGES[5])
        for col in df.columns:
            df[col] = df[col].apply(lambda text: enhance_arabic_text(text) if isinstance(text, str) else text)
        progress_bar.progress(6 / len(STAGES))"""

        # Step 7: Extract text
        status_text.text(STAGES[6])
        extracted_text = extract_text_from_images(image_files, OUTPUT_IMAGES_PATH, config)

        save_extracted_text(pdf_file_name, extracted_text, OUTPUT_TEXT_PATH)
        progress_bar.progress(7 / len(STAGES))

        # Step 8: Convert output to JSON
        status_text.text(STAGES[7])
        json_output = df.to_dict(orient="records")
        progress_bar.progress(8 / len(STAGES))

        # Step 9: Extract fields (dummy step)
        status_text.text(STAGES[8])
        extracted_fields_dict = {"Texts": extracted_text, "Tables": json_output}  # Example extracted fields
        progress_bar.progress(9 / len(STAGES))

        # Display final output
        st.success("Processing completed!")
        #st.subheader("Extracted Table Data (first 10 rows):")
        #st.dataframe(df.head(10))

        # Provide download link for JSON
        json_string = json.dumps(extracted_fields_dict, ensure_ascii=False, indent=4)
        st.download_button(
            label="Download JSON Output",
            data=json_string,
            file_name="extracted_data.json",
            mime="application/json",
        )

        st.subheader("Extracted Fields:")
        st.json(json_output)

else:
    st.info("Please upload a PDF document to begin.")
