# 🚀 Travel Scheduler AI

An intelligent automation tool that reads travel booking emails (flight, train, bus), extracts booking details using AI, and automatically schedules them in Google Calendar with reminders.  
Supports both **Gmail inbox emails** and **local text files (.txt)** for testing.

---

## ✅ Features

✔ Extracts travel details (date, time, source, destination, passenger, PNR) using AI  
✔ Supports **Flight, Train, and Bus** booking emails  
✔ Adds events to **Google Calendar automatically**  
✔ Sets **3-hour prior reminders** for all journeys  
✔ Local testing using `.txt` files – no need to send actual emails  
✔ Modular, extensible code structure (services-based architecture)  
✔ Uses OAuth 2.0 securely for Gmail and Calendar access

---

## 🛠️ Tech Stack

| Component         | Technology Used |
|------------------|------------------|
| Language         | Python           |
| AI Model         | Google Gemini / OpenAI GPT |
| Email Fetching   | Gmail API        |
| Calendar Sync    | Google Calendar API |
| Authentication   | OAuth 2.0        |
| File-Based Testing | Local `.txt` email files |

---

## 📁 Project Structure

TravelSchedulerAI/
├── app/
│ ├── main.py # Full Gmail → AI → Calendar workflow
│ ├── config.py # API scopes, settings, timezones
│ ├── services/
│ │ ├── gmail_service.py # Reads emails via Gmail API
│ │ ├── ai_extractor.py # AI model extracts travel details
│ │ ├── calendar_service.py# Creates events in Google Calendar
│
├── tests/
│ ├── sample_emails/ # Test files for offline mode
│ │ ├── flight_email.txt
│ │ ├── train_email.txt
│ │ └── bus_email.txt
│ ├── test_local_emails.py # Run AI + Calendar without Gmail
│
├── credentials/
│ ├── credentials.json # OAuth client from Google Cloud Console
│ ├── token.json # Generated after login (do not upload)
│
├── requirements.txt
├── .env # API key for Gemini/OpenAI
├── README.md


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ComderCK12/Travel-Scheduler-AI.git
cd TravelSchedulerAI
```

### 2️⃣ Install Required Packages
```bash
pip install -r requirements.txt
```

### 3️⃣ Add .env File
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4️⃣ Add Google OAuth Credentials
Download from Google Cloud Console and save as:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### ▶️ How to Run
### ✅ Option A: Run with Local Sample Emails (No Gmail Needed)
```bash
python tests/test_local_emails.py
```
✔ Loads .txt files from tests/sample_emails/
✔ Extracts travel details using AI
✔ Adds events to Google Calendar after OAuth login

### ✅ Option B: Run with Real Gmail Travel Emails
```bash
python -m app.main
```
✔ Fetches unread booking emails from Gmail
✔ AI extracts travel details
✔ Creates Calendar events automatically

---

### ✅ Example Output (AI Extracted JSON)
```json
{
  "traveler_name": "Chirag Kathoye",
  "travel_mode": "flight",
  "from": "Mumbai (BOM)",
  "to": "Delhi (DEL)",
  "departure_date": "12 February 2026",
  "departure_time": "06:30 AM",
  "arrival_time": "08:45 AM",
  "pnr_or_ticket_no": "AB12CD"
}
```

---

### ✅ Google Calendar Integration

Events created in Google Calendar include:

- **Title:** `Flight: Mumbai → Delhi (Chirag Kathoye)`
- **Start & End Time:** Based on departure and arrival (or default duration)
- **Reminder:** Triggered 3 hours before departure
- **Description:** Includes PNR, passenger name, and other booking details

---

### 📌 Future Enhancements

- 📄 **PDF Ticket Extraction (OCR Support)** – Read and extract travel details from PDF attachments automatically  
- 🔁 **Return (Round-Trip) Journey Handling** – Create two calendar events for onward and return trips  
- 👥 **Multi-Passenger Travel Events** – Support for multiple travelers in one email  
- 💬 **WhatsApp/SMS Reminders** – Notify users via messaging platforms before travel  
- ⚙️ **Background Service / Cron Job** – Run automatically without manual execution

---

### 👤 Author

**Chirag Kathoye**  
Built with Python, AI, and automation ❤️  
Have ideas or suggestions? Open an issue or start a discussion!

Would you like me to add:

- ⭐ **GitHub badges** (Python version, License, Stars, Forks, etc.)
- 📸 **Screenshots or demo GIFs**

Just let me know!
