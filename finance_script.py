FINANCE_JS = """
<script>
    let authToken = localStorage.getItem("finance_token") || "", userName = localStorage.getItem("finance_name") || "", userCurrency = localStorage.getItem("finance_currency") || "$", editingId = null;
    const IDLE_LIMIT_MS = 10 * 60 * 1000;
    let idleTimer = null;
    const now = new Date();
    monthSelect.value = String(now.getMonth() + 1).padStart(2, "0");
    for (let y = now.getFullYear() - 3; y <= now.getFullYear() + 3; y++) {
        yearSelect.appendChild(Object.assign(document.createElement("option"), { value: String(y), textContent: String(y), selected: y === now.getFullYear() }));
    }
    const selectedMonthYear = () => `${yearSelect.value}-${monthSelect.value}`;
    const headers = () => ({ "Content-Type": "application/json", "Authorization": "Bearer " + authToken });
    function getLocalContinentTime() {
        const d = new Date();
        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";
        const formatted = d.toLocaleString("en-GB", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
        return `${formatted} (${tz})`;
    }
    function resetIdleTimer() {
        if (!authToken) return;
        localStorage.setItem("finance_last_active", String(Date.now()));
        clearTimeout(idleTimer);
        idleTimer = setTimeout(() => logout("🔒 Auto-locked after 10 minutes of inactivity."), IDLE_LIMIT_MS);
    }
    ["click", "touchstart", "keydown", "scroll"].forEach(evt => window.addEventListener(evt, resetIdleTimer, { passive: true }));
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden && authToken) {
            const last = Number(localStorage.getItem("finance_last_active") || Date.now());
            if (Date.now() - last > IDLE_LIMIT_MS) logout("🔒 Auto-locked after 10 minutes of inactivity.");
            else resetIdleTimer();
        }
    });
    async function submitAuth(url) {
        authError.textContent = "";
        const pwd = passInput.value;
        const isStrong = pwd.length >= 8 && /[A-Z]/.test(pwd) && /[a-z]/.test(pwd) && /\d/.test(pwd) && /[^A-Za-z0-9]/.test(pwd);
        if (!emailInput.value.trim() || !pwd || (url === "/auth/register" && !isStrong)) {
            authError.textContent = "Use a valid email and a strong password (8+ chars, uppercase, lowercase, number, and symbol).";
            return;
        }
        const res = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ name:nameInput.value.trim()||"User", email:emailInput.value.trim(), password:pwd, currency:authCurrency.value }) });
        const data = await res.json();
        if (!res.ok) {
            authError.textContent = Array.isArray(data.detail) ? data.detail.map(e => e.msg).join(", ") : (data.detail || "Auth failed");
            return;
        }
        startSession(data);
    }
    async function handleGoogle(r) {
        const res = await fetch("/auth/google", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ credential:r.credential, currency:authCurrency.value }) });
        const data = await res.json();
        if (!res.ok) return authError.textContent = data.detail || "Google sign-in failed";
        startSession(data);
    }
    function startSession(d) {
        authToken = d.token; userName = d.name; userCurrency = d.currency || userCurrency;
        localStorage.setItem("finance_token", authToken); localStorage.setItem("finance_name", userName); localStorage.setItem("finance_currency", userCurrency);
        vaultCurrency.value = userCurrency;
        nameInput.value = ""; emailInput.value = ""; passInput.value = "";
        authCard.style.display = "none"; appArea.style.display = "block"; userGreeting.textContent = "🔒 Private Vault: " + userName;
        resetIdleTimer(); loadSummary();
    }
    async function changeCurrency() {
        userCurrency = vaultCurrency.value; localStorage.setItem("finance_currency", userCurrency);
        await fetch("/auth/currency", { method:"PUT", headers:headers(), body:JSON.stringify({ currency:userCurrency }) });
        loadSummary();
    }
    async function logout(reason = "") {
        clearTimeout(idleTimer);
        if (authToken) await fetch("/auth/logout", { method: "POST", headers: headers() }).catch(() => {});
        authToken = ""; localStorage.clear();
        nameInput.value = ""; emailInput.value = ""; passInput.value = "";
        appArea.style.display = "none"; authCard.style.display = "block";
        authError.textContent = typeof reason === "string" ? reason : "";
    }
    async function loadSummary() { const res = await fetch(`/summary?month=${selectedMonthYear()}`, {headers:headers()}); if (res.status===401) return logout("Session expired. Please log in again."); renderDashboard(await res.json()); }
    function startEdit(tx) { editingId = tx.id; formTitle.textContent = "✏️ Edit Entry"; txTitle.value = tx.title; txAmount.value = tx.amount; txKind.value = tx.kind; txCategory.value = tx.category; saveBtn.textContent = "Update Entry"; cancelEditBtn.style.display = "block"; }
    function resetForm() { editingId = null; formTitle.textContent = "➕ Add Private Entry"; txTitle.value = txAmount.value = txCategory.value = ""; saveBtn.textContent = "Save Entry"; cancelEditBtn.style.display = "none"; }
    async function saveTx() {
        const res = await fetch(editingId ? `/transactions/${editingId}` : "/transactions", { method: editingId?"PUT":"POST", headers:headers(), body:JSON.stringify({ title:txTitle.value, amount:parseFloat(txAmount.value), kind:txKind.value, category:txCategory.value||"General", month_year:selectedMonthYear(), client_timestamp:getLocalContinentTime() }) });
        const data = await res.json();
        if (!res.ok) return txError.textContent = "Enter valid text and a positive amount.";
        resetForm(); renderDashboard(data);
    }
    async function deleteTx(id) { const res = await fetch(`/transactions/${id}?month=${selectedMonthYear()}`, {method:"DELETE", headers:headers()}); if (res.ok) renderDashboard(await res.json()); }
    async function downloadPDF() {
        const month = selectedMonthYear();
        const res = await fetch(`/transactions/pdf?month=${month}`, { headers: headers() });
        if (!res.ok) return;
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = Object.assign(document.createElement("a"), { href: url, download: `statement_${month}.pdf` });
        document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    }
    function renderDashboard(data) {
        const s = data.summary, c = data.currency || userCurrency;
        balanceText.textContent = `Balance: ${c}${s.balance.toFixed(2)}`; totalsText.textContent = `Income: ${c}${s.income.toFixed(2)} | Expenses: ${c}${s.expenses.toFixed(2)}`; adviceText.textContent = data.advice;
        catList.replaceChildren(...Object.entries(s.by_category).map(([cat, a]) => Object.assign(document.createElement("li"), {textContent:`${cat}: ${c}${a.toFixed(2)}`})));
        txList.replaceChildren(...s.transactions.map(tx => {
            const row = Object.assign(document.createElement("div"), {className:"tx-row"});
            const left = document.createElement("div");
            const info = Object.assign(document.createElement("div"), {textContent:`${tx.title} (${tx.category}): ${tx.kind==="income"?"+":"-"}${c}${tx.amount.toFixed(2)}`});
            const meta = Object.assign(document.createElement("small"), {textContent:`🌍 ${tx.created_at} • Budget: ${tx.month_year}`, style:"color:#a6adc8; display:block; margin-top:4px;"});
            left.append(info, meta);
            const btns = document.createElement("div");
            btns.append(Object.assign(document.createElement("button"), {className:"btn-edit", textContent:"Edit", onclick:()=>startEdit(tx)}), Object.assign(document.createElement("button"), {className:"btn-danger", textContent:"Delete", onclick:()=>deleteTx(tx.id)}));
            row.append(left, btns); return row;
        }));
    }
    if (authToken) {
        const last = Number(localStorage.getItem("finance_last_active") || Date.now());
        if (Date.now() - last > IDLE_LIMIT_MS) logout("🔒 Auto-locked after 10 minutes of inactivity.");
        else startSession({token:authToken, name:userName, currency:userCurrency});
    }
</script>
"""
