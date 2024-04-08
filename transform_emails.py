import json
import quopri
import re
from html import unescape
import base64
import pandas as pd
from dateutil import parser
import gpt


def clean_email_content(content):
    """
    Clean the content of an email.

    Args:
        content (str): The content of the email.

    Returns:
        str: The cleaned content of the email.
    """
    # Decode quoted-printable encoding
    decoded_content = quopri.decodestring(content).decode("utf-8", errors="ignore")
    # Decode HTML entities
    decoded_content = unescape(decoded_content)

    # Check if content has base64 encoding
    if "base64" in decoded_content:
        # Extract the base64 encoded message
        encoded_message = re.search(r"base64,(.*)", decoded_content)
        if encoded_message:
            # Decode the base64 encoded message
            encoded_message = encoded_message.group(1)
            decoded_message = base64.b64decode(encoded_message).decode("utf-8")
            # Update the decoded content with the decoded message
            decoded_content = decoded_message

    return decoded_content


email_cats = [
    "jobalert",
    "appconfirmation",
    "interviewinvite",
    "applicationrejected",
    "recruiteroutreach",
    "other",
]

### MAIN SCRIPT ###
with open("emails.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)
df["date"] = df["date"].apply(parser.parse)
df.content = df.content.str.replace("\n", " ")
pd.set_option("display.max_colwidth", None)


# Apply the cleaning function to your DataFrame
df["cleaned_content"] = df["content"].apply(clean_email_content)


prompt = "Respond to this emails: \n" + df["cleaned_content"][1342]

response = gpt.gpt3_chat(prompt)

# Display the cleaned/processed DataFrame
print(df["cleaned_content"][1342])
print(response)
