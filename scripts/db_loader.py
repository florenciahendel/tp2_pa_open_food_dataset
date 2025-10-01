#!/usr/bin/env python3
"""
db_loader.py
Modo de uso:
  # modo rápido usando la API (para pruebas)
  python scripts/db_loader.py --mode api --pages 2 --page_size 1000

  # modo dump (archivo gzip newline-delimited json)
  python scripts/db_loader.py --mode dump --file data/products_lines.json.gz --batch 500
"""
import os
import sys
import json
import gzip
import argparse
from pymongo import MongoClient, UpdateOne
import requests
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # lee .env si existe

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLL_NAME = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coll = db[COLL_NAME]


def normalize_product(d):
    #Extrae y normaliza campos útiles del JSON de Open Food Facts.
    if not isinstance(d, dict):
        return None
    out = {}
    # usar 'code' como _id si existe (código de barra)
    code = d.get("code") or d.get("_id")
    if code:
        out["_id"] = str(code)
    out["product_name"] = d.get("product_name") or d.get("product_name_en") or d.get("product_name_fr")
    out["brands"] = d.get("brands")
    out["categories_tags"] = d.get("categories_tags") or d.get("categories")
    out["countries_tags"] = d.get("countries_tags") or d.get("countries")
    # nutriments: limpia keys (reemplaza '-' por '_')
    nut = d.get("nutriments") or {}
    nut_norm = {}
    for k, v in nut.items():
        nk = k.replace("-", "_").replace(" ", "_")
        try:
            if v is None:
                continue
            if isinstance(v, (int, float)):
                nut_norm[nk] = v
            else:
                # intentar convertir strings numéricos
                try:
                    nut_norm[nk] = float(v)
                except Exception:
                    nut_norm[nk] = v
        except Exception:
            continue
    if nut_norm:
        out["nutriments"] = nut_norm
    out["nutriscore_grade"] = d.get("nutriscore_grade")
    out["labels_tags"] = d.get("labels_tags") or d.get("labels")
    out["ingredients_text"] = d.get("ingredients_text")
    return out


def bulk_upsert(docs):
    ops = []
    for d in docs:
        nd = normalize_product(d)
        if not nd:
            continue
        if "_id" in nd:
            ops.append(UpdateOne({"_id": nd["_id"]}, {"$set": nd}, upsert=True))
        else:
            # si no hay _id, upsert por name+brands (rústico)
            filter_q = {"product_name": nd.get("product_name"), "brands": nd.get("brands")}
            ops.append(UpdateOne(filter_q, {"$setOnInsert": nd}, upsert=True))
    if not ops:
        return None
    res = coll.bulk_write(ops, ordered=False)
    return res


def load_from_api(pages=1, page_size=1000, batch_size=500):
    base = "https://world.openfoodfacts.org/cgi/search.pl"
    for p in range(1, pages + 1):
        params = {"search_simple": 1, "action": "process", "json": 1, "page_size": page_size, "page": p}
        r = requests.get(base, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        prods = data.get("products", [])
        print(f"Página {p} -> {len(prods)} productos")
        batch = []
        for prod in prods:
            batch.append(prod)
            if len(batch) >= batch_size:
                bulk_upsert(batch)
                batch = []
        if batch:
            bulk_upsert(batch)


def load_from_dump(file_path, batch_size=500):
    # detecta si es newline-delimited JSON o un array JSON
    with gzip.open(file_path, "rt", encoding="utf-8") as fh:
        sample = fh.read(2048)
    if sample.lstrip().startswith("["):
        print("El archivo parece ser un array JSON. Recomiendo convertirlo a newline-delimited JSON con:")
        print("  jq -c '.[]' products.json > products_lines.json")
        print("Comprimilo y ejecutá: gzip products_lines.json")
        sys.exit(1)
    # si no empieza con [, asumimos newline-delimited JSON (una linea = 1 objeto)
    with gzip.open(file_path, "rt", encoding="utf-8") as fh:
        batch = []
        for line in tqdm(fh, desc="Leyendo dump"):
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
            except json.JSONDecodeError:
                continue
            batch.append(doc)
            if len(batch) >= batch_size:
                bulk_upsert(batch)
                batch = []
        if batch:
            bulk_upsert(batch)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["api", "dump"], default="api", help="api (prueba) o dump (archivo .json.gz)")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--page_size", type=int, default=1000)
    parser.add_argument("--file", type=str, help="ruta al .json.gz (modo dump)")
    parser.add_argument("--batch", type=int, default=500)
    args = parser.parse_args()

    print("Conectando a MongoDB:", MONGO_URI)
    print("DB:", DB_NAME, "Colección:", COLL_NAME)

    if args.mode == "api":
        load_from_api(pages=args.pages, page_size=args.page_size, batch_size=args.batch)
    else:
        if not args.file:
            parser.error("--file es obligatorio en modo dump")
        load_from_dump(args.file, batch_size=args.batch)

if __name__ == "__main__":
    main()
