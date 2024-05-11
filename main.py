import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as gen_ai

def extract_product_info(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extract product title
    try:
        title = soup.find("span", {"class": "VU-ZEz"}).text.strip()
    except AttributeError:
        title = None

    # Extract price
    try:
        price = soup.find("div", {"class": "Nx9bqj CxhGGd"}).text.strip()
    except AttributeError:
        price = None

    # Extract image URL
    try:
        image_div = soup.find("div", {"class": "z1kiw8"})
        image_url = image_div.find("img")["src"] if image_div else None
    except AttributeError:
        image_url = None

    # Extract Ingredients
    try:
        description = soup.find("td", string="Ingredients").find_next_sibling("td").text.strip()
        ingredients_website = [ingredient.strip() for ingredient in description.split(",")]
    except AttributeError:
        ingredients_website = []

    return title, price, image_url, ingredients_website

st.title("Flipkart Product Analyzer")

url = st.text_input("Enter the Flipkart product URL:")

if st.button("Show All Details"):
    if url:
        title, price, image_url, ingredients_website = extract_product_info(url)

        if title and price and image_url:
            st.subheader(title)
            st.write(f"Price: {price}")
            st.image(image_url)
        else:
            st.write("Unable to extract product information. Please check the URL and try again.")

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
        gemini_response = st.session_state.chat_session.send_message(f"Please provide each and every ingredient list of the {title}, if it is available on {url}. Fetch from it otherwise fetch from other sources. Merged ingredients: {ingredients_website}.")
            
            # Extract Gemini-generated ingredients
        ingredients_gemini = gemini_response.parts[0].text.strip().split("\n")
            
            # Merge website-extracted and Gemini-generated ingredients, remove duplicates
        merged_ingredients = list(set(ingredients_website + ingredients_gemini))

            # Provide the merged ingredient list to Gemini for analysis
        gemini_final_response = st.session_state.chat_session.send_message(f"Here is the merged ingredient list: {merged_ingredients}. Please analyze and provide the final ingredient list and put a ✅ emoji next to safe ingredients and a ❌ next to harmful ingredients. Don't include allergen information or extra details, stick to the ingredients only.")
        st.markdown(gemini_final_response.text)

        # Send harmful ingredients to Gemini for further analysis
        safety_score_response = st.session_state.chat_session.send_message(f"Compute the number of harmful ingredients in {gemini_final_response} and compute the safety_score = 100 - 4 * number of harmful ingredients and return the safety score as a number only")

            
    st.markdown(f"Safety Score: {safety_score_response.text}")

    harmful_analysis = st.session_state.chat_session.send_message(f"In a table format give the harmful ingredients and their effects in another column keep the effects very short and precise")
    st.markdown(harmful_analysis.text)

    # Prompt Gemini for product recommendation in the same category
    category_recommendation = st.session_state.chat_session.send_message(f"Please recommend a product in the same category as that of {title} that is better than the current product along with an Amazon link keep the content precise and short to the point do not brief.")

    # Prompt Gemini to analyze top 5 customer reviews and provide an overall summary
    reviews_summary = st.session_state.chat_session.send_message(f"Please analyze the top 5 customer reviews of {title} with given url {url} and provide an overall summary keep it super short not exceeding more than four lines.")
    st.write(category_recommendation.text)
    st.write(reviews_summary.text)
