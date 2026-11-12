from greeter import say_hello

def test_robot_greeter():
    assert say_hello("Alice") == "Hello, Alice! Welcome to coding!"
    assert say_hello("Bob") == "Hello, Bob! Welcome to coding!"
    print("🎉 ALL TESTS PASSED! You are officially a coder!")

test_robot_greeter()
