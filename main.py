import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as gen_ai

def extract_amazon_product_info(url):
    webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})
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

def extract_flipkart_product_info(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    title_element = soup.find("span", {"class": "VU-ZEz"})
    title = title_element.text.strip() if title_element else None

    # Extract price
    price_element = soup.find("div", {"class": "Nx9bqj CxhGGd"})
    price = price_element.text.strip() if price_element else None

    # Extract image URL
    image_div = soup.find("div", {"class": "z1kiw8"})
    image_url = image_div.find("img")["src"] if image_div else None

    # Extract Ingredients
    try:
        description = soup.find("td", string="Ingredients").find_next_sibling("td").text.strip()
        ingredients_website = [ingredient.strip() for ingredient in description.split(",")]
    except AttributeError:
        ingredients_website = []

    return title, price, image_url, ingredients_website

def identify_website(url):
    if 'amazon' in url:
        return 'Amazon'
    elif 'flipkart' in url:
        return 'Flipkart'
    else:
        return None

st.title('Product Analyzer')

url = st.text_input('Enter Product URL:')

if url:
    website_name = identify_website(url)
    if website_name:
        try:
            # Clear previous content
            st.empty()

            # Insert your Gemini API key here
            GOOGLE_API_KEY = "AIzaSyCMgUr_fxj9Sqoz9afpep-J6ZyQeEnu59c"

            # Set up Google Gemini-Pro AI model
            gen_ai.configure(api_key=GOOGLE_API_KEY)
            model = gen_ai.GenerativeModel('gemini-pro')

            # Initialize chat session in Streamlit if not already present
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = model.start_chat(history=[])

            if website_name.lower() == 'amazon':
                title, price, image_url, ingredients_list = extract_amazon_product_info(url)
            elif website_name.lower() == 'flipkart':
                title, price, image_url, ingredients_list = extract_flipkart_product_info(url)
            else:
                st.error("Invalid website name. Please enter a valid Amazon or Flipkart product URL.")

            if title and price and image_url:
                st.subheader(title)
                st.write(f"Price: {price}")
                st.image(image_url, caption='Product Image')
            else:
                st.write("Unable to extract product information. Please check the URL and try again.")

            # Continue with the rest of the analysis

            gemini_response = st.session_state.chat_session.send_message(f"Please provide each and every ingredient list of the {title}, if it is available on {url}. Fetch from it otherwise fetch from other sources. Merged ingredients: {ingredients_list}.")
            ingredients_gemini = gemini_response.parts[0].text.strip().split("\n")
            merged_ingredients = list(set(ingredients_list + ingredients_gemini))
            gemini_final_response = st.session_state.chat_session.send_message(f"Here is the merged ingredient list: {merged_ingredients}. Please analyze and provide the final ingredient list and put a ✅ emoji next to safe ingredients and a ❌ next to harmful ingredients. Don't include allergen information or extra details, stick to the ingredients only.")
            
            if st.button('Analyze Product'):
                with st.expander("Ingredients"):
                    st.markdown(gemini_final_response.text)

                    safety_score_response = st.session_state.chat_session.send_message(f"Compute the number of harmful ingredients in {gemini_final_response} and compute the safety_score = 100 - 4 * number of harmful ingredients and return the safety score as a number only avoid dangerous content")

                st.markdown(f"Safety Score: {safety_score_response.text}")

                harmful_analysis = st.session_state.chat_session.send_message(f"In a table format give the {title} harmful ingredients and their effects in another column keep the effects very short and precise avoid dangerous content")
                st.markdown(harmful_analysis.text)

                category_recommendation = st.session_state.chat_session.send_message(f"Please recommend a product in the same category as that of {title} that is better than the current product along with an {url} link keep the content precise and short to the point do not brief. avoid dangerous content.")

                reviews_summary = st.session_state.chat_session.send_message(f"Please analyze the top 5 customer reviews of {title} with given url {url} and provide an overall summary keep it super short not exceeding more than four lines.")
                st.write(category_recommendation.text)
                st.write(reviews_summary.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.error("Invalid URL. Please enter a valid Amazon or Flipkart product URL.")
