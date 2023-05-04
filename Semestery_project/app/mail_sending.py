from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from werkzeug.security import generate_password_hash

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
CREDENTIAL = os.path.join(PROJECT_ROOT, "static", "json", "credentials.json")
TOKEN = os.path.join(PROJECT_ROOT, "static", "json", "token.json")

SCOPES = ["https://mail.google.com/"]


def validation_code_generator(length=6):
    """Generates a random string of letters and digits with a given length
    :param length: length of the string, default is 6
    :return: random string
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_gmail_service(credentials_file):
    """Creates a Gmail API service instance with OAuth2 credentials.
    :param credentials_file: path to the JSON file containing the OAuth credentials
    :return: Gmail API service instance
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if TOKEN:
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


# GOOGLE API
# def send_validation_email(
#     sender="noreply@gmail.com", receiver=None, credentials_file=CREDENTIAL
# ):
#     """Sends an email with a validation code to the given receiver
#     :param sender: sender's email address
#     :param receiver: receiver's email address
#     :param smtp_port: SMTP server port
#     :param credentials_file: path to the JSON file containing the OAuth credentials
#     :return: hashed validation code
#     """

#     # Compose the message
#     validation_code = validation_code_generator()
#     message = MIMEText(f"The validation code for your account is: {validation_code}")
#     message["to"] = receiver
#     message["subject"] = "Validation code from Universal Bank"
#     message["from"] = sender
#     create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

#     try:
#         # Call the Gmail API
#         service = get_gmail_service(credentials_file)
#         message = (
#             service.users().messages().send(userId="me", body=create_message).execute()
#         )
#         print(f"Message Id: {message['id']}")

#     except HttpError as error:
#         # TODO(developer) - Handle errors from gmail API.
#         print(f"An error occurred: {error}")

#     return generate_password_hash(validation_code)

import smtplib
import configparser
def send_validation_email(sender='noreply@universalbank.com', receiver=None):
    """
    Sends an email with a validation code to the given receiver
    :param sender: sender's email address
    :param receiver: receiver's email address
    :return: hashed validation code
    """

    config = configparser.ConfigParser()

    with open('app/config.ini') as f:
        config.read_file(f)

    smtp_server = config.get('SMTP', 'server')
    smtp_port = config.getint('SMTP', 'port')
    smtp_username = config.get('SMTP', 'username')
    smtp_password = config.get('SMTP', 'password')

    # Compose the message
    validation_code = validation_code_generator()
    msg = MIMEMultipart()
    msg["to"] = receiver
    msg["subject"] = "Validation code from Universal Bank"
    msg["from"] = sender
    msg.attach(MIMEText(f"The validation code for your account is: {validation_code}"))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())

    print(f"Message sent to {receiver}, successfully.")
    return generate_password_hash(validation_code)


if __name__ == "__main__":
    send_validation_email(receiver="karel.najman@tul.cz")