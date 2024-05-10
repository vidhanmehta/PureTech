import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_product_info(url):
    webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    title_element = soup.select_one('#productTitle')
    title = title_element.text.strip() if title_element else None

    # Extract price
    price_element = soup.select_one('span.a-offscreen')
    price = price_element.text.strip() if price_element else None

    # Extract image URL
    image_element = soup.select_one('#landingImage')
    image_url = image_element['src'] if image_element else None

    # Extract Ingredients if available
    ingredients = []
    ingredients_element = soup.find('div', {'id': 'important-information'})
    if ingredients_element and ingredients_element.find('h4', string='Ingredients:'):
        ingredients_text = ingredients_element.find('h4', string='Ingredients:').find_next('p').text.strip()
        ingredients = [ingredient.strip() for ingredient in ingredients_text.split(',')]

    return title, price, image_url, ingredients

st.title('Amazon Product Scraper')

url = st.text_input('Enter Amazon Product URL:')
if url:
    title, price, image_url, ingredients = extract_product_info(url)

    if title and price and image_url:
        st.subheader(title)
        st.write(f"Price: {price}")
        st.image(image_url, caption='Product Image', use_column_width=True)
        if ingredients:
            st.write(f"Product Ingredients: {ingredients}")
        else:
            st.write("Product Ingredients: Not available")
    else:
        st.write("Unable to extract product information. Please check the URL and try again.")
