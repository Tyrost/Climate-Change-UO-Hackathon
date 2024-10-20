import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAILS = get_emails.subscribers

TEMPLATE = "Thank you for subscribing to the Newsletter, here is"

def send_email(email, body, subject):
    """
    Gmail's SMTP server 
    port for TLS encryption is 587
    """
    server_name = 'smtp.gmail.com'
    port = 587
    sender = 'tyrost9@gmail.com'
    password = 'ksdcflhwpxelzpcc'

    try:
        server = smtplib.SMTP(server_name, port)
        server.starttls()
        server.login(sender, password)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body))

        server.sendmail(sender, email, msg.as_string())
        print(f"Email successfully sent to {email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()

def send_all():
    for i in EMAILS:
        send_email(EMAILS[i][0], TEMPLATE, 'Regular subscriber newsletter')
