import os
from todo import add_task, get_tasks

def test_todo_storage():
    test_file = "temp_test_tasks.txt"
    
    # Clean up any leftover test file before starting
    if os.path.exists(test_file):
        os.remove(test_file)

    # Test 1: Add two tasks to the file
    add_task(test_file, "Learn Python files")
    add_task(test_file, "Build a to-do app")

    # Test 2: Read them back and verify they saved properly
    saved_tasks = get_tasks(test_file)
    assert saved_tasks == ["Learn Python files", "Build a to-do app"]

    # Test 3: Add a third task and verify it appends to the bottom
    add_task(test_file, "Celebrate!")
    assert get_tasks(test_file) == ["Learn Python files", "Build a to-do app", "Celebrate!"]

    # Clean up the temporary test file after passing
    os.remove(test_file)
    print("📝 ALL TO-DO STORAGE TESTS PASSED! Ready to make it interactive!")

test_todo_storage()
