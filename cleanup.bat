@echo off
echo Organizing Quantum AI Chef project...

:: Create folders
mkdir scripts 2>nul
mkdir tests 2>nul

:: Move all fix_*.py files to scripts
move fix_aibrain.py scripts\ 2>nul
move fix_all.py scripts\ 2>nul
move fix_ingredients.py scripts\ 2>nul
move fix_main.py scripts\ 2>nul
move fix_nutrition.py scripts\ 2>nul
move fix_opt2.py scripts\ 2>nul
move fix_optimizer.py scripts\ 2>nul
move fix_recipe_fusion.py scripts\ 2>nul
move fix_steps.py scripts\ 2>nul
move fix_times.py scripts\ 2>nul
move fix_times2.py scripts\ 2>nul
move fix_veg.py scripts\ 2>nul
move fix3.py scripts\ 2>nul
move add_cuisines.py scripts\ 2>nul
move get_models.py scripts\ 2>nul
move write_aibrain2.py scripts\ 2>nul
move write_ing.py scripts\ 2>nul
move write_ingredients.py scripts\ 2>nul
move write_main_fix.py scripts\ 2>nul
move write_main.py scripts\ 2>nul
move write_optimizer.py scripts\ 2>nul
move write_optimizer2.py scripts\ 2>nul

:: Move all test_*.py files to tests
move test_image.py tests\ 2>nul
move test_image2.py tests\ 2>nul
move test_imports.py tests\ 2>nul
move test_nutrition.py tests\ 2>nul
move test_nutrition2.py tests\ 2>nul
move test_recipe.py tests\ 2>nul
move test_translate.py tests\ 2>nul
move test_unsplash.py tests\ 2>nul

echo Done! Project is now organized.
echo.
echo Structure:
echo   backend/        - API and AI brain
echo   frontend/       - Streamlit app
echo   quantum_engine/ - Quantum algorithms
echo   data/           - Ingredients data
echo   scripts/        - Utility scripts
echo   tests/          - Test files
pause