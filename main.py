import streamlit as st
import requests
from bs4 import BeautifulSoup

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

    # Extract ingredients
    try:
        description = soup.find("td", text="Ingredients").find_next_sibling("td").text.strip()
    except AttributeError:
        description = None
    
    return title, price, image_url, description

st.title('Flipkart Product Scraper')

url = st.text_input('Enter Flipkart Product URL:')
if url:
    title, price, image_url, description = extract_product_info(url)

    st.write(f"Product Title: {title}")
    st.write(f"Product Price: {price}")
    if image_url:
        st.image(image_url, caption='Product Image', use_column_width=True)
    st.write(f"Ingredients: {description}")
