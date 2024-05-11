import requests
from bs4 import BeautifulSoup
import random

# Define a list of user-agent strings
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def extract_amazon_product_info(url):
    webpage = requests.get(url, headers={'User-Agent': random.choice(user_agent_list)})
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    title_element = soup.find("span", {"id": "productTitle"})
    title = title_element.get_text(strip=True) if title_element else None

    # Extract price
    price_element = soup.find("span", {"class": "a-offscreen"})
    price = price_element.get_text(strip=True) if price_element else None

    # Extract image URL
    image_element = soup.find("img", {"id": "landingImage"})
    image_url = image_element["src"] if image_element else None

    # Extract Ingredients
    ingredients_element = soup.find('div', {'id': 'important-information'})
    if ingredients_element and ingredients_element.find('h4', string='Ingredients:'):
        ingredients_text = ingredients_element.find('h4', string='Ingredients:').find_next('p').text.strip()
        ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(',')]
    else:
        ingredients_list = []

    return title, price, image_url, ingredients_list
