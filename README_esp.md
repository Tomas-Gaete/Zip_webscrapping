# Zip_webscrapping
Webscraping para descargar un archivo .xlsx comprimido y extraer información del coordinador nacional de electricidad de Chile.

Antes de seguir estas instrucciones, considere que esto asume que ha clonado este repositorio o descargado el archivo de Python.

Para que este webscraping funcione, puede seguir estas instrucciones:

1. Después de clonar o descargar el repositorio, asegúrese de que Python esté instalado y ejecute `pip install -r requirements.txt` para descargar todas las dependencias.

2. Necesita instalar un controlador de navegador para el navegador correspondiente. Como este proyecto se creó con Chrome, para que este código funcione, debe instalar un chromedriver compatible con su sistema operativo desde esta página: https://googlechromelabs.github.io/chrome-for-testing/#stable (asegúrese de copiar la URL correspondiente y, después de pegarla en el cuadro de búsqueda de su navegador, debería descargar un archivo zip).

3. Con el archivo zip descargado, debe extraerlo en un directorio seguro. Recomendamos crear una nueva carpeta desde la raíz. Por ejemplo, cree una carpeta llamada `chromedriver` y coloque los archivos extraídos allí (debería estar en la carpeta `C:\chromedriver`).

4. Después de extraer los archivos, debe agregar la carpeta al PATH como una variable de entorno.
    Para hacer esto, puede buscar en su menú de inicio (presione el botón de Windows o haga clic en el cuadro de búsqueda en la parte inferior de su pantalla) y busque variables de entorno. Seleccione Editar las variables de entorno del sistema. En el cuadro de propiedades del sistema que se acaba de abrir, haga clic en el botón de variables de entorno en la parte inferior, luego busque en variables del sistema la variable Path y haga doble clic en ella, luego haga clic en nuevo y pegue la carpeta que tiene los archivos extraídos.

Opcional: Escriba `chromedriver` en bash, cmd o cualquier consola y si obtiene un mensaje como Starting ChromeDriver 91.0.4472.19 (XXXXXX) on port XXXX o chromedriver started on port XXXX, ha instalado correctamente el chromedriver. Si esto no funciona, intente reiniciar.

5. Abra una terminal o consola en la carpeta que contiene este repositorio o el archivo .py con el código para el webscraping y ejecútelo.

Para ejecutar el archivo `Web_scrapper.py`, escriba esto en la consola: `python Web_scrapper.py`.

Después de ejecutar el código, debería terminar con los archivos de Excel extraídos y un informe correspondiente a la fecha de los costos previstos.
