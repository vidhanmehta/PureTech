import requests
from bs4 import BeautifulSoup

url ="https://www.flipkart.com/beyond-snack-3-pack-combo-kerala-banana-chips/p/itm1f87d331e5bbb?pid=CHPFPDNWNPUNJSUJ&lid=LSTCHPFPDNWNPUNJSUJQKDW3L&marketplace=FLIPKART&q=chips&store=eat%2Flng&spotlightTagId=FkPickId_eat%2Flng&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=27d54fc7-e51b-4d1e-8db9-8883ee2d0093.CHPFPDNWNPUNJSUJ.SEARCH&ppt=sp&ppn=sp&ssid=s4l6zy4na80000001715164286240&qH=19136e394ab695f9"


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

    # Extract Ingridents
    try:
        description = soup.find("td", text="Ingredients").find_next_sibling("td").text.strip()
    except AttributeError:
        description = None
    
    return title, price, image_url, description

title, price, image_url, description = extract_product_info(url)
print("Title:", title)
print("Price:", price)
print("Image URL:", image_url)
print("Ingridents:", description)
