# scripts/verify_db.py
from pymongo import MongoClient
import pandas as pd

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["foodfacts_db"]
col = db["products"]

total = col.count_documents({})
print("Total documentos en products:", total)

# Mostrar un sample de 5 filas como tabla
cursor = col.aggregate([{"$sample": {"size": 5}}])
df_sample = pd.DataFrame(list(cursor))
print("\nEjemplo (5 docs):")
print(df_sample[["product_name","brands","nutriscore_grade"]].fillna("-").to_string(index=False))

# Top 10 por azúcar (si existe el campo)
top_sugar = list(col.find(
    {"nutriments.sugars_100g": {"$exists": True}},
    {"product_name":1,"nutriments.sugars_100g":1}
).sort([("nutriments.sugars_100g",-1)]).limit(10))
print("\nTop 10 productos por sugars_100g:")
for d in top_sugar:
    name = d.get("product_name") or "-"
    sugar = d.get("nutriments",{}).get("sugars_100g")
    print(f"{sugar}\t{name}")
