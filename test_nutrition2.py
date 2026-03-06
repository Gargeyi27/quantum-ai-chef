import os, sys
sys.path.insert(0, '.')
os.environ['GROQ_API_KEY'] = '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'
from backend.ai_brain import AIRecipeBrain
brain = AIRecipeBrain()
result = brain.generate_recipe('butter chicken', 'Indian', None, False,
    ['chicken','tomato','garlic','ginger','cream','butter'], 'Beginner')
nutrition = result.get('nutrition', {})
print("CALORIES:", nutrition.get('per_serving',{}).get('calories'))
print("BENEFITS:", nutrition.get('health_benefits'))
print("SWAPS:", nutrition.get('healthy_swaps'))