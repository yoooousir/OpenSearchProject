# Sentence Transformers를 활용해 아이템 설명(description)을 벡터화

from sentence_transformers import SentenceTransformer
import numpy as np
from env_setting import items, client, index_name

# 임베딩 모델 설정
model = SentenceTransformer("all-MiniLM-L6-v2")

# 아이템 데이터 벡터화
for item in items:
    embedding = model.encode(item["description"]).tolist()
    item["embedding"] = embedding
    client.index(index=index_name, id=item["id"], body=item)
print("Embeddings added successfully!")
