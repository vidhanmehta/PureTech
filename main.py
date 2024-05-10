import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_product_info(url):
    img_urls = []
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    try:
        title = soup.find("h1").text.strip()
    except AttributeError:
        title = None

    # Extract price
    try:
        price_div = soup.find("h4", {"data-test-id": "pdp-selling-price"})
        if not price_div:
            price_div = soup.find("h4", {"data-testid": "pdp-discounted-selling-price"})
        price = price_div.text.strip() if price_div else None
    except AttributeError:
        price = None

    # Extract image URLs
    slider_wrapper_div = soup.find('div', id='slider-wrapper')
    if slider_wrapper_div:
        holder_div = slider_wrapper_div.find('div', id='holder')
        if holder_div:
            image_urls = [img['src'] for img in holder_div.find_all('img')]
            img_urls.extend(image_urls)

    # Extract description
    try:
        description_div = soup.find("div", {"data-testid": "about-product-container"})
        description = description_div.find("p").text.strip() if description_div else None
    except AttributeError:
        description = None

    return title, price, img_urls, description

st.title('Zepto Product Scraper')

url = st.text_input('Enter Zepto Product URL:')
if url:
    title, price, img_urls, description = extract_product_info(url)

    st.write(f"Product Title: {title}")
    st.write(f"Product Price: {price}")
    
    if img_urls:
        st.write("Product Image URLs:")
        for img_url in img_urls:
            st.image(img_url, caption='Product Image', use_column_width=True)

    st.write(f"Product Description: {description}")
