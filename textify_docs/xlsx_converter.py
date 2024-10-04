import pandas as pd

from .base import BaseConverter


class XlsxConverter(BaseConverter):
    """
    Responsible for extractiong data from spreadsheets
    """

    def convert_to_text(self, file_path):
        """
        Extract text from an XLSX file.
        """
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            print(f"An error occurred while converting the excel file: {e}")
            return None


<<<<<<< HEAD
=======
if __name__ == "__main__":
    converter = XlsxConverter()
    PATH = "./data/xlsx.xlsx"
    text = converter.convert_to_text(PATH)
    with open("./data/xlsx_text.txt", "w") as file:
        file.writelines(text)
>>>>>>> d8aaba0a301085dac8844dff99b057a4b32e8837
