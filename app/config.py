# app/config.py
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "credentials/token.json"

# New: calendar & time defaults
DEFAULT_TIMEZONE = "Asia/Kolkata"
DEFAULT_DURATION_MIN = 120         # when arrival_time is missing
REMINDER_MINUTES = 180             # 3 hours prior
CALENDAR_ID = "primary"            # change to another calendar ID if needed