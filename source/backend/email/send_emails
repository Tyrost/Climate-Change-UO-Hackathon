import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# TODO Change this to get data from SQL list
EMAILS = ['rayf@uoregon.edu', 'fisher.ray843@gmail.com']

def send_emails(email, body, subject):
    """
    Gmail's SMTP server 
    port for TLS encryption is 587
    """
    server_name = 'smtp.gmail.com'
    port = 587
    sender = 'tyrost9@gmail.com'
    password = 'ksdcflhwpxelzpcc'

    # msg = MIMEMultipart()
    # msg['From'] = sender
    # msg['To'] = email
    # msg['Subject'] = subject

    # msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP(server_name, port)
        server.starttls()
        server.login(sender, password)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(body))

    except Exception as e:
        print(f"failed to send email: {e}")

    finally:
        server.quit()


