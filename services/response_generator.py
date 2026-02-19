import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompts import RESPONSE_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(question: str, books: list) -> str:
    """
    Uses Gemini to generate a natural language answer
    based on the question and retrieved book results.
    """
    #no results found
    if not books:
        return "I couldn't find any matching books in the dataset."

    model = genai.GenerativeModel("gemini-2.5-flash")  

    prompt = RESPONSE_PROMPT.format(
        question=question,
        books=books
    )

    response = model.generate_content(prompt)
    return response.text