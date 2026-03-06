import requests

key = "qmCNDMgmqsWpP0sYMGQ8bVlYvFM7n8aq_wOioGmcXks"
query = "butter chicken food"

resp = requests.get(
    f"https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=landscape",
    headers={"Authorization": "Client-ID " + key},
    timeout=10
)
print("Status:", resp.status_code)
print("Response:", resp.text[:500])