from finance_styles import FINANCE_CSS
from finance_script import FINANCE_JS

def render_finance_page(google_client_id: str) -> str:
    google_client_id = google_client_id.strip()
    g_script = '<script src="https://google.com" async defer></script>' if google_client_id else ""
    g_btn = (
        '<div id="googleBtnContainer" style="display:flex;justify-content:center;margin-top:14px;min-height:44px;"></div>'
        f'<script>window.addEventListener("load", () => {{ if (window.google) {{ google.accounts.id.initialize({{ client_id: "{google_client_id}", callback: handleGoogle }}); google.accounts.id.renderButton(document.getElementById("googleBtnContainer"), {{ theme: "outline", size: "large", text: "continue_with", width: 320 }}); }} }});</script>'
        if google_client_id
        else '<p style="font-size:0.85rem;color:#a6adc8;">Google Sign-In ready via GOOGLE_CLIENT_ID.</p>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Esosa's Private AI Finance App</title>{g_script}{FINANCE_CSS}
</head>
<body>
    <div class="container">
        <h1>🛡️ Secure Private AI Budget App</h1>
        <div id="authCard" class="card" style="max-width:440px;margin:20px auto;">
            <h2>🔐 Private Account Access</h2>
            <input id="nameInput" placeholder="Your Name (for Sign Up)" />
            <input id="emailInput" type="email" placeholder="Email Address" />
            <input id="passInput" type="password" placeholder="Strong Password (8+ chars, A-z, 0-9, !@#)" />
            <button onclick="submitAuth('/auth/login')">Log In</button>
            <button class="btn-secondary" onclick="submitAuth('/auth/register')">Create Private Account</button>
            {g_btn}<p id="authError" class="error"></p>
        </div>

        <div id="appArea" style="display:none;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span id="userGreeting" style="color:#a6e3a1;font-weight:bold;"></span>
                <button class="btn-secondary" style="width:auto;margin:0;padding:8px 14px;" onclick="logout()">Log Out</button>
            </div>
            <div class="card" style="margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                <span style="font-weight:bold;color:#89b4fa;">📅 Select Budget Month & Year:</span>
                <div style="display:flex;gap:8px;">
                    <select id="monthSelect" style="width:auto;margin:0;" onchange="loadSummary()">
                        <option value="01">January</option><option value="02">February</option><option value="03">March</option>
                        <option value="04">April</option><option value="05">May</option><option value="06">June</option>
                        <option value="07">July</option><option value="08">August</option><option value="09">September</option>
                        <option value="10">October</option><option value="11">November</option><option value="12">December</option>
                    </select>
                    <select id="yearSelect" style="width:auto;margin:0;" onchange="loadSummary()"></select>
                </div>
            </div>
            <div class="grid">
                <div class="card">
                    <h2 id="balanceText" class="balance">Balance: $0.00</h2>
                    <p id="totalsText">Income: $0.00 | Expenses: $0.00</p>
                    <p id="adviceText" class="advice"></p>
                    <h3>📊 Spending by Category</h3><ul id="catList"></ul>
                </div>
                <div class="card">
                    <h3 id="formTitle">➕ Add Private Entry</h3>
                    <input id="txTitle" maxlength="80" placeholder="Title (e.g. Salary, Groceries)" />
                    <input id="txAmount" type="number" step="0.01" min="0.01" placeholder="Amount ($)" />
                    <select id="txKind"><option value="income">Income (+)</option><option value="expense">Expense (-)</option></select>
                    <input id="txCategory" maxlength="40" placeholder="Category (e.g. Salary, Food)" />
                    <button id="saveBtn" onclick="saveTx()">Save Entry</button>
                    <button id="cancelEditBtn" class="btn-secondary" style="display:none;" onclick="resetForm()">Cancel Edit</button>
                    <p id="txError" class="error"></p>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                    <h3 style="margin:0;">🧾 Your Private Transactions</h3>
                    <button class="btn-secondary" style="width:auto;margin:0;padding:8px 14px;" onclick="downloadPDF()">📄 Download PDF</button>
                </div>
                <div id="txList" style="margin-top:10px;"></div>
            </div>
        </div>
    </div>
    {FINANCE_JS}
</body>
</html>"""
