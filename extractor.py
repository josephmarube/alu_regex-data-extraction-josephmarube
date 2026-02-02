import re
import json
import os

# Regex Patterns

EMAIL_REGEX = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
)

URL_REGEX = re.compile(
    r'\bhttps?://[^\s<>"]+(?<![.,])'
)

PHONE_REGEX = re.compile(
    r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
)

CREDIT_CARD_REGEX = re.compile(
    r'\b(?:\d{4}[- ]?){3}\d{4}\b'
)

TIME_REGEX = re.compile(
    r'\b(?:(?:[01]?\d|2[0-3]):[0-5]\d(?:\s?[APap][Mm])?|(?:[01]\d|2[0-3])[0-5]\d\s?hrs)\b'
)

HASHTAG_REGEX = re.compile(
    r'#\w+'
)

# Security Helpers

def mask_credit_card(card):
    """Mask all but last 4 digits of credit card"""
    digits = re.sub(r'\D', '', card)
    return "**** **** **** " + digits[-4:]

def mask_email(email):
    """Keep first and last character of the username."""
    username, domain = email.split("@")

    if len(username) <= 2:
        masked_username = "*" * len(username)
    else:
        masked_username = username[0] + "*" * (len(username) - 2) + username[-1]

    return f"{masked_username}@{domain}"

def is_safe_match(value):
    """
    Reject common malicious patterns like script tags or SQL injection attempts.
    """
    blacklist = [
        r'<script',
        r'</script>',
        r'drop\s+table',
        r'select\s+.*\s+from'
    ]
    for pattern in blacklist:
        if re.search(pattern, value, re.IGNORECASE):
            return False
    return True


# Extraction Logic

def extract_data(text):
    extracted = {
        "emails": [],
        "urls": [],
        "phones": [],
        "credit_cards": [],
        "times": [],
        "hashtags": []
    }

    for match in EMAIL_REGEX.findall(text):
        if is_safe_match(match):
            extracted["emails"].append(mask_email(match))

    for match in URL_REGEX.findall(text):
        if is_safe_match(match):
            # block insecure http links
            if match.startswith("http://"):
                continue
            
            extracted["urls"].append(match)

    for match in PHONE_REGEX.findall(text):
        if is_safe_match(match):
            extracted["phones"].append(match)

    for match in CREDIT_CARD_REGEX.findall(text):
        extracted["credit_cards"].append(mask_credit_card(match))

    for match in TIME_REGEX.findall(text):
        extracted["times"].append(match)

    for match in HASHTAG_REGEX.findall(text):
        extracted["hashtags"].append(match)

    return extracted

# Main Execution

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    input_path = os.path.join(BASE_DIR, "sample_input.txt")
    output_path = os.path.join(BASE_DIR, "sample_output.json")

    with open(input_path, "r", encoding="utf-8") as file:
        raw_text = file.read()

    result = extract_data(raw_text)

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=4)

    print("Extraction complete.")
          
    print("Output saved to sample_output.json")
