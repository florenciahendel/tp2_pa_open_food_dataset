# OpenFood Facts — Dashboard (MongoDB + Jupyter + Plotly)

## Resumen
Proyecto que descarga y almacena productos de Open Food Facts en MongoDB y ofrece un notebook interactivo para explorar nutrientes y etiquetas.

## Requisitos
- Python 3.10+
- Docker (opcional para MongoDB) o MongoDB local / Atlas
- jq (opcional, para procesar dumps grandes)

## Instalación rápida
1. Clonar:
   ```bash
   git clone https://github.com/TU_USUARIO/tp2_pa_open_food_dataset.git
   cd tp2_pa_open_food_dataset

2. Crear venv e instalar dependencias. Correr los siguientes comandos en la consola, posicionados en la carpeta raíz del proyecto:
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt

3. Levantar Mongo DB (opción Docker):
docker run --name mongo-foodfacts -p 27017:27017 -d mongo:6.0

4. Levantar MongoDB (opción local):
Asegurarse de que la ruta de MongoDB esté agregada al path. Verificar que exista la carpeta C:\data\db; si no existe, crearla. La base se va a crear al momento de correr la notebook
