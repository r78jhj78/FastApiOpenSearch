# import os
# import firebase_admin
# from firebase_admin import credentials, firestore
# from opensearchpy import OpenSearch

# # Variables de entorno para Railway
# FIREBASE_SERVICE_ACCOUNT = os.getenv("FIREBASE_SERVICE_ACCOUNT", "serviceAccount.json")
# OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
# OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
# OPENSEARCH_PASS = os.getenv("OPENSEARCH_PASS", "admin")

# # 1️⃣ Firebase
# cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # 2️⃣ OpenSearch
# client = OpenSearch(
#     hosts=[{"host": OPENSEARCH_HOST, "port": 9200}],
#     http_auth=(OPENSEARCH_USER, OPENSEARCH_PASS),
#     use_ssl=False
# )

# INDEX_NAME = "recipes_idx"

# # 3️⃣ Crear índice avanzado si no existe
# def create_index():
#     if not client.indices.exists(INDEX_NAME):
#         client.indices.create(
#             index=INDEX_NAME,
#             body={
#                 "settings": {
#                     "analysis": {
#                         "filter": {
#                             "spanish_stop": {"type": "stop", "stopwords": "_spanish_"},
#                             "spanish_synonym": {
#                                 "type": "synonym",
#                                 "synonyms": [
#                                     "pollo, gallina",
#                                     "maní, cacahuate, mani",
#                                     "palta, aguacate"
#                                 ]
#                             },
#                             "spanish_stemmer": {"type": "stemmer", "language": "light_spanish"}
#                         },
#                         "analyzer": {
#                             "spanish_custom": {
#                                 "tokenizer": "standard",
#                                 "filter": ["lowercase","asciifolding","spanish_stop","spanish_synonym","spanish_stemmer"]
#                             }
#                         }
#                     }
#                 },
#                 "mappings": {
#                     "properties": {
#                         "title": {"type": "text", "analyzer": "spanish_custom"},
#                         "main_ingredient": {"type": "keyword"},
#                         "ingredients": {"type": "text", "analyzer": "spanish_custom"},
#                         "instructions": {"type": "text", "analyzer": "spanish_custom"},
#                         "calories": {"type": "integer"},
#                         "portions": {"type": "integer"},
#                         "prep_time": {"type": "text"},
#                         "image_url": {"type": "keyword"}
#                     }
#                 }
#             }
#         )
#         print("✅ Índice recipes_idx creado")

# # 4️⃣ Función ETL
# def sync_recipes():
#     create_index()
#     docs = db.collection("recetas").stream()
#     count = 0
#     for doc in docs:
#         r = doc.to_dict()
#         receta_idx = {
#             "title": r.get("titulo"),
#             "main_ingredient": r.get("ingrediente_principal"),
#             "ingredients": r.get("ingredientes", []),
#             "instructions": r.get("instrucciones", ""),
#             "calories": r.get("calorias"),
#             "portions": r.get("porciones"),
#             "prep_time": r.get("preparationTime"),
#             "image_url": r.get("imagen_final_url")
#         }
#         client.index(index=INDEX_NAME, id=doc.id, body=receta_idx)
#         count += 1
#     print(f"🎉 Total recetas indexadas: {count}")
#     return count

# # 5️⃣ Función de búsqueda avanzada
# def search_recipes(query: str):
#     body = {
#         "query": {
#             "multi_match": {
#                 "query": query,
#                 "fields": [
#                     "main_ingredient^5",
#                     "title^3",
#                     "ingredients^2",
#                     "instructions"
#                 ],
#                 "operator": "or",
#                 "fuzziness": "AUTO"
#             }
#         }
#     }
#     res = client.search(index=INDEX_NAME, body=body)
#     return [hit["_source"] for hit in res["hits"]["hits"]]
import os
import firebase_admin
from firebase_admin import credentials, firestore
from opensearchpy import OpenSearch
import json

# Variables de entorno
FIREBASE_SERVICE_ACCOUNT = os.getenv("FIREBASE_SERVICE_ACCOUNT", "app/serviceAccount.json")
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASS = os.getenv("OPENSEARCH_PASS", "admin")

# Firebase
# Firebase: soporta archivo local o variable de entorno
if FIREBASE_SERVICE_ACCOUNT and os.path.exists(FIREBASE_SERVICE_ACCOUNT):
    # ✅ Usar archivo local
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
elif FIREBASE_SERVICE_ACCOUNT and FIREBASE_SERVICE_ACCOUNT.strip().startswith("{"):
    try:
        # ✅ Usar JSON en variable de entorno
        cred_dict = json.loads(FIREBASE_SERVICE_ACCOUNT)
        cred = credentials.Certificate(cred_dict)
    except Exception as e:
        raise RuntimeError("❌ FIREBASE_SERVICE_ACCOUNT parece JSON pero no se pudo parsear") from e
else:
    raise RuntimeError("❌ No se encontró serviceAccount.json ni variable FIREBASE_SERVICE_ACCOUNT")

firebase_admin.initialize_app(cred)
db = firestore.client()

# OpenSearch
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": 9200}],
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASS),
    use_ssl=False
)

INDEX_NAME = "recipes_idx"

def create_index():
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {
                    "analysis": {
                        "filter": {
                            "spanish_stop": {"type": "stop", "stopwords": "_spanish_"},
                            "spanish_synonym": {
                                "type": "synonym",
                                "synonyms": [
                                    "pollo, gallina",
                                    "maní, cacahuate, mani",
                                    "palta, aguacate"
                                ]
                            },
                            "spanish_stemmer": {"type": "stemmer", "language": "light_spanish"}
                        },
                        "analyzer": {
                            "spanish_custom": {
                                "tokenizer": "standard",
                                "filter": ["lowercase","asciifolding","spanish_stop","spanish_synonym","spanish_stemmer"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text", "analyzer": "spanish_custom"},
                        "main_ingredient": {"type": "keyword"},
                        "ingredients": {"type": "text", "analyzer": "spanish_custom"},
                        "instructions": {"type": "text", "analyzer": "spanish_custom"},
                        "calories": {"type": "integer"},
                        "portions": {"type": "integer"},
                        "prep_time": {"type": "text"},
                        "image_url": {"type": "keyword"}
                    }
                }
            }
        )
        print("✅ Índice recipes_idx creado")

def sync_recipes():
    create_index()
    docs = db.collection("recetas").stream()
    count = 0
    for doc in docs:
        r = doc.to_dict()
        receta_idx = {
            "title": r.get("titulo"),
            "main_ingredient": r.get("ingrediente_principal"),
            "ingredients": r.get("ingredientes", []),
            "instructions": r.get("instrucciones", ""),
            "calories": r.get("calorias"),
            "portions": r.get("porciones"),
            "prep_time": r.get("preparationTime"),
            "image_url": r.get("imagen_final_url")
        }
        client.index(index=INDEX_NAME, id=doc.id, body=receta_idx)
        count += 1
    print(f"🎉 Total recetas indexadas: {count}")
    return count

def search_recipes(query: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "main_ingredient^5",
                    "title^3",
                    "ingredients^2",
                    "instructions"
                ],
                "operator": "or",
                "fuzziness": "AUTO"
            }
        }
    }
    res = client.search(index=INDEX_NAME, body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]
