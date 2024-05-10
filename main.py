import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as gen_ai

st.title('Product Assist')

url = st.text_input('Enter Amazon Product URL:')
if url:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape product title
        title_element = soup.select_one('#productTitle')
        title = title_element.text.strip() if title_element else "Not found"
        st.write(f"Product Title: {title}")

        # Scrape product price
        price_element = soup.select_one('span.a-offscreen')
        price = price_element.text.encode('utf-8').decode('utf-8') if price_element else "Not found"
        st.write(f"Product Price: {price}")

        # Scrape product image
        image_element = soup.select_one('#landingImage')
        image = image_element.attrs.get('src') if image_element else "Not found"
        st.image(image, caption='Product Image')

        # Scrape product ingredients
        ingredients_element = soup.find('div', {'id': 'important-information'})
        if ingredients_element and ingredients_element.find('h4', string='Ingredients:'):
            ingredients_text = ingredients_element.find('h4', string='Ingredients:').find_next('p').text.strip()
            ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(',')]
            st.write(f"Product Ingredients: {ingredients_list}")
        else:
            st.write("Product Ingredients: Not available")

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

        with st.expander("Ingredients"):
            # Provide the merged ingredient list to Gemini for analysis
            gemini_response = st.session_state.chat_session.send_message(f"Please provide each and every ingredient list of the {title}, if it is available on {url}. Fetch from it otherwise fetch from other sources. Merged ingredients: {ingredients_list}.")
            
            if gemini_response.parts:
                # Extract Gemini-generated ingredients
                ingredients_gemini = gemini_response.parts[0].text.strip().split("\n")
                
                # Merge website-extracted and Gemini-generated ingredients, remove duplicates
                merged_ingredients = list(set(ingredients_list + ingredients_gemini))

                # Provide the merged ingredient list to Gemini for analysis
                gemini_final_response = st.session_state.chat_session.send_message(f"Here is the merged ingredient list: {merged_ingredients}. Please analyze and provide the final ingredient list and put a ✅ emoji next to safe ingredients and a ❌ next to harmful ingredients. Don't include allergen information or extra details, stick to the ingredients only.")
                st.markdown(gemini_final_response.text)
            else:
                st.write("No response from Gemini. Please try again.")
    else:
        st.write(str(response.status_code) + ' - Error loading the page')
