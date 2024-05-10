import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_product_info(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    try:
        title = soup.find("span", {"class": "VU-ZEz"}).text.strip()
    except AttributeError:
        title = None

    # Extract price
    try:
        price = soup.find("div", {"class": "Nx9bqj CxhGGd"}).text.strip()
    except AttributeError:
        price = None

    # Extract image URL
    try:
        image_div = soup.find("div", {"class": "z1kiw8"})
        image_url = image_div.find("img")["src"] if image_div else None
    except AttributeError:
        image_url = None

    # Extract Ingredients
    try:
        description = soup.find("td", string="Ingredients").find_next_sibling("td").text.strip()
        ingredients_website = [ingredient.strip() for ingredient in description.split(",")]
    except AttributeError:
        ingredients_website = []

    return title, price, image_url, ingredients_website

st.title("Flipkart Product Analyzer")

url = st.text_input("Enter the Flipkart product URL:")

if st.button("Show All Details"):
    if url:
        title, price, image_url, ingredients_website = extract_product_info(url)

        if title and price and image_url:
            st.subheader(title)
            st.write(f"Price: {price}")
            st.image(image_url)
        else:
            st.write("Unable to extract product information. Please check the URL and try again.")

    # Clear previous content
    st.empty()
