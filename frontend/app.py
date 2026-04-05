import streamlit as st
import requests
import json
import random
from datetime import datetime

API_URL = "http://localhost:8002"

st.set_page_config(page_title="Gargeyi's Chromodynamics Cafe", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }
.stButton>button {
    background: linear-gradient(135deg, #885133, #d62300);
    color: white; border: none; border-radius: 10px;
    padding: 0.5rem 2rem; font-size: 1.1rem; font-weight: bold; width: 100%;
}
.recipe-box {
    background: #f4f0ec; border-radius: 15px; padding: 1.5rem;
    margin: 0.5rem 0; border-left: 4px solid #d62300;
}
.ing-box {
    background: #f0e6d7; border-radius: 10px; padding: 0.8rem 1rem;
    margin: 0.3rem 0; border-left: 3px solid #27ae60;
}
.shop-item {
    background: #f0e6d7; border-radius: 8px; padding: 0.6rem 1rem;
    margin: 0.2rem 0; border-left: 3px solid #f39c12;
}
.meal-card {
    background: #f4f0ec; border-radius: 12px; padding: 1rem;
    margin: 0.3rem; border-top: 3px solid #885133; text-align: center;
    min-height: 100px;
}
.sub-box {
    background: #f0e6d7; border-radius: 10px; padding: 1rem;
    margin: 0.3rem 0; border-left: 3px solid #3498db;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'recipe_history' not in st.session_state:
    st.session_state.recipe_history = []
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = {d: None for d in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']}
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}
if 'recipe_ready' not in st.session_state:
    st.session_state.recipe_ready = False
if 'last_recipe' not in st.session_state:
    st.session_state.last_recipe = {}
if 'last_nutrition' not in st.session_state:
    st.session_state.last_nutrition = {}
if 'last_quantum' not in st.session_state:
    st.session_state.last_quantum = {}
if 'last_servings' not in st.session_state:
    st.session_state.last_servings = 2
if 'last_spice' not in st.session_state:
    st.session_state.last_spice = "Medium"
if 'last_skill' not in st.session_state:
    st.session_state.last_skill = "Beginner"

DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

st.title("⚛️ Gargeyi's Chromodynamics Cafe")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🍳 Generate Recipe", "📅 Weekly Meal Planner", "⭐ Recipe History"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        cuisine = st.selectbox("🌍 Cuisine Style", [
            "Indian","Chinese","Japanese","Italian","Mexican","Thai","American",
            "Korean","Greek","Spanish","French","Middle Eastern","Vietnamese","Turkish","Ethiopian"
        ])
        diet = st.selectbox("🥗 Dietary Preference", ["None","Vegetarian","Vegan","Gluten-Free","Keto","Low-Calorie"])
        spice = st.select_slider("🌶️ Spice Level", options=["Mild","Medium","Hot","Extra Hot","Volcanic"])
    with col2:
        dish = st.text_input("🍽️ What dish do you want?", placeholder="e.g. pasta, biryani, soup")
        skill = st.selectbox("👨‍🍳 Skill Level", ["Beginner","Intermediate","Advanced"])
        servings = st.number_input("👥 Servings", min_value=1, max_value=10, value=2)

    fusion = st.checkbox("✨ Fusion Recipe")
    fusion_cuisine = None
    if fusion:
        fusion_cuisine = st.selectbox("Fuse with:", [
            "Indian","Chinese","Japanese","Italian","Mexican","Thai","American",
            "Korean","Greek","Spanish","French","Middle Eastern","Vietnamese","Turkish","Ethiopian"
        ])

    st.markdown("---")

    # Chef Voice Mode - always visible before generate button
    st.markdown("### 🗣️ Chef Voice Settings")
    vc1, vc2 = st.columns([1, 2])
    with vc1:
        voice_mode = st.checkbox("Enable Chef's Voice Mode", key="voice_cb", value=False)
    with vc2:
        voice_options = {
            "👩 Rachel - Warm & Friendly": {"rate": 0.85, "pitch": 1.1, "gender": "female"},
            "👨 James - Calm & Clear": {"rate": 0.80, "pitch": 0.95, "gender": "male"},
            "👩 Emma - Energetic & Fun": {"rate": 0.95, "pitch": 1.2, "gender": "female"},
            "👨 Oliver - Deep & Relaxed": {"rate": 0.75, "pitch": 0.85, "gender": "male"},
            "👩 Sophie - Crisp & Professional": {"rate": 0.90, "pitch": 1.05, "gender": "female"},
        }
        selected_voice_name = st.selectbox("Select Voice", list(voice_options.keys()), key="voice_select")
    selected_voice = voice_options[selected_voice_name]
    st.markdown("---")
    
    # Backend Health Check in Sidebar
    st.sidebar.markdown("### 🛠️ System Status")
    try:
        health_resp = requests.get(API_URL + "/health", timeout=3)
        if health_resp.status_code == 200:
            st.sidebar.success("✅ Backend Connected")
        else:
            st.sidebar.error("❌ Backend Error: " + str(health_resp.status_code))
    except Exception:
        st.sidebar.error("❌ Backend Unreachable (8002)")
        st.sidebar.info("Tip: Make sure the FastAPI server is running on the same EC2 instance.")

    if st.sidebar.checkbox("🔍 Show Debug Console"):
        st.sidebar.markdown("---")
        st.sidebar.write(f"**API URL:** `{API_URL}`")
        if st.session_state.get('recipe_ready'):
            st.sidebar.write("✅ Last Recipe: Ready")
        else:
            st.sidebar.write("⏳ Waiting for generation...")

    if st.button("⚛️ Generate Recipe with Quantum AI"):
        with st.spinner("⚛️ Quantum algorithms optimizing... 🤖 AI Chef crafting your recipe..."):
            try:
                special = []
                if diet != "None": special.append(diet)
                if spice != "Medium": special.append(spice + " spice level")
                if servings != 2: special.append("serves " + str(servings) + " people")
                special_str = ", ".join(special) if special else None

                payload = {
                    "dish": dish if dish else "chef special",
                    "food_type": "Veg" if diet in ["Vegetarian","Vegan"] else "Non-Veg",
                    "style": "Fusion" if fusion else cuisine,
                    "cuisine": cuisine,
                    "fusion_cuisine": fusion_cuisine if fusion else None,
                    "skill_level": skill,
                    "special_requests": special_str
                }

                response = requests.post(API_URL + "/generate-recipe", json=payload, timeout=90)

                if response.status_code == 200:
                    result = response.json()
                    d = result.get("data", {})
                    recipe = d.get("recipe", {})
                    nutrition = d.get("nutrition", {})
                    quantum = d.get("quantum_optimization", {})

                    st.session_state.last_recipe = recipe
                    st.session_state.last_nutrition = nutrition
                    st.session_state.last_quantum = quantum
                    st.session_state.last_servings = servings
                    st.session_state.last_spice = spice
                    st.session_state.last_skill = skill
                    st.session_state.last_dish = dish if dish else "chef special"
                    st.session_state.last_cuisine = cuisine
                    st.session_state.recipe_ready = True

                    st.session_state.recipe_history.append({
                        "name": recipe.get("dish_name", "Recipe"),
                        "cuisine": cuisine,
                        "timestamp": datetime.now().strftime("%d %b %Y %H:%M"),
                        "recipe": recipe,
                        "nutrition": nutrition,
                        "rating": 0
                    })
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()
                else:
                    st.error("API Error " + str(response.status_code) + ": " + response.text)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend! Start uvicorn on port 8002.")
            except Exception as e:
                st.error("Error: " + str(e))

    # Display recipe from session state
    if st.session_state.recipe_ready and st.session_state.last_recipe:
        recipe = st.session_state.last_recipe
        nutrition = st.session_state.last_nutrition
        quantum = st.session_state.last_quantum
        servings = st.session_state.last_servings
        spice = st.session_state.last_spice
        skill = st.session_state.last_skill

        st.success("Recipe Ready!")
        st.markdown("---")

        dish_name = recipe.get("dish_name", "Your Recipe")
        tagline = recipe.get("tagline", "")
        st.markdown("## 🍽️ " + dish_name)
        if tagline:
            st.markdown("*" + tagline + "*")

        # Dish image using Pexels API (Non-blocking)
        user_dish = st.session_state.get("last_dish", dish_name)
        if st.checkbox("🖼️ Show Dish Image", value=True):
            try:
                import requests as req, base64
                pexels_key = "Qo5UbnliTuhsVKamqEOcRITecVHcHtEfUXGLwPzaIialDQX703rp6Qu5"
                query = str(user_dish) + " food"
                resp = req.get(
                    "https://api.pexels.com/v1/search?query=" + query + "&per_page=1&orientation=landscape",
                    headers={"Authorization": pexels_key},
                    timeout=5
                )
                if resp.status_code == 200:
                    photos = resp.json().get("photos", [])
                    if photos:
                        img_url = photos[0]["src"]["large"]
                        photographer = photos[0]["photographer"]
                        st.image(img_url, caption=f"📸 Photo by {photographer} on Pexels", use_column_width=True)
            except Exception:
                pass
        else:
            st.caption("🍽️ " + dish_name)
        col_a, col_b, col_c, col_d, col_e = st.columns(5)
        col_a.metric("⏱️ Prep", recipe.get("prep_time", "N/A"))
        col_b.metric("🔥 Cook", recipe.get("cook_time", "N/A"))
        col_c.metric("👥 Serves", servings)
        col_d.metric("📊 Difficulty", recipe.get("difficulty", skill))
        col_e.metric("🌶️ Spice", spice)

        st.markdown("---")

        left, right = st.columns([1, 1])

        with left:
            st.markdown("### 🧾 Ingredients")
            ingredients_list = recipe.get("ingredients", [])
            shopping_items = []
            for ing in ingredients_list:
                if isinstance(ing, dict):
                    name = ing.get("name", "")
                    amount = ing.get("amount", "")
                    note = ing.get("note", "")
                    shopping_items.append(amount + " " + name)
                    line = "**" + amount + "** " + name
                    if note:
                        line += " — *" + note + "*"
                    st.markdown("<div class='ing-box'>🥄 " + line + "</div>", unsafe_allow_html=True)
                elif isinstance(ing, str):
                    shopping_items.append(ing)
                    st.markdown("<div class='ing-box'>🥄 " + ing + "</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🛒 Shopping List")
            shop_text = "\n".join(["[ ] " + item for item in shopping_items])
            st.download_button("📥 Download Shopping List", data=shop_text,
                file_name=dish_name + "_shopping_list.txt", mime="text/plain")
            for item in shopping_items:
                st.markdown("<div class='shop-item'>☐ " + item + "</div>", unsafe_allow_html=True)

        with right:
            st.markdown("### 📊 Nutrition & Calorie Calculator")
            # Safe nutrition access - handle both dict and list
            nutr = nutrition if isinstance(nutrition, dict) else {}
            per_serving = nutr.get("per_serving", {}) if isinstance(nutr.get("per_serving"), dict) else {}
            if per_serving:
                cal = per_serving.get("calories", 0)
                total_cal = int(cal) * int(servings) if str(cal).isdigit() else cal
                st.metric("🔥 Total Calories", str(total_cal) + " kcal", str(cal) + " kcal per serving")
                n1, n2, n3 = st.columns(3)
                n1.metric("💪 Protein", str(per_serving.get("protein_g", 0)) + "g")
                n2.metric("🌾 Carbs", str(per_serving.get("carbs_g", 0)) + "g")
                n3.metric("🥑 Fat", str(per_serving.get("fat_g", 0)) + "g")
                n4, n5 = st.columns(2)
                n4.metric("🌿 Fiber", str(per_serving.get("fiber_g", 0)) + "g")
                n5.metric("🧂 Sodium", str(per_serving.get("sodium_mg", 0)) + "mg")

            benefits = nutr.get("health_benefits", [])
            if benefits and isinstance(benefits, list):
                st.markdown("**✅ Health Benefits:**")
                for b in benefits:
                    if b and "specific benefit" not in str(b).lower():
                        st.markdown("🟢 " + str(b))

            swaps = nutr.get("healthy_swaps", [])
            if swaps and isinstance(swaps, list):
                st.markdown("**💡 Healthy Swaps:**")
                for s in swaps:
                    if s and "specific swap" not in str(s).lower():
                        st.markdown("🔄 " + str(s))

            avoid = nutr.get("who_should_avoid", [])
            if avoid and isinstance(avoid, list):
                st.markdown("**⚠️ Who Should Avoid:**")
                for a in avoid:
                    if a and "specific" not in str(a).lower():
                        st.markdown("⛔ " + str(a))

            best_time = nutr.get("best_time_to_eat", "")
            if best_time and "when" not in str(best_time).lower():
                st.markdown("**🕐 Best Time:** " + str(best_time))

        st.markdown("---")

        equipment = recipe.get("equipment_needed", [])
        if equipment:
            st.markdown("### 🔧 Equipment Needed")
            st.markdown(" • ".join(equipment))
            st.markdown("---")

        st.markdown("### 👨‍🍳 Step-by-Step Instructions")

        raw_steps = recipe.get("cooking_steps", []) if isinstance(recipe, dict) else []
        steps = raw_steps if isinstance(raw_steps, list) else []
        full_text = ""
        for step in steps:
            if isinstance(step, dict):
                num = step.get("step", "")
                title = step.get("title", "")
                instruction = step.get("instruction", "")
                tip = step.get("tip", "")
                cue = step.get("sensory_cue", "")
                time_est = step.get("time", "")
                full_text += "Step " + str(num) + ". " + title + ". " + instruction + " "
                content = "<b>Step " + str(num) + " — " + title + "</b>"
                if time_est:
                    content += " <i>(" + time_est + ")</i>"
                content += "<br><br>" + instruction
                if tip:
                    content += "<br><br>💡 <b>Tip:</b> " + tip
                if cue:
                    content += "<br>👃 <b>Look for:</b> " + cue
                st.markdown("<div class='recipe-box'>" + content + "</div>", unsafe_allow_html=True)
            elif isinstance(step, str):
                full_text += step + " "
                st.markdown("<div class='recipe-box'>" + step + "</div>", unsafe_allow_html=True)

        # Chef Voice Mode - simple browser speech
        if voice_mode and full_text:
            v_rate = selected_voice["rate"]
            v_pitch = selected_voice["pitch"]
            safe_text = full_text[:4000].replace("'", " ").replace('"', ' ').replace(chr(10), ' ').replace(chr(13), ' ')
            st.markdown("**🗣️ " + selected_voice_name + " is ready:**")
            voice_html = """
            <div style="padding:1rem;background:#1e2130;border-radius:12px;margin:0.5rem 0;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;">
                <button id="playBtn" style="background:linear-gradient(135deg,#c0392b,#8e44ad);color:white;border:none;border-radius:8px;padding:0.7rem 1.8rem;cursor:pointer;font-size:1rem;font-weight:bold;">▶ Play</button>
                <button id="pauseBtn" style="background:#2c3e50;color:white;border:none;border-radius:8px;padding:0.7rem 1.5rem;cursor:pointer;font-size:1rem;">⏸ Pause</button>
                <button id="stopBtn" style="background:#7f1d1d;color:white;border:none;border-radius:8px;padding:0.7rem 1.5rem;cursor:pointer;font-size:1rem;">⏹ Stop</button>
                <span id="status" style="color:#aaa;font-size:0.9rem;margin-left:0.5rem;"></span>
            </div>
            <script>
            var txt = '""" + safe_text + """';
            var rate = """ + str(v_rate) + """;
            var pitch = """ + str(v_pitch) + """;
            var synth = window.speechSynthesis;
            var voices = [];
            function loadVoices() {
                voices = synth.getVoices();
            }
            loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = loadVoices;
            }
            document.getElementById('playBtn').addEventListener('click', function() {
                synth.cancel();
                var u = new SpeechSynthesisUtterance(txt);
                u.rate = rate;
                u.pitch = pitch;
                u.volume = 1.0;
                u.lang = 'en-US';
                // Try to pick matching gender voice
                var gender = '""" + selected_voice["gender"] + """';
                var preferred = voices.filter(function(v) {
                    return gender === 'female' ? v.name.match(/female|woman|girl|zira|susan|karen|victoria|samantha/i) :
                                                 v.name.match(/male|man|david|mark|daniel|alex|george/i);
                });
                if (preferred.length > 0) u.voice = preferred[0];
                u.onstart = function() { document.getElementById('status').textContent = 'Playing...'; };
                u.onend = function() { document.getElementById('status').textContent = 'Done!'; };
                u.onerror = function(e) { document.getElementById('status').textContent = 'Error: ' + e.error; };
                synth.speak(u);
            });
            document.getElementById('pauseBtn').addEventListener('click', function() {
                if (synth.speaking && !synth.paused) { synth.pause(); document.getElementById('status').textContent = 'Paused'; }
                else if (synth.paused) { synth.resume(); document.getElementById('status').textContent = 'Resumed...'; }
            });
            document.getElementById('stopBtn').addEventListener('click', function() {
                synth.cancel(); document.getElementById('status').textContent = 'Stopped';
            });
            </script>"""
            st.components.v1.html(voice_html, height=90)

        st.markdown("---")

        subs = recipe.get("substitutions", [])
        if subs:
            st.markdown("### 🔄 Ingredient Substitutions")
            for sub in subs:
                if isinstance(sub, dict):
                    orig = sub.get("original", "")
                    alt = sub.get("substitute", "")
                    impact = sub.get("flavor_impact", "")
                    st.markdown("<div class='sub-box'>🔄 <b>" + orig + "</b> → <b>" + alt + "</b><br><small>" + impact + "</small></div>", unsafe_allow_html=True)
            st.markdown("---")

        tc, vc = st.columns(2)
        with tc:
            tips = recipe.get("chef_tips", [])
            if tips:
                st.markdown("### 💡 Chef's Pro Tips")
                for tip in tips:
                    st.markdown("✅ " + tip)
        with vc:
            variations = recipe.get("variations", [])
            if variations:
                st.markdown("### 🔀 Variations")
                for v in variations:
                    st.markdown("• " + v)

        st.markdown("---")

        st.markdown("### ⭐ Rate This Recipe")
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            rating = st.select_slider("Your Rating", options=[1,2,3,4,5], value=5,
                format_func=lambda x: "⭐" * x)
            if st.button("Submit Rating"):
                dn = recipe.get("dish_name", "Recipe") if isinstance(recipe, dict) else "Recipe"
                st.session_state.ratings[dn] = rating
                if st.session_state.recipe_history:
                    st.session_state.recipe_history[-1]["rating"] = rating
                st.success("Rated " + ("⭐" * rating))
        with rc2:
            st.text_area("Write a review (optional)", placeholder="How did it taste?")

        st.markdown("---")

        st.markdown("### 📅 Add to Weekly Meal Plan")
        mp1, mp2 = st.columns(2)
        with mp1:
            mp_day = st.selectbox("Day", DAYS)
        with mp2:
            if st.button("➕ Add to Meal Plan"):
                st.session_state.meal_plan[mp_day] = dish_name
                st.success("Added to " + mp_day + "!")

        if quantum:
            with st.expander("⚛️ Quantum Optimization Details"):
                q1, q2, q3 = st.columns(3)
                q1.metric("Algorithm", quantum.get("method", "QAOA"))
                q2.metric("Qubits Used", quantum.get("qubits_used", 0))
                q3.metric("Fusion Score", str(round(quantum.get("fusion_score", 0), 2)))
                st.markdown("VQE: " + quantum.get("vqe_recommendation", "N/A"))
                st.markdown("Quantum Ingredients: " + ", ".join(quantum.get("selected_ingredients", [])))

        with st.expander("🔍 Raw Recipe Data"):
            st.json(recipe)

