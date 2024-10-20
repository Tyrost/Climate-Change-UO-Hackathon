import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sql_conn import innit_conn
from datetime import datetime

def send_email(email, body, subject):
    """
    Gmail's SMTP server 
    port for TLS encryption is 587
    """
    server_name = 'smtp.gmail.com'
    port = 587
    sender = 'tyrost9@gmail.com'
    password = 'ksdcflhwpxelzpcc'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

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

def sql_execute(query = 'SELECT * FROM newsletter'):

    current_date = str(datetime.today().date())

    users = innit_conn(query=query)

    subject = f'Monthly Wildfire Awareness - {current_date} - TEST'

    for user in users:
        name,email = user[1], user[2]

        body_message = (f'Hello {name}!\n\
                        This is a test message for our newly created Wildfire Awareness website!\n\
                        Feel free to ignore this message :)\n\
                        Thank for bring great!\n\n\
                        Best, Burn Watchers team.')
        
        send_email(email=email, body=body_message, subject=subject)
        print('Email(s) sent successfully!')
    return

# sql_execute()