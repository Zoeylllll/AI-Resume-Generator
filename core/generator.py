import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def polish_resume_text(text: str, lang: str, template: str = "tech") -> str:
    style_prompts = {
        "tech": "Use a concise and professional tone suitable for a technical resume.",
        "business": "Use a confident and polished tone suitable for business leadership roles.",
        "academic": "Use a formal and scholarly tone suitable for academic research positions."
    }

    prompt = f"{style_prompts.get(template, '')} Translate or polish the following resume content into {lang.upper()}:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()
