import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE

def get_gmail_service():
    creds = None

    # Load token.json if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_recent_emails(max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        for part in msg_data["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                text = base64.urlsafe_b64decode(
                    part["body"]["data"]).decode("utf-8")
                email_list.append(text)

    return email_list
