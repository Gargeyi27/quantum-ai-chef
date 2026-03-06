# Update frontend app.py
with open('frontend/app.py', 'r', encoding='utf-8') as f:
    app = f.read()

app = app.replace(
    '''    cuisine = st.selectbox("🌍 Select Cuisine Style", [
        "Indian", "Chinese", "Japanese", "Italian", "Mexican", "Thai", "American"
    ])''',
    '''    cuisine = st.selectbox("🌍 Select Cuisine Style", [
        "Indian", "Chinese", "Japanese", "Italian", "Mexican", "Thai", "American",
        "Korean", "Greek", "Spanish", "French", "Middle Eastern", "Vietnamese", "Turkish", "Ethiopian"
    ])'''
)

app = app.replace(
    '''fusion_cuisine = st.selectbox("Fuse with:", [
        "Indian", "Chinese", "Japanese", "Italian", "Mexican", "Thai", "American"
    ])''',
    '''fusion_cuisine = st.selectbox("Fuse with:", [
        "Indian", "Chinese", "Japanese", "Italian", "Mexican", "Thai", "American",
        "Korean", "Greek", "Spanish", "French", "Middle Eastern", "Vietnamese", "Turkish", "Ethiopian"
    ])'''
)

with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(app)
print("frontend/app.py updated!")

# Update ai_brain.py with new cuisine knowledge
with open('backend/ai_brain.py', 'r', encoding='utf-8') as f:
    brain = f.read()

brain = brain.replace(
    '''    "Thai": {
        "techniques": ["balancing 5 flavors", "wok cooking", "pounding in mortar", "steaming"],
        "flavor_base": "lemongrass, galangal, kaffir lime, fish sauce",
        "spices": "Thai basil, bird eye chili, turmeric, coriander root",
        "regional": "Central (balanced), Northern (milder), Southern (spicy)"
    }
}''',
    '''    "Thai": {
        "techniques": ["balancing 5 flavors", "wok cooking", "pounding in mortar", "steaming"],
        "flavor_base": "lemongrass, galangal, kaffir lime, fish sauce",
        "spices": "Thai basil, bird eye chili, turmeric, coriander root",
        "regional": "Central (balanced), Northern (milder), Southern (spicy)"
    },
    "Korean": {
        "techniques": ["fermentation", "grilling (grill)", "braising", "stir-frying"],
        "flavor_base": "gochujang, soy sauce, sesame oil, garlic, ginger",
        "spices": "gochugaru, doenjang, perilla, green onion",
        "regional": "Seoul (bold flavors), Jeonju (rich), Busan (seafood-forward)"
    },
    "Greek": {
        "techniques": ["grilling", "slow roasting", "marinating", "baking"],
        "flavor_base": "olive oil, lemon, garlic, oregano",
        "spices": "oregano, thyme, rosemary, mint, cinnamon",
        "regional": "Athens (classic), Islands (seafood), Northern (meat-heavy)"
    },
    "Spanish": {
        "techniques": ["sauteing", "slow braising", "grilling", "pickling"],
        "flavor_base": "olive oil, garlic, tomato, saffron, paprika",
        "spices": "smoked paprika, saffron, cumin, parsley",
        "regional": "Andalusia (tapas), Catalonia (seafood), Basque (pintxos)"
    },
    "French": {
        "techniques": ["sauteing", "braising", "poaching", "flambeing", "reduction"],
        "flavor_base": "butter, cream, wine, shallots, herbs",
        "spices": "herbes de Provence, tarragon, thyme, bay leaf",
        "regional": "Provence (olive oil), Normandy (cream), Lyon (classic)"
    },
    "Middle Eastern": {
        "techniques": ["grilling", "slow roasting", "stewing", "frying"],
        "flavor_base": "olive oil, lemon, garlic, tahini, pomegranate",
        "spices": "za'atar, sumac, cumin, coriander, cardamom, cinnamon",
        "regional": "Lebanese (fresh), Persian (fragrant), Turkish (spiced)"
    },
    "Vietnamese": {
        "techniques": ["fresh assembly", "pho broth simmering", "grilling", "stir-frying"],
        "flavor_base": "fish sauce, lime, lemongrass, fresh herbs",
        "spices": "star anise, cinnamon, cloves, coriander, chili",
        "regional": "Hanoi (subtle), Hue (spicy), Saigon (sweet)"
    },
    "Turkish": {
        "techniques": ["grilling", "slow braising", "baking", "stuffing"],
        "flavor_base": "olive oil, tomato, onion, garlic, yogurt",
        "spices": "cumin, paprika, mint, sumac, allspice, cinnamon",
        "regional": "Istanbul (diverse), Aegean (olive oil), Southeast (spicy)"
    },
    "Ethiopian": {
        "techniques": ["slow simmering", "injera making", "spiced butter cooking", "stewing"],
        "flavor_base": "berbere spice, niter kibbeh, onion, garlic, ginger",
        "spices": "berbere, mitmita, fenugreek, cardamom, black cumin",
        "regional": "Addis Ababa (diverse), Tigray (mild), Oromia (spicy)"
    }
}'''
)

with open('backend/ai_brain.py', 'w', encoding='utf-8') as f:
    f.write(brain)
print("backend/ai_brain.py updated!")
print("All 8 cuisines added successfully!")