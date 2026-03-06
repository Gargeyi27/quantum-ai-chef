with open('backend/ai_brain.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the hardcoded time examples in the prompt
c = c.replace(
    '"prep_time": "20 minutes",\n  "cook_time": "30 minutes",',
    '"prep_time": "CALCULATE realistic prep time for this specific dish",\n  "cook_time": "CALCULATE realistic cook time for this specific dish",'
)

c = c.replace(
    '"difficulty": "{skill_level}",',
    '"difficulty": "Easy/Medium/Hard based on actual complexity of this dish",'
)

c = c.replace(
    '"serves": 2,',
    '"serves": 2,'
)

with open('backend/ai_brain.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed! Times will now be dish-specific.")