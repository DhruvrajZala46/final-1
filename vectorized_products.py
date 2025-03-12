from langchain_huggingface import HuggingFaceEmbeddings
import faiss
import numpy as np
import os
from fetch_products import fetch_products

# Fetch products
products = fetch_products()
product_texts = [f"{p['title']} - {p['description']} (₹{p['price']})" for p in products]

if not product_texts:
    raise ValueError("No products found. Ensure your Shopify API is working correctly.")

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
product_vectors = embedding_model.embed_documents(product_texts)

# Convert list of vectors to NumPy array
product_vectors = np.array(product_vectors).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(product_vectors.shape[1])
index.add(product_vectors)

# Save the index
faiss.write_index(index, "vectorized_list.index")
print("✅ Product embeddings saved successfully!")
