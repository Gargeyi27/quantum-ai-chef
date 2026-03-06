# This fixes main.py - removes any direct recipe["difficulty"] access
# and fixes the return to pass recipe as-is without touching its keys

with open('backend/main.py', 'r') as f:
    c = f.read()

# Replace any bracket access of recipe fields with .get()
import re
c = re.sub(r'recipe\["difficulty"\]', 'recipe.get("difficulty", "Medium")', c)
c = re.sub(r'recipe\["name"\]', 'recipe.get("name", "Recipe")', c)
c = re.sub(r'recipe\["steps"\]', 'recipe.get("steps", [])', c)

with open('backend/main.py', 'w') as f:
    f.write(c)

print("main.py fixed!")

# Also check ai_brain for the real crash location
with open('backend/ai_brain.py', 'r') as f:
    ab = f.read()

# Find any bracket access on recipe that could fail
import re
hits = re.findall(r'recipe\["[^"]+"\]', ab)
print("ai_brain bracket accesses:", hits)