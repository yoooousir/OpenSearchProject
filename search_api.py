# FastAPI로 검색 및 추천 API 구현

from fastapi import FastAPI, HTTPException
from sentence_transformers_embedding import items, client, index_name, model

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Game Items Search API! Use /search/ or /recommend/ endpoints."}

@app.get("/search/")
def search_items(query: str):
    # 키워드 검색
    try:
        body = {"query": {"match": {"description": query}}}
        results = client.search(index=index_name, body=body)
        return results["hits"]["hits"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/recommend/")
def recommend_items(query: str):
    # 벡터 검색
    try:
        embedding = model.encode(query).tolist()
        body = {
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": 2
                    }
                }
            }
        }
        results = client.search(index=index_name, body=body)
        return results["hits"]["hits"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")
