import streamlit as st
import requests
import json
import os
import cv2
import numpy as np

# Define lists of blocked brands and their corresponding replacements
blocked_brands = ["aquafina", "BlockedBrand2", "BlockedBrand3"]
replacement_brands = ["Replacement1", "Replacement2", "Replacement3"]

# List of blocked brands for the sidebar
blocked_list = [
    "Lipton", "Nescafé", "nestle Elvan", "aqua", "pavane", "coffee mate",
    "nestle water", "Coca-Cola", "Schweppes", "mirinda", "Tang", "Fanta",
    "Sprit", "Pepsi", "AQUAFINA", "Tropicana", "Mounten Dew", "7up", "CERILAC",
    "bledina", "Beblac", "Donone", "NIDO", "Activia", "kraft", "Marlboro",
    "quaker", "corn fleaks", "special k", "coco pops", "Kellogg’s Frosties",
    "Maggi", "Knorr", "Heinz", "kinder", "twix", "moroo", "freerio rusher",
    "Hohos", "country كورن فليكس", "Danone", "Lion", "Tuc", "Cadbury DairyMILK",
    "Oreo", "Baskin-Robbins", "Kitkat", "m&ms", "SNICKERS", "BOUNTY", "MARS",
    "kinder", "twix", "moroo", "freerio roshiere", "Hohos", "Cheetos", "Doritos",
    "pringles", "puvana", "Vaseline", "Dove", "Cif", "Clear", "Lux", "Axe",
    "Unilever", "Surf", "Ponds", "Kia", "L'Oreal", "The Body Shop", "Maybelline",
    "Procter & Gamble", "Head & Shoulders", "Gillette", "Pantene", "BRAUN", "VO5",
    "SUNSILK", "Pizza Hut", "Starbucks", "Dunkin' Donuts", "Burger King",
    "Papa John's", "McDonald's", "KFC (Kentucky Fried Chicken)", "Nesquik", "ice cream",
    "Starbucks", "Downy Comfort", "Fairy", "Crest", "Oral-B", "Ariel", "Tide", "Always",
    "Pampers", "Johnsons baby", "Garnier", "Tide", "OMO", "fa", "Lifebuoy", "Lux",
    "clean&Clear", "Pril", "Ariel", "Comfort", "cif", "DAC", "neutrogena", "Jif",
    "Sandisk", "Xerox", "philips", "Dell", "hp", "Gillette", "Venus", "Braun",
    "Camay", "zest", "apple", "Nike", "polo", "lacosta"
]

def barcode_lookup(barcode):
    api_key = "6rlauhu0u2zzl0y3oveow51fcineni"
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
st.markdown(f"<h1 style='text-align: center; font-size:50px;'>{('مقاطعة المنتجات التي تدعم إسرائيل')}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; font-size:20px;'>{('تحديد المنتجات التي تدعم إسرائيل عن طريق تحديد البار كود الخاص ب المنتج و ترشيح بديل')}</h1>", unsafe_allow_html=True)

# Sidebar with the list of blocked brands
st.sidebar.title("Blocked List")
st.sidebar.write(blocked_list)

uploaded_image = st.file_uploader("ارفع صوره للباركود الموجود علي المنتج", type=["jpg", "png"])
manual_barcode_input = st.number_input("ادخل البار كود الخاص ب المنتج ", value=0, min_value=0, step=1)

if uploaded_image is not None:
    # Read the uploaded image and use OpenCV for barcode detection
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use an appropriate thresholding method to binarize the image
    _, thresholded = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Find and decode barcodes using pyzbar
    detected_barcodes = decode(thresholded)

    if detected_barcodes:
        extracted_barcode = detected_barcodes[0].data.decode('utf-8')
        st.write("Extracted Barcode from Image:", extracted_barcode)
        barcode_lookup(extracted_barcode)
    else:
        st.write("Unable to extract a valid barcode from the uploaded image.")

if st.button("بحث "):
    barcode_lookup(manual_barcode_input)
