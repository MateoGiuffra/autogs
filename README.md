# Proyecto: Sistema de Automatización y API REST para Resúmenes

## Descripción General
Este proyecto es una combinación de automatización de tareas y una API REST que permite generar y obtener un resumen financiero a partir de un sistema externo. Utiliza herramientas modernas como Flask, Selenium y Pandas para ofrecer una solución robusta y escalable.

## Características Principales
- **Automatización Web**: Navega automáticamente por el sistema externo, ingresa credenciales, descarga reportes y procesa la información.
- **API REST**: Ofrece endpoints para interactuar con la automatización y obtener resúmenes financieros.
- **Procesamiento de Datos**: Analiza reportes descargados utilizando Pandas y extrae información relevante.

## Estructura del Proyecto
```
autogs/
├── AbsPath.py
├── application/
│   ├── APIREST/
│   │   ├── __init__.py
│   │   └── SummaryApi.py
│   │   ├── utils/
│   │       ├── CacheManager.py
│   ├── automation/
│   │   ├── DateSetter.py
│   │   ├── FileDownloader.py
│   │   ├── Login.py
│   │   ├── Report.py
│   │   └── WebDriverManager.py
│   ├── pandas/
│   │   └── ExcelReader.py
│   ├── service/
│   │   └── SummaryService.py
├── front/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           
│   │   ├── js/
│   │   │   └── scripts.css  
│   │   ├── assets/
│   ├── templates/
│   │   │   └── index.html
├── Dockerfile.py
├── Procfile.py
└── requeriments.txt
```

### Descripción de Carpetas y Archivos
- **APIREST/**: Implementa la API REST con Flask.
  - `SummaryApi.py`: Define los endpoints `/resumen` y `/obtenerResumen` para interactuar con el servicio.
- **automation/**: Contiene los scripts de automatización basados en Selenium.
  - `WebDriverManager.py`: Configura el WebDriver, navega y descarga reportes.
  - `DateSetter.py`: Establece rangos de fechas en formularios.
  - `Login.py`: Realiza el inicio de sesión en el sistema externo.
  - `Report.py`: Navega al reporte deseado dentro del sistema.
  - `FileDownloader.py`: Descarga el archivo del reporte y verifica su existencia.
- **pandas/**: Procesa los datos de los reportes descargados.
  - `ExcelReader.py`: Lee y analiza los archivos descargados para extraer el total.
- **service/**: Define la lógica del negocio.
  - `SummaryService.py`: Orquesta los pasos de automatización y procesamiento de datos.
- **AbsPath.py**: Define rutas absolutas para asegurar que los archivos se almacenen correctamente.
- **requeriments.txt**: Lista de dependencias necesarias para ejecutar el proyecto.

## Tecnologías Utilizadas
- **Flask**: Framework para construir la API REST.
- **Selenium**: Para la automatización de navegación y descargas.
- **Pandas**: Para el análisis y procesamiento de datos.
- **dotenv y decouple**: Manejo de configuraciones sensibles como credenciales y variables de entorno.

## Requisitos Previos
1. **Python 3.12+**
2. Instalación de dependencias:
   ```bash
   pip install -r requeriments.txt
   ```
3. **Google Chrome** y su correspondiente **ChromeDriver**.
4. Configurar un archivo `.env` con las credenciales:
   ```env
   DB_USER=usuario
   DB_PASSWORD=contraseña
   ```

## Cómo Ejecutar el Proyecto
1. Clona el repositorio y navega al directorio principal:
   ```bash
   git clone <url_repositorio>
   cd carpeta_raiz
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requeriments.txt
   ```
3. Ejecuta la API REST:
   ```bash
   python application/APIREST/SummaryApi.py
   ```
4. Accede a los endpoints:
   - POST `/resumen`: Envía "resumen" para obtener el total financiero.
   - GET `/obtenerResumen`: Obtiene el resumen en formato JSON.

## Ventajas del Proyecto
- **Escalabilidad**: Diseñado con una arquitectura modular para agregar nuevas funcionalidades.
- **Automatización Eficiente**: Reduce el tiempo de procesamiento de tareas repetitivas.
- **Fácil Integración**: Puede ser integrado en otros sistemas mediante la API REST.

## Posibles Mejoras
- Implementar autenticación en la API REST.
- Dockerizar el proyecto para facilitar su despliegue.
- Ampliar los casos de uso de automatización.

## Contacto
Cualquier consulta o mejora, no dudes en contactarme.


