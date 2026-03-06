with open('backend/ai_brain.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Find and print the current prompt section around prep_time
idx = c.find('prep_time')
print("CURRENT:", repr(c[idx-5:idx+50]))