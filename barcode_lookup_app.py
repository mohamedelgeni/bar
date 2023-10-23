import streamlit as st
import requests
import json
import os
from PIL import Image
import pytesseract

# Define lists of blocked brands and their corresponding replacements
blocked_brands = ["aquafina ", "BlockedBrand2", "BlockedBrand3"]
replacement_brands = ["Replacement1", "Replacement2", "Replacement3"]

def barcode_lookup(barcode):
    api_key = "omi4zeddt00qn3t8b5bticf0iviji1"
    url = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        barcode = data["products"][0]["barcode_number"]
        name = data["products"][0]["title"]
        brand = data["products"][0]["brand"].strip().lower()  # Compare in a case-insensitive manner and remove leading/trailing whitespace

        st.write("Barcode Number:", barcode)
        st.write("Title:", name)
        st.write("Brand:", brand)

        # Check if the brand is in the list of blocked brands
        if brand in (blocked.strip().lower() for blocked in blocked_brands):
            index = [blocked.strip().lower() for blocked in blocked_brands].index(brand)
            replacement = replacement_brands[index]
            st.write("This brand is blocked. Here is a replacement:", replacement)
        else:
            st.write("This brand is not blocked.")
    else:
        st.write("Error:", response.status_code)

# Streamlit UI
st.title("مقاطعة المنتجات التي تدعم إسرائيل")
st.markdown(f"<h1 style='text-align: center; color:#3E3F3A; font-size:50px;'>{('مقاطعة المنتجات التي تدعم إسرائيل عن طريق تحديد البار كود الخاص ب المنتج وتحديد بديل')}</h1>", unsafe_allow_html=True)
uploaded_image = st.file_uploader("ارفع صوره للباركود الموجود علي المنتج", type=["jpg", "png"])
manual_barcode_input = st.number_input("ااكتبه البار كود الخاص ب المنتج ", value=0, min_value=0, step=1)

if uploaded_image is not None:
    # Read the uploaded image and use OCR to extract the barcode number
    image = Image.open(uploaded_image)
    extracted_text = pytesseract.image_to_string(image)
    
    # Try to extract a number from the extracted text
    extracted_barcode = "".join(filter(str.isdigit, extracted_text))
    
    if extracted_barcode:
        st.write("Extracted Barcode from Image:", extracted_barcode)
        barcode_lookup(extracted_barcode)
    else:
        st.write("Unable to extract a valid barcode from the uploaded image.")

if st.button("بحث "):
    barcode_lookup(manual_barcode_input)
