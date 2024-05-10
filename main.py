import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    try:
        title = soup.find("span", {"class": "B_NuCI"}).text.strip()
    except AttributeError:
        title = None

    # Extract price
    try:
        price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).text.strip()
    except AttributeError:
        price = None

    # Extract image URL
    try:
        image_div = soup.find("div", {"class": "_2_AcLJ"})
        image_url = image_div.find("img")["src"] if image_div else None
    except AttributeError:
        image_url = None

    # Extract Ingredients
    try:
        description = soup.find("div", {"class": "_1AtVbE"}).text.strip()
    except AttributeError:
        description = None
    
    return title, price, image_url, description

# Streamlit app
def main():
    st.title("Product Information Extractor")
    url = st.text_input("Enter Product URL:")
    if st.button("Extract"):
        if url:
            title, price, image_url, description = extract_product_info(url)
            st.write("Title:", title)
            st.write("Price:", price)
            st.write("Image URL:", image_url)
            st.write("Ingredients:", description)
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()
