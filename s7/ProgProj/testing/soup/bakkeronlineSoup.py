import json
import requests
from bs4 import BeautifulSoup
import time

# URL of the website containing the category URLs
url = "https://webshop.broodenbanketmartens.be/be-nl/martens"

# Send a GET request to the website
response = requests.get(url)

time.sleep(5)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Find all category links on the page
category_links = soup.select('ul.list li a.category-link')

# Extract category URLs and store them in a list
category_urls = [link['href'] for link in category_links]
print("Category URLs:", category_urls)

# List to store scraped data
all_products = []

# Loop through each category URL and scrape products
for category_url in category_urls:
    # Construct full URL
    full_url = f"https://webshop.broodenbanketmartens.be{category_url}"
    print("Scraping URL:", full_url)
    
    # Send a GET request to the category URL
    category_response = requests.get(full_url)
    
    # Parse the HTML content of the category page
    category_soup = BeautifulSoup(category_response.content, "html.parser")
    
    # Find all product cards on the category page
    product_cards = category_soup.select('form.blocks.product-card')

    # Extract and store product names, images, and prices for this category
    category_products = []
    for product_card in product_cards:
        product_name_element = product_card.select_one('h3.product-title strong')
        product_name = product_name_element.text.strip()
        
        # Extract product image URL or assign None if it's missing
        product_image_element = product_card.select_one('div.cover')
        product_image_url = product_image_element.get('style').replace('background-image:url("', '').replace('")', '') if product_image_element else None
        
        product_price_element = product_card.select_one('strong.price.total')
        product_price = product_price_element.text.strip()
        
        product_data = {
            "Product Name": product_name,
            "Product Image URL": product_image_url,
            "Product Price": product_price
        }
        
        # Append the dictionary to the list for this category
        category_products.append(product_data)

    # Add category products to the main list
    all_products.append({full_url: category_products})

# Write the scraped data to a JSON file
with open("bakkerOutput.json", "w") as outfile:
    json.dump(all_products, outfile, indent=4)

print("Scraped data has been successfully written to 'bakkerOutput.json'.")
