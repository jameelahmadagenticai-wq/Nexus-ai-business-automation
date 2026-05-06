from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from datetime import datetime

from auth import router as auth_router

from routers.agents import router as agents_router
from routers.chat import router as chat_router
from routers.documents import router as documents_router
from routers.crm import router as crm_router
from routers.reports import router as reports_router
from routers.memory import (
    router as memory_router
)


app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================

app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(crm_router)
app.include_router(reports_router)
app.include_router(memory_router)

# =========================
# REQUEST LOGGER
# =========================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    print({
        "endpoint": request.url.path,
        "method": request.method,
        "timestamp": datetime.utcnow()
    })

    response = await call_next(request)

    return response

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }