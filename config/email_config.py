import os

class EmailConfig:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.skip_sending = os.getenv("SKIP_EMAIL_SENDING", "false").lower() == "true"
        
        if not all([self.host, self.username, self.password]):
            raise ValueError("Missing required SMTP configuration")
