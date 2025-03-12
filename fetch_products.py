import os
import requests

# Load sensitive data from environment variables
SHOPIFY_STORE_URL = "https://chargic.myshopify.com" #your store url
ACCESS_TOKEN = os.getenv("shopify_api_key")  #environment variable name

def fetch_products():
    if not ACCESS_TOKEN:
        raise ValueError("Missing Shopify access token. Set SHOPIFY_ACCESS_TOKEN as an environment variable.")

    url = f"{SHOPIFY_STORE_URL.rstrip('/')}/admin/api/2023-10/products.json"
    headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}
    
    all_products = []
    params = {"limit": 250}  # Maximum limit per request is 250

    while url:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            products = data.get("products", [])
            all_products.extend(products)

            # Check for pagination link
            link_header = response.headers.get("Link", "")
            next_url = None

            if 'rel="next"' in link_header:
                parts = link_header.split(", ")
                for part in parts:
                    if 'rel="next"' in part:
                        next_url = part.split(";")[0].strip("<>")

            url = next_url  # Update URL for next request or exit loop if None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            break

    return [
        {
            "title": p["title"],
            "description": p["body_html"],
            "price": p["variants"][0]["price"],
            "image": p["images"][0]["src"] if p["images"] else "https://default-image.com/no-image.jpg"
        }
        for p in all_products
    ]

if __name__ == "__main__":
    products = fetch_products()
    print(f"Total products fetched: {len(products)}")
    print(products[:10])  # Print first 10 products for testing
