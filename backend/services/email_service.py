import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:

    def __init__(self):

        # =========================
        # SMTP CONFIG
        # =========================

        self.smtp_server = "smtp.gmail.com"

        self.smtp_port = 587

        self.email = "YOUR_EMAIL@gmail.com"

        self.password = "aocx owvk mjdw uiql"

    # =========================
    # SEND EMAIL
    # =========================

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ):

        # =========================
        # CREATE MESSAGE
        # =========================

        msg = MIMEMultipart()

        msg["From"] = self.email

        msg["To"] = recipient

        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "plain")
        )

        # =========================
        # SMTP CONNECTION
        # =========================

        server = smtplib.SMTP(
            self.smtp_server,
            self.smtp_port
        )

        server.starttls()

        server.login(
            self.email,
            self.password
        )

        # =========================
        # SEND EMAIL
        # =========================

        server.sendmail(
            self.email,
            recipient,
            msg.as_string()
        )

        server.quit()

        return {
            "status": "sent",
            "recipient": recipient
        }