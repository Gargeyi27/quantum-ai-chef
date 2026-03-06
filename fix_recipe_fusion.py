# Fix ingredients and fusion issues

# Fix 1: Update main.py
with open('backend/main.py', 'r') as f:
    c = f.read()

c = c.replace(
    'ai_result = ai_brain.generate_recipe(\n            dish_hint=dish_hint,\n            cuisine1=req.cuisine,\n            cuisine2=cuisine2,\n            veg=veg,\n            ingredients=optimized_ingredients,\n            skill_level=req.skill_level\n        )',
    'ai_result = ai_brain.generate_recipe(\n            dish_hint=dish_hint,\n            cuisine1=req.cuisine,\n            cuisine2=cuisine2,\n            veg=veg,\n            ingredients=optimized_ingredients,\n            skill_level=req.skill_level,\n            is_fusion=is_fusion\n        )'
)

with open('backend/main.py', 'w') as f:
    f.write(c)
print("main.py updated!")

# Fix 2: Update ai_brain.py
with open('backend/ai_brain.py', 'r') as f:
    ab = f.read()

# Fix function signature
ab = ab.replace(
    'def generate_recipe(self, dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level="Beginner"):',
    'def generate_recipe(self, dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level="Beginner", is_fusion=False):'
)

# Fix chef prompt call
ab = ab.replace(
    'prompt = chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion, skill_level)',
    'prompt = chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion or (cuisine2 is not None and cuisine2 != cuisine1), skill_level)'
)

# Fix ingredients line in prompt to be dish-aware
ab = ab.replace(
    "Ingredients available: {', '.join(ingredients)}",
    "Quantum-suggested ingredients (use as guide only): {', '.join(ingredients)}\nChoose ALL correct ingredients needed to make authentic {dish_hint}. Do not limit yourself to only the suggested list."
)

with open('backend/ai_brain.py', 'w') as f:
    f.write(ab)
print("ai_brain.py updated!")
print("Done! Restart uvicorn now.")