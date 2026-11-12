def build_homepage(name, hobby):
    return f"<html><body><h1>Welcome, {name}!</h1><p>I love building {hobby}.</p></body></html>"
def build_homepage(name, hobby):
    return "<html><body><h1>Welcome, " + name + "!</h1><p>I love building " + hobby + ".</p></body></html>"

if __name__ == "__main__":
    html_code = build_homepage("Esosa", "websites, mobile apps, AI, and games")
    with open("index.html", "w") as file:
        file.write(html_code)
    print("🚀 index.html created! Starting local web server...")
