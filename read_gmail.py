import base64
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.metadata",
]

def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_latest_school_email(sender_filter: str = ""):
    service = build("gmail", "v1", credentials=authenticate_gmail())
    query = f'from:{sender_filter}' if sender_filter else ""

    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])
    if not messages:
        return None, None

    msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()
    payload = msg["payload"]
    parts = payload.get("parts", [])

    email_text = ""
    for part in parts:
        if part["mimeType"] == "text/plain":
            data = part["body"]["data"]
            email_text = base64.urlsafe_b64decode(data).decode()
            break
        elif part["mimeType"] == "text/html":
            data = part["body"]["data"]
            html = base64.urlsafe_b64decode(data).decode()
            soup = BeautifulSoup(html, "html.parser")
            email_text = soup.get_text()
            break

    headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
    subject = headers.get("Subject", "")

    return subject, email_text.strip()
