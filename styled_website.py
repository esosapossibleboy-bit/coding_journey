def build_styled_page(name):
    return f"""<html>
<body>
    <style>
        body {{
            background-color: navy;
            color: white;
        }}
    </style>
    <h1>Hello, {name}!</h1>
    <button onclick="alert('You clicked the button!')">Click Me</button>
</body>
</html>"""
if __name__ == "__main__":
    with open("index.html", "w") as file:
        file.write(build_styled_page("Esosa"))
    print("🎨 Updated index.html! Run 'python -m http.server 8000' to click your button!")
