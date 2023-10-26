import streamlit as st
from PIL import Image
import pytesseract
from sqlalchemy.orm import Session
import re
from models import *
from db import get_db, CreateTables
import db
import pandas as pd

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path
# pytesseract.pytesseract.tessdata_dir_config = '--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'  # Adjust to your setup
st.title("BizCardX: Extracting Business Card Data with OCR")
st.write("Technologies:OCR,streamlit GUI, SQL,Data Extraction")
image = st.file_uploader("upload your image here", type=["jpg","png","jpeg"])
CreateTables()
if image is not None:
     image = Image.open(image)
     # image = cv2.imread(image)
     # image_np = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
     text = pytesseract.image_to_string(image)
     st.write(text)
     name_pattern = r"^[A-Z][a-z]+"
     position_pattern = r"[A-Z][A-Z\s]+"
     mobile_pattern = r"(\+?\d{3}-\d{3}-\d{4})"
     website_pattern = r"www\.[A-Za-z0-9]+\.[a-z]+"
     email_pattern = r"\S+@\S+"
     address_pattern = r"\d{1,4}\s[A-Za-z0-9\s,]+\d{6}"

     # Extract data using regular expressions
     card = text
     name = re.search(name_pattern, text).group() if re.search(name_pattern, text) else None
     position = re.search(position_pattern, text).group() if re.search(position_pattern, text) else None
     mobile = re.findall(mobile_pattern, text) if re.search(mobile_pattern, text) else None
     website = re.search(website_pattern, text).group() if re.search(website_pattern, text) else None
     email = re.search(email_pattern, text).group() if re.search(email_pattern, text) else None
     address = re.search(address_pattern, text).group() if re.search(address_pattern, text) else None

     # lines = text.split('\n')

# Extract components based on the structure of the text
#      name = lines[0]
#      position = lines[1]
#      mobile = [line for line in lines if line.startswith('& +')][0].strip()
#      email = [line for line in lines if line.startswith('~ ')][0][2:].strip()
#      website = [line for line in lines if line.startswith('Q www.')][0].strip()

# # Address is a bit more complex, but you can join lines until you reach the postal code
#      address = ""
#      for line in lines[lines.index(website) + 1:]:
#           if any(char.isdigit() for char in line):
#                break
#           address += line + ' '
          # Print the extracted information
     st.write("Name:", name)
     st.write("Position:", position)
     st.write("Mobile:", mobile)
     st.write("Website:", website)
     st.write("Email:", email)
     st.write("Address:", address)

     if st.button("image to text"):
          db = next(get_db())
          card = Card.create_card(db,name,position,mobile,website,email,address)
          st.write("Data saved to db")
     if st.button("Full text"):
          db = next(get_db())
          full_card = CardInfo.full_card(db,card)
          st.write("Data saved to db")
     if st.button("List Card Info"):
          output = []
          db = next(get_db())
          db_return = Card.get_card(db)
          for data in db_return:
               result = {
                    'name' : data.name,
                    'position' : data.position,
                    'mobile' : data.mobile,
                    'website' : data.website,
                    'email' : data.email,
                    'address' : data.address,
               }
               output.append(result)
          st.write(pd.DataFrame(output))

     if st.button("Full text List"):
          output = []
          db = next(get_db())
          db_return = CardInfo.full_text(db)
          for data in db_return:
               result = {
                    'card' : data.card
               }
               output.append(result)
          st.write(pd.DataFrame(output))
else:
     st.write("Updoad a card Image") 