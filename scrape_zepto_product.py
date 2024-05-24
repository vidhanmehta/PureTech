import requests
from bs4 import BeautifulSoup

url = "https://www.zeptonow.com/pn/mamaearth-onion-shampoo-for-hair-fall-control/pvid/15260611-7fc2-4bf7-8420-7683a74b51ef"
img_urls = []
def extract_product_info(url):
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
           price_div = soup.find("h4", {"data-testid" : "pdp-discounted-selling-price" })
        price = price_div.text.strip() if price_div else None
    except AttributeError:
        price = None

    # Extract image URL
    slider_wrapper_div = soup.find('div', id='slider-wrapper')

    if slider_wrapper_div:
    # Find the div with id 'holder' within the 'slider-wrapper' div
        holder_div = slider_wrapper_div.find('div', id='holder')

        if holder_div:
        # Find all the img tags within the 'holder' div and extract the 'src' 0.
             image_urls = [img['src'] for img in holder_div.find_all('img')]

        # Print the extracted image URLs
             for url in image_urls:

               img_urls.append(url)

        else:
           print("Div with id 'holder' not found within the 'slider-wrapper' div.")
    else:
        print("Div with id 'slider-wrapper' not found.")

    # Extract description
    try:
        description_div = soup.find("div", {"data-testid": "about-product-container"})
        description = description_div.find("p").text.strip() if description_div else None
    except AttributeError:
        description = None

    return title, price, img_urls[1:], description

title, price, img_urls, description = extract_product_info(url)
print("Title:", title)
print("Price:", price)
print("Image URL:", img_urls)
print("Description:", description)
