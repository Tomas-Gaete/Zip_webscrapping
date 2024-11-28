import os
import zipfile
import glob
import time
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service  # Import the Service class


current_directory = os.path.dirname(os.path.abspath(__file__))

#get today's date
current_date = datetime.now()
# Set Chrome options to automatically download files to the script's directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": current_directory,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")

# Automatically manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = "https://www.coordinador.cl/operacion/documentos/programas-de-operacion-2021/"

#assing respective number to months to match website dates for webscrapping

months = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# we create strings for automatic webscrapping
today = f"{current_date.day} de {months[current_date.month]}, {current_date.year}"
today_excel = f"{current_date.day}_de_{months[current_date.month]}_{current_date.year}"
tomorrow_number = current_date + timedelta(days=1)
next_day= f"{tomorrow_number.day} de {months[tomorrow_number.month]}, {tomorrow_number.year}"
next_day_excel= f"{tomorrow_number.day}_de_{months[tomorrow_number.month]}_{tomorrow_number.year}"


#Now we set the date number for the file name format (YYMMDD having only 2 digits for the year)
today_file_number = f"{current_date.year-2000}{current_date.month:02}{current_date.day:02}"
tomorrow_file_number = f"{tomorrow_number.year-2000}{tomorrow_number.month:02}{tomorrow_number.day:02}"

# Open the URL
driver.get(url)

# Wait for the page to load completely (optional, useful for dynamic content)
time.sleep(10)
#Clicks read more button to show the download links if it isn't in the 4 top links
read_more = driver.find_element(By.CSS_SELECTOR, "#readMore_btn")
read_more.click()
time.sleep(10)

#Now we set the link to start the download
try:
    xpath_next_day = f"//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), \"{next_day}\")]/following::a[contains(@href, '.zip')]"
    download_link = driver.find_element(By.XPATH, xpath_next_day)
    zip_url = download_link.get_attribute('href')
    file_name = 'PRG'+f'{tomorrow_file_number}'+'.xlsx'
    Report = f"{next_day}"
    Report_excel = f"{next_day_excel}"
except NoSuchElementException:
    # If tomorrows prediction isn't available yet, we download today's prediction
    try:
        xpath_today = f"//span[contains(text(), 'Programa de Operación y Lista de Prioridades')]/following::span[contains(text(), \"{today}\")]/following::a[contains(@href, '.zip')]"
        download_link = driver.find_element(By.XPATH, xpath_today)
        zip_url = download_link.get_attribute('href')
        file_name = 'PRG'+f'{today_file_number}'+'.xlsx'
        Report = f"{today}"
        Report_excel = f"{today_excel}"
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

class PDFReport(FPDF):
    def header(self):
        self.set_font("Times", "B", 12)
        self.cell(0, 10, f"Reporte: {Report}", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

def add_central_data_to_pdf(pdf, central_name, data_row):
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 10, f"Central: {central_name}", 0, 1)
    pdf.ln(5)

    pdf.set_font("Times", "", 10)
    for i in range(4, 28):
        value = data_row.iloc[0, i]
        pdf.cell(0, 10, f"El costo de la hora {i-3} para la central será: {value}", 0, 1)
    
    average_cost = data_row['Hora 24'].values[0]
    pdf.ln(5)
    pdf.set_font("Times", "B", 10)
    pdf.cell(0, 10, f"El costo marginal promedio de {central_name} es: {average_cost}", 0, 1)
    pdf.ln(10)
#Now we extract the latest downloaded file wich is the desired zip file
list_of_files = glob.glob(os.path.join(os.getcwd(), "*.zip"))
latest_file = max(list_of_files, key=os.path.getctime)
with zipfile.ZipFile(latest_file, 'r') as zip_ref:
    zip_ref.extractall(os.getcwd())
    print("Extraction complete.")
print(f"Extracted files are located in: {os.getcwd()}")
#save extracted excel file paths to delete later
extracted_files = [os.path.join(os.getcwd(), name) for name in zip_ref.namelist()]

#if zip file still exists delete it
if os.path.exists(latest_file):
    os.remove(latest_file)
    print(f"Deleted ZIP file: {latest_file}")

pdf = PDFReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
current_directory = os.path.dirname(os.path.abspath(__file__))
pdf.set_font("Times", "B", 16)
pdf.cell(0, 10, "Reporte de Costos Marginales", 0, 1, "C")
pdf.ln(10)

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

df.rename(columns={"Column3": "Central"}, inplace=True)
df.rename(columns={"Column28": "Promedio Cmg"}, inplace=True)

hour_columns = {f"Column{i}": f"Hora {i-3}" for i in range(4, 28)}

df.rename(columns=hour_columns, inplace=True)

selected_rows = pd.DataFrame()
specific_row = df[df['Central'] == 'CNavia220']

if not specific_row.empty:
    cost = specific_row['Promedio Cmg'].values[0]
    selected_rows = pd.concat([selected_rows, specific_row.iloc[:, 3:29]])
    print(f"El costo marginal promedio de cerronavia es: {cost}")
    add_central_data_to_pdf(pdf, "Cerro Navia", specific_row)
else:
    print("No data found for the specified condition.")

print("")
print("")
#desired_data = input("Ingrese el nombre de la central que desea consultar: ")
#desired_row = df[df['Central'] == desired_data]
#print(desired_row)
#print("")
#if not desired_row.empty:
#    cmg = desired_row['Promedio Cmg'].values[0]
#    selected_rows = pd.concat([selected_rows, desired_row.iloc[:, 3:29]])
#    print(f"El costo marginal promedio de la central especificada es: {cmg}")
#    add_central_data_to_pdf(pdf, desired_data, desired_row)
#    print("")
#else:
#    print("No se encontro data de la central especificada, asegurese de haber ingresado el nombre correcto.")

pdf_file_name = f"Reporte {Report}.pdf"
pdf.output(pdf_file_name)

# Ahora transponemos la data para tener 1 columna por central
df_T = selected_rows.T
row_titles = ["Datos"]  # Título inicial
row_titles += [f"Hora {i}" for i in range(1, 25)]  # Agregar "Hora 1" a "Hora 24"
row_titles.append("Costo Marginal Promedio")#Genera los informes
df_T.rename(columns=df.iloc[0], inplace = True)

df_T.insert(0, "Centrales", row_titles)
# Crear un directorio de salida
output_directory = os.path.join(current_directory, "output")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define el nombre del archivo Excel en el directorio de salida
excel_file_name = os.path.join(output_directory, f"Costos_Marginales_{Report_excel}.xlsx")
df_T.to_excel(excel_file_name, index=False)
print(f"Data exported to {excel_file_name}")

#Borra los archivos extraídos
for file in extracted_files:
    if os.path.exists(file):
        os.remove(file)