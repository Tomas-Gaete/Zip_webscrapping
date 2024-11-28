FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl xvfb libxi6 libgconf-2-4 libnss3 libasound2 fonts-liberation libappindicator3-1 xdg-utils gpg \
    && apt-get clean

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip /usr/local/bin/chromedriver-linux64

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Copy the application
COPY . /app

# Default command to run the script
CMD ["xvfb-run", "-a", "python", "Web_scrapper.py"]
