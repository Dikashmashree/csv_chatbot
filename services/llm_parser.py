import json
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Normalization Layer

COLUMN_ALIASES = {
    "author": "authors",
    "writer": "authors",
    "written_by": "authors",
    "book_title": "title",
    "rating": "average_rating",
    "pages": "num_pages",
    "year": "published_year"
}
# llm
def parse_query(question: str):
    prompt = f"""
You are a strict JSON query generator.
Dataset columns:
- isbn13
- title
- subtitle
- authors
- categories
- description
- published_year
- average_rating
- num_pages
- ratings_count

Rules:
- Return ONLY valid JSON.
- No explanation.
- Use exact column names.
- Extract clean values (no extra words like "write", "book", etc.)

JSON format:
{{
  "filters": {{}},
  "sort_by": null,
  "order": "desc",
  "limit": 5
}}

User question:
{question}
"""
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # to remove markdown code block if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```[a-z]*\n?", "", raw_text)
        raw_text = re.sub(r"\n?```$", "", raw_text).strip()

    try:
        parsed = json.loads(raw_text)
    except Exception:
        print("LLM JSON ERROR:", raw_text)
        return {
            "filters": {},
            "sort_by": None,
            "order": "desc",
            "limit": 5
        }

    # Normalize Filters
    if "filters" in parsed:
        normalized_filters = {}
        for key, value in parsed["filters"].items():
            # Normalize column name via aliases
            normalized_key = COLUMN_ALIASES.get(key.lower(), key)

            # Clean value — strip common junk words
            cleaned_value = re.sub(
                r"\b(write|wrote|book|books|novel|novels)\b",
                "",
                str(value),
                flags=re.IGNORECASE
            ).strip()

            normalized_filters[normalized_key] = cleaned_value
        parsed["filters"] = normalized_filters

    return parsed