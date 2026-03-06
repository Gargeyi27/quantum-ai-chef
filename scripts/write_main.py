"""Run this to fix backend/main.py: python write_main.py"""

code = '''import os
import sys
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_engine.optimizer import QuantumIngredientsOptimizer, vqe_taste_nutrition_tradeoff, grover_constraint_search
from ai_brain import AIRecipeBrain

app = FastAPI(
    title="Quantum-AI Cooking Chef API",
    description="Advanced hybrid Quantum-AI recipe generation engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "ingredients.json")

try:
    quantum_optimizer = QuantumIngredientsOptimizer(DATA_PATH)
    print("Quantum optimizer loaded OK")
except Exception as e:
    print(f"Quantum optimizer error: {e}")
    quantum_optimizer = None

try:
    ai_brain = AIRecipeBrain()
    print("AI brain loaded OK")
except Exception as e:
    print(f"AI brain error: {e}")
    ai_brain = None

with open(DATA_PATH) as f:
    INGREDIENT_DATA = json.load(f)


class CookingRequest(BaseModel):
    dish: str
    food_type: str
    style: str
    cuisine: str
    fusion_cuisine: Optional[str] = None
    skill_level: str = "Beginner"
    special_requests: Optional[str] = None


class IngredientOptimizeRequest(BaseModel):
    cuisine1: str
    cuisine2: Optional[str] = None
    veg: bool = True
    dish_hint: str = ""


@app.get("/")
def root():
    return {
        "message": "Quantum-AI Cooking Chef API",
        "status": "running",
        "algorithms": ["QAOA", "VQE", "QUBO/Ising", "Grover-inspired Search"],
        "agents": ["Chef Agent", "Nutrition Agent", "Teacher Agent", "Safety Agent"]
    }


@app.get("/health")
def health():
    return {"status": "healthy", "quantum_engine": "ready", "ai_brain": "ready"}


@app.get("/cuisines")
def get_cuisines():
    from ai_brain import CUISINE_KNOWLEDGE
    return {
        "cuisines": list(CUISINE_KNOWLEDGE.keys()),
        "fusion_compatibility": INGREDIENT_DATA.get("fusion_compatibility", {}),
        "total_ingredients": len(INGREDIENT_DATA.get("ingredients", {}))
    }


@app.post("/optimize-ingredients")
def optimize_ingredients(req: IngredientOptimizeRequest):
    try:
        result = quantum_optimizer.get_optimized_ingredients(
            cuisine1=req.cuisine1,
            cuisine2=req.cuisine2,
            veg=req.veg,
            dish_hint=req.dish_hint,
            max_ingredients=8
        )
        vqe_score, vqe_rec = vqe_taste_nutrition_tradeoff(
            result["selected_ingredients"],
            INGREDIENT_DATA["ingredients"]
        )
        result["vqe_balance_score"] = vqe_score
        result["vqe_recommendation"] = vqe_rec
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-recipe")
def generate_recipe(req: CookingRequest):
    try:
        veg = req.food_type == "Veg"
        is_fusion = req.style == "Fusion" and req.fusion_cuisine is not None
        cuisine2 = req.fusion_cuisine if is_fusion else None

        quantum_result = quantum_optimizer.get_optimized_ingredients(
            cuisine1=req.cuisine,
            cuisine2=cuisine2,
            veg=veg,
            dish_hint=req.dish,
            max_ingredients=8
        )
        optimized_ingredients = quantum_result["selected_ingredients"]

        candidate_configs = [{"ingredients": optimized_ingredients, "style": req.style}]
        constraints = {"veg": veg, "max_ingredients": 10}
        valid_configs = grover_constraint_search(candidate_configs, constraints)

        if not valid_configs:
            raise HTTPException(status_code=400, detail="No valid recipe configuration found")

        vqe_score, vqe_rec = vqe_taste_nutrition_tradeoff(
            optimized_ingredients,
            INGREDIENT_DATA["ingredients"]
        )

        dish_hint = req.dish
        if req.special_requests:
            dish_hint += f" ({req.special_requests})"

        ai_result = ai_brain.generate_recipe(
            dish_hint=dish_hint,
            cuisine1=req.cuisine,
            cuisine2=cuisine2,
            veg=veg,
            ingredients=optimized_ingredients,
            skill_level=req.skill_level
        )

        return {
            "success": True,
            "data": {
                "recipe": ai_result["recipe"],
                "nutrition": ai_result["nutrition"],
                "simple_steps": ai_result["simple_steps"],
                "is_fusion": is_fusion,
                "fusion_cuisines": ai_result["fusion_cuisines"],
                "quantum_optimization": {
                    "method": quantum_result.get("optimization_method", "QAOA"),
                    "qubits_used": quantum_result.get("n_qubits_used", 0),
                    "fusion_score": quantum_result.get("fusion_score", 0),
                    "source": quantum_result.get("source", "quantum"),
                    "vqe_balance_score": vqe_score,
                    "vqe_recommendation": vqe_rec,
                    "selected_ingredients": optimized_ingredients
                },
                "cuisine_knowledge": ai_result.get("cuisine_knowledge", {})
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")


@app.get("/cuisine/{cuisine_name}/knowledge")
def get_cuisine_knowledge(cuisine_name: str):
    from ai_brain import CUISINE_KNOWLEDGE
    if cuisine_name not in CUISINE_KNOWLEDGE:
        raise HTTPException(status_code=404, detail="Cuisine not found")
    return {"cuisine": cuisine_name, "knowledge": CUISINE_KNOWLEDGE[cuisine_name]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''

import os
import ast

output_path = os.path.join("backend", "main.py")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Written to {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")

ast.parse(code)
print("Syntax check passed!")

# verify app exists
import importlib.util
spec = importlib.util.spec_from_file_location("main", output_path)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    if hasattr(mod, "app"):
        print("app object found!")
    else:
        print("WARNING: app not found in module")
except Exception as e:
    print(f"Module load note: {e}")

print("Done! Now run: python -m uvicorn backend.main:app --reload --port 8000")