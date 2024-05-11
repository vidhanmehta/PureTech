import requests
from bs4 import BeautifulSoup
import random
import time

# Define a list of user-agent strings
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def extract_bigbasket_product_info(url):
    # Send a GET request to the URL and get the HTML content
    headers = {"User-Agent": random.choice(user_agent_list)}
    response = requests.get(url, headers=headers)

    # Delay for a random time between 2 and 5 seconds
    time.sleep(random.uniform(2, 5))

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the product title
    title_element = soup.find("h1", class_="Description___StyledH-sc-82a36a-2 bofYPK")
    if title_element:
        title = title_element.text.strip()
    else:
        title = None

    # Extract the product price
    price_element = soup.find("td", class_="Description___StyledTd-sc-82a36a-4 fLZywG")
    if price_element:
        price_text = price_element.text.strip()
        try:
            price = price_text.split(":")[1].strip()
        except IndexError:
            price = None
    else:
        price = None

    # Extract the product image URL
    image_div = soup.find("div", class_="sticky self-start")
    if image_div:
        image_element = image_div.find("img")
        if image_element:
            image_url = image_element["src"]
        else:
            image_url = None
    else:
        image_url = None

    # Extract Ingredients
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

    return title, price, image_url, ingredient_section
