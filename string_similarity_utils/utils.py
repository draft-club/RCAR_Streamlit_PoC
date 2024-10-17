# utils.py
import re

def clean_text(text):
    """Cleans and normalizes Arabic text by removing diacritics, normalizing characters, and handling common variations."""
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

    # Remove special characters, punctuation, and extra spaces
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Normalize Arabic characters
    text = text.replace('أ', 'ا')  # Normalize different forms of Alef
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')
    text = text.replace('ة', 'ه')  # Convert Teh Marbuta to Heh
    text = text.replace('ى', 'ي')  # Normalize final Alef Maqsura to Ya
    text = text.replace('ؤ', 'و')  # Convert Hamza on Waw to Waw
    text = text.replace('ئ', 'ي')  # Convert Hamza on Ya to Ya

    return text
