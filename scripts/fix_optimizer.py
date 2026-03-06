with open('quantum_engine/optimizer.py', 'r') as f:
    c = f.read()

c = c.replace('self.data["ingredients"]', 'self.data')

with open('quantum_engine/optimizer.py', 'w') as f:
    f.write(c)

remaining = c.count('self.data["ingredients"]')
print('Fixed!')
print('Remaining occurrences:', remaining)