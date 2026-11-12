from my_website import build_homepage

def test_homepage_html():
    page = build_homepage("Esosa", "games and AI")
    
    # Check that proper HTML tags exist
    assert "<html>" in page
    assert "<body>" in page
    assert "<h1>Welcome, Esosa!</h1>" in page
    assert "<p>I love building games and AI.</p>" in page
    assert "</body></html>" in page
    
    print("🌐 ALL WEBSITE HTML TESTS PASSED! Ready to launch in your browser!")

test_homepage_html()
