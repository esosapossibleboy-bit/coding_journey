import sqlite3
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from finance_db import init_finance_db, add_transaction, get_financial_summary
from rate_limiter import RateLimiter

app = FastAPI(title="Esosa's Secure AI Personal Finance App")
FINANCE_DB = "finance.db"
tx_limiter = RateLimiter(max_requests=30)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

class TransactionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    amount: float = Field(gt=0, le=1_000_000_000)
    kind: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=40)

def generate_budget_advice(summary):
    income = summary["income"]
    expenses = summary["expenses"]
    balance = summary["balance"]
    by_cat = summary["by_category"]

    if income <= 0:
        return "Add your first income source to start tracking your budget!"

    top_category = max(by_cat, key=by_cat.get) if by_cat else "None"

    if expenses > income:
        return f"⚠️ Warning: Overspending! Trim your {top_category} costs."
    elif balance >= income * 0.2:
        return f"🌟 Great job saving! Top spending category: {top_category}."
    else:
        return f"💡 Tip: Reduce {top_category} spending to reach a 20% savings goal."

@app.get("/summary")
def api_summary():
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    summary = get_financial_summary(conn)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.post("/transactions")
def api_add_transaction(req: TransactionRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not tx_limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    add_transaction(conn, req.title.strip(), req.amount, req.kind, req.category.strip())
    summary = get_financial_summary(conn)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.get("/", response_class=HTMLResponse)
def finance_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Esosa's Secure AI Finance App</title>
        <style>
            * { box-sizing: border-box; }
            body {
                background: #1e1e2e;
                color: #cdd6f4;
                font-family: system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 16px;
            }
            .container { max-width: 960px; margin: 0 auto; }
            h1 { font-size: clamp(1.4rem, 4vw, 2rem); text-align: center; color: #89b4fa; }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
                gap: 16px;
            }
            .card {
                background: #11111b;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #313244;
            }
            input, select, button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                border-radius: 8px;
                border: 1px solid #45475a;
                background: #181825;
                color: white;
                font-size: 16px;
            }
            button {
                background: #89b4fa;
                color: #11111b;
                font-weight: bold;
                border: none;
                cursor: pointer;
            }
            button:hover { opacity: 0.9; }
            .balance { color: #a6e3a1; font-size: 1.8rem; margin: 0 0 8px 0; }
            .advice { color: #f9e2af; font-weight: bold; margin-top: 12px; }
            .error { color: #f38ba8; font-size: 0.9rem; margin-top: 8px; }
            ul { padding-left: 20px; }
            li { margin-bottom: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Secure AI Personal Finance & Budget App</h1>
            <div class="grid">
                <div class="card">
                    <h2 id="balanceText" class="balance">Balance: $0.00</h2>
                    <p id="totalsText">Income: $0.00 | Expenses: $0.00</p>
                    <p id="adviceText" class="advice">Loading AI Coach...</p>
                    <h3>📊 Spending by Category</h3>
                    <ul id="catList"></ul>
                </div>

                <div class="card">
                    <h3>➕ Add Transaction</h3>
                    <input id="title" maxlength="80" placeholder="Title (e.g. Salary, Groceries)" />
                    <input id="amount" type="number" step="0.01" min="0.01" placeholder="Amount ($)" />
                    <select id="kind">
                        <option value="income">Income (+)</option>
                        <option value="expense">Expense (-)</option>
                    </select>
                    <input id="category" maxlength="40" placeholder="Category (e.g. Salary, Food, Games)" />
                    <button onclick="submitTx()">Add Entry</button>
                    <p id="errorText" class="error"></p>
                </div>
            </div>
        </div>

        <script>
            function renderUI(data) {
                const s = data.summary;
                document.getElementById("balanceText").textContent = `Balance: $${s.balance.toFixed(2)}`;
                document.getElementById("totalsText").textContent = `Income: $${s.income.toFixed(2)} | Expenses: $${s.expenses.toFixed(2)}`;
                document.getElementById("adviceText").textContent = data.advice;

                // Safe DOM rendering (prevents XSS script injection!)
                const list = document.getElementById("catList");
                list.replaceChildren();
                Object.entries(s.by_category).forEach(([cat, amt]) => {
                    const li = document.createElement("li");
                    li.textContent = `${cat}: $${amt.toFixed(2)}`;
                    list.appendChild(li);
                });
            }

            async function loadData() {
                const res = await fetch("/summary");
                renderUI(await res.json());
            }

            async function submitTx() {
                const errorBox = document.getElementById("errorText");
                errorBox.textContent = "";
                const payload = {
                    title: document.getElementById("title").value,
                    amount: parseFloat(document.getElementById("amount").value),
                    kind: document.getElementById("kind").value,
                    category: document.getElementById("category").value || "General"
                };
                const res = await fetch("/transactions", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) {
                    errorBox.textContent = "Invalid input: please enter a positive amount and valid text.";
                    return;
                }
                document.getElementById("title").value = "";
                document.getElementById("amount").value = "";
                renderUI(data);
            }

            loadData();
        </script>
    </body>
    </html>
    """
