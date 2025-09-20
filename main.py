from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import logging
import uvicorn

from models.email_request import EmailRequest
from config.email_config import EmailConfig
from services.email_service import EmailService

load_dotenv()

app = FastAPI(title="Email API", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

email_config = EmailConfig()
email_service = EmailService(email_config)

@app.post("/send-email")
async def send_email_endpoint(email_data: EmailRequest):
    try:
        email_service.send_email(email_data)
        return {"message": "Email sent successfully", "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
