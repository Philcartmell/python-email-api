import os

class EmailConfig:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.skip_sending = os.getenv("SKIP_EMAIL_SENDING", "false").lower() == "true"
        
        # Check for missing or empty configuration fields
        missing_fields = []
        if not self.host or self.host.strip() == "":
            missing_fields.append("SMTP_HOST")
        if not self.username or self.username.strip() == "":
            missing_fields.append("SMTP_USERNAME")
        if not self.password or self.password.strip() == "":
            missing_fields.append("SMTP_PASSWORD")
        
        if missing_fields:
            raise ValueError(f"Missing required SMTP configuration: {', '.join(missing_fields)}")
    
    def validate_configuration(self):
        """
        Validate SMTP configuration and return health status
        Returns dict with status, message, and configuration details
        """
        try:
            # If email sending is skipped, just return healthy
            if self.skip_sending:
                return {
                    "status": "healthy",
                    "message": "Email sending is disabled (development mode)",
                    "smtp_configured": False
                }
            
            # Validate SMTP configuration when email sending is enabled
            missing_config = []
            
            if not self.host or self.host.strip() == "":
                missing_config.append("SMTP_HOST")
            
            if not self.username or self.username.strip() == "":
                missing_config.append("SMTP_USERNAME")
            
            if not self.password or self.password.strip() == "":
                missing_config.append("SMTP_PASSWORD")
            
            # Check if port is valid (should be a positive integer)
            if not isinstance(self.port, int) or self.port <= 0:
                missing_config.append("SMTP_PORT")
            
            if missing_config:
                return {
                    "status": "unhealthy",
                    "message": f"Missing or invalid SMTP configuration: {', '.join(missing_config)}",
                    "smtp_configured": False,
                    "missing_config": missing_config
                }
            
            return {
                "status": "healthy",
                "message": "SMTP configuration is valid",
                "smtp_configured": True,
                "smtp_host": self.host,
                "smtp_port": self.port
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}",
                "smtp_configured": False
            }