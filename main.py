import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product title
    title_element = soup.find("span", {"class": "VU-ZEz"})
    title = title_element.text.strip() if title_element else "Not found"

    # Extract product price
    price_element = soup.find("div", {"class": "Nx9bqj CxhGGd"})
    price = price_element.text.strip() if price_element else "Not found"

    # Extract product image
    image_element = soup.find("div", {"class": "z1kiw8"})
    image = image_element.find('img')['src'] if image_element else "Not found"

    # Extract product description
    description_element = soup.find("td", {"class": "HPETK2"})
    description = description_element.text.strip() if description_element else "Not found"

    return title, price, image, description

st.title('Flipkart Product Scraper')

url = st.text_input('Enter Flipkart Product URL:')
if url:
    title, price, image, description = extract_product_info(url)

    st.write(f"Product Title: {title}")
    st.write(f"Product Price: {price}")
    st.image(image, caption='Product Image', use_column_width=True)
    st.write(f"Product Description: {description}")
