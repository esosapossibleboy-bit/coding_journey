from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ai_mood import detect_mood

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family: sans-serif; background: #1e1e2e; color: white; padding: 40px;">
        <h1>🤖 Full-Stack AI Mood Analyzer</h1>
        <input id="userInput" placeholder="Type a sentence..." style="padding: 10px; width: 300px;" />
        <button onclick="checkMood()" style="padding: 10px;">Analyze Mood</button>
        <h2 id="result">Mood: Waiting...</h2>

        <script>
            async function checkMood() {
                const text = document.getElementById("userInput").value;
                const response = await fetch("/analyze?text=" + encodeURIComponent(text));
                const data = await response.json();
                document.getElementById("result").innerText = "Mood: " + data.mood;
            }
        </script>
    </body>
    </html>
    """

@app.get("/analyze")
def analyze_text(text: str):
    result = detect_mood(text)
    return {"text": text, "mood": result}
