import sys
sys.path.insert(0, '.')

print("Testing imports...")

try:
    from fastapi import FastAPI
    print("✅ fastapi OK")
except Exception as e:
    print("❌ fastapi:", e)

try:
    from quantum_engine.optimizer import QuantumIngredientsOptimizer
    print("✅ quantum_engine OK")
except Exception as e:
    print("❌ quantum_engine:", e)

try:
    from backend.ai_brain import AIRecipeBrain
    print("✅ ai_brain OK")
except Exception as e:
    print("❌ ai_brain:", e)

try:
    from groq import Groq
    print("✅ groq OK")
except Exception as e:
    print("❌ groq:", e)

try:
    from fastapi import FastAPI
    app = FastAPI()
    print("✅ app created OK")
except Exception as e:
    print("❌ app creation:", e)