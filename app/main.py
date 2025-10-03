# import os
# from fastapi import FastAPI, Query
# from pydantic import BaseModel
# from typing import List
# from .firebase_to_opensearch import sync_recipes, search_recipes

# app = FastAPI(title="CamCook Search")

# class Recipe(BaseModel):
#     id: str
#     title: str
#     main_ingredient: str
#     ingredients: List[str]
#     instructions: str
#     calories: int = None
#     portions: int = None
#     prep_time: str = None
#     image_url: str = None

# @app.post("/sync_firebase")
# async def sync_from_firebase():
#     count = sync_recipes()
#     return {"status": "ok", "indexed_recipes": count}

# @app.get("/search")
# async def search(q: str = Query(..., description="Texto a buscar")):
#     results = search_recipes(q)
#     return {"hits": results, "query": q}
from fastapi import FastAPI, Query
from app.firebase_to_opensearch import sync_recipes, search_recipes

app = FastAPI(title="CamCook Search")

@app.post("/sync_firebase")
async def sync_from_firebase():
    try:
        count = sync_recipes()
        return {"status": "ok", "indexed_recipes": count}
    except Exception as e:
        # Captura errores de indexación y devuelve detalle
        return {"status": "error", "details": str(e)}

@app.get("/search")
async def search(
    q: str = Query(..., description="Texto a buscar"),
    userId: str = Query(None, description="ID del usuario"),
    lang: str = Query("es", description="Idioma de búsqueda")
):
    try:
        # Llama a tu función de búsqueda
        results = search_recipes(q)
        return {"hits": results, "query": q, "userId": userId, "lang": lang}
    except Exception as e:
        # Devuelve un error amigable en JSON
        return {"status": "error", "details": str(e)}
