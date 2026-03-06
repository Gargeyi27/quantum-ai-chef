with open('backend/ai_brain.py', 'r') as f:
    c = f.read()

# Find where recipe dict is accessed after parsing and add .get() safety
# The issue is recipe["difficulty"] instead of recipe.get("difficulty", "Medium")
c = c.replace('recipe["difficulty"]', 'recipe.get("difficulty", "Medium")')
c = c.replace('recipe["name"]', 'recipe.get("name", "Chef\'s Special")')
c = c.replace('recipe["description"]', 'recipe.get("description", "")')
c = c.replace('recipe["prep_time"]', 'recipe.get("prep_time", "15 mins")')
c = c.replace('recipe["cook_time"]', 'recipe.get("cook_time", "30 mins")')
c = c.replace('recipe["servings"]', 'recipe.get("servings", 2)')
c = c.replace('recipe["ingredients"]', 'recipe.get("ingredients", [])')
c = c.replace('recipe["steps"]', 'recipe.get("steps", [])')

with open('backend/ai_brain.py', 'w') as f:
    f.write(c)

print('Fixed! ai_brain.py is now defensive against missing keys.')