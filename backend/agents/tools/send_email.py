async def send_email(
    recipient: str,
    subject: str,
    body: str
):

    return f"""
    Email sent successfully

    To: {recipient}
    Subject: {subject}
    """