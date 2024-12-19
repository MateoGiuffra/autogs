# Define una variable de argumento para el puerto (puedes cambiarlo al build si es necesario)
ARG PORT=10000

# Usa una imagen base con soporte de Python (no es necesario usar una imagen de Cypress si no usas sus funcionalidades)
FROM python:3.10-slim-buster

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias primero para aprovechar la cache en las instalaciones
COPY requirements.txt ./requirements.txt

# Instala las dependencias necesarias del sistema y Python
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    unzip \
    && pip install --no-cache-dir -r requirements.txt \
    # Instalar chromedriver
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    # Agregar permisos de ejecución
    && chmod +x /usr/local/bin/chromedriver

# Copia el resto de los archivos del proyecto al directorio de trabajo
COPY . .

# Define la variable de entorno para el PATH
ENV PATH="/root/.local/bin:${PATH}"

# Expone el puerto para que esté disponible externamente
EXPOSE 10000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "application.APIREST.SummaryApi:app"]
