# utils.py
import openai
from django.conf import settings

def call_gemini_api(prompt):
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7,
    )
    return response.choices[0].message.content
