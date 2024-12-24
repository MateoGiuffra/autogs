# Proyecto: Sistema de Automatización y API REST para Resúmenes

## Descripción General
Este proyecto es una combinación de automatización de tareas y una API REST que permite generar y obtener un resumen financiero a partir de un sistema externo. Utiliza herramientas modernas como Flask, Selenium y Pandas para ofrecer una solución robusta y escalable.

## Características Principales
- **Automatización Web**: Navega automáticamente por el sistema externo, ingresa credenciales, descarga reportes y procesa la información.
- **API REST**: Ofrece endpoints para interactuar con la automatización y obtener resúmenes financieros.
- **Procesamiento de Datos**: Analiza reportes descargados utilizando Pandas y extrae información relevante.
- **Frontend Interactivo**: Interfaz web diseñada para interactuar con los endpoints de la API. Está optimizada para dispositivos móviles, 
  permitiendo al usuario acceder fácilmente desde su celular y obtener los resúmenes financieros con facilidad

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
└── requirements.txt
```

### Descripción de Carpetas y Archivos
- **controller/**: Implementa la API REST con Flask.
  - `SummaryApi.py`: Define los endpoints `/diferenciaResumenes` y `/obtenerResumen` para interactuar con el servicio.
  - `CacheManager.py`: Mini implementacion de cache para no saturar endpoints en un periodo de tiempo definido (en este caso 10 minutos).
- **automation/**: Contiene los scripts de automatización basados en Selenium.
  - `WebDriverManager.py`: Trabaja como Orquestador usando el resto de las clases. Configura el WebDriver, navega y descarga reportes.
  - `DateSetter.py`: Establece rangos de fechas en formularios dependiendo lo requerido.
  - `Login.py`: Realiza el inicio de sesión en el sistema externo.
  - `Report.py`: Navega al reporte deseado dentro del sistema.
  - `FileDownloader.py`: Descarga el archivo del reporte y verifica su existencia.
- **pandas/**: Procesa los datos del reporte descargado.
  - `ExcelReader.py`: Lee y analiza el archivo descargado para extraer el total. Se maneja de forma eficiente borrando al anterior 
    para ahorrar espacio en memoria y recursos.
- **service/**: Define la lógica del negocio.
  - `SummaryService.py`: Orquesta los pasos de automatización y procesamiento de datos.
- **AbsPath.py**: Define rutas absolutas para asegura que el archivo se almacene correctamente.
- **requeriments.txt**: Lista de dependencias necesarias para ejecutar el proyecto.
- **Dockerfile**: Archivo de Docker preparado para que todo funcione correctamente en produccion. 
- **front/**: Un mini front para interactuar con la aplicación. Hecho solo con CSS, HTML y JavaScript para que la app sea lo menos pesado y eficiente.

## Tecnologías Utilizadas
- **Flask**: Framework para construir la API REST.
- **Selenium**: Para la automatización de navegación y descargas.
- **Pandas**: Para el análisis y procesamiento de datos.
- **dotenv y decouple**: Manejo de configuraciones sensibles como credenciales y variables de entorno.

## Requisitos Previos
1. **Python 3.12+**
2. Instalación de dependencias:
   ```bash
   pip install -r requirements.txt
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
   pip install -r requirements.txt
   ```
3. Ejecuta la API REST:
   ```bash
   python -m application.controller.APIREST.SummaryApi
   ```
4. Accede a los endpoints:
   - GET `/diferenciaResumenes`: Devuelve en formato JSON el resumen del mes anterior y el diferencial con el resumen actual
   - GET `/obtenerResumen`: Devuelve el resumen del dia actual en formato JSON.

## Ventajas del Proyecto
- **Escalabilidad**: Diseñado con una arquitectura modular para agregar nuevas funcionalidades.
- **Automatización Eficiente**: Reduce el tiempo de procesamiento de tareas repetitivas.
- **Fácil Integración**: Puede ser integrado en otros sistemas mediante la API REST.
- **Eficiencia**: Busca ser lo mas optimazado posible, consumiendo lo minimo e indispensable.  

## Deploy
- El proyecto ya esta listo para el deploy a traves del Dockerfile. 
Especificamente listo para Render ya que esta escuchando en el puerto 10000, pero podes cambiarlo segun tus necesidades.

## Contacto
Cualquier consulta o mejora, no dudes en contactarme: matteogiuffrah40@gmail.com


