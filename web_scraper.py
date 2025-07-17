import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_flipkart(search_query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    base_url = "https://www.flipkart.com/search?q=" + search_query.replace(' ', '+')

    product_names = []
    prices = []
    links = []

    for page in range(1, 3):  # scrape 2 pages
        url = f"{base_url}&page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        titles = soup.find_all("div", class_="_4rR01T")
        prices_html = soup.find_all("div", class_="_30jeq3 _1_WHN1")
        product_links = soup.find_all("a", class_="_1fQZEK")

        for name, price, link in zip(titles, prices_html, product_links):
            product_names.append(name.text.strip())
            prices.append(price.text.strip())
            links.append("https://www.flipkart.com" + link['href'])

        time.sleep(2)  # be polite and wait 2 seconds

    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': prices,
        'Link': links
    })
    
    df.to_csv('flipkart_products.csv', index=False)
    print("Scraping completed. Data saved to flipkart_products.csv.")

# Run the function
query = input("Enter a product to search on Flipkart: ")
scrape_flipkart(query)
