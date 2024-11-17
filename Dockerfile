# Usa una imagen base de Python con soporte para Selenium
FROM python:3.10-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Crea el directorio de salida en la imagen Docker
RUN mkdir -p /app/output

# Copia los archivos necesarios a la imagen
COPY . .

# Instala las dependencias necesarias para Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libxrender1 \
    --no-install-recommends && apt-get clean

# Descarga e instala Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Descarga la versión específica de Chromedriver para Linux
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.69/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip /usr/local/bin/chromedriver-linux64

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt


# Comando por defecto para ejecutar el script
CMD ["python", "Web_scrapper.py"]




