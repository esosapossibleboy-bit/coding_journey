import os

def add_task(filename, task):
    with open(filename, "a") as file:
        file.write(task + "\n")

def get_tasks(filename):
    if not os.path.exists(filename):
        return []
    tasks = []
    with open(filename, "r") as file:
        for line in file:
            tasks.append(line.strip())
    return tasks

def run_todo_app():
    filename = "my_tasks.txt"
    while True:
        print("\n--- 📝 MY TO-DO LIST ---")
        print("1. Add a task")
        print("2. Show my tasks")
        print("3. Quit")
        choice = input("Pick 1, 2, or 3: ")

        if choice == "1":
            new_task = input("What do you need to do? ")
            add_task(filename, new_task)
            print("✅ Saved!")
        elif choice == "2":
            tasks = get_tasks(filename)
            print("\nYour Tasks:")
            for task in tasks:
                print("- " + task)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Please type 1, 2, or 3.")

if __name__ == "__main__":
    run_todo_app()
