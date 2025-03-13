from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import faiss
import numpy as np
import os
from fetch_products import fetch_products

# Load FAISS index
index_path = "vectorized_list.index"
if not os.path.exists(index_path):
    raise FileNotFoundError(f"FAISS index '{index_path}' not found. Run vectorize_products.py first.")

index = faiss.read_index(index_path)

# Load the same embedding model used in vectorization
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def recommend_product(user_query):
    query_vector = np.array(embedding_model.embed_query(user_query)).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, k=3)

    products = fetch_products()
    
    recommended_products = []
    for i in indices[0]:
        if i < len(products):
            recommended_products.append({
                "title": products[i]["title"],
                "description": products[i]["description"],
                "price": products[i]["price"],
                "image": products[i].get("image", "https://default-image.com/no-image.jpg")  # Handle missing image
            })
    
    return recommended_products

if __name__ == "__main__":
    query = input("Enter your product preference: ")
    recommendations = recommend_product(query)
    for product in recommendations:
        print(f"🔹 {product['title']} - ₹{product['price']}\n   {product['description']}\n   Image: {product['image']}\n")
