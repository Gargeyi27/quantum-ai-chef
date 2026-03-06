"""
Advanced AI Recipe Brain - Hybrid Quantum-AI System
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
    },
    "Korean": {
        "techniques": ["fermentation", "grilling (grill)", "stir-frying", "steaming"],
        "flavor_base": "gochujang, soy sauce, sesame oil, garlic, ginger",
        "spices": "gochugaru, doenjang, sesame seeds, green onion",
        "regional": "Seoul (modern), Jeonju (traditional), Busan (seafood)"
    },
    "Greek": {
        "techniques": ["grilling", "slow roasting", "braising", "baking"],
        "flavor_base": "olive oil, lemon, garlic, oregano, tomato",
        "spices": "oregano, thyme, rosemary, cinnamon, mint",
        "regional": "Athens (modern), Islands (seafood), Northern (meat-heavy)"
    },
    "Spanish": {
        "techniques": ["sauteing", "slow braising", "grilling", "baking paella"],
        "flavor_base": "olive oil, garlic, tomato, saffron, paprika",
        "spices": "smoked paprika, saffron, cumin, parsley",
        "regional": "Catalonia (creative), Andalusia (fried), Basque (pintxos)"
    },
    "French": {
        "techniques": ["sauteing", "braising", "poaching", "flambeing"],
        "flavor_base": "butter, shallots, wine, cream, stock",
        "spices": "thyme, tarragon, bay leaf, herbes de Provence",
        "regional": "Provence (olive oil), Normandy (cream), Lyon (classic)"
    },
    "Middle Eastern": {
        "techniques": ["grilling", "slow roasting", "stewing", "frying"],
        "flavor_base": "olive oil, garlic, lemon, tahini, yogurt",
        "spices": "cumin, coriander, sumac, za'atar, cardamom, turmeric",
        "regional": "Lebanese (fresh), Persian (aromatic), Turkish (spiced)"
    },
    "Vietnamese": {
        "techniques": ["fresh assembly", "pho broth simmering", "grilling", "stir-frying"],
        "flavor_base": "fish sauce, lime, lemongrass, fresh herbs",
        "spices": "star anise, cinnamon, coriander, chili, mint",
        "regional": "Hanoi (subtle), Hue (spicy), Saigon (sweet)"
    },
    "Turkish": {
        "techniques": ["grilling", "slow braising", "baking", "stuffing"],
        "flavor_base": "olive oil, onion, garlic, tomato, yogurt",
        "spices": "cumin, sumac, paprika, mint, cinnamon",
        "regional": "Istanbul (fusion), Anatolia (hearty), Aegean (olive oil)"
    },
    "Ethiopian": {
        "techniques": ["slow stewing", "injera making", "spice blending", "frying"],
        "flavor_base": "berbere, niter kibbeh, onion, garlic, ginger",
        "spices": "berbere, mitmita, fenugreek, turmeric, cardamom",
        "regional": "Addis Ababa (modern), Tigray (traditional), Oromia (spiced)"
    },
}


def chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion, skill_level):
    fusion_note = ""
    if is_fusion and cuisine2:
        fusion_note = f"""
FUSION RECIPE RULES:
- This is a {cuisine1} x {cuisine2} FUSION dish
- Combine cooking techniques from BOTH {cuisine1} AND {cuisine2}
- The dish name MUST reflect both cultures (e.g. Tikka Masala Pasta for Indian x Italian)
- Use spices and flavor profiles from BOTH cuisines creatively
"""

    diet_note = "STRICTLY VEGETARIAN - NO meat, NO chicken, NO beef, NO pork, NO fish, NO shrimp, NO seafood whatsoever" if veg else "Non-Vegetarian - can include meat, poultry, seafood as appropriate"

    quantum_ingredients = ", ".join(ingredients)

    return f"""You are a Michelin 3-star professional chef with 30 years of experience. You MUST create an EXTREMELY DETAILED and COMPLETE recipe.

