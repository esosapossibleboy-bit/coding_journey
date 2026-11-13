from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse, Response
from db_adapter import get_db_connection
from finance_auth import (
    ADMIN_KEY,
    GOOGLE_CLIENT_ID,
    TransactionRequest,
    auth_limiter,
    auth_router,
    get_current_user,
)
from finance_db import (
    add_transaction,
    delete_transaction,
    get_financial_summary,
    init_finance_db,
    update_transaction,
)
from finance_pdf import build_statement_pdf
from finance_ui import render_finance_page
from rate_limiter import RateLimiter

app = FastAPI(title="Esosa's Secure Private Finance App")
FINANCE_DB = "finance.db"
tx_limiter = RateLimiter(max_requests=60)
app.include_router(auth_router)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://google.com; "
        "style-src 'self' 'unsafe-inline' https://google.com; "
        "frame-src https://google.com; "
        "connect-src 'self' https://google.com;"
    )
    return response

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

@app.get("/summary")
def api_summary(month: Optional[str] = None, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = get_db_connection(FINANCE_DB)
    init_finance_db(conn)
    summary = get_financial_summary(conn, user["user_id"], month)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary), "currency": user["currency"]}

@app.get("/transactions/pdf")
def api_download_pdf(month: Optional[str] = None, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = get_db_connection(FINANCE_DB)
    init_finance_db(conn)
    summary = get_financial_summary(conn, user["user_id"], month)
    conn.close()

    pdf_bytes = build_statement_pdf(user["name"], summary, user["currency"])
    filename = f"statement_{summary['month_year']}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

@app.post("/transactions")
def api_add_tx(req: TransactionRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if not tx_limiter.allow_request(str(user["user_id"])):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    conn = get_db_connection(FINANCE_DB)
    init_finance_db(conn)
    add_transaction(conn, user["user_id"], req.title.strip(), req.amount, req.kind, req.category.strip(), req.month_year, req.client_timestamp)
    summary = get_financial_summary(conn, user["user_id"], req.month_year)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary), "currency": user["currency"]}

@app.put("/transactions/{tx_id}")
def api_edit_tx(tx_id: int, req: TransactionRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = get_db_connection(FINANCE_DB)
    init_finance_db(conn)
    updated = update_transaction(conn, user["user_id"], tx_id, req.title.strip(), req.amount, req.kind, req.category.strip(), req.month_year)
    if not updated:
        conn.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    summary = get_financial_summary(conn, user["user_id"], req.month_year)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary), "currency": user["currency"]}

@app.delete("/transactions/{tx_id}")
def api_delete_tx(tx_id: int, month: Optional[str] = None, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    conn = get_db_connection(FINANCE_DB)
    init_finance_db(conn)
    deleted = delete_transaction(conn, user["user_id"], tx_id)
    if not deleted:
        conn.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    summary = get_financial_summary(conn, user["user_id"], month)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary), "currency": user["currency"]}
