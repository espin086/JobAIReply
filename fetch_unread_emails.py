import imaplib
from dotenv import dotenv_values

# Load the .env file
env = dotenv_values(".env")

# Get the username and password from the .env file
username = env["USERNAME"]
password = env["PASSWORD"]


def fetch_unread_emails(username, password):
    # Connect to the Gmail IMAP server
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to the Gmail account
    imap_server.login(username, password)

    # Select the mailbox (e.g., 'INBOX')
    imap_server.select("INBOX")

    # Search for unread emails
    _, message_numbers = imap_server.search(None, "UNSEEN")

    # Fetch the unread emails
    for num in message_numbers[0].split():
        _, message_data = imap_server.fetch(num, "(RFC822)")
        # Process the email data as needed
        print(message_data[0][1])  # Print the email data

    # Logout from the Gmail account
    imap_server.logout()
    return message_data


if __name__ == "__main__":
    fetch_unread_emails(username=username, password=password)
