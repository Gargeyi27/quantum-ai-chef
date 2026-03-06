with open('backend/ai_brain.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix nutrition prompt to be more specific per dish
old = '''def nutrition_agent_prompt(dish_name, ingredients):
    return f"""You are a certified nutritionist. Analyze: {dish_name} with: {', '.join(ingredients)}.

Respond ONLY with valid JSON, no markdown:
{{
  "per_serving": {{
    "calories": 350,
    "protein_g": 12,
    "carbs_g": 45,
    "fat_g": 10,
    "fiber_g": 6,
    "sodium_mg": 400
  }},
  "health_benefits": ["benefit1", "benefit2", "benefit3"],
  "who_should_avoid": ["group1"],
  "dietary_tags": ["tag1", "tag2"],
  "healthy_swaps": ["swap1", "swap2"],
  "best_time_to_eat": "Lunch or Dinner"
}}"""'''

new = '''def nutrition_agent_prompt(dish_name, ingredients):
    return f"""You are a certified nutritionist. Calculate ACCURATE nutrition for: {dish_name}
Ingredients: {', '.join(ingredients)}

Give REALISTIC values specific to THIS dish. For example:
- Sweet corn soup: ~150 calories, low fat
- Butter chicken: ~350 calories, high protein
- Pasta: ~400 calories, high carbs
- Salad: ~120 calories, low calories

Respond ONLY with valid JSON, no markdown, no extra text:
{{
  "per_serving": {{
    "calories": 0,
    "protein_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "fiber_g": 0,
    "sodium_mg": 0
  }},
  "health_benefits": ["specific benefit 1 for {dish_name}", "specific benefit 2", "specific benefit 3"],
  "who_should_avoid": ["specific group if any"],
  "dietary_tags": ["relevant tag"],
  "healthy_swaps": ["specific swap for {dish_name}"],
  "best_time_to_eat": "specific meal time"
}}"""'''

if old in c:
    c = c.replace(old, new)
    with open('backend/ai_brain.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Nutrition prompt fixed!")
else:
    print("Pattern not found - checking what's there:")
    idx = c.find('def nutrition_agent_prompt')
    print(c[idx:idx+300])