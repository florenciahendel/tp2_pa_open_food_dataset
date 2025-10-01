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
   git clone https://github.com/TU_USUARIO/tp2_pa_open_food_facts_dataset.git
   cd tp2_pa_open_food_facts_dataset

2. Crear venv e instalar:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Levantar Mongo DB (opción Docker):
docker run --name mongo-foodfacts -p 27017:27017 -d mongo:6.0

