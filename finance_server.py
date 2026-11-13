import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from finance_db import init_finance_db, add_transaction, get_financial_summary

app = FastAPI(title="Esosa's AI Personal Finance App")
FINANCE_DB = "finance.db"

class TransactionRequest(BaseModel):
    title: str
    amount: float
    kind: str
    category: str

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
def api_add_transaction(req: TransactionRequest):
    conn = sqlite3.connect(FINANCE_DB)
    init_finance_db(conn)
    add_transaction(conn, req.title, req.amount, req.kind, req.category)
    summary = get_financial_summary(conn)
    conn.close()
    return {"summary": summary, "advice": generate_budget_advice(summary)}

@app.get("/", response_class=HTMLResponse)
def finance_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8" /><title>Esosa's AI Finance & Budget App</title></head>
    <body style="background:#1e1e2e; color:white; font-family:sans-serif; max-width:650px; margin:40px auto; padding:20px;">
        <h1>💰 AI Personal Finance & Budget App</h1>
        <div style="background:#11111b; padding:18px; border-radius:10px; margin-bottom:20px;">
            <h2 id="balanceText" style="color:#a6e3a1;">Balance: $0.00</h2>
            <p id="totalsText">Income: $0.00 | Expenses: $0.00</p>
            <p id="adviceText" style="color:#f9e2af; font-weight:bold;">Loading AI Coach...</p>
        </div>

        <div style="background:#11111b; padding:18px; border-radius:10px; margin-bottom:20px;">
            <h3>➕ Add Transaction</h3>
            <input id="title" placeholder="Title (e.g. Salary, Groceries)" style="padding:8px; width:45%;" />
            <input id="amount" type="number" placeholder="Amount ($)" style="padding:8px; width:25%;" />
            <select id="kind" style="padding:8px;">
                <option value="income">Income (+)</option>
                <option value="expense">Expense (-)</option>
            </select><br/><br/>
            <input id="category" placeholder="Category (e.g. Salary, Food, Games)" style="padding:8px; width:55%;" />
            <button onclick="submitTx()" style="padding:8px 16px; background:#89b4fa; border:none; border-radius:6px; font-weight:bold;">Add Entry</button>
        </div>

        <div style="background:#11111b; padding:18px; border-radius:10px;">
            <h3>📊 Spending by Category</h3>
            <ul id="catList"></ul>
        </div>

        <script>
            function renderUI(data) {
                const s = data.summary;
                document.getElementById("balanceText").innerText = `Balance: $${s.balance.toFixed(2)}`;
                document.getElementById("totalsText").innerText = `Income: $${s.income.toFixed(2)} | Expenses: $${s.expenses.toFixed(2)}`;
                document.getElementById("adviceText").innerText = data.advice;
                const list = document.getElementById("catList");
                list.innerHTML = Object.entries(s.by_category).map(([cat, amt]) => `<li><b>${cat}:</b> $${amt.toFixed(2)}</li>`).join("");
            }

            async function loadData() {
                const res = await fetch("/summary");
                renderUI(await res.json());
            }

            async function submitTx() {
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
                renderUI(await res.json());
            }

            loadData();
        </script>
    </body>
    </html>
    """
