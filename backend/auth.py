from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

# =========================
# JWT CONFIG
# =========================

SECRET_KEY = "nexus_secret_key"
ALGORITHM = "HS256"

# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================
# TEMP DATABASE
# =========================

fake_users_db = {}

# =========================
# REQUEST MODELS
# =========================

class RegisterModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

# =========================
# REGISTER
# =========================

@router.post("/register")
async def register(user: RegisterModel):

    if user.username in fake_users_db:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = pwd_context.hash(
        user.password
    )

    fake_users_db[user.username] = {
        "username": user.username,
        "password": hashed_password
    }

    return {
        "message": "User registered successfully"
    }

# =========================
# LOGIN
# =========================

@router.post("/login")
async def login(user: LoginModel):

    db_user = fake_users_db.get(
        user.username
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not pwd_context.verify(
        user.password,
        db_user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token_data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }