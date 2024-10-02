import re
import unicodedata

def remove_after_cp(text):
    """
    Function to remove text in column "DOMICILIO" using regular expression to remove all text that comes after ZIP
    """    
    
    # Define the regex pattern to match "c.p. " followed by 5 digits and any text after that    
    pattern = r'(\.\s*|\,\s*)*(TEL\.|TELS\.).*|(\.\s*|\,\s*)*[a-zA-Z0-9.*%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}.*'
    # pattern = r'((C\.P\. \d{5})|(TEL\.|TELS\.))*'    
    #pattern = r'([\.,]\sTEL\.|[\.,]\sTELS\.).+'

    # Use re.sub to replace everything after the pattern with an empty string
    # result = re.sub(pattern, r'\1', text)
    result = re.sub(pattern, '', text)
    
    return result.strip()    


# Function to remove accents from vowels
def remove_accents(input_str):
    """
    Function to remove accents, receives a string a return the same string without accent
    we ommit Ñ to avoid lossing data
    """
    normalized_str  = unicodedata.normalize('NFD', input_str)
    # Use regex to remove diacritical marks, but preserve "Ñ"
    result = re.sub(r'(?<![Nn])[\u0300-\u036f]', '', normalized_str)
    return unicodedata.normalize("NFC", result)