import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# models = genai.list_models()
# for model in models:
#     print(f"Model Name: {model.name}, Generation: {model.supported_generation_methods}")

def extract_travel_details(email_text: str):
    prompt = f"""
    You are an AI that extracts travel booking details from the email below.
    Return ONLY a valid JSON object in this format:

    {{
      "traveler_name": "",
      "travel_mode": "",
      "from": "",
      "to": "",
      "departure_date": "",
      "departure_time": "",
      "arrival_time": "",
      "duration": "",
      "pnr_or_ticket_no": "",
      "for_whom": ""
    }}

    If something is missing, leave it as an empty string.

    EMAIL CONTENT:
    {email_text}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text
