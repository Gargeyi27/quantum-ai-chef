import requests, json, os, sys
sys.path.insert(0, '.')
os.environ['GROQ_API_KEY'] = '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'

from backend.ai_brain import AIRecipeBrain
brain = AIRecipeBrain()
result = brain.generate_recipe(
    'butter chicken', 'Indian', None, False,
    ['chicken', 'tomato', 'garlic', 'ginger', 'onion', 'cream', 'butter', 'spices'],
    'Beginner'
)
recipe = result['recipe']
print("=== DISH ===")
print(recipe.get('dish_name'))
print("\n=== INGREDIENTS (" + str(len(recipe.get('ingredients',[]))) + ") ===")
for i in recipe.get('ingredients', []):
    if isinstance(i, dict):
        print(f"  - {i.get('amount','?')} {i.get('name','?')} | {i.get('note','')}")
    else:
        print("  -", i)
print("\n=== STEPS (" + str(len(recipe.get('cooking_steps',[]))) + ") ===")
for s in recipe.get('cooking_steps', []):
    if isinstance(s, dict):
        print(f"  Step {s.get('step')}: {s.get('title')} ({s.get('time','')})")
        print(f"    {s.get('instruction','')[:100]}...")
    else:
        print("  -", str(s)[:100])