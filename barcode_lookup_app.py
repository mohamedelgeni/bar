import streamlit as st
import requests
import json
import os
import cv2
import numpy as np

# Define a list of blocked brands
blocked_brands = [
    "Lipton", "Nescafé", "Nestle Elvan", "Aqua", "Pavane",
    "Coffee Mate", "Nestle Water", "Coca-Cola", "Schweppes",
    "Mirinda", "Tang", "Fanta", "Sprit", "Pepsi", "Aquafina",
    "Tropicana", "Mounten Dew", "7up", "CERILAC", "Bledina",
    "Beblac", "Donone", "NIDO", "Activia", "Kraft", "Marlboro",
    "Quaker", "Corn Flakes", "Special K", "Coco Pops",
    "Kellogg’s Frosties", "Maggi", "Knorr", "Heinz",
    "Kinder", "Twix", "Moroo", "Freerio Rusher", "Hohos",
    "Country كورن فليكس", "Danone", "Lion", "Tuc",
    "Cadbury DairyMILK", "Oreo", "Baskin-Robbins", "Kitkat",
    "M&Ms", "SNICKERS", "BOUNTY", "MARS", "Kinder",
    "Twix", "Moroo", "Freerio Rusher", "Hohos", "Cheetos",
    "Doritos", "Pringles", "Pavane", "Vaseline", "Dove",
    "Cif", "Clear", "Lux", "Axe", "Unilever", "Surf",
    "Ponds", "Kia", "L'Oreal", "The Body Shop", "Maybelline",
    "Procter & Gamble", "Head & Shoulders", "Gillette", "Pantene",
    "BRAUN", "VO5", "SUNSILK", "Pizza Hut", "Starbucks",
    "Dunkin' Donuts", "Burger King", "Papa John's", "McDonald's",
    "KFC (Kentucky Fried Chicken)", "Nesquik", "Ice Cream", "Starbucks",
    "Downy Comfort", "Fairy", "Crest", "Oral-B", "Ariel", "Tide",
    "Always", "Pampers", "Johnsons Baby", "Garnier", "Tide", "OMO",
    "Fa", "Lifebuoy", "Lux", "Clean & Clear", "Pril", "Ariel",
    "Comfort", "Cif", "DAC", "Neutrogena", "Jif", "Sandisk",
    "Xerox", "Philips", "Dell", "HP", "Gillette", "Venus",
    "Braun", "Camay", "Zest", "Apple", "Nike", "Polo", "Lacoste"
]

# Remove duplicates and sort the list for better user experience
blocked_brands = sorted(list(set(blocked_brands)))

def barcode_lookup(barcode):
    # Your barcode lookup code here

# Streamlit UI

# Create a multiselect widget to select blocked brands
selected_blocked_brands = st.multiselect("Blocked Brands List", blocked_brands)

# Display the selected blocked brands
st.write("Selected Blocked Brands:", selected_blocked_brands)

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
