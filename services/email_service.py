import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.email_request import EmailRequest
from config.email_config import EmailConfig

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, config: EmailConfig):
        self.config = config
    
    def send_email(self, email_data: EmailRequest):
        if self.config.skip_sending:
            logger.info("Email sending skipped (development mode)")
            return True
        
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = email_data.from_email
            msg["To"] = ", ".join(email_data.to)
            msg["Subject"] = email_data.subject
            
            msg.attach(MIMEText(email_data.plain_body, "plain"))
            
            if email_data.html_body:
                msg.attach(MIMEText(email_data.html_body, "html"))
            
            with smtplib.SMTP(self.config.host, self.config.port) as server:
                server.starttls()
                server.login(self.config.username, self.config.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {email_data.to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