DISH: {dish_hint}
CUISINE: {cuisine1}{" x " + cuisine2 if is_fusion and cuisine2 else ""}
{fusion_note}
DIET: {diet_note}
SKILL LEVEL: {skill_level}
QUANTUM-OPTIMIZED BASE INGREDIENTS: {quantum_ingredients}

=== STRICT INGREDIENT RULES (VERY IMPORTANT) ===
You MUST list AT LEAST 20 ingredients. No exceptions.
Include ALL of the following categories:
1. MAIN INGREDIENT of the dish (e.g. for biryani: basmati rice AND meat/paneer)
2. ALL vegetables needed
3. ALL spices individually (e.g. cumin seeds, coriander powder, turmeric, garam masala separately)
4. ALL liquids (water, broth, cream, coconut milk, stock etc with exact ml/cups)
5. ALL aromatics (garlic, ginger, onion, shallots etc)
6. ALL oils, butter, ghee with exact amounts
7. ALL garnishes (fresh herbs, lemon, cream, nuts etc)
8. ALL pantry staples (salt, pepper, sugar if needed)
9. ALL sauces, pastes (tomato puree, soy sauce, fish sauce etc)
10. ALL additional flavor enhancers (bay leaves, cardamom, cloves etc)

NEVER use "as needed" or "to taste" alone - always give exact amounts.
Every ingredient MUST have:
- Exact amount with unit (e.g. "2 tablespoons", "200 grams", "1.5 cups")
- Preparation note (e.g. "finely chopped", "freshly grated", "soaked 30 minutes")

=== STRICT STEP RULES (VERY IMPORTANT) ===
You MUST write AT LEAST 12 detailed cooking steps. No exceptions.
Each step MUST include:
- Exact temperature in Celsius AND Fahrenheit
- Exact cooking time in minutes
- Precise technique with explanation of WHY
- What could go wrong and how to avoid it
- Sensory cue (what to see, smell, hear)
- A beginner tip

Include these as SEPARATE steps:
- Ingredient preparation (washing, chopping, marinating)
- Making the base/sauce
- Cooking main protein or main ingredient
- Adding spices and building flavor
- Final assembly
- Plating and garnishing

CRITICAL: Respond ONLY with valid JSON. No markdown, no text outside JSON. Keep each ingredient note under 10 words. Keep each step instruction under 100 words. The entire JSON must be complete and valid:
{{
  "dish_name": "Creative authentic name for {dish_hint}",
  "tagline": "One irresistible mouth-watering sentence",
  "cuisine_type": "{cuisine1}{" x " + cuisine2 if is_fusion and cuisine2 else ""}",
  "serves": 2,
  "prep_time": "X minutes",
  "cook_time": "X minutes",
  "difficulty": "{skill_level}",
  "ingredients": [
    {{"name": "ingredient 1", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 2", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 3", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 4", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 5", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 6", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 7", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 8", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 9", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 10", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 11", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 12", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 13", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 14", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 15", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 16", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 17", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 18", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 19", "amount": "exact amount with unit", "note": "detailed prep note"}},
    {{"name": "ingredient 20", "amount": "exact amount with unit", "note": "detailed prep note"}}
  ],
  "equipment_needed": ["equipment1", "equipment2", "equipment3", "equipment4", "equipment5"],
  "cooking_steps": [
    {{
      "step": 1,
      "title": "Clear Descriptive Title",
      "instruction": "Write 4-5 detailed sentences. Include exact temperature in Celsius AND Fahrenheit. Include exact time. Explain the technique clearly. Explain WHY this step is important. Mention what could go wrong.",
      "tip": "Very specific helpful tip for a beginner for this exact step",
      "sensory_cue": "Exactly what you should see, smell, hear or feel when this step is done correctly",
      "time": "X minutes"
    }},
    {{
      "step": 2,
      "title": "Clear Descriptive Title",
      "instruction": "Write 4-5 detailed sentences with exact temp, time and technique.",
      "tip": "Specific tip for this step",
      "sensory_cue": "What to look/smell/hear for",
      "time": "X minutes"
    }}
  ],
  "plating": "Very detailed plating and garnish instructions for a beautiful restaurant-quality presentation",
  "chef_tips": ["Professional tip 1", "Professional tip 2", "Storage instructions", "Reheating tip", "Serving suggestion"],
  "variations": ["Variation 1 with description", "Variation 2 with description", "Variation 3 with description"],
  "substitutions": [
    {{"original": "ingredient", "substitute": "alternative ingredient", "flavor_impact": "exactly how the taste and texture changes"}}
  ],
  "nutrition": {{
    "per_serving": {{
      "calories": CALCULATE_ACCURATE_calories_for_{dish_hint},
      "protein_g": CALCULATE_ACCURATE_protein,
      "carbs_g": CALCULATE_ACCURATE_carbs,
      "fat_g": CALCULATE_ACCURATE_fat,
      "fiber_g": CALCULATE_ACCURATE_fiber,
      "sodium_mg": CALCULATE_ACCURATE_sodium
    }},
    "health_benefits": ["specific benefit from actual ingredients used", "specific benefit 2", "specific benefit 3"],
    "who_should_avoid": ["specific dietary restriction 1", "specific restriction 2"],
    "dietary_tags": ["tag1", "tag2"],
    "healthy_swaps": ["specific swap for THIS dish", "specific swap 2"],
    "best_time_to_eat": "when and why this dish is best eaten"
  }}
}}"""


def nutrition_agent_prompt(dish_name, ingredients):
    ing_list = ', '.join(ingredients)
    return f"""You are a certified nutritionist with 20 years experience. Calculate ACCURATE nutrition for {dish_name}.

