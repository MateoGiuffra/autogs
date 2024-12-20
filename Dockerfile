FROM python:3.10-slim-buster

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar la cache en las instalaciones
COPY requirements.txt ./requirements.txt

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
   locales-all \
   libgl1-mesa-glx \
   libglib2.0-0 \
   fonts-liberation \
   libappindicator3-1 \
   libasound2 \
   libnspr4 \
   libnss3 \
   lsb-release \
   xdg-utils \
   wget \
   unzip \
   curl \
   gnupg2 \
   libx11-xcb1 \
   libxcomposite1 \
   libxrandr2 \
   libxdamage1 \
   libgdk-pixbuf2.0-0 \
   libgbm1 \
   libvulkan1 \
# Limpiar la cache de apt para reducir el tamaño de la imagen
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/* \
# Instalar Google Chrome
   && curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb \
   && dpkg -i google-chrome-stable_current_amd64.deb \
   && apt-get -y --fix-broken install \
   && rm google-chrome-stable_current_amd64.deb \
# Instalar las dependencias de Python
   && pip install --no-cache-dir -r requirements.txt \
# Fijar la versión específica de ChromeDriver e instalar
   && CHROME_DRIVER_VERSION=114.0.5735.90 \
   && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip \
   && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
   && rm /tmp/chromedriver.zip \
   && chmod +x /usr/local/bin/chromedriver

# Copiar el resto de los archivos del proyecto al directorio de trabajo
COPY . .

# Definir las variables de entorno para el locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Exponer el puerto para que esté disponible externamente
EXPOSE 10000

# Comando para ejecutar la aplicación con Gunicorn y un timeout adecuado para Selenium
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "--timeout", "600", "application.controller.APIREST.wsgi:app"]
