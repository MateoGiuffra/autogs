# Proyecto: Sistema de Automatización y API REST para Resúmenes

## Descripción General
Este proyecto es una combinación de automatización de tareas y una API REST que permite generar y obtener un resumen financiero a partir de un sistema externo. Utiliza herramientas modernas como Flask, Selenium y Pandas para ofrecer una solución robusta y escalable.

## Características Principales
- **Automatización Web**: Navega automáticamente por el sistema externo, ingresa credenciales, descarga reportes y procesa la información.
- **API REST**: Ofrece endpoints para interactuar con la automatización y obtener resúmenes financieros.
- **Procesamiento de Datos**: Analiza reportes descargados utilizando Pandas y extrae información relevante.
- **SchedulerService**: Automatiza procesos recurrentes como generación de reportes y actualización de datos mediante tareas programadas, optimizando tiempo y reduciendo intervención manual.
- **Frontend Interactivo**: Interfaz web diseñada para interactuar con los endpoints de la API. Está optimizada para dispositivos móviles, 
  permitiendo al usuario acceder fácilmente desde su celular y obtener los resúmenes financieros con facilidad

![Muestra del GIF](./front/static/assets/muestra-version-nueva.gif)


## Estructura del Proyecto
```
autogs/
├── abs_path.py
├── application/
│   ├── configuration/
│   │   └── firebase_config.py
│   ├── controller/
│   │   ├── rest/
│   │   │   ├── wsgi.py
│   │   │   └── SummaryREST.py
│   ├── models/
|   |   ├── Summary.py
│   │   ├── automation/
│   │   │   ├── date_setter/
│   │   │   │   ├── DateSetter.py 
│   │   │   │   ├── DateSetterLastMonth.py
│   │   │   │   ├── DateSetterLastMonthToday.py
│   │   │   │   └── DateSetterCurrentMonth.py
│   │   │   ├── file_downloader_module.py
│   │   │   ├── login_module.py
│   │   │   ├── report_module.py
│   │   │   └── WebDriverManager.py
│   │   ├── pandas/
│   │   └── excel_reader.py
│   ├── service/
│   │   ├── SchedulerService.py
│   │   └── SummaryService.py
│   ├── persistence/
│   │   └── SummaryDAO.py
├── front/
│   ├── static/
│   │   ├── css/
│   │   │   └── mystyle.css           
│   │   ├── js/
│   │   │   └── scripts.css  
│   │   ├── assets/
│   ├── templates/
│   │   │   └── index.html
├── Dockerfile.py
└── requirements.txt
```


### Descripción de Carpetas y Archivos
- **configuration/**: Configuracion de la base de datos.
  - `firebase_config.py`: Encargado de leer las credenciales para inicializar la app de firebase y crear una instancia de firestore.  
- **controller/**: Implementa la API REST con Flask.
  - `SummaryApi.py`: Define los endpoints `/diferenciaResumenes`,  `/diferenciaResumenesHoy` y `/obtenerResumen` para interactuar con el servicio.
- **models/**: Contiene el modelo del proyecto. En el se encuentra el objeto Summary el cual almacena la informacion de los reportes, las carpetas automation y pandas. 
- **automation/**: Contiene los scripts de automatización basados en Selenium.
  - `WebDriverManager.py`: Trabaja como Orquestador usando el resto de las clases. Configura el WebDriver, navega y descarga reportes.
  - `DateSetter.py`: Establece rangos de fechas en formularios dependiendo lo requerido.
  - `login_module.py`: Realiza el inicio de sesión en el sistema externo.
  - `report_module.py`: Navega al reporte deseado dentro del sistema.
  - `file_downloader_module.py`: Descarga el archivo del reporte y verifica su existencia.
  - `Summary.py`: Define la lógica del negocio. Orquesta los pasos de automatización y procesamiento de datos. Almacena los datos de valor.  
- **pandas/**: Procesa los datos del reporte descargado.
  - `ExcelReader.py`: Lee y analiza el archivo descargado para extraer el total. Se maneja de forma eficiente borrando al anterior 
    para ahorrar espacio en memoria y recursos.
- **service/**: Se encarga de interactuar con el modelo y la capa de persistencia.
  - `SummaryService.py`: Interviene como intermediario entre el negocio y la persistencia de datos para asegurar consistencia en los datos.
  - `SchedulerService.py`: Implementacion de APScheduler para ejecutar registro de reportes en dias y horarios especificos. Especificamente, obtiene el resumen de este mismo dia pero de un mes atras cada dia que pasa y el resumen total del mes pasado cada vez que cambia el mes.  
- **persistencia/**: Se encarga de interactuar con la base de datos (firestore).
  - `SummaryDAO.py`: Crea y actualiza instancias de Summary con lo suficiente para asegurar su correcto funcionamiento.
- **abs_path.py**: Define rutas absolutas para asegura que el archivo se almacene correctamente.
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
   DB_KEY=key de firebase (tiene que estar en una sola linea)
   TIMEZONE=declaras la zona horaria de tu preferencia, por defecto esta la de BsAs 
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
   - PUT `/resumenDelMesPasado`: Actualizar el monto obtenido en todo el mes anterior y en la pagina se muestra su diferencia con el resumen actual en forma de porcentaje. 
     -- ``Ejemplo``: Suponiendo que hoy es 26/12/2024, entonces la resta es entre el resumen del 30/11/2024 y del 26/12/2024 
   - PUT `/resumenDeUnMesAtras`: Actualizar el monto obtenido este mismo dia pero de un mes anterior y en la pagina se muestra su diferencia con el resumen actual en forma de porcentaje.
     -- ``Ejemplo``: La resta es entre el resumen del 26/11/2024 y del 26/12/2024
   - PUT `/resumenActual`: Actualiza los datos obteniendo el resumen del dia actual, fecha con hora de cuando se solicito por ult vez el resumen y la diferencia con el total anteriormente pedido.

## Ventajas del Proyecto
- **Escalabilidad**: Diseñado con una arquitectura modular para agregar nuevas funcionalidades.
- **Automatización Eficiente**: Reduce significativamente el tiempo empleado en tareas repetitivas, aumentando la productividad.
- **Fácil Integración**: Puede ser integrado en otros sistemas mediante la API REST.
- **Eficiencia**: Optimizado para consumir únicamente los recursos necesarios, garantizando un desempeño eficiente.
- **Consistencia de Datos**: Utiliza Firestore como base de datos, asegurando la consistencia, alta disponibilidad y escalabilidad de los datos en tiempo real.

## Deploy
- El proyecto ya esta listo para el deploy a traves del Dockerfile.
-  *¿Donde y como hacerlo?*
  - Primero carga la variables de entorno de USER, PASSWORD y DB_KEY.    
  - Render: Carga la variable de entorno PORT con 10000
  - Railway: no hagas nada mas.  

## Contacto
Cualquier consulta o mejora, no dudes en contactarme: matteogiuffrah40@gmail.com