Ingredients: {ing_list}

CRITICAL RULES:
- Calculate REALISTIC values for THIS specific dish - do NOT use generic placeholder values
- Butter chicken: ~450 cal, 35g protein, 15g carbs, 28g fat
- Biryani: ~550 cal, 25g protein, 65g carbs, 18g fat  
- Pasta with cream: ~600 cal, 18g protein, 70g carbs, 25g fat
- Vegetable soup: ~120 cal, 5g protein, 18g carbs, 3g fat
- Caesar salad: ~350 cal, 12g protein, 15g carbs, 28g fat
- Use these as reference and calculate accurately for {dish_name}
- Health benefits must be SPECIFIC to the actual ingredients (e.g. turmeric = anti-inflammatory)
- Healthy swaps must be SPECIFIC to this dish

Respond ONLY with valid JSON, no markdown, no extra text:
{{
  "per_serving": {{
    "calories": CALCULATE_REALISTIC_VALUE,
    "protein_g": CALCULATE_REALISTIC_VALUE,
    "carbs_g": CALCULATE_REALISTIC_VALUE,
    "fat_g": CALCULATE_REALISTIC_VALUE,
    "fiber_g": CALCULATE_REALISTIC_VALUE,
    "sodium_mg": CALCULATE_REALISTIC_VALUE
  }},
  "health_benefits": ["specific benefit from actual ingredient 1", "specific benefit 2", "specific benefit 3"],
  "who_should_avoid": ["specific group 1", "specific group 2"],
  "dietary_tags": ["tag1", "tag2", "tag3"],
  "healthy_swaps": ["specific swap for this dish 1", "specific swap 2"],
  "best_time_to_eat": "when this dish is best eaten and why"
}}"""


def teacher_agent_prompt(cooking_steps, skill_level):
    steps_text = json.dumps(cooking_steps)
    return f"""Rewrite these steps for a complete beginner: {steps_text}

