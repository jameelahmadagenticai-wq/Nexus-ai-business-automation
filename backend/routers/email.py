from fastapi import APIRouter

from pydantic import BaseModel

from agents.core.email_agent import EmailAgent

from services.email_store import EMAIL_STORE


router = APIRouter()


# =========================
# REQUEST SCHEMA
# =========================

class EmailRequest(BaseModel):

    sender: str

    subject: str

    body: str


# =========================
# EMAIL PROCESSING ENDPOINT
# =========================

@router.post("/email")
async def process_email(
    request: EmailRequest
):

    # =========================
    # INITIALIZE AGENT
    # =========================

    agent = EmailAgent()

    # =========================
    # BUILD TASK
    # =========================

    task = f"""
    Sender: {request.sender}

    Subject: {request.subject}

    Body:
    {request.body}
    """

    # =========================
    # RUN EMAIL AGENT
    # =========================

    result = await agent.run(task)

    # =========================
    # STORE EMAIL DATA
    # =========================

    email_data = {

        "sender": request.sender,

        "subject": request.subject,

        "body": request.body,

        "draft_reply": result["result"],

        "approved": False
    }

    EMAIL_STORE.append(email_data)

    # =========================
    # RETURN RESPONSE
    # =========================

    return {

        "status": "processed",

        "email_data": email_data
    }