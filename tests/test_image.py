import requests

key = "a18b605c8aec45038424e33fb0f8f9d2"

dishes = ["butter chicken", "biryani", "malai kofta", "shawarma", "pasta"]

for dish in dishes:
    resp = requests.get(
        f"https://api.spoonacular.com/recipes/complexSearch?query={dish}&number=1&apiKey={key}",
        timeout=10
    )
    results = resp.json().get("results", [])
    if results:
        print(f"{dish}: {results[0].get('title')} -> {results[0].get('image')}")
    else:
        print(f"{dish}: NO RESULTS - status {resp.status_code}")