Respond ONLY with valid JSON array, no markdown:
[
  {{
    "step": 1,
    "simple_instruction": "Simple instruction anyone can follow",
    "sensory_cue": "what you see or smell",
    "safety_note": "what to watch out for",
    "emoji_guide": "relevant emoji"
  }}
]"""


class AIRecipeBrain:
    def __init__(self):
        # All available Groq free tier models - rotates on rate limit
        # Ordered by output token capacity (highest first)
        self.models = [
            "openai/gpt-oss-120b",                           # 65k out - highest capacity
            "openai/gpt-oss-20b",                            # 65k out
            "llama-3.1-8b-instant",                          # 131k out - very high
            "qwen/qwen3-32b",                                # 40k out
            "moonshotai/kimi-k2-instruct-0905",              # 16k out, 262k context
            "moonshotai/kimi-k2-instruct",                   # 16k out
            "llama-3.3-70b-versatile",                       # 32k out - best quality
            "meta-llama/llama-4-maverick-17b-128e-instruct", # 8k out
            "meta-llama/llama-4-scout-17b-16e-instruct",     # 8k out
            "groq/compound",                                 # 8k out
            "groq/compound-mini",                            # 8k out
        ]
        self.model = self.models[0]

    def _call_groq(self, prompt, max_tokens=8000):
        messages = [{"role": "user", "content": prompt}]
        last_error = None
        for model in self.models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=messages
                )
                if model != self.models[0]:
                    print(f"Used fallback model: {model}")
                return response.choices[0].message.content
            except Exception as e:
                if "rate_limit" in str(e) or "429" in str(e):
                    print(f"Rate limit on {model}, trying next...")
                    last_error = e
                    continue
                raise e
        raise last_error

    def _parse_json(self, text):
        import re
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        replacements = [("‑","-"),("‒","-"),("–","-"),("—","-"),
            ("‘","'"),("’","'"),("“",'"'),("”",'"'),
            ("½","1/2"),("¼","1/4"),("¾","3/4"),(" "," "),(" "," ")]
        for code, repl in replacements:
            text = text.replace(code, repl)
        start = text.find("{")
        end = text.rfind("}") + 1
        if start < 0 or end <= start:
            return {}
        raw = text[start:end]
        try:
            return json.loads(raw)
        except Exception:
            pass
        fixed = []
        in_string = False
        escape_next = False
        for ch in raw:
            if escape_next:
                fixed.append(ch)
                escape_next = False
            elif ch == chr(92):
                fixed.append(ch)
                escape_next = True
            elif ch == chr(34) and not escape_next:
                fixed.append(ch)
                in_string = not in_string
            elif in_string and ch in (chr(10), chr(13), chr(9)):
                fixed.append(" ")
            else:
                fixed.append(ch)
        try:
            return json.loads("".join(fixed))
        except Exception:
            pass
        try:
            return json.loads("".join(fixed), strict=False)
        except Exception:
            pass
        return {}

    def generate_recipe(self, dish_hint, cuisine1, cuisine2, veg, ingredients, skill_level="Beginner", is_fusion=False):
        is_fusion = is_fusion or (cuisine2 is not None and cuisine2 != cuisine1)

        try:
            prompt = chef_agent_prompt(dish_hint, cuisine1, cuisine2, veg, ingredients, is_fusion, skill_level)
            raw = self._call_groq(prompt, max_tokens=8000)
            recipe = self._parse_json(raw)
            if not recipe:
                print("WARNING: JSON parse failed. Raw response:", raw[:500])
        except Exception as e:
            print("ERROR in chef agent:", str(e))
            recipe = {}

        if not recipe:
            recipe = self._fallback_recipe(dish_hint, cuisine1, ingredients)

        # Extract nutrition from recipe response (included in main prompt)
        nutrition = recipe.pop("nutrition", {}) if isinstance(recipe, dict) else {}
        
        # Validate nutrition has real values not placeholder text
        per_s = nutrition.get("per_serving", {}) if isinstance(nutrition, dict) else {}
        cal = per_s.get("calories", 0)
        if not nutrition or not isinstance(nutrition, dict) or not per_s or not isinstance(cal, (int, float)) or cal == 0:
            # Fallback: make separate nutrition call
            try:
                ing_names = [i.get("name", i) if isinstance(i, dict) else i for i in recipe.get("ingredients", ingredients)]
                prompt2 = nutrition_agent_prompt(recipe.get("dish_name", dish_hint), ing_names)
                raw2 = self._call_groq(prompt2, max_tokens=1500)
                nutrition = self._parse_json(raw2)
            except Exception:
                nutrition = {}

        if not nutrition or isinstance(nutrition, list):
            nutrition = self._fallback_nutrition(dish_hint=dish_hint, ingredients=ingredients)
        if not isinstance(nutrition.get("per_serving"), dict):
            nutrition = self._fallback_nutrition(dish_hint=dish_hint, ingredients=ingredients)
        # Final check - if calories is still placeholder text, use fallback
        cal_val = nutrition.get("per_serving", {}).get("calories", 0)
        if not isinstance(cal_val, (int, float)) or cal_val == 0:
            nutrition = self._fallback_nutrition(dish_hint=dish_hint, ingredients=ingredients)

        simple_steps = []
        if skill_level == "Beginner":
            try:
                prompt3 = teacher_agent_prompt(recipe.get("cooking_steps", []), skill_level)
                raw3 = self._call_groq(prompt3, max_tokens=2000)
                raw3 = raw3.strip()
                if "```json" in raw3:
                    raw3 = raw3.split("```json")[1].split("```")[0].strip()
                elif "```" in raw3:
                    raw3 = raw3.split("```")[1].split("```")[0].strip()
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
            "dish_name": f"{cuisine} {dish_hint.title()}",
            "tagline": f"A delicious authentic {cuisine} dish",
            "cuisine_type": cuisine,
            "serves": 2,
            "prep_time": "15 minutes",
            "cook_time": "25 minutes",
            "difficulty": "Easy",
            "ingredients": [
                {"name": "salt", "amount": "1 teaspoon", "note": "or to taste"},
                {"name": "black pepper", "amount": "1/2 teaspoon", "note": "freshly ground"},
                {"name": "olive oil", "amount": "2 tablespoons", "note": "for cooking"},
                {"name": "garlic", "amount": "3 cloves", "note": "minced"},
                {"name": "onion", "amount": "1 large", "note": "finely diced"},
                {"name": "fresh herbs", "amount": "2 tablespoons", "note": "chopped for garnish"},
            ],
            "equipment_needed": ["Pan", "Knife", "Cutting board"],
            "cooking_steps": [
                {"step": 1, "title": "Prepare Ingredients", "instruction": "Wash and chop all ingredients into even pieces. Keep everything in separate bowls ready to use.", "tip": "Prep before turning on heat.", "sensory_cue": "Everything clean and ready.", "time": "10 minutes"},
                {"step": 2, "title": "Heat Oil", "instruction": "Place pan over medium heat. Add oil and heat 60 seconds until shimmering.", "tip": "Never let oil smoke.", "sensory_cue": "Oil shimmers when ready.", "time": "2 minutes"},
                {"step": 3, "title": "Cook Aromatics", "instruction": "Add onion and garlic. Stir every 30 seconds for 3 minutes until golden.", "tip": "Keep stirring to avoid burning.", "sensory_cue": "Sweet fragrant aroma.", "time": "3 minutes"},
                {"step": 4, "title": "Add Main Ingredients", "instruction": "Add remaining ingredients. Cook on medium-high for 5-7 minutes stirring occasionally.", "tip": "Don't overcrowd pan.", "sensory_cue": "Steady sizzle.", "time": "7 minutes"},
                {"step": 5, "title": "Season and Finish", "instruction": "Add salt, pepper, spices. Stir well. Taste and adjust. Cook 2 more minutes.", "tip": "Season gradually.", "sensory_cue": "Rich spiced aroma.", "time": "2 minutes"},
                {"step": 6, "title": "Plate and Serve", "instruction": "Transfer to warm plates. Garnish and serve hot.", "tip": "Warm plates keep food hot longer.", "sensory_cue": "Colorful and appetizing.", "time": "2 minutes"}
            ],
            "plating": "Serve in a warm bowl with fresh herb garnish",
            "chef_tips": ["Use fresh ingredients", "Season at every stage", "Serve immediately"],
            "variations": ["Add chili for heat", "Add lemon for brightness"],
            "substitutions": []
        }

    def _fallback_nutrition(self, dish_hint="", ingredients=None):
        dish = dish_hint.lower() if dish_hint else ""
        ings = str(ingredients or []).lower()

        # Dish-specific nutrition data
        if any(x in dish for x in ["biryani","pulao"]):
            cal,pro,carb,fat,fib,sod = 520,22,65,16,4,680
            benefits = ["Basmati rice provides quick energy and is easy to digest","Whole spices like cardamom and cloves are rich in antioxidants","Saffron contains anti-inflammatory compounds"]
            swaps = ["Use brown rice instead of white for more fiber","Reduce ghee by half and use olive oil","Add extra vegetables like peas and carrots for nutrients"]
            avoid = ["People with gluten sensitivity should check spice blends","Those on low-carb diets due to high rice content"]
            best = "Best enjoyed at lunch when digestion is strongest"
        elif any(x in dish for x in ["butter chicken","murgh makhani"]):
            cal,pro,carb,fat,fib,sod = 420,35,18,25,3,720
            benefits = ["Chicken is an excellent source of lean protein for muscle repair","Tomatoes provide lycopene which supports heart health","Spices like turmeric have powerful anti-inflammatory effects"]
            swaps = ["Use Greek yogurt instead of cream to reduce fat","Replace butter with olive oil for heart health","Use skinless chicken breast to lower calories"]
            avoid = ["Individuals with lactose intolerance due to cream and butter","People on low-sodium diets"]
            best = "Best enjoyed at dinner with naan or rice"
        elif any(x in dish for x in ["tikka","masala","korma","curry"]):
            cal,pro,carb,fat,fib,sod = 380,30,20,22,4,680
            benefits = ["Spices like cumin and coriander aid digestion","Chicken provides complete protein with all essential amino acids","Ginger and garlic have natural antibacterial properties"]
            swaps = ["Use coconut milk instead of cream for dairy-free option","Reduce oil by half and add water when cooking","Use more vegetables to increase fiber content"]
            avoid = ["People with dairy allergies if cream is used","Those with nightshade sensitivity due to tomatoes"]
            best = "Best enjoyed at lunch or dinner with flatbread"
        elif any(x in dish for x in ["pasta","spaghetti","carbonara","lasagna"]):
            cal,pro,carb,fat,fib,sod = 580,18,72,22,5,540
            benefits = ["Pasta provides sustained energy through complex carbohydrates","Tomato sauce is rich in lycopene and vitamin C","Olive oil contains heart-healthy monounsaturated fats"]
            swaps = ["Use whole wheat pasta for more fiber and nutrients","Replace heavy cream with Greek yogurt","Add spinach or zucchini to boost vegetable content"]
            avoid = ["People with gluten intolerance or celiac disease","Those on low-carb or keto diets"]
            best = "Best enjoyed at lunch for sustained afternoon energy"
        elif any(x in dish for x in ["soup","broth","dal","lentil"]):
            cal,pro,carb,fat,fib,sod = 180,10,24,5,8,480
            benefits = ["High fiber content supports healthy digestion","Plant-based protein from lentils is heart-friendly","Low calorie and filling making it ideal for weight management"]
            swaps = ["Reduce salt and use herbs for flavor instead","Add a squeeze of lemon for extra vitamin C","Use low-sodium broth to reduce sodium content"]
            avoid = ["People with kidney issues should monitor potassium intake","Those with legume allergies"]
            best = "Excellent as a light dinner or starter any time of day"
        elif any(x in dish for x in ["salad","slaw"]):
            cal,pro,carb,fat,fib,sod = 220,8,18,14,6,320
            benefits = ["Raw vegetables retain maximum vitamins and minerals","High fiber content promotes healthy digestion","Low calorie and hydrating making it perfect for weight loss"]
            swaps = ["Use lemon juice instead of dressing to reduce calories","Add chickpeas or grilled chicken for more protein","Replace croutons with nuts for healthy fats"]
            avoid = ["People on blood thinners should monitor vitamin K from leafy greens","Those with irritable bowel syndrome may need to avoid raw vegetables"]
            best = "Perfect as a light lunch or side dish"
        elif any(x in dish for x in ["burger","sandwich","wrap"]):
            cal,pro,carb,fat,fib,sod = 520,28,42,24,4,860
            benefits = ["Good source of protein from meat or legumes","Iron and zinc from beef support immune function","Whole grain bun provides fiber and B vitamins"]
            swaps = ["Use lettuce wrap instead of bun to reduce carbs","Choose lean turkey or chicken patty instead of beef","Add avocado instead of cheese for healthy fats"]
            avoid = ["People on low-sodium diets due to sauces and processed cheese","Those with gluten intolerance due to bun"]
            best = "Best enjoyed at lunch for an energizing midday meal"
        elif any(x in dish for x in ["pizza"]):
            cal,pro,carb,fat,fib,sod = 480,20,55,18,4,780
            benefits = ["Tomato sauce provides lycopene a powerful antioxidant","Cheese delivers calcium for strong bones and teeth","Whole grain crust adds fiber and essential minerals"]
            swaps = ["Use cauliflower crust for a low-carb alternative","Reduce cheese and add more vegetables as toppings","Use part-skim mozzarella to lower saturated fat"]
            avoid = ["People with lactose intolerance due to cheese","Those with gluten sensitivity due to wheat crust"]
            best = "Best enjoyed at dinner as a sharing meal"
        elif any(x in dish for x in ["shawarma","kebab"]):
            cal,pro,carb,fat,fib,sod = 450,35,30,18,3,820
            benefits = ["High protein from grilled meat supports muscle growth","Garlic and herbs provide natural antimicrobial benefits","Spices like cumin and paprika are rich in antioxidants"]
            swaps = ["Use whole wheat pita instead of white for more fiber","Add more salad vegetables for vitamins and minerals","Use low-fat yogurt sauce instead of tahini to reduce calories"]
            avoid = ["People on low-sodium diets due to marinades and sauces","Those with gluten sensitivity should avoid pita bread"]
            best = "Great as a satisfying lunch or post-workout dinner"
        elif any(x in dish for x in ["naan","roti","paratha","bread"]):
            cal,pro,carb,fat,fib,sod = 300,8,48,10,3,420
            benefits = ["Provides quick energy from carbohydrates","Contains B vitamins essential for energy metabolism","Pairs well with protein-rich dishes for balanced nutrition"]
            swaps = ["Use whole wheat flour for more fiber and nutrients","Reduce butter or ghee topping by half","Try baking instead of frying for lower fat content"]
            avoid = ["People with gluten intolerance or celiac disease","Those on low-carb or keto diets"]
            best = "Best enjoyed fresh at lunch or dinner"
        elif any(x in dish for x in ["rice","pulao","fried rice"]):
            cal,pro,carb,fat,fib,sod = 400,10,75,8,2,480
            benefits = ["Provides quick energy from easily digestible carbohydrates","Gluten-free and suitable for most dietary needs","Fortified with B vitamins supporting energy metabolism"]
            swaps = ["Use cauliflower rice for a low-carb alternative","Add vegetables like peas and carrots for more nutrition","Use brown rice for significantly more fiber"]
            avoid = ["People with diabetes should monitor portion sizes","Those on strict low-carb diets"]
            best = "Best enjoyed at lunch for sustained afternoon energy"
        else:
            cal,pro,carb,fat,fib,sod = 380,18,40,14,5,520
            benefits = ["Provides a balanced mix of macronutrients for sustained energy","Contains essential vitamins and minerals for overall health","Homemade meals are lower in preservatives than processed food"]
            swaps = ["Reduce oil or butter by half to lower calorie content","Add more vegetables to increase fiber and vitamin intake","Use herbs and spices instead of salt for flavoring"]
            avoid = ["Check all ingredients for personal food allergies","Consult a nutritionist for specific dietary requirements"]
            best = "Best enjoyed fresh as part of a balanced meal"

        return {
            "per_serving": {
                "calories": cal, "protein_g": pro, "carbs_g": carb,
                "fat_g": fat, "fiber_g": fib, "sodium_mg": sod
            },
            "health_benefits": benefits,
            "who_should_avoid": avoid,
            "dietary_tags": ["Balanced", "Homemade"],
            "healthy_swaps": swaps,
            "best_time_to_eat": best
        }
        