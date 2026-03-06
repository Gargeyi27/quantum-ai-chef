import requests

api_key = "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"
url = "https://api.groq.com/openai/v1/models"
headers = {"Authorization": "Bearer " + api_key}
response = requests.get(url, headers=headers)
data = response.json()

# Filter only text generation models (exclude whisper/audio)
exclude = ["whisper", "guard", "allam", "orpheus", "safeguard"]
models = []
for m in sorted(data.get("data", []), key=lambda x: x["id"]):
    mid = m["id"]
    if not any(e in mid.lower() for e in exclude):
        print(f"{mid} | context: {m['context_window']} | max_out: {m['max_completion_tokens']}")
        models.append(mid)

print("\nTotal text models:", len(models))