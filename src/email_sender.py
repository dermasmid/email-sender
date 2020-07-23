import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



class Mailbox:


    def __init__(self, host: str, port: int):
        ssl_context = ssl.create_default_context()
        self.mailbox = smtplib.SMTP_SSL(host, port, context= ssl_context)


    def login(
        self, 
        email_address: str, 
        password: str,
        from_name: str = None,
        ):
        self.sender_email = email_address
        self.mailbox.login(email_address, password)
        self.from_name = f"{from_name} <{email_address}>" if from_name else email_address

    
    def send_email(
        self, 
        to_email: str, 
        subject: str = "", 
        text: str = None, 
        html: str = None, 
        attachments: list = [],
        ):

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.from_name
        message["To"] = to_email

        # Attach attachments
        for attachment_path in attachments:
            print("h")
            file_name = attachment_path if not "/" in attachment_path else attachment_path.split("/")[-1]
            with open(attachment_path, "rb") as f:
                attachment_data = f.read()
            attachment_mimetype = guess_type(attachment_path)
            attachment = MIMEBase(attachment_mimetype[0], "octet-stream")
            attachment.set_payload(attachment_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename= file_name)
            message.attach(attachment)
        

        if text:
            message.attach(MIMEText(text, "plain"))
        
        if html:
            message.attach(MIMEText(html, "html"))

        # Send email
        self.mailbox.sendmail(self.sender_email, to_email, message.as_string())



