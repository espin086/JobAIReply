import imaplib
from dotenv import dotenv_values
import logging
import email
import json
import sys
import argparse
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the .env file
env = dotenv_values(".env")

# Get the username and password from the .env file
username = env["USERNAME"]
password = env["PASSWORD"]


def create_imap_server(username, password):
    """Create and connect to the Gmail IMAP server using SSL."""
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(username, password)
    imap_server.select("INBOX")
    return imap_server


class EmailMetrics:
    """Class to store email metrics."""

    def __init__(self, date, to, subject, sender, content):
        self.date = date
        self.to = to
        self.subject = subject
        self.sender = sender
        self.content = content

    def to_dict(self):
        """Convert EmailMetrics object to a dictionary."""
        return {
            "date": self.date,
            "to": self.to,
            "subject": self.subject,
            "sender": self.sender,
            "content": self.content,
        }


def parse_email(email_data):
    """Parse email data and return an EmailMetrics object."""
    message = email.message_from_bytes(email_data)
    date = message["date"]
    to = message["to"]
    subject = message["subject"]
    sender = message["from"]
    content = ""
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            content = part.as_string()
    email_metrics = EmailMetrics(date, to, subject, sender, content)
    return email_metrics


def read_emails(imap_server):
    """Read all emails from the Gmail account and return a list of EmailMetrics objects."""
    _, message_numbers = imap_server.search(None, "ALL")
    all_emails = []
    for num in message_numbers[0].split():
        logging.info(f"Fetching email number {num}")
        _, message_data = imap_server.fetch(num, "(RFC822)")
        email_metrics = parse_email(message_data[0][1])
        all_emails.append(email_metrics.to_dict())
    return all_emails


def read_unread_emails(imap_server):
    """Read unread emails from the Gmail account."""
    _, message_numbers = imap_server.search(None, "UNSEEN")
    unread_emails = []
    for num in message_numbers[0].split():
        _, message_data = imap_server.fetch(num, "(RFC822)")
        unread_emails.append(message_data[0][1])
    return unread_emails


def fetch_unread_emails(username, password):
    """Fetch unread emails and return them as a list of EmailMetrics objects."""
    imap_server = create_imap_server(username, password)
    emails = read_emails(imap_server)
    imap_server.logout()
    return emails


def save_emails_to_json(emails, filename):
    """Save emails to a JSON file."""
    with open(filename, "w") as file:
        json.dump(emails, file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Fetch unread emails and save them to a JSON file."
    )
    parser.add_argument("username", help="Gmail username", default=username)
    parser.add_argument("password", help="Gmail password", default=password)
    parser.add_argument("--output", help="Output filename", default="emails.json")
    args = parser.parse_args()

    username = args.username
    password = args.password
    output_filename = args.output

    emails = fetch_unread_emails(username, password)
    save_emails_to_json(emails, output_filename)
