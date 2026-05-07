from fastapi import APIRouter

from pydantic import BaseModel

from services.email_service import EmailService


router = APIRouter()


# =========================
# REQUEST SCHEMA
# =========================

class SendEmailRequest(BaseModel):

    recipient: str

    subject: str

    body: str


# =========================
# SEND EMAIL ENDPOINT
# =========================

@router.post("/send")
async def send_email(
    request: SendEmailRequest
):

    email_service = EmailService()

    result = email_service.send_email(
        recipient=request.recipient,
        subject=request.subject,
        body=request.body
    )

    return result