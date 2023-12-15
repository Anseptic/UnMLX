import re
from email.utils import parsedate, formatdate
from datetime import datetime

def parse_emlx(emlx_content):
    # regular expressions for extracting information
    header_pattern = re.compile(r"^([^\s:]+):\s*(.*)$")
    from_pattern = re.compile(r"^From: (.+)$")

    # variables to store extracted information
    email_time = None
    email_headers = {}
    sender = None
    receiver = None

    # split EMLX content into lines
    lines = emlx_content.split('\n')

    # iterate through lines to extract information
    for line in lines:
        # extract email headers
        header_match = header_pattern.match(line)
        if header_match:
            key, value = header_match.groups()
            email_headers[key] = value

            # extract sender
            if key.lower() == 'from':
                sender_match = from_pattern.match(line)
                if sender_match:
                    sender = sender_match.group(1)

    # extract receiver
    receiver = email_headers.get('To', None)

    # extract date using parsedate
    email_time = parsedate(email_headers.get('Date', None))

    # create a datetime object from parsed values
    if email_time:
        email_time = datetime(*email_time[:6])

    # return the extracted information
    return {
        'time': email_time,
        'headers': email_headers,
        'sender': sender,
        'receiver': receiver
    }

# prompt user for the location and name of the EMLX file
file_location = input("Enter the location of the EMLX file: ")
file_name = input("Enter the name of the EMLX file: ")

# construct the full file path
file_path = f"{file_location}/{file_name}"

# read the content of EMLX file
try:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        emlx_content = file.read()
        result = parse_emlx(emlx_content)

    # display result in neat format
    print("\nParsed Information:")
    print(f"Time: {result['time'].strftime('%Y-%m-%d %H:%M:%S') if result['time'] else None}")
    print("Headers:")
    for key, value in result['headers'].items():
        print(f"  {key}: {value}")
    print(f"Sender: {result['sender']}")
    print(f"Receiver: {result['receiver']}")

except FileNotFoundError:
    print(f"\nError: The file '{file_path}' does not exist.")
except Exception as e:
    print(f"\nAn error occurred: {e}")