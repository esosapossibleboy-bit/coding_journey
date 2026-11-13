from finance_styles import FINANCE_CSS

def render_finance_page(google_client_id: str) -> str:
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
            <input id="passInput" type="password" placeholder="Password (min 6 chars)" />
            <button onclick="submitAuth('/auth/login')">Log In</button>
            <button class="btn-secondary" onclick="submitAuth('/auth/register')">Create Private Account</button>
            {g_btn}<p id="authError" class="error"></p>
        </div>

        <div id="appArea" style="display:none;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span id="userGreeting" style="color:#a6e3a1;font-weight:bold;"></span>
                <button class="btn-secondary" style="width:auto;margin:0;padding:8px 14px;" onclick="logout()">Log Out</button>
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
            <div class="card" style="margin-top:16px;"><h3>🧾 Your Private Transactions</h3><div id="txList"></div></div>
        </div>
    </div>
    <script>
        let authToken = localStorage.getItem("finance_token") || "", userName = localStorage.getItem("finance_name") || "", editingId = null;
        const headers = () => ({{ "Content-Type": "application/json", "Authorization": "Bearer " + authToken }});
        async function submitAuth(url) {{
            authError.textContent = "";
            if (!emailInput.value.trim() || passInput.value.length < 6) {{
                authError.textContent = "Enter a valid email and a password with at least 6 characters.";
                return;
            }}
            const res = await fetch(url, {{ method:"POST", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{ name:nameInput.value.trim()||"User", email:emailInput.value.trim(), password:passInput.value }}) }});
            const data = await res.json();
            if (!res.ok) {{
                authError.textContent = Array.isArray(data.detail) ? data.detail.map(e => e.msg).join(", ") : (data.detail || "Auth failed");
                return;
            }}
            startSession(data);
        }}
        async function handleGoogle(r) {{
            const res = await fetch("/auth/google", {{ method:"POST", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{credential:r.credential}}) }});
            const data = await res.json();
            if (!res.ok) return authError.textContent = data.detail || "Google sign-in failed";
            startSession(data);
        }}
        function startSession(d) {{
            authToken = d.token; userName = d.name; localStorage.setItem("finance_token", authToken); localStorage.setItem("finance_name", userName);
            authCard.style.display = "none"; appArea.style.display = "block"; userGreeting.textContent = "🔒 Private Vault: " + userName; loadSummary();
        }}
        function logout() {{ authToken = ""; localStorage.clear(); appArea.style.display = "none"; authCard.style.display = "block"; }}
        async function loadSummary() {{ const res = await fetch("/summary", {{headers:headers()}}); if (res.status===401) return logout(); renderDashboard(await res.json()); }}
        function startEdit(tx) {{ editingId = tx.id; formTitle.textContent = "✏️ Edit Entry"; txTitle.value = tx.title; txAmount.value = tx.amount; txKind.value = tx.kind; txCategory.value = tx.category; saveBtn.textContent = "Update Entry"; cancelEditBtn.style.display = "block"; }}
        function resetForm() {{ editingId = null; formTitle.textContent = "➕ Add Private Entry"; txTitle.value = txAmount.value = txCategory.value = ""; saveBtn.textContent = "Save Entry"; cancelEditBtn.style.display = "none"; }}
        async function saveTx() {{
            const res = await fetch(editingId ? `/transactions/${{editingId}}` : "/transactions", {{ method: editingId?"PUT":"POST", headers:headers(), body:JSON.stringify({{ title:txTitle.value, amount:parseFloat(txAmount.value), kind:txKind.value, category:txCategory.value||"General" }}) }});
            const data = await res.json();
            if (!res.ok) return txError.textContent = "Enter valid text and a positive amount.";
            resetForm(); renderDashboard(data);
        }}
        async function deleteTx(id) {{ const res = await fetch(`/transactions/${{id}}`, {{method:"DELETE", headers:headers()}}); if (res.ok) renderDashboard(await res.json()); }}
        function renderDashboard(data) {{
            const s = data.summary;
            balanceText.textContent = `Balance: $${{s.balance.toFixed(2)}}`; totalsText.textContent = `Income: $${{s.income.toFixed(2)}} | Expenses: $${{s.expenses.toFixed(2)}}`; adviceText.textContent = data.advice;
            catList.replaceChildren(...Object.entries(s.by_category).map(([c, a]) => Object.assign(document.createElement("li"), {{textContent:`${{c}}: $${{a.toFixed(2)}}`}})));
            txList.replaceChildren(...s.transactions.map(tx => {{
                const row = Object.assign(document.createElement("div"), {{className:"tx-row"}});
                const info = Object.assign(document.createElement("span"), {{textContent:`${{tx.title}} (${{tx.category}}): ${{tx.kind==="income"?"+":"-"}}$${{tx.amount.toFixed(2)}}`}});
                const btns = document.createElement("div");
                btns.append(Object.assign(document.createElement("button"), {{className:"btn-edit", textContent:"Edit", onclick:()=>startEdit(tx)}}), Object.assign(document.createElement("button"), {{className:"btn-danger", textContent:"Delete", onclick:()=>deleteTx(tx.id)}}));
                row.append(info, btns); return row;
            }}));
        }}
        if (authToken) startSession({{token:authToken, name:userName}});
    </script>
</body>
</html>"""
