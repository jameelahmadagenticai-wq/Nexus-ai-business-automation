import httpx
import os

BASE_URL = os.getenv(
    "NEXUS_API_URL",
    "http://127.0.0.1:8000"
)


def _error_response(error):

    if isinstance(error, httpx.HTTPStatusError):

        try:

            details = error.response.json()

            return {
                "error": details.get(
                    "detail",
                    str(error)
                )
            }

        except Exception:

            return {
                "error": str(error)
            }

    return {
        "error": str(error)
    }

# =========================
# REGISTER
# =========================

def register_user(
    username: str,
    password: str
):

    payload = {
        "username": username,
        "password": password
    }

    try:

        response = httpx.post(
            f"{BASE_URL}/register",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# LOGIN
# =========================

def login_user(
    username: str,
    password: str
):

    payload = {
        "username": username,
        "password": password
    }

    try:

        response = httpx.post(
            f"{BASE_URL}/login",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# STREAM CHAT
# =========================

def stream_chat_message(
    message: str,
    history: list = None
):

    if not message:

        return

    payload = {
        "message": message,
        "history": history or []
    }

    timeout = httpx.Timeout(
        300,
        connect=10,
        read=300
    )

    try:

        with httpx.stream(
            "POST",
            f"{BASE_URL}/chat/stream",
            json=payload,
            timeout=timeout
        ) as response:

            response.raise_for_status()

            for chunk in response.iter_text():

                if chunk:

                    yield chunk

    except Exception as e:

        yield f"Error: {str(e)}"

# =========================
# HEALTH
# =========================

def get_health():

    try:

        response = httpx.get(
            f"{BASE_URL}/health",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# AGENTS
# =========================

def get_agents():

    try:

        response = httpx.get(
            f"{BASE_URL}/agents/",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# CRM
# =========================

def get_crm():

    try:

        response = httpx.get(
            f"{BASE_URL}/crm/",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# REPORTS
# =========================

def get_reports():

    try:

        response = httpx.get(
            f"{BASE_URL}/reports/",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# GET MEMORIES
# =========================

def get_memories():

    try:

        response = httpx.get(
            f"{BASE_URL}/memory/",
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# DELETE MEMORY
# =========================

def delete_memory(
    memory_id: str
):

    try:

        response = httpx.delete(
            f"{BASE_URL}/memory/{memory_id}",
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)

# =========================
# UPDATE MEMORY
# =========================

def update_memory(
    memory_id: str,
    content: str
):

    try:

        response = httpx.put(
            f"{BASE_URL}/memory/{memory_id}",
            json={
                "content": content
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return _error_response(e)
