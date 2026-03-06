#  Gargeyi's Chromodynamics Café
### Where Quantum Physics Meets Culinary Art

**Gargeyi's Chromodynamics Café** is an intelligent recipe generation system that combines the power of **Quantum Computing** and **Large Language Models (LLMs)** to create highly personalized, restaurant-quality recipes.

Most recipe apps simply search a database. This app works differently — it **thinks** like a chef and **computes** like a quantum computer:

### How It Works

**Step 1 — Quantum Ingredient Optimization**
When you enter a dish and ingredients, three quantum algorithms run simultaneously:
- **QAOA** evaluates thousands of ingredient combinations and picks the most flavorful and compatible set
- **VQE** finds the optimal balance between taste richness and nutritional value
- **Grover's Algorithm** rapidly validates which ingredients satisfy your dietary constraints (vegetarian, spice level, allergies)

**Step 2 — Multi-Agent LLM Recipe Generation**
The quantum-optimized ingredients are passed to a **Multi-Agent LLM System** built on Groq's ultra-fast API. Each agent is a specialized role assigned to a Large Language Model (LLM) — the same powerful AI given a different expert persona via a carefully engineered prompt:
-  **Chef Agent** — LLM acts as a professional chef, crafting a detailed recipe with 20+ ingredients (exact amounts and prep notes) and 15+ cooking steps with precise temperatures in °C/°F
-  **Nutrition Agent** — LLM acts as a certified nutritionist, calculating accurate calories, protein, carbs, fat, fiber and generating dish-specific health benefits and smart ingredient swaps
- **Teacher Agent** — LLM acts as a cooking teacher, simplifying complex steps for beginners with extra tips, warnings and explanations

All three agents run on the same Groq LLM infrastructure with **11 models rotating automatically** to maximize free tier usage (~1.7M tokens/day)

**Step 3 — Rich Experience**
The generated recipe is presented with a real food photograph, downloadable shopping list, chef voice narration, and can be saved to a weekly meal planner — all in a sleek dark-themed interface.

> In short: Quantum computing picks the best ingredients. AI turns them into a masterpiece recipe. 🍳⚛️

## ✨ Features

-  **Quantum Optimization** — QAOA, VQE, and Grover's algorithm for ingredient selection
-  **AI Recipe Generation** — Powered by Groq API (LLaMA, GPT, Qwen models)
-  **20+ Ingredients** — Exact amounts and preparation notes
-  **15+ Detailed Steps** — With temperatures in °C/°F and timing
-  **Food Images** — Real dish photos via Pexels API
-  **Chef Voice Mode** — Text-to-speech recipe reading
-  **Shopping List** — Downloadable ingredient checklist
-  **Nutrition Calculator** — Calories, protein, carbs, fat per serving
-  **Weekly Meal Planner** — 7-day meal planning grid
-  **Recipe Rating** — Rate and review your recipes
-  **15 Cuisines** — Indian, Italian, Japanese, Korean, Ethiopian and more
-  **Spice Level** — Mild to Volcanic customization
-  **Ingredient Substitutions** — Smart swap suggestions

##  Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/quantum-ai-chef.git
cd quantum-ai-chef
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set API keys
```bash
$env:GROQ_API_KEY="your_groq_api_key"
```

### 5. Start the app
```bash
# Double-click start.bat OR run manually:

# Terminal 1 - Backend
python -B -m uvicorn backend.main:app --port 8000

# Terminal 2 - Frontend
python -m streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

##  API Keys Required

| API | Purpose | Free Tier |
|-----|---------|-----------|
| [Groq](https://console.groq.com) | AI recipe generation | 100K-500K tokens/day |
| [Pexels](https://www.pexels.com/api/) | Food images | 200 requests/hour |

##  Project Structure

```
quantum_ai_chef/
├── backend/
│   ├── main.py          # FastAPI server
│   └── ai_brain.py      # AI recipe generation
├── frontend/
│   └── app.py           # Streamlit UI
├── quantum_engine/
│   └── optimizer.py     # Quantum algorithms
├── data/
│   └ingredients.json    # Ingredient database
├── tests/               # Test scripts
├── scripts/             # Utility scripts
├── requirements.txt
├── start.bat
└── README.md
```

##  AI Models (Auto-Rotation)

All models share one Groq API key and rotate automatically when rate limit is hit:

| Priority | Model | Output Tokens |
|----------|-------|--------------|
| 1 | `openai/gpt-oss-120b` | 65,536 |
| 2 | `openai/gpt-oss-20b` | 65,536 |
| 3 | `llama-3.1-8b-instant` | 131,072 |
| 4 | `qwen/qwen3-32b` | 40,960 |
| 5 | `moonshotai/kimi-k2-instruct-0905` | 16,384 |
| 6 | `moonshotai/kimi-k2-instruct` | 16,384 |
| 7 | `llama-3.3-70b-versatile` | 32,768 |
| 8 | `meta-llama/llama-4-maverick-17b-128e-instruct` | 8,192 |
| 9 | `meta-llama/llama-4-scout-17b-16e-instruct` | 8,192 |
| 10 | `groq/compound` | 8,192 |
| 11 | `groq/compound-mini` | 8,192 |

> Total combined free tokens/day: **~1,700,000+**

##  Quantum Algorithms

Implemented in `quantum_engine/optimizer.py` using Qiskit:

| Algorithm | Full Name | Purpose |
|-----------|-----------|---------|
| **QAOA** | Quantum Approximate Optimization Algorithm | Selects the best ingredient combinations from available options |
| **VQE** | Variational Quantum Eigensolver | Balances the taste vs nutrition tradeoff for optimal recipes |
| **Grover's** | Grover's Search Algorithm | Validates ingredient constraints and searches for optimal combos |

##  AI Algorithms

Implemented in `backend/ai_brain.py`:

### Multi-Agent System
| Agent | Role |
|-------|------|
|  **Chef Agent** | Generates full recipe — dish name, ingredients with exact amounts, 15+ detailed cooking steps with temperatures |
|  **Nutrition Agent** | Calculates accurate macros — calories, protein, carbs, fat, fiber, sodium, health benefits and swaps |
| **Teacher Agent** | Simplifies steps for beginner skill level with extra tips and explanations |

### Other AI Techniques
- **Model Rotation** — Automatically switches between 11 Groq models when rate limit is hit, giving ~1.7M tokens/day
- **JSON Parser** — Character-by-character parser to fix malformed AI responses with unicode characters and unescaped newlines
- **Fallback Chain** — Graceful degradation with dish-specific estimates when all API calls fail
- **Prompt Engineering** — Structured prompts with strict rules forcing 20+ ingredients and 15+ steps

##  Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **AI**: Groq API (11 models in rotation)
- **Quantum**: Qiskit (QAOA, VQE, Grover)
- **Images**: Pexels API
- **Voice**: Browser Speech Synthesis API

##  Built by Gargeyi

