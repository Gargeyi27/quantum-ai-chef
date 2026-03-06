with open('backend/main.py', 'r') as f:
    c = f.read()

c = c.replace('INGREDIENT_DATA["ingredients"]', 'INGREDIENT_DATA')

with open('backend/main.py', 'w') as f:
    f.write(c)

print('Fixed! Replacements made.')
print('Verify - ingredients string remaining:', c.count('INGREDIENT_DATA["ingredients"]'))