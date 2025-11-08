# app/services/calendar_service.py
import os
from datetime import datetime, timedelta
from dateutil import parser as dtparser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.config import (
    SCOPES, CREDENTIALS_FILE, TOKEN_FILE,
    DEFAULT_TIMEZONE, DEFAULT_DURATION_MIN, REMINDER_MINUTES, CALENDAR_ID
)

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("Calendar token missing. Run Gmail auth first to create token.json.")
    return build("calendar", "v3", credentials=creds)

def _smart_parse_datetime(date_str: str | None, time_str: str | None, tz: str) -> datetime | None:
    """
    Accepts flexible inputs like:
      date: '2025-02-10' OR '10 Feb 2025' OR 'Feb 10, 2025'
      time: '06:30 AM' OR '18:45' OR None
    Returns naive datetime in local terms (timezone added later when sending to Google).
    """
    if not date_str:
        return None
    text = date_str.strip()
    if time_str:
        text = f"{date_str.strip()} {time_str.strip()}"
    # dateutil can parse lots of formats
    dt = dtparser.parse(text, dayfirst=False)  # adjust if most emails are DD/MM/YYYY
    return dt

def create_calendar_event(travel_data: dict):
    """
    travel_data expects (strings may be empty):
      traveler_name, travel_mode, from, to,
      departure_date, departure_time, arrival_time (optional),
      pnr_or_ticket_no, for_whom
    """
    service = get_calendar_service()

    # Required fields check
    required = ["from", "to", "departure_date"]
    missing = [k for k in required if not travel_data.get(k)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    # Parse start datetime
    start_dt = _smart_parse_datetime(
        travel_data.get("departure_date"),
        travel_data.get("departure_time"),
        DEFAULT_TIMEZONE
    )
    if not start_dt:
        raise ValueError("Could not parse departure date/time.")

    # Parse end datetime using arrival_time if available, otherwise use duration fallback
    end_dt = None
    if travel_data.get("arrival_time"):
        # If arrival time is earlier than departure (e.g., crosses midnight), add a day
        cand_end = _smart_parse_datetime(travel_data.get("departure_date"), travel_data.get("arrival_time"), DEFAULT_TIMEZONE)
        if cand_end and cand_end <= start_dt:
            cand_end = cand_end + timedelta(days=1)
        end_dt = cand_end

    if not end_dt:
        # Fallback duration
        end_dt = start_dt + timedelta(minutes=DEFAULT_DURATION_MIN)

    # Compose event fields
    traveler = (travel_data.get("traveler_name") or "").strip() or "Traveler"
    who = (travel_data.get("for_whom") or "").strip()
    who_suffix = f" ({who})" if who and who.lower() != "self" else ""
    mode = (travel_data.get("travel_mode") or "Travel").title()
    src = (travel_data.get("from") or "").strip()
    dst = (travel_data.get("to") or "").strip()
    pnr = (travel_data.get("pnr_or_ticket_no") or "").strip()

    summary = f"{mode}: {src} → {dst} ({traveler})"
    description_lines = []
    if pnr:
        description_lines.append(f"PNR/Ticket: {pnr}")
    if who:
        description_lines.append(f"For: {who}")
    description = "\n".join(description_lines) if description_lines else ""

    event_body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": DEFAULT_TIMEZONE},
        "end":   {"dateTime": end_dt.isoformat(),   "timeZone": DEFAULT_TIMEZONE},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": REMINDER_MINUTES}
            ]
        }
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
    return created
