import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extract_number_from_url(url):
    product_pattern = r'/product/(\d+)'
    category_pattern = r'/category/(\d+)'

    product_matches = re.findall(product_pattern, url)
    category_matches = re.findall(category_pattern, url)

    if product_matches:
        return product_matches[-1]
    elif category_matches:
        return category_matches[-1]
    else:
        return None

start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-cache")
# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL of the website containing the category URLs
url = "https://waardamme.bakkerijkerkhove.be/be-nl/bakkerijkerkhove-waardamme/overview"

# Open the website
driver.get(url)

wait = WebDriverWait(driver, 3)  # 3 max seconds timeout
shortwait = WebDriverWait(driver, 1)
category_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.list li a.category-link')))

# Extract category URLs and store them in a list
category_urls = [link.get_attribute('href') for link in category_links]

# Dictionary to store scraped data per category
all_products = {}
category_mapping = {}
products = []

# Loop through each category URL and scrape products
for category_url in category_urls:
    # Construct full URL
    full_url = f"{category_url}"
    print("Scraping URL:", full_url)
    
    category_id = extract_number_from_url(full_url)

    # Open the website
    driver.get(full_url)

    # Extract product links with a try-except block
    try:
        product_links_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'form.blocks.product-card a.card-image.image-link')))
        product_links = [link.get_attribute('href') for link in product_links_elements]
    except Exception as e:
        # print("No products on:", category_url)
        continue

    # Loop through product URLs and extract product data (name, price, image URL, allergen info, price unit)
    for product_link in product_links:
        driver.get(product_link)
        id = extract_number_from_url(product_link)
        print("PRODUC: ", id)
        try:
            try:
                product_name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'header.grid-header h1.product-title')))
                product_name = product_name_element.text
            except Exception as e:
                product_name = None

            try:
                product_price_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-price strong.price.total-price')))
                product_price = product_price_element.text
            except Exception as e:
                product_price = None

            try:
                product_price_unit_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-price div.unit-price strong:last-child')))
                product_price_unit = product_price_unit_element.text
            except Exception as e:
                product_price_unit = None

            try:
                product_image_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.product-image div.contain')))
                product_image_url = product_image_element.value_of_css_property("background-image").replace('url("', '').replace('")', '')
            except Exception as e:
                product_image_url = None

            # Extract all product info if available
            try:
                product_info_elements = shortwait.until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.product-info div.item'))
                )
                description = None
                ingredients = None
                allergen_info = None

                # Loop through each item within product-info
                for product_info_element in product_info_elements:
                    # Extract title text and corresponding content using JavaScript
                    try:
                        title_element = driver.execute_script("return arguments[0].querySelector('h3').textContent.trim();", product_info_element)
                        content_element = driver.execute_script("return arguments[0].querySelector('h3 + p').textContent.trim();", product_info_element)
                    except:
                        print("no title element for:", product_name, " info data")

                    # Check if the title is Beschrijving or Ingrediënten and extract the corresponding text
                    if title_element == "Beschrijving":
                        description = content_element if content_element else None
                        # print("Description:", description)
                    elif title_element == "Ingrediënten":
                        ingredients = content_element if content_element else None
                        # print("Ingredients:", ingredients)
                    elif title_element == "Allergenen":
                        allergen_info = content_element if content_element else None
                        # print("Allergens:", allergen_info)
                    else:
                        print("unknown: " + title_element)
            except Exception as e:
                description = None
                ingredients = None
                allergen_info = None
                print("Product info error", product_name )

            product_data = {
                "Product Id": id,
                "Product Link": product_link,
                "Success": True,
                "Product Name": product_name,
                "Product Price": product_price,
                "Price Unit": product_price_unit,
                "Product Image URL": product_image_url,
                "Allergen Information": allergen_info,
                "Ingredients": ingredients,
                "Description": description,
                "Category Id": category_id
            }

            products.append(product_data)
            # print("Product Name:", product_name)
        except Exception as e:
            product_data = {
                "Product Id": id,
                "Product Link": product_link,
                "Success": False,
                "Category Id": category_id
            }
            products.append(product_data)
            print("Error occurred while extracting product data:", product_link)
        
    category_mapping[category_id] = full_url

# Add category products to the main dictionary
all_products["products"] = products
all_products["categories"] = category_mapping

# Print all product data per category
print("All Product Data:")
print(json.dumps(all_products, indent=4))

# Quit the driver
driver.quit()

output_json = json.dumps(all_products, indent=4)
with open("bakkerOutput.json", "w") as outfile:
    outfile.write(output_json)

print("Scraped data has been successfully written to 'bakkerOutput.json'.")

end_time = time.time()
execution_time = end_time - start_time
print(f"Script execution time: {execution_time:.2f} seconds")
