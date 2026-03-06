with open('quantum_engine/optimizer.py', 'r') as f:
    c = f.read()

# Fix the candidate filtering to exclude meat when veg=True
old = """        candidates = []
        for name, info in all_ingredients.items():
            cuisines = [c.lower() for c in info.get("cuisines", [])]
            score = 0.0
            if cuisine1_lower in cuisines:
                score += 1.0
            if cuisine2_lower and cuisine2_lower in cuisines:
                score += 0.8
            score += info.get("fusion_score", 0.5)
            nutrition = info.get("nutrition", {})
            health = (nutrition.get("protein", 0) + nutrition.get("fiber", 0)) / 20.0
            score += health * 0.3
            candidates.append((name, info, score))"""

new = """        NON_VEG = {"chicken", "beef", "shrimp", "salmon", "fish", "pork", "lamb", "turkey", "bacon", "meat", "prawn", "crab", "lobster", "tuna", "anchovy"}

        candidates = []
        for name, info in all_ingredients.items():
            # Skip non-veg ingredients if veg mode
            if veg and name.lower() in NON_VEG:
                continue
            cuisines = [c.lower() for c in info.get("cuisines", [])]
            score = 0.0
            if cuisine1_lower in cuisines:
                score += 1.0
            if cuisine2_lower and cuisine2_lower in cuisines:
                score += 0.8
            score += info.get("fusion_score", 0.5)
            nutrition = info.get("nutrition", {})
            health = (nutrition.get("protein", 0) + nutrition.get("fiber", 0)) / 20.0
            score += health * 0.3
            candidates.append((name, info, score))"""

if old in c:
    c = c.replace(old, new)
    with open('quantum_engine/optimizer.py', 'w') as f:
        f.write(c)
    print("Fixed! Veg filter added to optimizer.")
else:
    print("Pattern not found - printing relevant section for manual fix:")
    lines = c.split('\n')
    for i, line in enumerate(lines):
        if 'candidates' in line and 'append' not in line:
            print(f"Line {i}: {line}")