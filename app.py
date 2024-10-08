import streamlit as st
import time
import pandas as pd
from PIL import Image, ImageEnhance
import json
import io
import os

from column_standarizer.constants import REFERENCE_COLUMNS
from new_main_2 import preprocess_image
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
from openai_local.refrence_dictionaries.target_fields import expropriation_data
from openai_local.utils import get_field_from_text, setup_openai
from openai_local.prompts import MAIN_PROMPT
from app_css import APP_CSS
from constants import STAGES

# Load configuration
config = load_config()

# Set page configuration
st.set_page_config(page_title="RCAR E-Consignation Proof of Concept", page_icon=":keyboard:")

# Apply custom CSS
st.markdown(APP_CSS, unsafe_allow_html=True)

# App title
st.title("RCAR E-Consignation Proof of Concept")

# File upload control
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf", key="unique_pdf_uploader")

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
        header = config["header_margin"]
        footer = config["footer_margin"]
        for image in enhanced_images:
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
        input_columns_list = df.columns.to_list()
        # Assuming a column standardization function exists
        #standardized_names_list = standardize_columns(input_columns_list)

        # Step 7: Extract text
        status_text.text(STAGES[6])
        extracted_text = extract_text_from_images(image_files, OUTPUT_IMAGES_PATH, config)
        save_extracted_text(pdf_file_name, extracted_text, OUTPUT_TEXT_PATH)
        progress_bar.progress(7 / len(STAGES))

        # Step 8: Convert output to JSON
        status_text.text(STAGES[7])
        json_output = df.to_dict(orient="records")
        st.json(json_output)
        # Convert the JSON output to a formatted string
        json_string = json.dumps(json_output, ensure_ascii=False, indent=4)

        # Export the JSON string to a text file
        output_txt = io.BytesIO()
        output_txt.write(json_string.encode('utf-8'))
        output_txt.seek(0)

        # Create a download button for the JSON text file
        st.download_button(
            label="Download JSON Output as Text File",
            data=output_txt,
            file_name="extracted_data.txt",
            mime="text/plain"
        )
        progress_bar.progress(8 / len(STAGES))

        # Step 9: Extract fields using OpenAI
        status_text.text(STAGES[8])
        client = OpenAI(api_key=setup_openai())
        results = []

        TEXT = extracted_text
        TABLE = extracted_text

        for item in expropriation_data:
            field = item.get("field")
            field_prompt = item.get("field_prompt")
            lookuptext = item.get("lookuptext")
            dynamic = item.get("dynamic")
            default_value = item.get("default_value")

            if dynamic:
                response = get_field_from_text(client, MAIN_PROMPT, field_prompt, TEXT if lookuptext == "text" else TABLE, field)
            else:
                response = default_value

            results.append({'Champs': field, 'Valeur': response})

        df = pd.DataFrame(results)
        progress_bar.progress(9 / len(STAGES))

        # Step 10: Analyze LLM Response (placeholder)
        status_text.text(STAGES[9])
        progress_bar.progress(10 / len(STAGES))

        # Export DataFrame to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Display final output
        st.success("Processing completed!")
        st.write("### Expropriation Data Results")
        st.dataframe(df)

        # Download Excel file
        st.download_button(
            label="Download Excel Output",
            data=output,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Please upload a PDF document to begin.")
