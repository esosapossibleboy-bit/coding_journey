import requests

def format_joke(joke_data):
    return joke_data["setup"] + " -> " + joke_data["punchline"]

def get_live_joke():
    url = "https://jokeapi.dev"
    headers = {"User-Agent": "CodingJourneyApp/1.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        formatted = {"setup": data["setup"], "punchline": data["delivery"]}
        return format_joke(formatted)
    except Exception:
        return "Backup Joke: Why do Java developers wear glasses? -> Because they don't C#!"

if __name__ == "__main__":
    print(get_live_joke())
