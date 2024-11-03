import os
import zipfile
import glob
import time
import pandas as pd
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

#Now we set the date number for the file name format (YYMMDD having only 2 digits for the year)
today_file_number = f"{current_date.year-2000}{current_date.month:02}{current_date.day:02}"
tomorrow_file_number = f"{tomorrow_number.year-2000}{tomorrow_number.month:02}{tomorrow_number.day:02}"

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
    file_name = 'PRG'+f'{tomorrow_file_number}'+'.xlsx'
    Report = f"{next_day}"
except NoSuchElementException:
    # If tomorrows prediction isn't available yet, we download today's prediction
    try:
        xpath_today = f"//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), \"{today}\")]/following::a[contains(@href, '.zip')]"
        download_link = driver.find_element(By.XPATH, xpath_today)
        zip_url = download_link.get_attribute('href')
        file_name = 'PRG'+f'{today_file_number}'+'.xlsx'
        Report = f"{today}"
    except NoSuchElementException:
        print("No file found for today or tommorrow.")
        driver.quit()
        exit() 


#start the download
download_link.click()

#wait for the download to finish before closing the browser
time.sleep(6)
# Close the browser
driver.quit()

#Now we extract the latest downloaded file wich is the desired zip file
list_of_files = glob.glob(os.path.join(os.getcwd(), "*.zip"))
latest_file = max(list_of_files, key=os.path.getctime)

with zipfile.ZipFile(latest_file, 'r') as zip_ref:
    zip_ref.extractall(os.getcwd())
    print("Extraction complete.")
print(f"Extracted files are located in: {os.getcwd()}")

#Now use pandas to access the extracted file that is relevant to us

file_path = os.path.join(os.getcwd(), file_name)

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    found = False
    for i in range(1, 10):
        file_name = 'PRG' + f'{tomorrow_file_number}-{i}' + '.xlsx'
        file_path = os.path.join(os.getcwd(), file_name)
        try:
            df = pd.read_excel(file_path)
            found = True
            break
        except FileNotFoundError:
            continue
    if not found:
        for i in range(1, 10):
            file_name = f'PRG{today_file_number}-{i}.xlsx'
            file_path = os.path.join(os.getcwd(), file_name)
            try:
                df = pd.read_excel(file_path)
                found = True
                break
            except FileNotFoundError:
                continue  # Continue to the next alternative file name

    # If no file is found after all attempts, print an error and exit
    if not found:
        print("All alternative file names for today and tomorrow were not found. Exiting the program.")
        exit()

df.columns = [f"Column{i}" for i in range(len(df.columns))]

specific_row = df[df['Column3'] == 'CNavia220']

if not specific_row.empty:
    cost = specific_row['Column28'].values[0]
    print(f"El costo marginal promedio de cerronavia es: {cost}")
    with open(f"Reporte{Report}.txt", "w") as file:
        file.write(f"Los Costos marginales para cerro Navia serán los siguientes:\n\n\n")
        for i in range(4, 28):
            value = specific_row.iloc[0, i]
            file.write(f"El costo de la hora {i-3} para la central será: {value}\n\n")
        file.write(f"Finalmente, el costo marginal promedio de cerro Navia es: {cost}\n\n\n")
        file.write(f"====================================================================================================\n\n\n")
else:
    print("No data found for the specified condition.")

print("")
print("")
desired_data = input("Ingrese el nombre de la central que desea consultar: ")
desired_row = df[df['Column3'] == desired_data]
#print(desired_row)
print("")
if not desired_row.empty:
    cmg = desired_row['Column28'].values[0]
    print(f"El costo marginal promedio de la central especificada es: {cmg}")
    print("")
    with open(f"Reporte{Report}.txt", "a") as file:
        file.write(f"Los Costos marginales para la central {desired_data} serán los siguientes:\n\n\n")
        for i in range(4, 28):
            value = desired_row.iloc[0, i]  
            #print(f"El costo de la hora {i-3} para la central será: {value}")
            #print("")
            file.write(f"El costo de la hora {i-3} para la central será: {value}\n\n")
        file.write(f"Finalmente, el costo marginal promedio de la central especificada es: {cmg}")
else:
    print("No se encontro data de la central especificada, asegurese de haber ingresado el nombre correcto.")