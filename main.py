import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as gen_ai

st.title('Ingredient Assist')
st.markdown('- Made by Sumith, Vidhan, Swathi, and Venkat')

url = st.text_input('Enter Amazon Product URL:')
if url:
    button_clicked = st.button('Your Health in a Click')

    if button_clicked:
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
                gemini_response = st.session_state.chat_session.send_message(f"Please provide each and every ingredient list of the {title}, if it is available on {url}. Fetch from it otherwise fetch from other sources.")

                # Provide the final response to Gemini
                final_response = st.session_state.chat_session.send_message(f"Here is the ingredient list as suggested in website {ingredients_list} and these are the AI generated ingredient list {gemini_response} please provide the final ingredient list and analyze the ingredients as safe and harmful indiacted by green tick and red cross respectively. ")
                st.markdown(final_response.text)

                # Send harmful ingredients to Gemini for further analysis
                harmful_response = st.session_state.chat_session.send_message(f"Give the number of harmful ingredients in {final_response}")

            # Compute safety score and identify harmful ingredients
            safety_score = 100 - 4 * int(harmful_response.text)
        st.markdown(f"Safety Score: {safety_score}")

        harmful_analysis = st.session_state.chat_session.send_message(f"In a table format give the harmful ingredients and their effects in another column keep the effects very short and precise")
        st.markdown(harmful_analysis.text)

        # Prompt Gemini for product recommendation in the same category
        category_recommendation = st.session_state.chat_session.send_message("Please recommend a product in the same category as that of {title} that is better than the current product along with an Amazon link.")

        # Prompt Gemini to analyze top 5 customer reviews and provide an overall summary
        reviews_summary = st.session_state.chat_session.send_message("Please analyze the top 5 customer reviews of {title} with given url {url} and provide an overall summary.")
        st.write(category_recommendation.text)
        st.write(reviews_summary.text)

    else:
            st.write('Error loading the page')
