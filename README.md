# Zip_webscrapping
Webscrapping to download a zipped .xlsx file and extract information.

Before following this instructions consider that this asumes you have either cloned this repository or downloaded the python file.

To make this webscraping work you can follow this instructions:

1. Make sure Python is installed and run pip install selenium

2. You need to install a browser driver for the corresponding browser, as this project was created with chrome to make this code work
you need to install a working chromedriver for your OS from this page https://googlechromelabs.github.io/chrome-for-testing/#stable (make sure you copy the corresponding url and after pasting it in the searchbox of your browser it should download a zip file)

3. With the zipfile downloaded you need to extract it on a safe directory, we recomend creating a new folder from root. For example create a folder named chromedriver and place the extracted files there. (it should be in the folder C:\chromedriver) 

4. After extracting the files you have to add the folder to the PATH as a environment variable.
    To do this you can search in your start menu (press the windows button or click the search box at the bottom of your screen) and search for environment variables, Select Edit the system environment variables. In the system properties box that just opened click on the environment variables button at the bottom, then search in system variables for Path and double click it then click on new and paste the folder that has the extracted files.

Optional: Type chromedriver on bash, cmd or any console and if you get a message like Starting ChromeDriver 91.0.4472.19 (XXXXXX) on port XXXX or chromedriver started on port XXXX  you have succesfully installed the chromedriver. If this doesn't work try rebooting

5. Open a terminal or console in the folder containing this repository or the .py file with the code for the webscraping and run it.

To run the Example.py file type this into the console: python Example.py