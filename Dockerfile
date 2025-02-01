FROM python:3.10-slim-buster

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Configurar la zona horaria de Argentina
ENV TZ=America/Argentina/Buenos_Aires

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    tzdata \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -y --fix-broken install \
    && rm google-chrome-stable_current_amd64.deb

# Copiar el archivo de dependencias e instalar las dependencias de Python
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la carpeta drivers con el ChromeDriver
COPY drivers /app/drivers

# Dar permisos de ejecución al ChromeDriver (solo para Linux/macOS)
RUN chmod +x /app/drivers/chromedriver

# Copiar el resto de los archivos del proyecto al directorio de trabajo
COPY . .

# Definir las variables de entorno para el locale
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Exponer el puerto para Docker (opcional, no afecta Railway)
EXPOSE 10000

# Comando para ejecutar la aplicación con Gunicorn usando $PORT
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} --timeout 1200 --access-logfile '-' --error-logfile '-' application.controller.rest.wsgi:app"]