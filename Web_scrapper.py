import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


current_directory = os.path.dirname(os.path.abspath(__file__))
#get today's date
current_date = datetime.now()

# Set Chrome options to automatically download files to the script's directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": current_directory,  # Set to the script's directory
    "download.prompt_for_download": False,  # Disable download prompt
    "directory_upgrade": True,
    "safebrowsing.enabled": True  # Enable safe browsing
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.coordinador.cl/operacion/documentos/programas-de-operacion-2021/"

#assing respective number to months to match website dates for webscrapping

months = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# we create strings for automatic webscrapping
today = f"{current_date.day} de {months[current_date.month]}, {current_date.year}"
tomorrow_number = current_date + timedelta(days=1)
next_day= f"{tomorrow_number.day} de {months[tomorrow_number.month]}, {tomorrow_number.year}"
# Open the URL
driver.get(url)

# Wait for the page to load completely (optional, useful for dynamic content)
driver.implicitly_wait(5)

#Clicks read more button to show the download links if it isn't in the 4 top links
read_more = driver.find_element(By.CSS_SELECTOR, "#readMore_btn")
read_more.click()

#Now we set the link to start the download
try:
    xpath_next_day = f"//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), \"{next_day}\")]/following::a[contains(@href, '.zip')]"
    download_link = driver.find_element(By.XPATH, xpath_next_day)
    zip_url = download_link.get_attribute('href')
    print(f"ZIP file download URL: {zip_url}")
    print(next_day)
except NoSuchElementException:
    # If tomorrows prediction isn't available yet, we download today's prediction
    try:
        xpath_today = f"//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), \"{today}\")]/following::a[contains(@href, '.zip')]"
        download_link = driver.find_element(By.XPATH, xpath_today)
        zip_url = download_link.get_attribute('href')
        print(f"ZIP file download URL: {zip_url}")
    except NoSuchElementException:
        print("No file found for today or tommorrow.")
        print(next_day)
        print(today)
        driver.quit()
        exit() 


#start the download
download_link.click()

#wait for the download to finish before closing the browser
time.sleep(10)
# Close the browser
driver.quit()
