def detect_mood(message):
    clean_text = message.lower()

    if "love" in clean_text or "awesome" in clean_text or "great" in clean_text:
        return "Positive"
    elif "hate" in clean_text or "broken" in clean_text or "bad" in clean_text:
        return "Negative"
    else:
        return "Neutral"