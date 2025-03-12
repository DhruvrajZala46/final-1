import os
from fastapi import FastAPI
from recommend_products import recommend_product  # ✅ Correct function name

app = FastAPI()

@app.get("/recommend/")
def recommend(query: str):
    recommended_products = recommend_product(query)  # ✅ Call the correct function

    response = {
        "recommended_products": [
            {
                "title": p["title"],
                "description": p["description"],
                "price": p["price"],
                "image": p["image"]
            }
            for p in recommended_products
        ],
    }

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
