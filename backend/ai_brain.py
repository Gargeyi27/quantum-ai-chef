"""
Advanced AI Recipe Brain - Hybrid Quantum-AI System
"""

import json
import os
from typing import List, Dict, Optional
from groq import Groq

client = Groq(api_key="GROQ_API_KEY")

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
        "techniques": ["fermentation", "grilling", "stir-frying", "steaming"],
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
        fusion_note = (
            "FUSION RECIPE RULES:\n"
            "- This is a " + cuisine1 + " x " + cuisine2 + " FUSION dish\n"
            "- Combine cooking techniques from BOTH " + cuisine1 + " AND " + cuisine2 + "\n"
            "- The dish name MUST reflect both cultures\n"
            "- Use spices and flavor profiles from BOTH cuisines creatively\n"
        )

    diet_note = "STRICTLY VEGETARIAN - NO meat, NO chicken, NO beef, NO pork, NO fish, NO shrimp, NO seafood whatsoever" if veg else "Non-Vegetarian - can include meat, poultry, seafood as appropriate"
    quantum_ingredients = ", ".join(ingredients)
    cuisine_display = cuisine1 + (" x " + cuisine2 if is_fusion and cuisine2 else "")

    prompt = (
        "You are a Michelin 3-star professional chef with 30 years of experience.\n\n"
        "DISH: " + dish_hint + "\n"
        "CUISINE: " + cuisine_display + "\n"
        "DIET: " + diet_note + "\n"
        "SKILL LEVEL: " + skill_level + "\n"
        "BASE INGREDIENTS: " + quantum_ingredients + "\n"
        + fusion_note +
        "\n=== MANDATORY RULES ===\n"
        "1. List MINIMUM 20 ingredients with exact amounts and detailed prep notes.\n"
        "2. Write MINIMUM 15 cooking steps. Each step MUST have 6-7 sentences: what to do, exact temp C and F, exact time, why this step matters, what goes wrong if you rush it, how a beginner knows they are doing it right.\n"
        "3. tip field: practical beginner advice for that specific step.\n"
        "4. sensory_cue field: exactly what to SEE, SMELL or HEAR at this step.\n"
        "5. RESPOND ONLY WITH VALID JSON. No markdown, no text outside JSON.\n\n"
        '{\n'
        '  "dish_name": "Authentic name for ' + dish_hint + '",\n'
        '  "tagline": "One irresistible sentence",\n'
        '  "cuisine_type": "' + cuisine_display + '",\n'
        '  "serves": 2,\n'
        '  "prep_time": "X minutes",\n'
        '  "cook_time": "X minutes",\n'
        '  "difficulty": "' + skill_level + '",\n'
        '  "ingredients": [\n'
        '    {"name": "ingredient 1", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 2", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 3", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 4", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 5", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 6", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 7", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 8", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 9", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 10", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 11", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 12", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 13", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 14", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 15", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 16", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 17", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 18", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 19", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 20", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 21", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 22", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 23", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 24", "amount": "exact amount", "note": "prep note"},\n'
        '    {"name": "ingredient 25", "amount": "exact amount", "note": "prep note"}\n'
        '  ],\n'
        '  "equipment_needed": ["item1", "item2", "item3", "item4", "item5"],\n'
        '  "cooking_steps": [\n'
        '    {"step": 1, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 2, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 3, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 4, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 5, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 6, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 7, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 8, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 9, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 10, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 11, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 12, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 13, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 14, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"},\n'
        '    {"step": 15, "title": "title", "instruction": "detailed instruction", "tip": "tip", "sensory_cue": "cue", "time": "X min"}\n'
        '  ],\n'
        '  "plating": "Detailed restaurant-quality plating instructions",\n'
        '  "chef_tips": ["tip1", "tip2", "storage tip", "reheating tip", "serving tip"],\n'
        '  "variations": ["variation 1", "variation 2", "variation 3"],\n'
        '  "substitutions": [{"original": "ingredient", "substitute": "alternative", "flavor_impact": "how taste changes"}],\n'
        '  "nutrition": {\n'
        '    "per_serving": {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "sodium_mg": 0},\n'
        '    "health_benefits": ["benefit1", "benefit2", "benefit3"],\n'
        '    "who_should_avoid": ["restriction1", "restriction2"],\n'
        '    "dietary_tags": ["tag1", "tag2"],\n'
        '    "healthy_swaps": ["swap1", "swap2"],\n'
        '    "best_time_to_eat": "when and why"\n'
        '  }\n'
        '}'
    )
    return prompt


