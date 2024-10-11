from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Define the URL
#url = "https://www.coordinador.cl/"
url = "https://www.coordinador.cl/operacion/documentos/programas-de-operacion-2021/"
# Initialize the Chrome driver (adjust the executable path if needed)
driver = webdriver.Chrome()  # Or provide the path to chromedriver if not in PATH

# Open the URL
driver.get(url)

# Wait for the page to load completely (optional, useful for dynamic content)
driver.implicitly_wait(5)

date = "11 de Octubre, 2024"
read_more = driver.find_element(By.CSS_SELECTOR, "#readMore_btn")
read_more.click()
#Gets download link for zip file
download_link = driver.find_element(By.XPATH, "//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), '11 de Octubre, 2024')]/following::a[contains(@href, '.zip')]")
zip_url = download_link.get_attribute('href')
print(f"ZIP file download URL: {zip_url}")


#start the download
download_link.click()

#wait for the download to finish before closing the browser
time.sleep(10)
# Close the browser
driver.quit()
