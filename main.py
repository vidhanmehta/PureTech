import streamlit as st
import requests
from bs4 import BeautifulSoup
from gemini_api import GeminiAPI

# Initialize Gemini API
gemini = GeminiAPI(api_key="your_gemini_api_key")

def scrape_amazon_product(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape product title
        title_element = soup.select_one('#productTitle')
        title = title_element.text.strip()

        # Scrape product rating
        rating_element = soup.select_one('#acrPopover')
        rating_text = rating_element.attrs.get('title')
        rating = rating_text.replace('out of 5 stars', '')

        # Scrape product price
        price_element = soup.select_one('span.a-offscreen')
        price = price_element.text.encode('utf-8').decode('utf-8')

        # Scrape product image
        image_element = soup.select_one('#landingImage')
        image = image_element.attrs.get('src')

        # Scrape product description
        description_element = soup.select_one('#productDescription')
        description = description_element.text.strip()

        # Additional details (example: number of reviews)
        reviews_element = soup.select_one('#acrCustomerReviewText')
        if reviews_element:
            reviews = reviews_element.text
        else:
            reviews = "Not available"

        return {
            "title": title,
            "rating": rating,
            "price": price,
            "image": image,
            "description": description,
            "reviews": reviews
        }
    else:
        return None

def analyze_ingredients(product_description):
    # Use Gemini API to analyze the ingredients
    ingredients = gemini.analyze_ingredients(product_description)

    # Identify harmful ingredients
    harmful_ingredients = [ingredient for ingredient in ingredients if ingredient.is_harmful]

    # Generate recommendations
    recommendations = gemini.generate_recommendations(harmful_ingredients)

    return harmful_ingredients, recommendations

def main():
    st.title("Ingredient Analyzer")

    # User input for Amazon product URL
    product_url = st.text_input("Enter the Amazon product URL:")

    if st.button("Analyze"):
        # Scrape product information from Amazon
        product_info = scrape_amazon_product(product_url)

        if product_info:
            # Display product information
            st.header(product_info["title"])
            st.image(product_info["image"])
            st.write(f"Rating: {product_info['rating']}")
            st.write(f"Price: {product_info['price']}")
            st.write(f"Reviews: {product_info['reviews']}")
            st.write(product_info["description"])

            # Analyze ingredients using Gemini
            harmful_ingredients, recommendations = analyze_ingredients(product_info["description"])

            # Display harmful ingredients and recommendations
            if harmful_ingredients:
                st.subheader("Harmful Ingredients:")
                for ingredient in harmful_ingredients:
                    st.write(ingredient.name)

            st.subheader("Recommendations:")
            for recommendation in recommendations:
                st.write(recommendation)
        else:
            st.error("Error: Unable to retrieve product information.")

if __name__ == "__main__":
    main()