def nutrition_agent_prompt(dish_name, ingredients):
    ing_list = ', '.join(ingredients)
    return (
        "You are a certified nutritionist. Calculate ACCURATE nutrition for " + dish_name + ".\n"
        "Ingredients: " + ing_list + "\n\n"
        "Calculate REALISTIC values for THIS specific dish.\n"
        "Reference: Butter chicken ~450cal/35g protein, Biryani ~550cal/25g protein, Pasta ~580cal/18g protein\n"
        "Health benefits must be SPECIFIC to actual ingredients used.\n\n"
        "Respond ONLY with valid JSON, no markdown:\n"
        '{\n'
        '  "per_serving": {\n'
        '    "calories": 400,\n'
        '    "protein_g": 25,\n'
        '    "carbs_g": 30,\n'
        '    "fat_g": 15,\n'
        '    "fiber_g": 4,\n'
        '    "sodium_mg": 600\n'
        '  },\n'
        '  "health_benefits": ["benefit1", "benefit2", "benefit3"],\n'
        '  "who_should_avoid": ["group1", "group2"],\n'
        '  "dietary_tags": ["tag1", "tag2"],\n'
        '  "healthy_swaps": ["swap1", "swap2"],\n'
        '  "best_time_to_eat": "when and why"\n'
        '}'
    )


def teacher_agent_prompt(cooking_steps, skill_level):
    steps_text = json.dumps(cooking_steps)
    return (
        "Rewrite these cooking steps for a complete beginner: " + steps_text + "\n\n"
        "Respond ONLY with valid JSON array, no markdown:\n"
        "[\n"
        '  {\n'
        '    "step": 1,\n'
        '    "simple_instruction": "Simple instruction anyone can follow",\n'
        '    "sensory_cue": "what you see or smell",\n'
        '    "safety_note": "what to watch out for",\n'
        '    "emoji_guide": "relevant emoji"\n'
        '  }\n'
        "]"
    )