with tab2:
    st.markdown("## 📅 Weekly Meal Planner")
    st.markdown("---")
    cols = st.columns(7)
    for i, day in enumerate(DAYS):
        with cols[i]:
            meal = st.session_state.meal_plan.get(day)
            if meal:
                st.markdown("<div class='meal-card'><b>" + day + "</b><br><br>🍽️ " + meal + "</div>", unsafe_allow_html=True)
                if st.button("Remove", key="rm_" + day):
                    st.session_state.meal_plan[day] = None
                    st.rerun()
            else:
                st.markdown("<div class='meal-card'><b>" + day + "</b><br><br><i>Empty</i></div>", unsafe_allow_html=True)

    st.markdown("---")
    planned = [(d, m) for d, m in st.session_state.meal_plan.items() if m]
    if planned:
        st.markdown("### " + str(len(planned)) + "/7 Days Planned")
        for day, meal in planned:
            st.markdown("• **" + day + ":** " + meal)
        if st.button("Clear Meal Plan"):
            st.session_state.meal_plan = {d: None for d in DAYS}
            st.rerun()
    else:
        st.info("Generate recipes and add them to your meal plan!")

with tab3:
    st.markdown("## ⭐ Recipe History")
    st.markdown("---")
    if not st.session_state.recipe_history:
        st.info("No recipes yet! Generate your first recipe.")
    else:
        st.markdown(str(len(st.session_state.recipe_history)) + " recipes generated")
        for i, item in enumerate(reversed(st.session_state.recipe_history)):
            rating = item.get("rating", 0)
            stars = ("⭐" * rating) if rating else "Unrated"
            with st.expander("🍽️ " + item["name"] + " — " + item["cuisine"] + " — " + item["timestamp"] + " — " + stars):
                recipe = item.get("recipe", {})
                nutrition = item.get("nutrition", {})
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("⏱️ Prep", recipe.get("prep_time", "N/A"))
                c2.metric("🔥 Cook", recipe.get("cook_time", "N/A"))
                c3.metric("📊 Difficulty", recipe.get("difficulty", "N/A"))
                per_s = nutrition.get("per_serving", {}) if isinstance(nutrition, dict) else {}
                c4.metric("Calories", str(per_s.get("calories", "N/A")))
                st.markdown("**Ingredients:**")
                for ing in recipe.get("ingredients", []):
                    if isinstance(ing, dict):
                        st.markdown("• " + ing.get("amount", "") + " " + ing.get("name", ""))
                    else:
                        st.markdown("• " + str(ing))
                if st.button("Add to Meal Plan", key="add_" + str(i)):
                    day = random.choice(DAYS)
                    st.session_state.meal_plan[day] = item["name"]
                    st.success("Added to " + day + "!")
        if st.button("Clear All History"):
            st.session_state.recipe_history = []
            st.rerun()


