code = r'''"""
Advanced AI Recipe Brain
"""

import json
import os
from typing import List, Dict, Optional
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

CUISINE_KNOWLEDGE = {
    "Indian": {
        "techniques": ["tempering (tadka)", "slow simmering", "dry roasting spices", "pressure cooking"],
        "flavor_base": "garlic, ginger, onion, tomato",
        "spices": "cumin, coriander, turmeric, garam masala, cardamom",
        "regional": "North Indian (rich gravies), South Indian (coconut + lentils), Street food (chaat)"
    },
    "Chinese": {
        "techniques": ["stir-fry (wok hei)", "steaming", "braising", "deep frying"],
        "flavor_base": "garlic, ginger, scallions, soy sauce",
        "spices": "five-spice, star anise, Sichuan pepper, white pepper",
        "regional": "Cantonese (mild), Sichuan (spicy), Shanghai (sweet)"
    },
    "Japanese": {
        "techniques": ["umami layering", "dashi broth", "steaming", "grilling"],
        "flavor_base": "dashi, miso, soy sauce, mirin, sake",
        "spices": "wasabi, shichimi, yuzu, ginger",
        "regional": "Tokyo (soy-forward), Kyoto (dashi-forward), Osaka (bold)"
    },
    "Italian": {
        "techniques": ["slow simmering", "al dente pasta", "emulsification", "grilling"],
        "flavor_base": "olive oil, garlic, tomato, fresh herbs",
        "spices": "basil, oregano, rosemary, thyme, black pepper",
        "regional": "Northern (cream, butter), Southern (tomato, olive oil)"
    },
    "American": {
        "techniques": ["grilling", "BBQ smoking", "deep frying", "baking"],
        "flavor_base": "butter, onion, garlic, stock",
        "spices": "paprika, cayenne, garlic powder, BBQ rubs",
        "regional": "Southern BBQ, New England seafood, Tex-Mex"
    },
    "Mexican": {
        "techniques": ["charring peppers", "toasting spices", "slow braising", "grilling"],
        "flavor_base": "chili, lime, cilantro, garlic, onion",
        "spices": "cumin, chili powder, oregano, smoked paprika",
        "regional": "Oaxacan (mole), Yucatan (citrus), Street food (tacos)"
    },
    "Thai": {
        "techniques": ["balancing 5 flavors", "wok cooking", "pounding in mortar", "steaming"],
        "flavor_base": "lemongrass, galangal, kaffir lime, fish sauce",
        "spices": "Thai basil, bird eye chili, turmeric, coriander root",
        "regional": "Central (balanced), Northern (milder), Southern (spicy)"
    }
}


def chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion, skill_level):
    fusion_note = ""
    if is_fusion and cuisine2:
        fusion_note = f"FUSION: Combine {cuisine1} structure with {cuisine2} flavors. Dish name should reflect both cultures."

    diet_note = "STRICTLY VEGETARIAN - absolutely no meat, chicken, beef, pork, fish, shrimp, seafood, or any animal flesh" if veg else "Non-Vegetarian"

    return f"""You are a world-class professional chef with 30 years experience. Generate a VERY DETAILED restaurant-quality recipe.

Request: {dish_hint}
Cuisine: {cuisine1}
{fusion_note}
Diet: {diet_note}
Ingredients available: {', '.join(ingredients)}
Skill level: {skill_level}

RULES:
- Provide EXACTLY 10 detailed cooking steps minimum
- Each step must have 3-5 sentences of detailed instruction
- Include exact quantities, temperatures (in Celsius and Fahrenheit), and cooking times
- Include separate prep steps (chopping, marinating, soaking)
- Explain WHY each action is done
- Add sensory cues (what to see, smell, hear) for each step
- {diet_note}

Respond ONLY in valid JSON, no markdown, no extra text:
{{
  "dish_name": "Full Dish Name",
  "tagline": "One enticing description sentence",
  "cuisine_type": "{cuisine1}",
  "serves": 2,
  "prep_time": "20 minutes",
  "cook_time": "30 minutes",
  "difficulty": "{skill_level}",
  "ingredients": [
    {{"name": "ingredient name", "amount": "exact quantity with unit", "note": "prep instruction e.g. finely chopped"}}
  ],
  "equipment_needed": ["Large pan", "Sharp knife", "Cutting board", "Measuring spoons"],
  "cooking_steps": [
    {{
      "step": 1,
      "title": "Descriptive Step Title",
      "instruction": "Detailed 3-5 sentence instruction. Include exact heat level, timing, and technique. Explain why this step is important. Mention what could go wrong and how to avoid it.",
      "tip": "Pro tip or beginner advice for this specific step",
      "sensory_cue": "Exactly what you should see, smell, hear or feel when done correctly",
      "time": "X minutes"
    }}
  ],
  "plating": "Detailed plating and garnish instructions",
  "chef_tips": ["Pro tip 1", "Pro tip 2", "Pro tip 3", "Storage tip", "Serving suggestion"],
  "variations": ["Variation 1 description", "Variation 2 description", "Variation 3 description"],
  "substitutions": [
    {{"original": "ingredient", "substitute": "alternative option", "flavor_impact": "how this changes the dish"}}
  ]
}}"""


def nutrition_agent_prompt(dish_name, ingredients):
    return f"""You are a certified nutritionist. Analyze: {dish_name} made with {', '.join(ingredients)}.

Respond ONLY in valid JSON, no markdown, no extra text:
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
}}"""


def teacher_agent_prompt(cooking_steps, skill_level):
    steps_text = json.dumps(cooking_steps)
    return f"""Rewrite these cooking steps for a complete beginner in very simple words: {steps_text}

Respond ONLY in valid JSON array, no markdown, no extra text:
[
  {{
    "step": 1,
    "simple_instruction": "Very simple instruction a child could understand",
    "sensory_cue": "what you see or smell",
    "safety_note": "what to watch out for",
    "emoji_guide": "relevant emoji"
  }}
]"""


class AIRecipeBrain:
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"

    def _call_groq(self, prompt, max_tokens=3000):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages
        )
        return response.choices[0].message.content

    def _parse_json(self, text):
        text = text.strip()
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
        start = text.find('[')
        end = text.rfind(']') + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
        return {}

    def generate_recipe(self, dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level="Beginner"):
        is_fusion = cuisine2 is not None and cuisine2 != cuisine1

        try:
            prompt = chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion, skill_level)
            raw = self._call_groq(prompt, max_tokens=3500)
            recipe = self._parse_json(raw)
        except Exception:
            recipe = {}

        if not recipe:
            recipe = self._fallback_recipe(dish_hint, cuisine1, ingredients)

        try:
            ing_names = [i.get("name", i) if isinstance(i, dict) else i for i in recipe.get("ingredients", ingredients)]
            prompt2 = nutrition_agent_prompt(recipe.get("dish_name", dish_hint), ing_names)
            raw2 = self._call_groq(prompt2, max_tokens=800)
            nutrition = self._parse_json(raw2)
        except Exception:
            nutrition = {}

        if not nutrition:
            nutrition = self._fallback_nutrition()

        simple_steps = []
        if skill_level == "Beginner":
            try:
                prompt3 = teacher_agent_prompt(recipe.get("cooking_steps", []), skill_level)
                raw3 = self._call_groq(prompt3, max_tokens=2000)
                raw3 = raw3.strip()
                if "```" in raw3:
                    raw3 = raw3.split("```")[1].split("```")[0].strip()
                    if raw3.startswith("json"):
                        raw3 = raw3[4:].strip()
                start = raw3.find('[')
                end = raw3.rfind(']') + 1
                if start >= 0:
                    simple_steps = json.loads(raw3[start:end])
            except Exception:
                simple_steps = []

        return {
            "recipe": recipe,
            "nutrition": nutrition,
            "simple_steps": simple_steps,
            "is_fusion": is_fusion,
            "fusion_cuisines": [cuisine1, cuisine2] if is_fusion else [cuisine1],
            "cuisine_knowledge": {
                "cuisine1": CUISINE_KNOWLEDGE.get(cuisine1, {}),
                "cuisine2": CUISINE_KNOWLEDGE.get(cuisine2, {}) if cuisine2 else {}
            }
        }

    def _fallback_recipe(self, dish_hint, cuisine, ingredients):
        return {
            "dish_name": f"{cuisine} {dish_hint.title()} Bowl",
            "tagline": f"A delicious {cuisine} inspired dish",
            "cuisine_type": cuisine,
            "serves": 2,
            "prep_time": "15 minutes",
            "cook_time": "25 minutes",
            "difficulty": "Easy",
            "ingredients": [{"name": ing, "amount": "as needed", "note": ""} for ing in ingredients],
            "equipment_needed": ["Pan", "Knife", "Cutting board"],
            "cooking_steps": [
                {"step": 1, "title": "Prepare Ingredients", "instruction": "Wash and chop all vegetables into even pieces about 1 inch in size. This ensures even cooking. Keep all prepped ingredients in separate bowls for easy access while cooking.", "tip": "Get everything ready before turning on the heat.", "sensory_cue": "Vegetables should look clean and uniform", "time": "10 minutes"},
                {"step": 2, "title": "Heat the Pan", "instruction": "Place a large pan over medium heat. Add 2 tablespoons of oil and let it heat for about 1 minute. The oil is ready when it shimmers slightly.", "tip": "Don't let the oil smoke - that means it is too hot.", "sensory_cue": "Oil should shimmer but not smoke", "time": "2 minutes"},
                {"step": 3, "title": "Cook Aromatics", "instruction": "Add garlic and onion to the hot oil. Stir frequently for 2-3 minutes until softened and golden. This builds the flavor base for the whole dish.", "tip": "Keep stirring to prevent burning.", "sensory_cue": "Should smell sweet and aromatic", "time": "3 minutes"},
                {"step": 4, "title": "Add Main Ingredients", "instruction": "Add the main ingredients to the pan. Spread them out evenly. Cook on medium-high heat for 5-7 minutes, stirring occasionally.", "tip": "Don't crowd the pan or ingredients will steam instead of fry.", "sensory_cue": "Should hear a steady sizzle", "time": "7 minutes"},
                {"step": 5, "title": "Season and Finish", "instruction": "Add spices and seasoning. Stir well to coat everything evenly. Taste and adjust salt. Cook for 2 more minutes.", "tip": "Season gradually and taste as you go.", "sensory_cue": "Should smell fragrant and look colorful", "time": "3 minutes"},
                {"step": 6, "title": "Plate and Serve", "instruction": "Transfer to a serving plate. Garnish with fresh herbs. Serve immediately while hot.", "tip": "Warm your plates first for a restaurant-style presentation.", "sensory_cue": "Should look colorful and appetizing", "time": "2 minutes"}
            ],
            "plating": "Serve in a warm bowl, garnish with fresh herbs and a drizzle of oil",
            "chef_tips": ["Use fresh ingredients for best flavor", "Season at every stage", "Serve immediately", "Taste before serving"],
            "variations": ["Add more vegetables", "Make it spicier with chili", "Add lemon for brightness"],
            "substitutions": []
        }

    def _fallback_nutrition(self):
        return {
            "per_serving": {
                "calories": 350,
                "protein_g": 12,
                "carbs_g": 45,
                "fat_g": 10,
                "fiber_g": 6,
                "sodium_mg": 400
            },
            "health_benefits": ["Good source of energy", "Contains essential nutrients", "Balanced macronutrients"],
            "who_should_avoid": ["People with specific food allergies should check ingredients"],
            "dietary_tags": ["Balanced"],
            "healthy_swaps": ["Use less oil", "Add more vegetables"],
            "best_time_to_eat": "Lunch or Dinner"
        }
'''

with open('backend/ai_brain.py', 'w') as f:
    f.write(code)

import ast
ast.parse(code)
print("ai_brain.py written and verified!")
print("Size:", len(code), "bytes")
