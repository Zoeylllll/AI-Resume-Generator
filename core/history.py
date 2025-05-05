# core/history.py
import json
import os
from datetime import datetime

def save_resume_history(content, lang, template):
    record = {
        "timestamp": datetime.now().isoformat(),
        "lang": lang,
        "template": template,
        "content": content
    }
    history_file = "resume_history.json"
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
