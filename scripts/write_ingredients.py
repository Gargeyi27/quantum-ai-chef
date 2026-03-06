"""Run this to fix ingredients.json: python write_ingredients.py"""

import json
import os

data = {
  "ingredients": {
    "rice": {"cuisines": ["Indian","Chinese","Japanese","Thai","Mexican"], "nutrition": {"calories": 206, "protein": 4, "carbs": 45, "fat": 0.4, "fiber": 0.6}, "allergens": [], "difficulty": 1, "flavor_profile": ["neutral", "starchy"]},
    "noodles": {"cuisines": ["Chinese","Japanese","Thai","Italian"], "nutrition": {"calories": 220, "protein": 7, "carbs": 43, "fat": 1.3, "fiber": 2}, "allergens": ["gluten"], "difficulty": 1, "flavor_profile": ["neutral", "chewy"]},
    "chicken": {"cuisines": ["Indian","Chinese","American","Mexican","Thai","Italian"], "nutrition": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0}, "allergens": [], "difficulty": 2, "flavor_profile": ["savory", "umami"]},
    "tofu": {"cuisines": ["Chinese","Japanese","Thai"], "nutrition": {"calories": 76, "protein": 8, "carbs": 2, "fat": 4.8, "fiber": 0.3}, "allergens": ["soy"], "difficulty": 2, "flavor_profile": ["neutral", "soft"]},
    "garlic": {"cuisines": ["Indian","Chinese","Italian","Mexican","Thai","American"], "nutrition": {"calories": 4, "protein": 0.2, "carbs": 1, "fat": 0, "fiber": 0.1}, "allergens": [], "difficulty": 1, "flavor_profile": ["pungent", "savory"]},
    "ginger": {"cuisines": ["Indian","Chinese","Japanese","Thai"], "nutrition": {"calories": 5, "protein": 0.1, "carbs": 1.1, "fat": 0, "fiber": 0.1}, "allergens": [], "difficulty": 1, "flavor_profile": ["spicy", "warm"]},
    "soy_sauce": {"cuisines": ["Chinese","Japanese","Thai"], "nutrition": {"calories": 10, "protein": 1, "carbs": 1, "fat": 0, "fiber": 0}, "allergens": ["soy","gluten"], "difficulty": 1, "flavor_profile": ["salty", "umami"]},
    "tomato": {"cuisines": ["Indian","Italian","Mexican","American"], "nutrition": {"calories": 22, "protein": 1, "carbs": 4.8, "fat": 0.2, "fiber": 1.5}, "allergens": [], "difficulty": 1, "flavor_profile": ["acidic", "sweet"]},
    "onion": {"cuisines": ["Indian","Chinese","Italian","Mexican","American","Thai"], "nutrition": {"calories": 44, "protein": 1.2, "carbs": 10, "fat": 0.1, "fiber": 1.9}, "allergens": [], "difficulty": 1, "flavor_profile": ["pungent", "sweet"]},
    "cumin": {"cuisines": ["Indian","Mexican","Thai"], "nutrition": {"calories": 8, "protein": 0.4, "carbs": 0.9, "fat": 0.5, "fiber": 0.2}, "allergens": [], "difficulty": 1, "flavor_profile": ["earthy", "warm"]},
    "chili": {"cuisines": ["Indian","Chinese","Mexican","Thai"], "nutrition": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 0.7}, "allergens": [], "difficulty": 1, "flavor_profile": ["hot", "spicy"]},
    "coconut_milk": {"cuisines": ["Indian","Thai","Japanese"], "nutrition": {"calories": 230, "protein": 2.3, "carbs": 5.5, "fat": 24, "fiber": 0}, "allergens": [], "difficulty": 1, "flavor_profile": ["creamy", "sweet", "rich"]},
    "pasta": {"cuisines": ["Italian","American"], "nutrition": {"calories": 220, "protein": 8, "carbs": 43, "fat": 1.3, "fiber": 2.5}, "allergens": ["gluten"], "difficulty": 1, "flavor_profile": ["neutral", "starchy"]},
    "cheese": {"cuisines": ["Italian","American","Mexican"], "nutrition": {"calories": 113, "protein": 7, "carbs": 0.4, "fat": 9, "fiber": 0}, "allergens": ["dairy"], "difficulty": 1, "flavor_profile": ["creamy", "savory", "rich"]},
    "beef": {"cuisines": ["American","Mexican","Italian","Japanese"], "nutrition": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "fiber": 0}, "allergens": [], "difficulty": 2, "flavor_profile": ["rich", "savory", "umami"]},
    "lemon": {"cuisines": ["Italian","Indian","American","Thai"], "nutrition": {"calories": 17, "protein": 0.6, "carbs": 5.4, "fat": 0.2, "fiber": 1.6}, "allergens": [], "difficulty": 1, "flavor_profile": ["acidic", "bright", "citrus"]},
    "cilantro": {"cuisines": ["Indian","Mexican","Thai","Chinese"], "nutrition": {"calories": 1, "protein": 0.1, "carbs": 0.1, "fat": 0, "fiber": 0.1}, "allergens": [], "difficulty": 1, "flavor_profile": ["fresh", "herbal"]},
    "miso": {"cuisines": ["Japanese"], "nutrition": {"calories": 34, "protein": 2.2, "carbs": 4.3, "fat": 1, "fiber": 0.9}, "allergens": ["soy"], "difficulty": 1, "flavor_profile": ["umami", "salty", "fermented"]},
    "tortilla": {"cuisines": ["Mexican","American"], "nutrition": {"calories": 146, "protein": 3.8, "carbs": 25, "fat": 3.5, "fiber": 1.5}, "allergens": ["gluten"], "difficulty": 1, "flavor_profile": ["neutral", "starchy"]},
    "basil": {"cuisines": ["Italian","Thai"], "nutrition": {"calories": 1, "protein": 0.2, "carbs": 0.1, "fat": 0, "fiber": 0.1}, "allergens": [], "difficulty": 1, "flavor_profile": ["sweet", "herbal", "fresh"]},
    "fish_sauce": {"cuisines": ["Thai"], "nutrition": {"calories": 6, "protein": 0.9, "carbs": 0.6, "fat": 0, "fiber": 0}, "allergens": ["fish"], "difficulty": 1, "flavor_profile": ["salty", "umami", "pungent"]},
    "lime": {"cuisines": ["Mexican","Thai","Indian"], "nutrition": {"calories": 20, "protein": 0.5, "carbs": 7, "fat": 0.1, "fiber": 1.9}, "allergens": [], "difficulty": 1, "flavor_profile": ["acidic", "bright", "citrus"]},
    "potato": {"cuisines": ["Indian","American","Italian"], "nutrition": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "fiber": 2.2}, "allergens": [], "difficulty": 1, "flavor_profile": ["starchy", "neutral"]},
    "eggs": {"cuisines": ["American","Chinese","Japanese","Italian"], "nutrition": {"calories": 78, "protein": 6, "carbs": 0.6, "fat": 5, "fiber": 0}, "allergens": ["eggs"], "difficulty": 1, "flavor_profile": ["rich", "savory"]},
    "butter": {"cuisines": ["American","Italian","Indian"], "nutrition": {"calories": 102, "protein": 0.1, "carbs": 0, "fat": 11.5, "fiber": 0}, "allergens": ["dairy"], "difficulty": 1, "flavor_profile": ["rich", "creamy", "fatty"]},
    "paneer": {"cuisines": ["Indian"], "nutrition": {"calories": 265, "protein": 18, "carbs": 3.6, "fat": 20, "fiber": 0}, "allergens": ["dairy"], "difficulty": 2, "flavor_profile": ["mild", "creamy", "fresh"]},
    "mushroom": {"cuisines": ["Chinese","Japanese","Italian","American"], "nutrition": {"calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3, "fiber": 1}, "allergens": [], "difficulty": 1, "flavor_profile": ["earthy", "umami", "savory"]},
    "salmon": {"cuisines": ["Japanese","American"], "nutrition": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0}, "allergens": ["fish"], "difficulty": 2, "flavor_profile": ["rich", "fatty", "umami"]},
    "avocado": {"cuisines": ["Mexican","American"], "nutrition": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15, "fiber": 7}, "allergens": [], "difficulty": 1, "flavor_profile": ["creamy", "buttery", "mild"]},
    "lentils": {"cuisines": ["Indian"], "nutrition": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4, "fiber": 8}, "allergens": [], "difficulty": 1, "flavor_profile": ["earthy", "nutty", "hearty"]}
  },
  "cuisine_flavor_profiles": {
    "Indian": {"primary": ["cumin","turmeric","garam_masala","cardamom"], "heat": "high", "acid": "medium", "fat": "medium", "key_technique": "tempering"},
    "Chinese": {"primary": ["soy_sauce","ginger","garlic","sesame"], "heat": "low-medium", "acid": "low", "fat": "medium", "key_technique": "stir_fry"},
    "Japanese": {"primary": ["miso","dashi","soy_sauce","mirin"], "heat": "low", "acid": "medium", "fat": "low", "key_technique": "umami_layering"},
    "Italian": {"primary": ["basil","oregano","garlic","olive_oil"], "heat": "low", "acid": "high", "fat": "medium", "key_technique": "slow_simmer"},
    "American": {"primary": ["bbq","ketchup","mustard","cheese"], "heat": "low-medium", "acid": "medium", "fat": "high", "key_technique": "grilling"},
    "Mexican": {"primary": ["cumin","chili","lime","cilantro"], "heat": "medium-high", "acid": "high", "fat": "medium", "key_technique": "charring"},
    "Thai": {"primary": ["fish_sauce","lemongrass","galangal","kaffir_lime"], "heat": "high", "acid": "high", "fat": "medium", "key_technique": "balance_five_flavors"}
  },
  "fusion_compatibility": {
    "Indian_Mexican": 0.88,
    "Indian_Chinese": 0.82,
    "Indian_Japanese": 0.71,
    "Indian_Italian": 0.75,
    "Indian_Thai": 0.85,
    "Chinese_Japanese": 0.91,
    "Chinese_Mexican": 0.73,
    "Chinese_Italian": 0.68,
    "Chinese_Thai": 0.89,
    "Japanese_Italian": 0.78,
    "Japanese_Mexican": 0.72,
    "Japanese_Thai": 0.87,
    "Italian_Mexican": 0.80,
    "Italian_American": 0.90,
    "Mexican_American": 0.93,
    "Mexican_Thai": 0.76,
    "Thai_American": 0.77
  }
}

# Write ingredients.json
output_path = os.path.join("data", "ingredients.json")
os.makedirs("data", exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Written to {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")

# Verify it loads back
with open(output_path, encoding="utf-8") as f:
    loaded = json.load(f)

print(f"Ingredients count: {len(loaded['ingredients'])}")
print(f"Cuisines: {len(loaded['cuisine_flavor_profiles'])}")
print("ingredients.json is valid!")

# Also delete any empty quantum_cache.json
cache_path = os.path.join("data", "quantum_cache.json")
if os.path.exists(cache_path):
    with open(cache_path, encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        os.remove(cache_path)
        print("Deleted empty quantum_cache.json")

print("\nAll done! Now run: python -m uvicorn backend.main:app --reload --port 8000")