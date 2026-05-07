from fastapi import APIRouter

from services.email_store import EMAIL_STORE


router = APIRouter()


# =========================
# GET ALL EMAILS
# =========================

@router.get("/emails")
async def get_emails():

    return EMAIL_STORE