from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://www.bakkerijemmerick.be/nl/shop/pistolets")

try:
    # Wait for the "Afhalen" button to be clickable (maximum wait time is 10 seconds)
    afhalen_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.takeaway[data-beko-action="setTakeaway"]'))
    )

    # Click the "Afhalen" button
    afhalen_button.click()

    # Rest of your automation script
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.price'))
    )
    price = price_element.text if price_element else "Price not found"

    # Print the price
    print("Price:", price)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the browser window
    driver.quit()