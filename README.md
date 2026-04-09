#  Gargeyi's Chromodynamics Café

Gargeyi's Chromodynamics Café is an intelligent recipe generation system that combines **Quantum Computing** and **Large Language Models (LLMs)** to create highly personalized, restaurant-quality recipes.

##  Demo Video
[![Demo Video](https://img.shields.io/badge/▶_Watch_Demo-Google_Drive-blue?style=for-the-badge&logo=googledrive)](https://drive.google.com/file/d/18Vr0qKRbZUkRA836r8Kdrpx2M4BSJa0-/view?usp=sharing)

---

## How It Works

### Step 1 — Quantum Ingredient Optimization
- **QAOA** *(Quantum Approximate Optimization Algorithm)* — picks the most compatible, flavorful ingredient combinations
- **VQE** *(Variational Quantum Eigensolver)* — balances taste richness vs nutritional value
- **Grover's Search Algorithm** — filters dietary constraints exponentially faster than classical search

### Step 2 — Multi-Agent LLM Recipe Generation
- **Chef Agent** — 25+ real ingredients with exact measurements + 15+ steps with precise °C/°F temperatures
- **Nutrition Agent** — dish-specific macros, health benefits and smart ingredient swaps
- **Teacher Agent** — adapts complexity based on your skill level

### Step 3 — Rich Experience
Real food photographs, downloadable shopping list, chef voice narration, weekly meal planner — all in a sleek warm-themed interface.

> **Quantum computing picks the best ingredients. AI turns them into a masterpiece recipe. **

---

##  Features
-  **Quantum Optimization** — QAOA, VQE, and Grover's algorithm
-  **AI Recipe Generation** — Powered by Groq API
-  **25+ Ingredients** — Exact amounts and preparation notes
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

---

##  Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Gargeyi27/quantum-ai-chef.git
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
# Set permanently in Windows
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_groq_key", "User")
[System.Environment]::SetEnvironmentVariable("PEXELS_API_KEY", "your_pexels_key", "User")
```

### 5. Start the app
```bash
# Double-click start.bat OR run manually:

# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8001

# Terminal 2 - Frontend
cd frontend
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

##  API Keys Required

| API | Purpose | Free Tier |
|-----|---------|-----------|
| Groq | AI recipe generation | 100K–500K tokens/day |
| Pexels | Food images | 200 requests/hour |

---

##  Project Structure

```
quantum_ai_chef/
├── backend/
│   ├── main.py              # FastAPI server
│   └── ai_brain.py          # AI recipe generation
├── frontend/
│   └── app.py               # Streamlit UI
├── quantum_engine/
│   └── optimizer.py         # Quantum algorithms
├── data/
│   └── ingredients.json     # Ingredient database
├── requirements.txt
├── start.bat
└── README.md
```

---

##  AI Models (Auto-Rotation)

| Priority | Model | Context Window |
|----------|-------|---------------|
| 1 | llama-3.3-70b-versatile | 128K |
| 2 | openai/gpt-oss-120b | 128K |
| 3 | openai/gpt-oss-20b | 128K |
| 4 | llama-3.1-8b-instant | 128K |
| 5 | llama3-70b-8192 | 8K |
| 6 | llama3-8b-8192 | 8K |
| 7 | moonshotai/kimi-k2-instruct-0905 | 256K |
| 8 | qwen/qwen-3-32b | 32K |
| 9 | meta-llama/llama-4-scout-17b-16e-instruct | 128K |
| 10 | meta-llama/llama-4-maverick-17b-128e-instruct | 128K |

---

##  Quantum Algorithms

| Algorithm | Full Name | Purpose |
|-----------|-----------|---------|
| QAOA | Quantum Approximate Optimization Algorithm | Selects best ingredient combinations |
| VQE | Variational Quantum Eigensolver | Balances taste vs nutrition tradeoff |
| Grover's | Grover's Search Algorithm | Validates ingredient constraints |

---

##  AI Agents

| Agent | Role |
|-------|------|
| Chef Agent | 25+ ingredients, 15+ detailed steps with temperatures |
| Nutrition Agent | Accurate macros and health benefits |
| Teacher Agent | Simplifies steps for beginners |

---

##  Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **AI**: Groq API (LLaMA, Gemma models)
- **Quantum**: Qiskit (QAOA, VQE, Grover)
- **Images**: Pexels API
- **Voice**: Browser Speech Synthesis API

---

*Built by Gargeyi*  



## Live Demo
http://ec2-3-26-244-79.ap-southeast-2.compute.amazonaws.com:8501

