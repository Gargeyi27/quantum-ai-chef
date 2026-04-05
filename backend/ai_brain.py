import os
import json
import random
from typing import List, Dict, Optional
from groq import Groq

# Support multiple Groq API keys for high availability
API_KEYS = os.environ.get("GROQ_API_KEYS", "").split(",")

def get_live_models(api_key: str):
    """Latest supported Groq models (2024-2025)"""
    return [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "llama3-8b-8192"
    ]

client = Groq(api_key=API_KEYS[0])

def chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level):
    veg_status = "purely Vegetarian" if veg else "Non-Vegetarian"
    fusion_note = f"a fusion of {cuisine1} and {cuisine2}" if cuisine2 else f"{cuisine1} style"
    
    prompt = (
        f"You are a World-Class Michelin Star Chef. Create a {fusion_note} {veg_status} recipe for: {dish_hint}.\n"
        f"SKILL LEVEL: {skill_level}. OPTIMIZED INGREDIENTS: {', '.join(ingredients)}\n\n"
        "Return ONLY a JSON object with this exact structure:\n"
        "{\n"
        '  "dish_name": "Unique Creative Name",\n'
        '  "tagline": "Catchy 1-sentence description",\n'
        '  "prep_time": "15 mins", "cook_time": "30 mins", "difficulty": "Intermediate",\n'
        '  "ingredients": [{"name": "item", "amount": "quantity", "note": "prep tip"}],\n'
        '  "cooking_steps": [{"step": 1, "title": "...", "instruction": "...", "tip": "...", "sensory_cue": "...", "time": "5m"}],\n'
        '  "equipment_needed": ["tool1", "tool2"],\n'
        '  "plating": "Detailed restaurant-quality plating instructions",\n'
        '  "chef_tips": ["tip1", "tip2", "storage tip", "reheating tip", "serving tip"],\n'
        '  "variations": ["variation 1", "variation 2", "variation 3"],\n'
        '  "substitutions": [{"original": "ingredient", "substitute": "alternative", "flavor_impact": "how taste changes"}],\n'
        '  "nutrition": {\n'
        '    "per_serving": {"calories": 400, "protein_g": 25, "carbs_g": 30, "fat_g": 15, "fiber_g": 4, "sodium_mg": 600},\n'
        '    "health_benefits": ["benefit1", "benefit2", "benefit3"],\n'
        '    "who_should_avoid": ["restriction1", "restriction2"],\n'
        '    "dietary_tags": ["tag1", "tag2"],\n'
        '    "healthy_swaps": ["swap1", "swap2"],\n'
        '    "best_time_to_eat": "when and why"\n'
        '  }\n'
        '}'
    )
    return prompt

def teacher_agent_prompt(steps, skill_level):
    return (
        f"As a cooking teacher for a {skill_level}, simplify these steps into clear, visual instructions:\n"
        f"STEPS: {json.dumps(steps)}\n"
        "Return a JSON list of simplified points."
    )

def safety_agent_prompt(recipe_json):
    return (
        "Check this recipe for safety issues (raw meat, allergens, etc.)\n"
        f"RECIPE: {json.dumps(recipe_json)}\n"
        "Return a JSON object with 'is_safe' (bool) and 'warnings' (list)."
    )

class AIRecipeBrain:
    def __init__(self):
        self.api_keys = [k.strip() for k in API_KEYS if k.strip()]
        if not self.api_keys:
            print("⚠️ No GROQ_API_KEYS found in environment!")

    def _call_groq(self, prompt, max_tokens=2500):
        keys = self.api_keys.copy()
        random.shuffle(keys)
        
        last_error = None
        for api_key in keys:
            groq_client = Groq(api_key=api_key)
            models = get_live_models(api_key)
            for model in models:
                try:
                    # Fast-fail for the large models to avoid long buffering
                    current_timeout = 8.0 if "70b" in model else 15.0
                    
                    response = groq_client.chat.completions.create(
                        model=model,
                        max_tokens=max_tokens,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        timeout=current_timeout
                    )
                    print(f"DEBUG: AI DONE! Success! Key ...{api_key[-4:]} responded.")
                    return response.choices[0].message.content
                except Exception as e:
                    err = str(e)
                    print(f"DEBUG: Key ...{api_key[-4:]} failed/timed out: {err[:60]}")
                    last_error = e
                    continue
        if last_error:
            raise last_error
        return "{}"

    def generate_recipe(self, dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level, is_fusion):
        prompt = chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level)
        
        raw_chef = self._call_groq(prompt)
        recipe = self._parse_json(raw_chef)
        
        if not recipe:
            recipe = self._fallback_recipe(dish_hint, cuisine1, ingredients)

        # Use nutrition from the main recipe JSON if available
        nutrition = recipe.get("nutrition", {})
        
        # Verify nutrition is complete, otherwise use fallback (don't do a second slow call)
        if not nutrition or not isinstance(nutrition, dict) or not nutrition.get("per_serving"):
            nutrition = self._fallback_nutrition(dish_hint=dish_hint, ingredients=ingredients)

        simple_steps = []
        # Skill level is already handled in the main chef prompt. 
        # Disabling redundant teacher call to speed up performance.
        """
        if skill_level == "Beginner":
            try:
                # ... skipping second AI call ...
                pass
            except Exception:
                simple_steps = []
        """

        return {
            "recipe": recipe,
            "nutrition": nutrition,
            "simple_steps": simple_steps,
            "is_fusion": is_fusion,
            "fusion_cuisines": [cuisine1, cuisine2] if cuisine2 else [cuisine1],
            "cuisine_knowledge": {}
        }

    def _parse_json(self, text):
        try:
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0:
                return json.loads(text[start:end])
            return {}
        except Exception:
            return {}

    def _fallback_recipe(self, dish, cuisine, ingredients):
        return {
            "dish_name": f"Quick {cuisine} {dish}",
            "tagline": "A fast and tasty manual creation",
            "ingredients": ingredients,
            "cooking_steps": ["Prepare ingredients", "Cook until ready", "Serve warm"],
            "prep_time": "10m", "cook_time": "15m"
        }

    def _fallback_nutrition(self, dish_hint="", ingredients=None):
        return {
            "per_serving": {"calories": "Approx 350-450", "protein_g": "15-25", "carbs_g": "30-50", "fat_g": "10-20"},
            "health_benefits": ["Balanced macros", "Fresh ingredients"],
            "who_should_avoid": ["Always check for allergens"],
            "healthy_swaps": ["Reduce salt", "Use olive oil"],
            "best_time_to_eat": "Lunch or Dinner"
        }

CUISINE_KNOWLEDGE = {
    "Indian": "Spices, curry leaves, lentils, diverse regional styles.",
    "Italian": "Pasta, olive oil, tomatoes, basil, cheese.",
    "Mexican": "Corn, beans, chilies, lime, cilantro.",
    "Japanese": "Rice, soy sauce, seafood, umami, fermentation.",
    "Thai": "Lime, fish sauce, coconut milk, lemongrass, heat."
}
