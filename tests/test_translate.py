import requests

def translate(text, target_lang):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": target_lang,
        "dt": "t",
        "q": text
    }
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code == 200:
        result = resp.json()
        translated = "".join([item[0] for item in result[0] if item[0]])
        return translated
    return text

# Test
print(translate("Heat oil in a pan and add garlic", "hi"))  # Hindi
print(translate("Add salt and pepper to taste", "ml"))      # Malayalam
print(translate("Cook for 10 minutes on medium heat", "te")) # Telugu