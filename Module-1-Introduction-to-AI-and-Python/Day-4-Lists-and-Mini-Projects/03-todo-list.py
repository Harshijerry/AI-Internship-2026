todo = []

while True:
    print("\n=== TO-DO LIST ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Exit")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        task = input("Enter task: ")
        todo.append(task)
        print("Task added!")

    elif choice == "2":
        if len(todo) == 0:
            print("No tasks yet!")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(todo, 1):
                print(f"{i}. {task}")

    elif choice == "3":
        if len(todo) == 0:
            print("No tasks to remove!")
        else:
            task = input("Enter task to remove: ")
            if task in todo:
                todo.remove(task)
                print("Task removed!")
            else:
                print("Task not found!")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")