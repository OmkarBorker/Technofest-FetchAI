import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSender:
    def __init__(self, smtp_server, smtp_port, smtp_password, sender_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_password = smtp_password
        self.sender_email = sender_email

    def send_email(self, subject, body, receiver_email):
        # Create the MIME object
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.smtp_password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())