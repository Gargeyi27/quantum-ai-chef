content = open('ai_brain.py', 'r', encoding='utf-8').read()

# Replace groq import and client with gemini
old_import = '''from groq import Groq

client = Groq(api_key="gsk_Zdq8U8oL64WH5qbgqEJQWGdyb3FY0hqpqm5nJfhIisMG1lgPk5c")'''

new_import = '''import google.generativeai as genai

genai.configure(api_key="AIzaSyCqUjswCQC7Zb6ZGpP7nfP7djYpA_5jg4k")'''

# Replace _call_groq method
old_call = '''    def _call_groq(self, prompt, max_tokens=12000):
        messages = [{"role": "user", "content": prompt}]
        last_error = None
        for model in self.models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=messages
                )
                if model != self.models[0]:
                    print(f"Used fallback model: {model}")
                return response.choices[0].message.content
            except Exception as e:
                if "rate_limit" in str(e) or "429" in str(e):
                    print(f"Rate limit on {model}, trying next...")
                    last_error = e
                    continue
                raise e
        raise last_error'''

new_call = '''    def _call_groq(self, prompt, max_tokens=12000):
        last_error = None
        for model in self.models:
            try:
                gemini = genai.GenerativeModel(model)
                response = gemini.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=0.7,
                    )
                )
                if model != self.models[0]:
                    print(f"Used fallback model: {model}")
                return response.text
            except Exception as e:
                print(f"Model {model} failed: {str(e)[:80]}, trying next...")
                last_error = e
                continue
        raise last_error'''

# Replace model list
old_models = '''        self.models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant",
            "qwen/qwen3-32b",
            "moonshotai/kimi-k2-instruct-0905",
            "moonshotai/kimi-k2-instruct",
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "groq/compound",
            "groq/compound-mini",
        ]'''

new_models = '''        self.models = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.0-pro",
        ]'''

content = content.replace(old_import, new_import)
content = content.replace(old_call, new_call)
content = content.replace(old_models, new_models)

open('ai_brain.py', 'w', encoding='utf-8').write(content)
print("Done! Switched to Gemini.")
print("Groq still present:", "from groq" in content)
print("Gemini present:", "google.generativeai" in content)