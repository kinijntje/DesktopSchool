import json
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver
driver = webdriver.Chrome()

# URL of the website containing the category URLs
url = "https://frituur-de-vrede.unipage.eu/"

# Open the website
driver.get(url)

driver.implicitly_wait(2)

# Find all div elements with class "row items"
items = driver.find_elements(By.CLASS_NAME, "row.items")

data = {}  # Dictionary to store the data in the desired structure

# Loop over each "row items" div
for item in items:
    # Find the first div with class "category"
    driver.implicitly_wait(2)
    
    category_div = item.find_element(By.CLASS_NAME, "category")
    category_name = category_div.text

    # Create a list to store product data for the category
    category_data = []

    # Loop over other divs inside the "row items" div
    other_divs = item.find_elements(By.CLASS_NAME, "item-top-part")
    for other_div in other_divs:
        # Skip the "category" div
        if other_div == category_div:
            continue

        # Extract information from each item
        card_title = other_div.find_element(By.CLASS_NAME, "card-title").find_element(By.TAG_NAME, "span").text
        try:
            card_subtitle = other_div.find_element(By.CLASS_NAME, "card-subtitle").text
        except Exception as e:
            print("Error occurred while extracting subtitle: ", card_title)
            card_subtitle = None

        card_image_element = other_div.find_element(By.CLASS_NAME, "image-wrap").find_element(By.TAG_NAME, "img")
        card_image = card_image_element.get_attribute("data-src")

        price = other_div.find_element(By.CLASS_NAME, "badge").text

        # Append product data to the category's data list
        product = {
            "Product Name": card_title,
            "Product Description": card_subtitle,
            "Product Image URL": card_image,  # Save Base64 image data
            "Product Price": price
        }
        category_data.append(product)

    # Store the category data under the category name in the main data dictionary
    data[category_name] = category_data

# Close the WebDriver when done
driver.quit()

# Write the data to a JSON file
with open("uniOutput.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data has been written to uniOutput.json")
