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
    && pip install --no-cache-dir -r requirements.txt
                                     
# Copia el resto de los archivos del proyecto al directorio de trabajo
COPY . .

# Define la variable de entorno para el PATH
ENV PATH="/root/.local/bin:${PATH}"

# Expone el puerto para que esté disponible externamente
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["uvicorn", "application.APIREST.SummaryApi:app", "--host", "0.0.0.0", "--port", "10000"]
