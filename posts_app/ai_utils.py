import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get('AI_API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def ai_response_to_comment(comment_text: str, post_text: str) -> str:
    # Simple AI response writer
    response = model.generate_content(f"""
    Please, give a friendly response to the next comment: {comment_text}. 
    This comment was made for post (just in case for context): {post_text}
    """)
    return response.text


def ai_check_for_rude_words(text: str) -> bool:
    # Return True if this post or comment need to be blocked
    if not text:
        return False
    try:
        response = model.generate_content(f"""
        Please, check this text for rude words: {text}. 
        Your answer must be strictly: 0 or 1. 0 if this text is appropriate and 1 if text contain 
        rude words""")
        r = response.text
        if r.startswith("Please provide the text you want me to check"):
            return False
        result = int(r)
        if r:
            return bool(result)
    except ValueError as e:
        print(e)
        return True
