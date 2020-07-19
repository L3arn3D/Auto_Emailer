import csv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import sys

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = input("Enter the sender e-mail address: ")
password = getpass.getpass("Enter the Password: ", stream=sys.stderr)


message = MIMEMultipart("alternative")
message["Subject"] = "Hello World!"
message["From"] = sender_email


# Create the plain-text and HTML version of your message
html = """\
<html>
  <body>
    <p>Hello there,<br>
       This is an automated python script for sending out emails to a csv list of email IDs and names. 
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("contacts.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for Name, Email in reader:
            print(f"Sending email to {Name}")
            # Send email here
            server.sendmail(
                sender_email,
                Email,
                message.as_string(),
            )
