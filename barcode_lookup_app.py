import streamlit as st
import requests
import json
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Define lists of blocked brands and their corresponding replacements
blocked_brands = [
    ["lay's", "crunchy max", "mini cheetos", "doritos", "pic rolls", "pic sticks", "sunbites", "lays pringles", "sudanese lay's de litch"],
    ["coca cola", "fanta", "pepsi", "sprite", "mirinda", "7up", "mountain dew"],
    ["aquafina", "baraka (nestle)", "dasani"],
    ["ho hos", "twinkies", "rolls", "any hostess product", "twinkez"],
    ["samba", "kraft", "boreo (kraft)", "oreo", "tuc"],
    ["trident", "clorets", "dentyne", "halls"],
    ["tang"],
    ["fairy"],
    ["danone", "activia", "rachitel", "danjou"],
    ["morro", "flutes", "snickers", "galaxy", "kit kat", "mandolin", "jersey", "twix", "mars" "bubbles", "maltesers", "bounty", "kinder"],
    ["nestle company"],
    ["kfc", "mcdonald's", "pizza hut", "little caesars", "hardee's", "domino's pizza", "fridays"],
    ["lipton"],
    ["lipton", "nescafé", "nestle elvan", "aqua", "pavane", "coffee mate", "starbucks"],
    ["ariel", "tide", "lang botex", "zest", "procter & gamble products", "downy fabric softener"],
    ["pantene", "johnson's baby", "head & shoulders"],
    ["johnson's"],
    ["pampers"],
    ["camay", "lux"],
    ["dell", "apple"],
    ["signal", "close up", "colgate", "crest"],
    ["avon", "hair cream (palmers)"]
]


alternative_brands = [
    ["Tats", "Tiger", "Rotito", "Fox", "Zigo", "Masrawy", "Windows", "Mexicorondos", "Break", "Lyon", "Bozo Cracky (twist)", "Waves Mannah", "jolio"],
    ["Spiro Spates", "Cinnacola", "Sport", "UGO", "V7", "big fresh", "Schneider is a fizzy beer"],
    ["Hayat", "Safi", "Bavana", "Isis", "beinnova", "Aqua Delta"],
    ["Tea Tea", "Chateau", "Drow Ferjallo", "Swiss Roll", "Cassy (Turkish)"],
    ["Lambada", "Shamadan", "Fresh", "Tempo", "Ulker (Turkey)", "Drow", "Any products from Annie Company (Turkish)"],
    ["Ghandour"],
    ["Frooty", "Best", "Aga", "Ferjallo", "Gehena", "Betty"],
    ["Brill"],
    ["Gehena", "Almarai", "Bakheer"],
    ["Pure", "Ulker Company (Turkish)", "All types of Turkish chocolate are widely"],
    ["Alicafe"],
    ["Moumen", "Wal3teen", "Ketchup", "Fotoma (El Mansoura)"],
    ["Al Rabie Express", "Twinings", "Ahmed Tea", "El-arosaa"],
    ["AliCafe", "AboAuof", "Barlico"],
    ["Persil", "Oxi", "Extra", "Comfort fabric softener"],
    ["Sparkle", "Elvive", "Clear", "Herbal Essences"],
    ["Dove", "Olay", "Eva", "Nivea", "Himalaya"],
    ["Baby Fine", "Giggle", "Sleepy"],
    ["Dove", "Fa", "Farah", "Duru Natural (Turkish)"],
    ["Toshiba"],
    ["Miswak", "Sensodyne", "Aqua Fresh"],
    ["My Way"]
]

# Define categories for the blocked brands
categories = {
    "Chips": ["Lay's", "Crunchy Max", "Mini Cheetos", "Doritos", "Pic Rolls", "Pic Sticks", "Sunbites", "Lays Pringles", "Sudanese Lay's De Litch"],
    "Beverages": ["Coca Cola", "Fanta", "Pepsi", "Sprite", "Miranda", "7UP", "Mountain Dew"],
    "Water": ["Aquafina", "Baraka (Nestle)", "Dasani"],
    "Cakes": ["Ho Hos", "Twinkies", "Rolls", "Any Hostess product", "Twinkez"],
    "Biscuits": ["Samba", "Kraft", "Boreo (Kraft)", "Oreo", "Tuc"],
    "Chewing Gum": ["Trident", "Clorets", "Dentyne", "Halls"],
    "Juices": ["Tang"],
    "Dishwashing Liquid": ["Fairy"],
    "Yogurt": ["Danone", "Activia", "Rachitel", "Danjou"],
    "Chocolate":["Morro", "Flutes", "Snickers", "Galaxy", "kit kat", "Mandolin", "Jersey", "Twix", "Mars" "Bubbles", "Maltesers", "Bounty", "kinder"],
    "Nescafe": ["Nestle company"],
    "Restaurants": ["KFC", "McDonald's", "Pizza Hut", "Little Caesars", "Hardee's", "Domino's Pizza", "Fridays"],
    "Tea": ["Lipton"],
    "Coffee": ["Lipton", "Nescafé", "nestle Elvan", "aqua", "pavane", "coffee mate", "Starbucks"],
    "Detergents": ["Ariel", "Tide", "Lang Botex", "Zest", "Procter & Gamble products", "Downy fabric softener"],
    "Shampoo": ["Pantene", "Johnson's Baby", "Head & Shoulders"],
    "Face creams": ["Johnson's"],
    "Baby products": ["Pampers"],
    "Soap": ["Camay", "Lux"],
    "Electronics companies": ["Dell", "Apple"],
    "Toothpaste": ["Signal", "Close Up", "Colgate", "Crest"],
    "Cosmetics": ["Avon", "Hair cream (Palmers)"]
}

def get_alternative_category(category):
    for cat, brands in categories.items():
        if cat != category and any(brand in blocked_brands for brand in brands):
            return categories[cat]
    return []

def barcode_lookup(barcode):
    api_key = "usrj7aj4owf0l7evt9qn74dqt9esl9"
    url = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        barcode = data["products"][0]["barcode_number"]
        name = data["products"][0]["title"]
        brand = data["products"][0]["brand"].strip().lower()

        st.write("Barcode Number:", barcode)
        st.write("Title:", name)
        st.write("Brand:", brand)

        if any(brand in blocked for blocked in blocked_brands):
            try:
                index = next((i for i, sublist in enumerate(blocked_brands) if brand in sublist))
                replacement = alternative_brands[index]
            except IndexError:
                category = next((cat for cat, brands in categories.items() if brand in brands), None)
                replacement = get_alternative_category(category)
                
            if replacement:
                st.write("This brand is blocked. Here are alternative brands:", replacement)
            else:
                st.write("This brand is blocked, and alternative brands are not available for this category.")
        else:
            st.write("This brand is not blocked.")
    else:
        st.write("Error:", response.status_code)

# Streamlit UI
st.markdown(f"<h1 style='text-align: center; font-size:50px;'>{('مقاطعة المنتجات التي تدعم إسرائيل')}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; font-size:20px;'>{('تحديد المنتجات التي تدعم إسرائيل عن طريق تحديد البار كود الخاص ب المنتج و ترشيح بديل')}</h1>", unsafe_allow_html=True)

# Sidebar to select brands by category
selected_category = st.sidebar.selectbox("Select a Category", list(categories.keys()))

# Display brands in the selected category
if selected_category:
    st.sidebar.markdown(f"**{selected_category}**")
    selected_brands = categories[selected_category]
    for brand in selected_brands:
        st.sidebar.text(brand)

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

if st.button("بحث"):
    barcode_lookup(manual_barcode_input)
