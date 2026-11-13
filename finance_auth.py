import os
import re
import secrets
from datetime import date
from typing import Literal, Optional
import requests as http_requests
from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel, Field, field_validator
from db_adapter import get_db_connection
from finance_db import (
    init_finance_db,
    register_email_user,
    verify_email_user,
    register_or_login_google,
    update_user_currency,
    get_user_stats,
)
from rate_limiter import RateLimiter

auth_router = APIRouter()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
ADMIN_KEY = os.getenv("ADMIN_KEY", "esosa-admin-secret")
ACTIVE_SESSIONS = {}
auth_limiter = RateLimiter(max_requests=20)

class RegisterRequest(BaseModel):
    email: str = Field(min_length=4, max_length=120)
    name: str = Field(min_length=1, max_length=60)
    password: str = Field(min_length=8, max_length=128)
    currency: str = Field(default="$", min_length=1, max_length=6)

    @field_validator("password")
    @classmethod
    def validate_strong_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must include a lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must include a number")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must include a special character")
        return v

class LoginRequest(BaseModel):
    email: str = Field(min_length=4, max_length=120)
    password: str = Field(min_length=1, max_length=128)

class GoogleAuthRequest(BaseModel):
    credential: str
    currency: str = Field(default="$", min_length=1, max_length=6)

class CurrencyUpdateRequest(BaseModel):
    currency: str = Field(min_length=1, max_length=6)

class TransactionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    amount: float = Field(gt=0, le=1_000_000_000)
    kind: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=40)
    month_year: str = Field(default_factory=lambda: date.today().strftime("%Y-%m"), pattern=r"^\d{4}-\d{2}$")
    client_timestamp: Optional[str] = Field(default=None, max_length=70)

def get_current_user(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please log in first")
    _, token = authorization.split(" ", 1)
    session = ACTIVE_SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return session

def create_session(user_id: int, name: str, currency: str = "$"):
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {"user_id": user_id, "name": name, "currency": currency or "$"}
    return {"token": token, "name": name, "currency": currency or "$"}

def get_db():
    import finance_server
    return get_db_connection(finance_server.FINANCE_DB)

@auth_router.post("/auth/register")
def api_register(req: RegisterRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not auth_limiter.allow_request(ip):
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")
    conn = get_db()
    init_finance_db(conn)
    user_id = register_email_user(conn, req.email, req.name, req.password, req.currency)
    conn.close()
    if user_id is None:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_session(user_id, req.name.strip(), req.currency)

@auth_router.post("/auth/login")
def api_login(req: LoginRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not auth_limiter.allow_request(ip):
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")
    conn = get_db()
    init_finance_db(conn)
    user = verify_email_user(conn, req.email, req.password)
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user_id, name, currency = user
    return create_session(user_id, name, currency)

@auth_router.post("/auth/google")
def api_google_login(req: GoogleAuthRequest):
    resp = http_requests.get("https://googleapis.com", params={"id_token": req.credential}, timeout=5)
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google sign-in token")
    info = resp.json()
    if GOOGLE_CLIENT_ID and info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Google token client mismatch")

    default_name = info["email"].split("@")[0]
    conn = get_db()
    init_finance_db(conn)
    user_id, name, currency = register_or_login_google(conn, info["email"], info.get("name", default_name), info["sub"], req.currency)
    conn.close()
    return create_session(user_id, name, currency)

@auth_router.put("/auth/currency")
def api_update_currency(req: CurrencyUpdateRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = get_db()
    init_finance_db(conn)
    update_user_currency(conn, user["user_id"], req.currency)
    conn.close()
    user["currency"] = req.currency
    return {"currency": req.currency}

@auth_router.get("/admin/users")
def api_admin_users(key: str = ""):
    import finance_server
    if not secrets.compare_digest(key, finance_server.ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Forbidden")
    conn = get_db()
    init_finance_db(conn)
    stats = get_user_stats(conn)
    conn.close()
    return stats
