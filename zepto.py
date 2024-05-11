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
            if len(image_urls) >= 2:  # Ensure at least 2 images are available
                img_urls.append(image_urls[1])  # Select the second image

    div = soup.find('div', class_='bg-skin-base p-4 text-lg font-subtitle text-skin-primary-void/60')
    if div:
        text_content = div.get_text(separator='\n', strip=True)
        if "Ingredients :" in text_content:
            ingredient_section = text_content.split("Ingredients :")[1].strip()
            if '\n' in ingredient_section:
                ingredient_section = ingredient_section.split('\n')[0]
        else:
            ingredient_section = []
    else:
        ingredient_section = []

    return title, price, img_urls, ingredient_section