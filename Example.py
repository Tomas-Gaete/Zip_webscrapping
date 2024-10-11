from selenium import webdriver
from selenium.webdriver.common.by import By

# Define the URL
url = "https://www.google.com"

# Initialize the Chrome driver (adjust the executable path if needed)
driver = webdriver.Chrome()  # Or provide the path to chromedriver if not in PATH

# Open the URL
driver.get(url)

# Wait for the page to load completely (optional, useful for dynamic content)
driver.implicitly_wait(5)

# Perform a search as an example
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('Selenium Web Scraping')  # Example search
search_box.submit()

# Print the current URL after search
print(f"Current URL after search: {driver.current_url}")

# Close the browser
driver.quit()
