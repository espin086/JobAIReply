import imaplib
from dotenv import dotenv_values
import logging
import email
import json
import sys
import argparse
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def send_email(username, password, recipient, subject, message):
    """Send an email using SMTP."""

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = recipient
    msg["Subject"] = subject

    # Add the message body
    msg.attach(MIMEText(message, "plain"))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, password)

        # Send the email
        server.send_message(msg)
        server.quit()
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")


def main():
    recipient = "jj.espinoza.la@gmail.com"
    subject = "Test Email from Python"
    message = "This is a test email sent from Python"

    # Create IMAP server
    imap_server = create_imap_server(username, password)
    logger.info("IMAP server created and connected.")

    # Send email
    send_email(username, password, recipient, subject, message)
    logger.info("Email sent.")

    # Close IMAP server connection
    imap_server.logout()
    logger.info("IMAP server connection closed.")


if __name__ == "__main__":
    main()
