# Fix: Calculate realistic times based on dish name in main.py
# This overrides whatever the AI returns with accurate times

with open('backend/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

time_fix_code = '''

def get_realistic_times(dish_hint):
    """Calculate realistic prep/cook times based on dish name."""
    dish = dish_hint.lower()
    
    # Complex dishes - long time
    if any(x in dish for x in ['biryani', 'dum', 'roast', 'brisket', 'slow cook', 'rendang', 'osso']):
        return '45 minutes', '90 minutes', 'Advanced'
    # Medium-complex dishes
    elif any(x in dish for x in ['curry', 'masala', 'korma', 'stew', 'lasagna', 'risotto', 'ramen', 'pho', 'tagine']):
        return '25 minutes', '45 minutes', 'Intermediate'
    # Pasta dishes  
    elif any(x in dish for x in ['pasta', 'spaghetti', 'carbonara', 'bolognese', 'fettuccine', 'linguine']):
        return '15 minutes', '25 minutes', 'Intermediate'
    # Stir fry / quick dishes
    elif any(x in dish for x in ['stir fry', 'stir-fry', 'fried rice', 'noodle', 'pad thai', 'chow mein']):
        return '15 minutes', '15 minutes', 'Beginner'
    # Soups
    elif any(x in dish for x in ['soup', 'broth', 'chowder', 'bisque', 'congee']):
        return '10 minutes', '25 minutes', 'Beginner'
    # Salads / cold dishes
    elif any(x in dish for x in ['salad', 'slaw', 'ceviche', 'tartare']):
        return '15 minutes', '0 minutes', 'Beginner'
    # Grilled / BBQ
    elif any(x in dish for x in ['grill', 'bbq', 'barbecue', 'kebab', 'satay', 'tandoor']):
        return '20 minutes', '30 minutes', 'Intermediate'
    # Baked dishes
    elif any(x in dish for x in ['bake', 'cake', 'bread', 'pizza', 'pie', 'tart', 'quiche']):
        return '20 minutes', '40 minutes', 'Intermediate'
    # Sandwiches / wraps
    elif any(x in dish for x in ['sandwich', 'wrap', 'burger', 'taco', 'burrito']):
        return '10 minutes', '15 minutes', 'Beginner'
    # Default
    else:
        return '20 minutes', '30 minutes', 'Intermediate'

'''

# Insert the function before the generate_recipe endpoint
c = c.replace(
    '@app.post("/generate-recipe")',
    time_fix_code + '@app.post("/generate-recipe")'
)

# Now use the function to override AI times in the recipe
c = c.replace(
    '        return {\n            "success": True,\n            "data": {\n                "recipe": ai_result["recipe"],',
    '''        # Override AI times with realistic calculated times
        prep_t, cook_t, diff = get_realistic_times(req.dish)
        if ai_result["recipe"]:
            ai_result["recipe"]["prep_time"] = prep_t
            ai_result["recipe"]["cook_time"] = cook_t
            if ai_result["recipe"].get("difficulty") in ["Beginner", "20 minutes", "30 minutes", None, ""]:
                ai_result["recipe"]["difficulty"] = diff

        return {
            "success": True,
            "data": {
                "recipe": ai_result["recipe"],'''
)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed! Times now calculated based on dish name.")
print("Biryani -> 45min prep, 90min cook")
print("Soup -> 10min prep, 25min cook")
print("Pasta -> 15min prep, 25min cook")