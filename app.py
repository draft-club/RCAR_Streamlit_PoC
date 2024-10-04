import streamlit as st
import time
import pandas as pd
from PIL import Image, ImageEnhance

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
import json
import os
from column_standarizer import standarize

# Load configuration
config = load_config()



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
    "Loading LLM response",
    "Exporting to excel",
    "Analyse LLM Response"
]




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
        input_columns_list = df.columns.to_list()
        #cols_to_keep_list=REFERENCE_COLUMNS
        #standarized_names_list = standarize.standardize_columns(input_columns_list)

        """try:
            df.columns=standarized_names_list
            # Keep only the columns that are in cols_to_keep_list
            df = df[df.columns.intersection(cols_to_keep_list)]
        except :
            pass"""


        # Step 7: Extract text
        status_text.text(STAGES[6])
        extracted_text = extract_text_from_images(image_files, OUTPUT_IMAGES_PATH, config)

        #save_extracted_text(pdf_file_name, extracted_text, OUTPUT_TEXT_PATH)
        progress_bar.progress(7 / len(STAGES))

        # Step 8: Convert output to JSON
        status_text.text(STAGES[7])
        json_output = df.to_dict(orient="records")
        progress_bar.progress(8 / len(STAGES))

        # Step 9: Extract fields
        status_text.text(STAGES[8])
        extracted_fields_dict = {"Texts": extracted_text, "Tables": json_output}
        progress_bar.progress(9 / len(STAGES))

        # Step 10: Analyse LLM Response
        from .openai_local.refrence_dictionaries.target_fields import expropriation_data
        from .openai_local.utils import get_field_from_text ,setup_openai
        import pandas as pd
        import io
        # Initialize OpenAI client with API key
        client = OpenAI(api_key=setup_openai())
        # Mock text and table data
        TEXT = extracted_text
        TABLE = json_output

        # Create an empty list to store the results
        results = []

        # Loop over the dictionary values and get the response for each field
        for item in expropriation_data:
            field = item.get("field")
            lookuptext = item.get("lookuptext")
            dynamic = item.get("dynamic", False)
            default_value = item.get("default_value", "N/A")
            # If the field is dynamic
            if dynamic:
                if lookuptext == "table":
                    response = get_field_from_text(client, TABLE, field)
                else:
                    # Use text data
                    response = get_field_from_text(client, TEXT, field)
            else:# If not dynamic, use default value
                response = default_value
                # Append the result to the list

            results.append({'Champs': field, 'Valeur': response})

        # Convert the results into a DataFrame
        df = pd.DataFrame(results)
        st.dataframe(results)

        # Print the DataFrame
        #print(df)

        # Export the DataFrame to an Excel file
        df.to_excel('expropriation_data_results.xlsx', index=False)
        #print("Data has been exported to 'expropriation_data_results.xlsx'.")
        progress_bar.progress(10/ len(STAGES))

        # Display final output
        st.success("Processing completed!")
        #st.subheader("Extracted Table Data (first 10 rows):")
        #st.dataframe(df.head(10))

        # Provide download link for JSON
        json_string = json.dumps(extracted_fields_dict, ensure_ascii=False, indent=4)

        # Create an in-memory Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            writer.save()

        # Rewind the buffer to the beginning
        output.seek(0)
        # Create a download button to download the Excel file
        st.download_button(
            label="Download Excel Output",
            data=output,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        #st.subheader("Extracted Fields:")
        #st.json(json_output)

else:
    st.info("Please upload a PDF document to begin.")
