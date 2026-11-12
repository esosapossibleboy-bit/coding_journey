from styled_website import build_styled_page

def test_styled_page():
    page = build_styled_page("Esosa")
    
    # Check HTML structure
    assert "<html>" in page
    assert "<body>" in page
    assert "<h1>Hello, Esosa!</h1>" in page
    
    # Check CSS styling
    assert "<style>" in page
    assert "background-color: navy;" in page
    assert "color: white;" in page
    
    # Check JavaScript interactive button
    assert "<button onclick=" in page
    assert "Click Me</button>" in page
    
    print("🎨 ALL STYLED & INTERACTIVE WEBSITE TESTS PASSED! Week 2 Complete!")

test_styled_page()
