import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver
driver = webdriver.Chrome()

# URL of the website containing the category URLs
url = "https://webshop.broodenbanketmartens.be/be-nl/martens"

# Open the website
driver.get(url)

# Wait for the category links to load (you might need to adjust the waiting time)
driver.implicitly_wait(2)

# Find all category links on the page
category_links = driver.find_elements(By.CSS_SELECTOR, 'ul.list li a.category-link')

# Extract category URLs and store them in a list
category_urls = [link.get_attribute('href') for link in category_links]

# List to store scraped data
all_products = []

# Loop through each category URL and scrape products
for category_url in category_urls:
    # Construct full URL
    full_url = f"{category_url}"
    print("Scraping URL:", full_url)
    
    # Open the website
    driver.get(full_url)
    
    # Wait for the products to load (you might need to adjust the waiting time)
    driver.implicitly_wait(2)
    
    # Find all product cards on the page
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'form.blocks.product-card')

    # Extract and store product names, images, and prices for this category
    category_products = []
    for product_card in product_cards:
        product_name_element = product_card.find_element(By.CSS_SELECTOR, 'h3.product-title strong')
        product_name = product_name_element.text
        
        # Extract product image URL or assign None if it's missing
        try:
            product_image_element = product_card.find_element(By.CSS_SELECTOR, 'div.cover')
            product_image_url = product_image_element.value_of_css_property("background-image").replace('url("', '').replace('")', '')
        except Exception as e:
            print("Error occurred while extracting image:", str(e))
            product_image_url = None
        
        product_price_element = product_card.find_element(By.CSS_SELECTOR, 'strong.price.total')
        product_price = product_price_element.text
        
        # Store data in a dictionary
        product_data = {
            "Product Name": product_name,
            "Product Image URL": product_image_url,
            "Product Price": product_price
        }
        
        # Append the dictionary to the list for this category
        category_products.append(product_data)

    # Add category products to the main list
    all_products.append({category_url: category_products})

# Close the driver
driver.quit()

# Convert the list of dictionaries to JSON format
output_json = json.dumps(all_products, indent=4)

# Write the JSON data to an output file
with open("bakkerOutput.json", "w") as outfile:
    outfile.write(output_json)

print("Scraped data has been successfully written to 'bakkerOutput.json'.")
