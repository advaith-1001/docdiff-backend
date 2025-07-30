import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)


async def get_ai_summary(text1: str, text2: str) -> str:

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are a helpful assistant who specializes in comparing documents. Your task is to provide a concise, bullet-point summary of the key differences between two versions of a text.
    Analyze the 'Old Version' and the 'New Version' provided below. Focus on significant additions, deletions, and major rephrasing. Ignore minor punctuation or capitalization changes unless they change the meaning.
    Start with a one-sentence overview, followed by a short detailed description of the key differences between two versions of a text.

    --- OLD VERSION ---
    {text1}

    --- NEW VERSION ---
    {text2}

    --- SUMMARY OF DIFFERENCES ---
    """

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Could not generate AI summary."