from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from routers.email import router as email_router

# =========================
# AUTH ROUTER
# =========================

from auth import router as auth_router

# =========================
# FEATURE ROUTERS
# =========================

from routers.agents import router as agents_router
from routers.chat import router as chat_router
from routers.documents import router as documents_router
from routers.crm import router as crm_router
from routers.reports import router as reports_router
from routers.memory import router as memory_router
from routers.send_email import (
    router as send_email_router
)

from routers.email_dashboard import (
    router as email_dashboard_router
)

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="NexusOS AI",
    description="Autonomous Multi-Agent AI Platform",
    version="1.0.0"
)


# =========================
# CORS MIDDLEWARE
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST LOGGER
# =========================

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):

    print({
        "endpoint": request.url.path,
        "method": request.method,
        "timestamp": datetime.utcnow()
    })

    response = await call_next(request)

    return response


# =========================
# ROOT ENDPOINT
# =========================

@app.get("/")
async def root():

    return {
        "message": "NexusOS AI Running",
        "version": "1.0.0",
        "status": "active"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }


# =========================
# AUTH ROUTES
# =========================

app.include_router(
    auth_router,
    tags=["Authentication"]
)


# =========================
# AGENT ORCHESTRATION ROUTES
# =========================

app.include_router(
    agents_router,
    prefix="/agents",
    tags=["Agents"]
)


# =========================
# CHAT ROUTES
# =========================

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)


# =========================
# DOCUMENT ROUTES
# =========================

app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"]
)


# =========================
# CRM ROUTES
# =========================

app.include_router(
    crm_router,
    prefix="/crm",
    tags=["CRM"]
)


# =========================
# REPORT ROUTES
# =========================

app.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"]
)


# =========================
# MEMORY ROUTES
# =========================

app.include_router(
    memory_router,
    prefix="/memory",
    tags=["Memory"]
)


app.include_router(
    email_router,
    prefix="/agents",
    tags=["Email Automation"]
)

app.include_router(
    send_email_router,
    prefix="/email",
    tags=["Send Email"]
)

app.include_router(
    email_dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)