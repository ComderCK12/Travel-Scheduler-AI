from app.services.gmail_service import fetch_recent_emails
from app.services.ai_extractor import extract_travel_details
from app.services.calendar_service import create_calendar_event
import json

if __name__ == "__main__":
    print("\n📩 Fetching recent emails...")
    emails = fetch_recent_emails(5)

    if not emails:
        print("❌ No emails found.")
        exit()

    for idx, email in enumerate(emails):
        # print(f"\n--- Email {idx + 1} ---")

        try:
            # 1. Extracting travel details using AI
            print(f"🧠 Extracting travel details for mail {idx + 1} using AI...")
            travel_details = extract_travel_details(email)
            print(f"📝 Raw AI Output: {travel_details}")

            # 2. Try converting to Python dict
            print(f"📦 Converting AI output to Python dictionary for mail {idx + 1}...")
            try:
                travel_details_dict = json.loads(travel_details)
            except json.JSONDecodeError:
                print(f"⚠️ AI did not return valid JSON. Skipping this email. Mail ID: {idx + 1}")
                continue

            # 3. Check required fields before creating event
            required_fields = ["traveler_name", "from", "to", "departure_date", "departure_time"]
            if not all(travel_details_dict.get(field) for field in required_fields):
                print("⚠️ Missing important travel information. Skipping event creation.")
                print(f"Missing fields: {[f for f in required_fields if not travel_details_dict.get(f)]}")
                continue

            # 4. Create Google Calendar event
            print("📅 Creating calendar event...")
            created_event = create_calendar_event(travel_details_dict)

            print("✅ Event added to Google Calendar!")
            print("🔗 Event Link:", created_event.get("htmlLink"))

        except Exception as e:
            print(f"❌ Error while processing Email {idx + 1}: {e}")

    print("\n✅ Process completed.\n")