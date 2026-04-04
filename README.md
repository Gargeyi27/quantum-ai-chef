#  Gargeyi's Chromodynamics Café


Gargeyi's Chromodynamics Café is an intelligent recipe generation system that combines **Quantum Computing** and **Large Language Models (LLMs)** to create highly personalized, restaurant-quality recipes.

##  Demo Video
[![Demo Video](https://img.shields.io/badge/?_Watch_Demo-Google_Drive-blue?style=for-the-badge&logo=googledrive)](https://drive.google.com/file/d/18Vr0qKRbZUkRA836r8Kdrpx2M4BSJa0-/view?usp=sharing)

---

## How It Works

Most recipe apps simply search a database. This app works differently — it **thinks like a chef** and **computes like a quantum computer**.

### Step 1 — Quantum Ingredient Optimization
When you enter a dish and ingredients, three quantum algorithms run simultaneously:
- **QAOA** evaluates thousands of ingredient combinations and picks the most flavorful and compatible set
- **VQE** finds the optimal balance between taste richness and nutritional value
- **Grover's Algorithm** rapidly validates which ingredients satisfy your dietary constraints

### Step 2 — Multi-Agent LLM Recipe Generation
The quantum-optimized ingredients are passed to a **Multi-Agent LLM System**. Each agent is a specialized role assigned to a Large Language Model:
- **Chef Agent** — Crafts a detailed recipe with **25+ ingredients** (exact amounts and prep notes) and **15+ cooking steps** with precise temperatures in °C/°F
- **Nutrition Agent** — Calculates accurate calories, protein, carbs, fat, fiber and generates dish-specific health benefits
- **Teacher Agent** — Simplifies complex steps for beginners with extra tips and warnings

### Step 3 — Rich Experience
The generated recipe is presented with a real food photograph, downloadable shopping list, chef voice narration, and can be saved to a weekly meal planner — all in a sleek dark-themed interface.

> **In short: Quantum computing picks the best ingredients. AI turns them into a masterpiece recipe. 🍳⚛️**

---

##  Features
-  **Quantum Optimization** — QAOA, VQE, and Grover's algorithm for ingredient selection
-  **AI Recipe Generation** — Powered by Groq API
-  **25+ Ingredients** — Exact amounts and preparation notes
-  **15+ Detailed Steps** — With temperatures in °C/°F and timing
-  **Food Images** — Real dish photos via Pexels API
-  **Chef Voice Mode** — Text-to-speech recipe reading
-  **Shopping List** — Downloadable ingredient checklist
-  **Nutrition Calculator** — Calories, protein, carbs, fat per serving
-  **Weekly Meal Planner** — 7-day meal planning grid
-  **Recipe Rating** — Rate and review your recipes
-  **15 Cuisines** — Indian, Italian, Japanese, Korean,   Ethiopian and more
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
$env:GROQ_API_KEY="your_groq_api_key"
$env:PEXELS_API_KEY="your_pexels_api_key"
```

### 5. Start the app
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

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

Models rotate automatically when rate limit is hit:

| Priority | Model | Context Window | Free Tokens/Day |
|----------|-------|---------------|-----------------|
| 1 | llama-3.3-70b-versatile | 128K | 100,000 |
| 2 | llama-3.1-8b-instant | 128K | 500,000 |
| 3 | mixtral-8x7b-32768 | 32K | 500,000 |

---

##  Quantum Algorithms

Implemented in `quantum_engine/optimizer.py` using Qiskit:

| Algorithm | Full Name | Purpose |
|-----------|-----------|---------|
| QAOA | Quantum Approximate Optimization Algorithm | Selects best ingredient combinations |
| VQE | Variational Quantum Eigensolver | Balances taste vs nutrition tradeoff |
| Grover's | Grover's Search Algorithm | Validates ingredient constraints |

---

##  AI Agents

| Agent | Role |
|-------|------|
| Chef Agent | Generates full recipe — 25+ ingredients, 15+ detailed steps with temperatures |
| Nutrition Agent | Calculates accurate macros and health benefits |
| Teacher Agent | Simplifies steps for beginners |

---

##  Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **AI**: Groq API
- **Quantum**: Qiskit (QAOA, VQE, Grover)
- **Images**: Pexels API
- **Voice**: Browser Speech Synthesis API

---

*Built by Gargeyi* 



## Live Demo
http://ec2-3-26-244-79.ap-southeast-2.compute.amazonaws.com:8501