class AIRecipeBrain:
    def __init__(self):
        self.models = [
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "moonshotai/kimi-k2-instruct-0905",
            "qwen/qwen-3-32b",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
        ]
        self.model = self.models[0]
        print("AI brain loaded OK")

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
                print(f"Model {model} failed: {str(e)[:80]}, trying next...")
                last_error = e
                continue
        raise last_error

    def _parse_json(self, text):
        text = text.strip()
        # Remove all markdown
        for fence in ["```json", "```JSON", "```", "~~~"]:
            text = text.replace(fence, "")
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        replacements = [
            ("\u2011", "-"), ("\u2012", "-"), ("\u2013", "-"), ("\u2014", "-"),
            ("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
            ("\u00bd", "1/2"), ("\u00bc", "1/4"), ("\u00be", "3/4"),
            ("\u2009", " "), ("\u00a0", " ")
        ]
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
            print("DEBUG: Prompt OK, length:", len(prompt))
            raw = self._call_groq(prompt, max_tokens=6000)
            print("DEBUG: Response length:", len(raw))
            print("DEBUG: First 200 chars:", raw[:200])
            recipe = self._parse_json(raw)
            if not recipe:
                print("WARNING: JSON parse failed. Raw:", raw[:500])
            else:
                print("DEBUG: ingredients:", len(recipe.get("ingredients", [])), "steps:", len(recipe.get("cooking_steps", [])))
        except Exception as e:
            import traceback
            print("ERROR in chef agent:", str(e))
            traceback.print_exc()
            recipe = {}

        if not recipe:
            recipe = self._fallback_recipe(dish_hint, cuisine1, ingredients)

        nutrition = recipe.pop("nutrition", {}) if isinstance(recipe, dict) else {}
        per_s = nutrition.get("per_serving", {}) if isinstance(nutrition, dict) else {}
        cal = per_s.get("calories", 0)
        if not nutrition or not isinstance(nutrition, dict) or not per_s or not isinstance(cal, (int, float)) or cal == 0:
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
            "dish_name": cuisine + " " + dish_hint.title(),
            "tagline": "A delicious authentic " + cuisine + " dish",
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
                {"step": 1, "title": "Prepare Ingredients", "instruction": "Wash and chop all ingredients into even pieces.", "tip": "Prep before turning on heat.", "sensory_cue": "Everything clean and ready.", "time": "10 minutes"},
                {"step": 2, "title": "Heat Oil", "instruction": "Place pan over medium heat 180C/350F. Add oil, heat 60 seconds.", "tip": "Never let oil smoke.", "sensory_cue": "Oil shimmers when ready.", "time": "2 minutes"},
                {"step": 3, "title": "Cook Aromatics", "instruction": "Add onion and garlic at 160C/320F. Stir every 30 seconds for 3 minutes.", "tip": "Keep stirring to avoid burning.", "sensory_cue": "Sweet fragrant aroma.", "time": "3 minutes"},
                {"step": 4, "title": "Add Main Ingredients", "instruction": "Add main ingredients at 180C/350F. Cook 5-7 minutes stirring occasionally.", "tip": "Don't overcrowd pan.", "sensory_cue": "Steady sizzle.", "time": "7 minutes"},
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

        if any(x in dish for x in ["biryani", "pulao"]):
            cal,pro,carb,fat,fib,sod = 520,22,65,16,4,680
            benefits = ["Basmati rice provides quick energy","Whole spices like cardamom are rich in antioxidants","Saffron contains anti-inflammatory compounds"]
            swaps = ["Use brown rice for more fiber","Reduce ghee by half","Add vegetables like peas and carrots"]
            avoid = ["People on low-carb diets","Those with gluten sensitivity should check spice blends"]
            best = "Best enjoyed at lunch when digestion is strongest"
        elif any(x in dish for x in ["butter chicken", "murgh makhani"]):
            cal,pro,carb,fat,fib,sod = 420,35,18,25,3,720
            benefits = ["Chicken is an excellent source of lean protein","Tomatoes provide lycopene for heart health","Turmeric has powerful anti-inflammatory effects"]
            swaps = ["Use Greek yogurt instead of cream","Replace butter with olive oil","Use skinless chicken breast"]
            avoid = ["Lactose intolerant individuals","People on low-sodium diets"]
            best = "Best enjoyed at dinner with naan or rice"
        elif any(x in dish for x in ["tikka", "masala", "korma", "curry"]):
            cal,pro,carb,fat,fib,sod = 380,30,20,22,4,680
            benefits = ["Cumin and coriander aid digestion","Chicken provides complete protein","Ginger and garlic have antibacterial properties"]
            swaps = ["Use coconut milk instead of cream","Reduce oil by half","Add more vegetables for fiber"]
            avoid = ["People with dairy allergies","Those with nightshade sensitivity"]
            best = "Best enjoyed at lunch or dinner with flatbread"
        elif any(x in dish for x in ["pasta", "spaghetti", "carbonara", "lasagna"]):
            cal,pro,carb,fat,fib,sod = 580,18,72,22,5,540
            benefits = ["Pasta provides sustained energy","Tomato sauce is rich in lycopene","Olive oil contains heart-healthy fats"]
            swaps = ["Use whole wheat pasta for more fiber","Replace cream with Greek yogurt","Add spinach or zucchini"]
            avoid = ["People with gluten intolerance","Those on low-carb diets"]
            best = "Best enjoyed at lunch for sustained energy"
        elif any(x in dish for x in ["soup", "broth", "dal", "lentil"]):
            cal,pro,carb,fat,fib,sod = 180,10,24,5,8,480
            benefits = ["High fiber supports digestion","Plant-based protein is heart-friendly","Low calorie and filling"]
            swaps = ["Use herbs instead of salt","Add lemon for vitamin C","Use low-sodium broth"]
            avoid = ["People with kidney issues","Those with legume allergies"]
            best = "Excellent as a light dinner or starter"
        else:
            cal,pro,carb,fat,fib,sod = 380,18,40,14,5,520
            benefits = ["Balanced macronutrients for sustained energy","Essential vitamins and minerals","Lower in preservatives than processed food"]
            swaps = ["Reduce oil by half","Add more vegetables","Use herbs instead of salt"]
            avoid = ["Check all ingredients for personal allergies","Consult a nutritionist for specific requirements"]
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





















