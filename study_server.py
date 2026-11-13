import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from study_db import (
    init_study_db,
    register_user,
    verify_user,
    add_study_note,
    get_user_notes,
)
from study_ai import StudyTutor
from rate_limiter import RateLimiter

app = FastAPI(title="Esosa's AI Study Buddy")
STUDY_DB = "study_buddy.db"
tutor = StudyTutor()
ai_limiter = RateLimiter(max_requests=10)

class AuthRequest(BaseModel):
    username: str
    password: str

class NoteRequest(BaseModel):
    user_id: int
    title: str
    content: str

class AskTutorRequest(BaseModel):
    user_id: int
    question: str

@app.get("/", response_class=HTMLResponse)
def study_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8" /><title>Esosa's AI Study Buddy</title></head>
    <body style="background:#1e1e2e; color:white; font-family:sans-serif; max-width:700px; margin:40px auto; padding:20px;">
        <h1>📚 Esosa's AI Study Buddy</h1>

        <div id="authScreen" style="background:#11111b; padding:20px; border-radius:10px;">
            <h2>🔐 Login or Create Account</h2>
            <input id="username" placeholder="Username" style="padding:8px; margin-right:8px;" />
            <input id="password" type="password" placeholder="Password" style="padding:8px; margin-right:8px;" />
            <button onclick="auth('/login')" style="padding:8px 14px;">Login</button>
            <button onclick="auth('/register')" style="padding:8px 14px;">Register</button>
            <p id="authMsg" style="color:#f38ba8;"></p>
        </div>

        <div id="appScreen" style="display:none;">
            <h2 id="welcomeBanner" style="color:#a6e3a1;"></h2>

            <div style="background:#11111b; padding:20px; border-radius:10px; margin-bottom:20px;">
                <h3>📝 Add a Study Note</h3>
                <input id="noteTitle" placeholder="Topic (e.g., Python Lists)" style="width:95%; padding:8px; margin-bottom:8px;" /><br/>
                <textarea id="noteContent" placeholder="Write your note here..." style="width:95%; height:70px; padding:8px;"></textarea><br/>
                <button onclick="saveNote()" style="padding:8px 16px; margin-top:8px;">Save Note & Build Flashcards</button>
            </div>

            <div style="background:#11111b; padding:20px; border-radius:10px; margin-bottom:20px;">
                <h3>🤖 Ask Your AI Tutor</h3>
                <input id="questionInput" placeholder="Ask a question about your notes..." style="width:70%; padding:8px;" />
                <button onclick="askTutor()" style="padding:8px 16px;">Ask AI</button>
                <p id="aiReply" style="color:#89b4fa; font-weight:bold;"></p>
            </div>

            <div style="background:#11111b; padding:20px; border-radius:10px;">
                <h3>🗂️ Auto-Generated Flashcards</h3>
                <ul id="flashcardList"></ul>
            </div>
        </div>

        <script>
            let currentUserId = null;

            async function auth(endpoint) {
                const username = document.getElementById("username").value;
                const password = document.getElementById("password").value;
                const res = await fetch(endpoint, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });
                const data = await res.json();
                if (!res.ok) {
                    document.getElementById("authMsg").innerText = data.detail;
                    return;
                }
                currentUserId = data.user_id;
                document.getElementById("authScreen").style.display = "none";
                document.getElementById("appScreen").style.display = "block";
                document.getElementById("welcomeBanner").innerText = "Welcome back, " + data.username + "!";
            }

            async function saveNote() {
                const title = document.getElementById("noteTitle").value;
                const content = document.getElementById("noteContent").value;
                const res = await fetch("/notes", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_id: currentUserId, title, content })
                });
                const data = await res.json();
                const list = document.getElementById("flashcardList");
                list.innerHTML = data.flashcards.map(c => `<li><b>Q:</b> ${c.question} <br/> <b>A:</b> ${c.answer}</li><br/>`).join("");
            }

            async function askTutor() {
                const question = document.getElementById("questionInput").value;
                const res = await fetch("/tutor/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_id: currentUserId, question })
                });
                const data = await res.json();
                document.getElementById("aiReply").innerText = res.ok ? data.answer : data.detail;
            }
        </script>
    </body>
    </html>
    """

@app.post("/register")
def api_register(req: AuthRequest):
    conn = sqlite3.connect(STUDY_DB)
    init_study_db(conn)
    user_id = register_user(conn, req.username, req.password)
    conn.close()
    if user_id is None:
        raise HTTPException(status_code=400, detail="Username already taken")
    return {"user_id": user_id, "username": req.username}

@app.post("/login")
def api_login(req: AuthRequest):
    conn = sqlite3.connect(STUDY_DB)
    init_study_db(conn)
    user_id = verify_user(conn, req.username, req.password)
    conn.close()
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": user_id, "username": req.username}

@app.post("/notes")
def api_add_note(req: NoteRequest):
    conn = sqlite3.connect(STUDY_DB)
    init_study_db(conn)
    add_study_note(conn, req.user_id, req.title, req.content)
    notes = get_user_notes(conn, req.user_id)
    conn.close()
    flashcards = tutor.make_flashcards(notes)
    return {"notes": notes, "flashcards": flashcards}

@app.post("/tutor/ask")
def api_ask_tutor(req: AskTutorRequest):
    if not ai_limiter.allow_request(str(req.user_id)):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    conn = sqlite3.connect(STUDY_DB)
    init_study_db(conn)
    notes = get_user_notes(conn, req.user_id)
    conn.close()
    answer = tutor.ask_tutor(notes, req.question)
    return {"answer": answer}
