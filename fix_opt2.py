with open('quantum_engine/optimizer.py', 'r') as f:
    c = f.read()

c = c.replace('info["difficulty"]', 'info.get("difficulty", 1)')
c = c.replace('info["veg"]', 'info.get("veg", True)')
c = c.replace('info["cuisine"]', 'info.get("cuisine", [])')
c = c.replace('info["score"]', 'info.get("score", 0.5)')

with open('quantum_engine/optimizer.py', 'w') as f:
    f.write(c)

print("Fixed! optimizer.py is now defensive.")