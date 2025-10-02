# OpenFood Facts — Dashboard (MongoDB + Jupyter + Plotly)

## Resumen
Proyecto que descarga y almacena productos de Open Food Facts en MongoDB y ofrece un notebook interactivo para explorar nutrientes y etiquetas. La URL de la API del dataset es https://world.openfoodfacts.org/cgi/search.pl

## Requisitos
- Python 3.10+
- Docker (opcional para MongoDB) o MongoDB local / Atlas
- jq (opcional, para procesar dumps grandes)

## Instalación rápida
1. Clonar el repo:
   ```bash
   git clone https://github.com/florenciahendel/tp2_pa_open_food_dataset.git
   cd tp2_pa_open_food_dataset

### Configuración en Windows

1. Crear venv e instalar dependencias. Correr los siguientes comandos en la consola, posicionados en la carpeta raíz del proyecto:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate.bat
   pip install -r requirements.txt

2. Levantar Mongo DB (opción Docker):
   ```bash
   docker run --name mongo-foodfacts -p 27017:27017 -d mongo:6.0

3. Levantar MongoDB (opción local):  
   - Asegurarse de que la ruta de MongoDB esté agregada al path.  
   - Crear el archivo _.env_ (usar el _.env.example_ agregado en el proyecto como guía).  
   - Verificar que exista la carpeta ```C:\data\db```; si no existe, crearla.  
   La base se va a crear al momento de correr la notebook.  


### Configuración en MacOS / Linux

1. Crear venv e instalar dependencias. Correr los siguientes comandos en la consola, posicionados en la carpeta raíz del proyecto:
   ```bash
   python -m venv venv
   source venv\bin\activate
   pip install -r requirements.txt

2. Levantar Mongo DB (opción Docker):
   ```bash
   docker run --name mongo-foodfacts -p 27017:27017 -d mongo:6.0

3. Levantar MongoDB local:  
   - Instalar MongoDB con Homebrew:
      ```bash
      brew tap mongodb/brew
      brew install mongodb-community@6.0

   - Iniciar el servicio:
      ```bash
      brew services start mongodb-community@6.0

   - Crear el archivo _.env_ (usar el _.env.example_ agregado en el proyecto como guía).
   - En macOS/Linux Mongo usa ```/usr/local/var/mongodb```.
   - No es necesario crear ```C:\data\db```.


### Ejecución del dashboard:  
1. Abrir el notebook ```dashboard.ipynb```
   ```Bash
      jupyter notebook dashboard.ipynb
2. Ejecutar el dashboard:
- Se puede ejecutar todo el dashboard de una vez (Con la opción _Run All_), o 
- celda por celda (Haciendo click en el botón de _Play_ al lado de cada celda).  
- Siempre ejecutar la primera celda, porque es la que realiza los imports y la conexión a la DB.