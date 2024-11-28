# Zip_webscrapping
Webscrapping to download a zipped .xlsx file and extract information from chilean national electricity coordinator.

Before following this instructions consider that this asumes you have either cloned this repository or downloaded the python file.

To make this webscraping work you can follow this instructions:

1. After cloning or downloading the repository, make sure Python is installed and run `pip install -r requirements.txt` to download all dependencies

2. You need to install a browser driver for the corresponding browser, as this project was created with chrome to make this code work
you need to install a working chromedriver for your OS from this page https://googlechromelabs.github.io/chrome-for-testing/#stable (make sure you copy the corresponding url and after pasting it in the searchbox of your browser it should download a zip file)

3. With the zipfile downloaded you need to extract it on a safe directory, we recomend creating a new folder from root. For example create a folder named `chromedriver` and place the extracted files there. (it should be in the folder `C:\chromedriver`) 

4. After extracting the files you have to add the folder to the PATH as a environment variable.
    To do this you can search in your start menu (press the windows button or click the search box at the bottom of your screen) and search for environment variables, Select Edit the system environment variables. In the system properties box that just opened click on the environment variables button at the bottom, then search in system variables for Path and double click it then click on new and paste the folder that has the extracted files.

Optional: Type `chromedriver` on bash, cmd or any console and if you get a message like Starting ChromeDriver 91.0.4472.19 (XXXXXX) on port XXXX or chromedriver started on port XXXX  you have succesfully installed the chromedriver. If this doesn't work try rebooting

5. Open a terminal or console in the folder containing this repository or the .py file with the code for the webscraping and run it.

To run the `Web_scrapper.py` file type this into the console: `python Web_scrapper.py`

After the code has been run you should end up with the extracted excel files and a report corresponding to the date of the predicted costs.

## Using Docker

If you prefer to run the program with Docker, follow these steps:

### 1. Install Docker Desktop
- Download and install Docker Desktop from [this page](https://www.docker.com/products/docker-desktop/).
- Follow the installation instructions for your operating system.
- After installation, ensure Docker is running.

### 2. Pull the Docker Image
- Open a terminal and run:
  docker pull aliturriaga/web-scraper:latest
### 3. Run the Image
Open Docker Desktop.
Go to the "Images" tab and find aliturriaga/web-scraper:latest.
Click on Run.
### 4. Configure Volumes
When running the container, configure the volume to save the Excel files:
Host Path: Select the folder on your machine where you want the Excel files to be saved (e.g., C:\Users\YourUser\Downloads\output).
Container Path: Set this to /app/output.
### 5. Check the Results
After the container finishes running, the Excel files and reports will be saved in the folder you selected as the Host Path.