import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Fetching environment variables
from_addr = os.getenv('EMAIL')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Debugging prints
print(f"EMAIL: {from_addr}")
print(f"PASSWORD: {'*' * len(password) if password else None}")

# Ensure the path is correct
csv_file_path = "D:/Shwet/python-projects/auto-mail/abc.csv"

# Check if environment variables are retrieved correctly
if not from_addr or not email or not password:
    raise ValueError("Environment variables for email and/or password are not set correctly.")

if not os.path.isfile(csv_file_path):
    print(f"Error: The file '{csv_file_path}' was not found.")
else:
    try:
        data = pd.read_csv(csv_file_path)
        if data.empty:
            raise ValueError("CSV file is empty.")
    except pd.errors.EmptyDataError:
        print(f"Error: No columns to parse from file '{csv_file_path}'.")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        to_addr = data['email'].tolist()
        name = data['name'].tolist()

        l = len(name)

        for i in range(l):
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr[i]
            msg['Subject'] = 'Just to Check'

            body = f"Hello {name[i]}, Enter your content here"
            msg.attach(MIMEText(body, 'plain'))

            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(email, password)
            text = msg.as_string()
            mail.sendmail(from_addr, to_addr[i], text)
            mail.quit()

        print("Emails sent successfully.")
