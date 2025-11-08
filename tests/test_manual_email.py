import json
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.services.ai_extractor import extract_travel_details
from app.services.calendar_service import create_calendar_event
from app.config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE

SAMPLE_EMAIL_DIR = "tests/sample_emails"

# ✅ Google Authentication — Works independently (no need to run main.py)
def authenticate_google():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("🔑 Opening browser for Google Login (Gmail + Calendar permission)...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

    print("✅ Authentication successful! Token saved.")
    return creds

if __name__ == "__main__":
    print("\n📂 Reading local sample emails from: tests/sample_emails/...")

    # ✅ Step 1: Authenticate before doing anything else
    authenticate_google()

    # ✅ Step 2: Loop through email files (same as your main.py structure)
    for idx, file in enumerate(os.listdir(SAMPLE_EMAIL_DIR), start=1):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(SAMPLE_EMAIL_DIR, file)
        with open(file_path, "r") as f:
            email = f.read()

        print(f"\n--- Sample Email {idx}: {file} ---")
        print(email)

        # ✅ Step 3: Extract travel details using AI
        print("🧠 Extracting travel details...")
        travel_details = extract_travel_details(email)
        print("📝 AI Output:", travel_details)

        # ✅ Step 4: Clean ```json formatting (if AI adds it)
        cleaned_json = travel_details.strip()
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json.replace("```json", "").replace("```", "").strip()

        # ✅ Step 5: Convert JSON to Python dict
        try:
            travel_dict = json.loads(cleaned_json)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON from AI. Skipping this email.")
            continue

        print("✅ Parsed JSON:", travel_dict)

        # ✅ Step 6: Check required fields exist
        required = ["from", "to", "departure_date", "departure_time"]
        if not all(travel_dict.get(f) for f in required):
            print("⚠️ Missing important fields. Skipping calendar event.")
            continue

        # ✅ Step 7: Create Calendar Event
        try:
            event = create_calendar_event(travel_dict)
            print("✅ Event added to calendar!")
            print("🔗 Event Link:", event.get("htmlLink"))
        except Exception as e:
            print("❌ Error adding event:", e)

    print("\n✅ Done! All sample emails processed.")
