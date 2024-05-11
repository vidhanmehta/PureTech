import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import time
import google.generativeai as gen_ai
from streamlit import secrets

# Importing custom scraping functions
from amazon import extract_amazon_product_info
from flipkart import extract_flipkart_product_info
from bigbasket import extract_bigbasket_product_info
from zepto import extract_product_info

# Set Streamlit theme to light
st.set_page_config(page_title="PureTech")

st.title('PureTech')
st.markdown("Made by - Sumith, Vidhan, Swathi, and Venkat")

url = st.text_input('Enter Product URL:')

if url:
    # Determine the website based on the URL entered
    if 'amazon' in url:
        website_name = 'Amazon'
    elif 'flipkart' in url:
        website_name = 'Flipkart'
    elif 'bigbasket' in url:
        website_name = 'BigBasket'
    elif 'zepto' in url:
        website_name = 'Zepto'
    else:
        website_name = None

    if website_name:
        try:
            # Clear previous content
            st.empty()

            if website_name.lower() == 'amazon':
                title, price, image_url, ingredients_list = extract_amazon_product_info(url)
            elif website_name.lower() == 'flipkart':
                title, price, image_url, ingredients_list = extract_flipkart_product_info(url)
            elif website_name.lower() == 'bigbasket':
                title, price, _, ingredients_list = extract_bigbasket_product_info(url)  # Ignore image_url for BigBasket
                image_url = None  # Set image_url to None for BigBasket
            elif website_name.lower() == 'zepto':
                title, price, image_url, ingredients_list = extract_product_info(url)
            else:
                st.error("Invalid website name. Please enter a valid URL.")

            if title and price:
                st.subheader(title)
                st.write(f"Price: {price}")
                if image_url and website_name.lower() != 'bigbasket':  # Exclude image display for BigBasket
                    st.image(image_url, caption='Product Image')
                
                # Get the API key from secrets
                GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']

                # Set up Google Gemini-Pro AI model
                gen_ai.configure(api_key=GOOGLE_API_KEY)
                model = gen_ai.GenerativeModel('gemini-pro')

                # Initialize chat session in Streamlit if not already present
                if "chat_session" not in st.session_state:
                    st.session_state.chat_session = model.start_chat(history=[])

                if st.button('Your Health in a Click'):
                    with st.expander("Ingredients"):
                        gemini_response = st.session_state.chat_session.send_message(f"Please provide each and every ingredient list of the {title}, if it is available on {url}. Fetch from it otherwise fetch from other sources.")
                        ingredients_gemini = gemini_response.parts[0].text.strip().split("\n")
                        merged_ingredients = list(set(ingredients_list + ingredients_gemini))
                        gemini_final_response = st.session_state.chat_session.send_message(f"Here is the merged ingredient list: {merged_ingredients}. Please analyze and provide the final ingredient list and put a ✅ emoji next to safe ingredients and a ❌ next to harmful ingredients. Don't include allergen information or extra details, stick to the ingredients only.")
                        safety_score_response = st.session_state.chat_session.send_message(f"Compute the number of harmful ingredients in {gemini_final_response} and compute the safety_score = 100 - 4 * number of harmful ingredients and return the safety score as a number only avoid dangerous content")
                        st.markdown(gemini_final_response.text)

                    st.markdown(f"Safety Score: {safety_score_response.text}")

                    harmful_analysis = st.session_state.chat_session.send_message(f"In a table format give the {title} harmful ingredients and their effects in another column keep the effects very short and precise")
                    st.markdown(harmful_analysis.text)

                    category_recommendation = st.session_state.chat_session.send_message(f"Please recommend a product in the same category as that of {title} that is better than the current product along with an {url} link keep the content precise and short to the point do not brief. avoid dangerous content.")

                    reviews_summary = st.session_state.chat_session.send_message(f"Please analyze the top 5 customer reviews of {title} with given url {url} and provide an overall summary keep it super short not exceeding more than four lines.")
                    st.write(category_recommendation.text)
                    st.write(reviews_summary.text)
            else:
                st.error("Unable to extract product information. Please check the URL and try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}. Please retry.")

    else:
        st.error("Invalid URL. Please enter a valid product URL.")
