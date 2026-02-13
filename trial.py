import google.generativeai as gen_ai
import os
from dotenv import load_dotenv

load_dotenv()
gen_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available models:")
for m in gen_ai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)