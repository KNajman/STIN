# vyhledani aktuálniho kurzu měny na webu ČNB
# vrací kurz měny vůči CZK
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import hashlib
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re


def get_currency_exchange_rate(currency_code, date=None):
    try:
        if date:
            url = f"https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_ostatnich_men/kurzy.txt?date={date}"
        else:
            url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"
        r = requests.get(url)
        r.raise_for_status()
        lines = r.text.splitlines()
        # line format: country|currency|amount|code|rate
        for line in lines:
            fields = line.split("|")
            if len(fields) < 5:
                continue
            if fields[3] == currency_code:
                amount = float(fields[2].replace(",", "."))
                rate = float(fields[4].replace(",", "."))
                return rate / amount
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def validation_code_generator(length=6):
    """Generates a random string of letters and digits with a given length
    :param length: length of the string, default is 6
    :return: random string
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def hash_code_generator(code):
    """Hashes the given code
    :param code: string to be hashed
    :return: hashed string
    """
    return hashlib.sha256(code.encode()).hexdigest()


def compare_hash_codes(code, hashed_code):
    """Compares the given code with the given hashed code
    :param code: string to be hashed
    :param hashed_code: hashed string
    :return: True if the code and the hashed code are the same, False otherwise
    """
    return hash_code_generator(code) == hashed_code


SCOPES = ["https://mail.google.com/"]


def get_gmail_service(credentials_file):
    """Creates a Gmail API service instance with OAuth2 credentials.
    :param credentials_file: path to the JSON file containing the OAuth credentials
    :return: Gmail API service instance
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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


def send_validation_email(sender, receiver, smtp_server, smtp_port, credentials_file):
    """Sends an email with a validation code to the given receiver
    :param sender: sender's email address
    :param receiver: receiver's email address
    :param smtp_server: SMTP server address
    :param smtp_port: SMTP server port
    :param credentials_file: path to the JSON file containing the OAuth credentials
    :return: hashed validation code
    """

    # Compose the message
    validation_code = validation_code_generator()
    hashed_code = hash_code_generator(validation_code)
    message = MIMEText(f"The validation code for your account is: {validation_code}")
    message["to"] = receiver
    message["subject"] = "Validation code from Python"
    message["from"] = sender
    create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        # Call the Gmail API
        service = get_gmail_service(credentials_file)
        message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f"Message Id: {message['id']}")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    return hashed_code


def is_valid_email(email):
    """Checks if the email address is valid"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_pin_valid(pin):
    """Checks if the PIN is valid"""
    pattern = r"^[0-9]{4}$"
    return re.match(pattern, pin) is not None

def is_name_valid(name):
    """Checks if the name is valid"""
    pattern = r"^[a-zA-Z]{2,}$"
    return re.match(pattern, name) is not None


# test main
if __name__ == "__main__":
    currency = "USD"
    rate = get_currency_exchange_rate(currency)
    print(f"Kurz měny {currency} je {rate}")

    hashed_code = send_validation_email(
        "vasebanka@noreply.cz",
        "karel.najman@tul.cz",
        "smtp.gmail.com",
        587,
        "C:/Users/najma/TUL/6_semestr/STIN_Softwarove_inzenirstvy/credentials.json",
    )

    print("Email sent successfully.")
    print(f"Hashed validation code: {hashed_code}")
