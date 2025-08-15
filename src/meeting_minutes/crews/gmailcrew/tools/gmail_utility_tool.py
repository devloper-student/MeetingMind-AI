import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

import markdown

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    {final_email_body}
</body>
</html>
"""


def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Returns:
        service: Authorized Gmail API service instance.
    """
    creds = None
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # The file token.json stores the user's access and refresh tokens.
    token_path = os.path.join(script_dir, 'token.json')
    credentials_path = os.path.join(script_dir, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Credentials not found at {credentials_path}.")

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, message_txt):
    """Create an email message using Gmail API with proper UTF-8 encoding."""

    # Ensure the message text is properly encoded as UTF-8
    if not message_txt:
        return None

    try:
        # Sanitize the input text to ensure proper UTF-8 encoding
        safe_message_txt = message_txt.encode(
            'utf-8', errors='ignore').decode('utf-8')

        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
        formatted_html = HTML_TEMPLATE.format(
            final_email_body=md.convert(safe_message_txt))

        message = EmailMessage()
        message['From'] = sender
        message['To'] = to
        message['Subject'] = subject
        message.set_content(formatted_html, subtype='html',
                            charset='utf-8')  # Explicitly set UTF-8

        # Encode the message with UTF-8
        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()).decode('utf-8')

        return {'raw': encoded_message}

    except Exception as error:
        print(f'An error occurred: {error}')
        return None


def create_draft(service, user_id, message_body):
    """Create a draft email using Gmail API with proper error handling."""

    if message_body is None:  # Check for None input
        print("Error: message_body is None")
        return None

    try:
        # If message_body is a dict with 'raw' key, use it directly
        if isinstance(message_body, dict) and 'raw' in message_body:
            draft = {
                'message': message_body
            }
        else:
            # If it's a string, encode it properly
            if isinstance(message_body, str):
                safe_body = message_body.encode(
                    'utf-8', errors='ignore').decode('utf-8')
                draft = {
                    'message': {
                        'raw': base64.urlsafe_b64encode(safe_body.encode('utf-8')).decode('utf-8')
                    }
                }
            else:
                print(f"Unexpected message_body type: {type(message_body)}")
                return None

        created_draft = service.users().drafts().create(
            userId=user_id, body=draft).execute()
        print(f'Draft Id: {created_draft["id"]}')
        return created_draft

    except Exception as error:
        print(f'An error occurred: {error}')
        return None
