from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "opensearch-node1", "port": 9200}],
    http_auth=("admin", "admin"),
)

INDEX_NAME = "recipes"

def index_recipe(recipe):
    client.index(index=INDEX_NAME, id=recipe["id"], body=recipe)
    return {"status": "ok", "recipe": recipe}

def search_recipes(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "ingredients", "instructions"]
            }
        }
    }
    res = client.search(index=INDEX_NAME, body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]
