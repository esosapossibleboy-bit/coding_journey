import os
import sqlite3
import secrets
from typing import Literal, Optional
import requests as http_requests
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from finance_db import (
    init_finance_db,
    register_email_user,
    verify_email_user,
    register_or_login_google,
    get_user_stats,
    add_transaction,
    update_transaction,
    delete_transaction,
    get_financial_summary,
)
from finance_ui import render_finance_page
from rate_limiter import RateLimiter

app = FastAPI(title="Esosa's Secure Private Finance App")
FINANCE_DB = "finance.db"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
ADMIN_KEY = os.getenv("ADMIN_KEY", "esosa-admin-secret")

ACTIVE_SESSIONS = {}
auth_limiter = RateLimiter(max_requests=20)
tx_limiter = RateLimiter(max_requests=60)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

class RegisterRequest(BaseModel):
    email: str = Field(min_length=4, max_length=120)
    name: str = Field(min_length=1, max_length=60)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str = Field(min_length=4, max_length=120)
    password: str = Field(min_length=1, max_length=128)

class GoogleAuthRequest(BaseModel):
    credential: str

class TransactionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    amount: float = Field(gt=0, le=1_000_000_000)
    kind: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=40)

def get_current_user(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please log in first")
    token = authorization.split(" ", 1)[1]
    session = ACTIVE_SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return session

def create_session(user_id: int, name: str):
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {"user_id": user_id, "name": name}
    return {"token": token, "name": name}

def generate_budget_advice(summary):
    income, expenses, balance, by_cat = (
        summary["income"],
        summary["expenses"],
        summary["balance"],
        summary["by_category"],
    )
    if income <= 0:
        return "Add your first income source to start tracking your private budget!"
    top_category = max(by_cat, key=by_cat.get) if by_cat else "None"
    if expenses > income:
        return f"⚠️ Warning: Overspending! Trim your {top_category} costs."
    elif balance >= income * 0.2:
        return f"🌟 Great job saving! Top spending category: {top_category}."
    return f"💡 Tip: Reduce {top_category} spending to reach a 20% savings goal."

@app.get("/", response_class=HTMLResponse)
def finance_dashboard():
    return render_finance_page(GOOGLE_CLIENT_ID)

@app.post("/auth/register")
def api_register(req: RegisterRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not auth_limiter.allow_request(ip):
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    user_id = register_email_user(conn, req.email, req.name, req.password)
    conn.close()
    if user_id is None:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_session(user_id, req.name.strip())

@app.post("/auth/login")
def api_login(req: LoginRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not auth_limiter.allow_request(ip):
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    user = verify_email_user(conn, req.email, req.password)
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return create_session(user[0], user[1])

@app.post("/auth/google")
def api_google_login(req: GoogleAuthRequest):
    resp = http_requests.get(
        "https://googleapis.com",
        params={"id_token": req.credential},
        timeout=5,
    )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google sign-in token")
    info = resp.json()
    if GOOGLE_CLIENT_ID and info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Google token client mismatch")

    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    user_id, name = register_or_login_google(
        conn, info["email"], info.get("name", info["email"].split("@")[0]), info["sub"]
    )
    conn.close()
    return create_session(user_id, name)

@app.get("/admin/users")
def api_admin_users(key: str = ""):
    if not secrets.compare_digest(key, ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Forbidden")
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    stats = get_user_stats(conn)
    conn.close()
    return stats

@app.get("/summary")
def api_summary(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    summary = get_financial_summary(conn, user["user_id"])
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.post("/transactions")
def api_add_tx(req: TransactionRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if not tx_limiter.allow_request(str(user["user_id"])):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    add_transaction(conn, user["user_id"], req.title.strip(), req.amount, req.kind, req.category.strip())
    summary = get_financial_summary(conn, user["user_id"])
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.put("/transactions/{tx_id}")
def api_edit_tx(tx_id: int, req: TransactionRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    updated = update_transaction(conn, user["user_id"], tx_id, req.title.strip(), req.amount, req.kind, req.category.strip())
    if not updated:
        conn.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    summary = get_financial_summary(conn, user["user_id"])
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.delete("/transactions/{tx_id}")
def api_delete_tx(tx_id: int, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    deleted = delete_transaction(conn, user["user_id"], tx_id)
    if not deleted:
        conn.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    summary = get_financial_summary(conn, user["user_id"])
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}
