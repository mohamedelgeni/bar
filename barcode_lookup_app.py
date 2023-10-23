import streamlit as st
import requests
import json
import os
from PIL import Image
import barcode
from barcode import decode

# Define lists of blocked brands and their corresponding replacements
blocked_brands = ["BlockedBrand1", "BlockedBrand2", "BlockedBrand3"]
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
st.title("Barcode Lookup App")
st.write("Upload an image of a barcode or enter a barcode manually.")

uploaded_image = st.file_uploader("Upload an image of a barcode", type=["jpg", "png"])
manual_barcode_input = st.number_input("Or enter a barcode manually", value=0, min_value=0, step=1)

if uploaded_image is not None:
    # Read the uploaded image and use python-barcode to decode the barcode
    image = Image.open(uploaded_image)
    try:
        barcode_data = barcode.decode(image)
        if barcode_data:
            extracted_barcode = barcode_data[0][1]
            st.write("Extracted Barcode from Image:", extracted_barcode)
            barcode_lookup(extracted_barcode)
        else:
            st.write("No barcode found in the uploaded image.")
    except Exception as e:
        st.write(f"Error decoding barcode from image: {str(e)}")

if st.button("Lookup Barcode"):
    barcode_lookup(manual_barcode_input)
