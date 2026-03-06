with open('backend/ai_brain.py', 'r') as f:
    c = f.read()

old = '''    return f"""You are an elite professional chef AI. Generate a complete authentic recipe.

Request: {dish_hint}
Cuisine: {cuisine1}
{fusion_note}
Diet: {"Vegetarian" if veg else "Non-Vegetarian"}
Ingredients available: {', '.join(ingredients)}
Skill level: {skill_level}

Respond ONLY in this exact JSON format, no other text:
{{
  "dish_name": "name here",
  "tagline": "one sentence description",
  "cuisine_type": "cuisine here",
  "serves": 2,
  "prep_time": "15 minutes",
  "cook_time": "20 minutes",
  "difficulty": "Easy",
  "ingredients": [
    {{"name": "ingredient", "amount": "quantity", "note": "prep note"}}
  ],
  "equipment_needed": ["Pan", "Knife"],
  "cooking_steps": [
    {{"step": 1, "title": "step title", "instruction": "what to do", "tip": "beginner tip", "sensory_cue": "what you see or smell"}}
  ],
  "plating": "how to serve",
  "chef_tips": ["tip1", "tip2", "tip3"],
  "variations": ["variation1", "variation2"],
  "substitutions": [{{"original": "ingredient", "substitute": "alternative", "flavor_impact": "taste change"}}]
}}"""'''

new = '''    return f"""You are a world-class professional chef AI with 30 years of experience. Generate a VERY DETAILED, authentic, restaurant-quality recipe.

Request: {dish_hint}
Cuisine: {cuisine1}
{fusion_note}
Diet: {"Vegetarian - ABSOLUTELY NO meat, chicken, beef, fish, or seafood" if veg else "Non-Vegetarian"}
Ingredients available: {', '.join(ingredients)}
Skill level: {skill_level}

IMPORTANT RULES:
- Provide AT LEAST 8-12 detailed cooking steps
- Each step must have a clear title, detailed instruction (3-5 sentences), a helpful tip, and a sensory cue
- Include exact quantities, temperatures, and cooking times in every step
- Include preparation steps (chopping, marinating, soaking) as separate steps
- {"USE ONLY VEGETARIAN INGREDIENTS - No meat, chicken, beef, pork, fish, shrimp, or seafood of any kind" if veg else "Use ingredients appropriately"}
- Make instructions beginner-friendly with clear explanations

Respond ONLY in this exact JSON format, no other text:
{{
  "dish_name": "name here",
  "tagline": "one enticing sentence description",
  "cuisine_type": "cuisine here",
  "serves": 2,
  "prep_time": "15 minutes",
  "cook_time": "30 minutes",
  "difficulty": "Easy",
  "ingredients": [
    {{"name": "ingredient", "amount": "exact quantity with unit", "note": "how to prep it e.g. finely chopped"}}
  ],
  "equipment_needed": ["Pan", "Knife", "Cutting board"],
  "cooking_steps": [
    {{
      "step": 1,
      "title": "Descriptive Step Title",
      "instruction": "Very detailed instruction with exact temperatures, times, and techniques. Explain WHY you are doing each action. Include what to watch out for.",
      "tip": "Helpful tip for beginners or how to make it better",
      "sensory_cue": "What you should see, smell, hear, or feel when this step is done correctly",
      "time": "5 minutes"
    }}
  ],
  "plating": "Detailed description of how to plate and garnish beautifully",
  "chef_tips": ["Professional tip 1", "Professional tip 2", "Professional tip 3", "Professional tip 4"],
  "variations": ["variation1", "variation2", "variation3"],
  "substitutions": [{{"original": "ingredient", "substitute": "alternative", "flavor_impact": "how taste changes"}}]
}}"""'''

if old in c:
    c = c.replace(old, new)
    with open('backend/ai_brain.py', 'w') as f:
        f.write(c)
    print("Fixed! Chef prompt now requests detailed steps.")
else:
    print("Pattern not found - writing backup fix...")
    # Fallback: just find and replace the key instruction line
    c = c.replace(
        '"cooking_steps": [\n    {{"step": 1, "title": "step title", "instruction": "what to do", "tip": "beginner tip", "sensory_cue": "what you see or smell"}}',
        '"cooking_steps": [\n    {{"step": 1, "title": "Descriptive Step Title", "instruction": "Very detailed 3-5 sentence instruction with exact temperatures and times", "tip": "Helpful beginner tip", "sensory_cue": "What you see/smell/hear", "time": "5 minutes"}}'
    )
    with open('backend/ai_brain.py', 'w') as f:
        f.write(c)
    print("Fallback fix applied.")