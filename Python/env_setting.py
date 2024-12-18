from opensearchpy import OpenSearch
import json

# OpenSearch 설정
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False,
    verify_certs=False
)

# 인덱스 이름 설정
index_name = "game-items"

# KNN 기능을 활성화한 인덱스 설정
index_settings = {
    "settings": {
        "index": {
            "knn": True  # KNN 기능 활성화
        }
    },
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "type": {"type": "keyword"},
            "description": {"type": "text"},
            "rarity": {"type": "keyword"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 384  # SentenceTransformer의 벡터 차원
            }
        }
    }
}

# 기존 인덱스 삭제 후 재생성
if client.indices.exists(index_name):
    client.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted.")

client.indices.create(index=index_name, body=index_settings)
print(f"Index '{index_name}' created with KNN mapping and settings.")

# 데이터 업로드
with open(r"C:\...\game_items.json", "r") as file:
    items = json.load(file)
    for item in items:
        client.index(index=index_name, id=item["id"], body=item)

print("Data indexed successfully!")
