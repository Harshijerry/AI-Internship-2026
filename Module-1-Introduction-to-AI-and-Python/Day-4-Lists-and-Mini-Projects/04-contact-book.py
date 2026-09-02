contacts = []

while True:
    print("\n=== CONTACT BOOK ===")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Exit")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        contacts.append([name, phone])
        print("Contact added!")

    elif choice == "2":
        if len(contacts) == 0:
            print("No contacts yet!")
        else:
            print("\nYour Contacts:")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact[0]} - {contact[1]}")

    elif choice == "3":
        search = input("Enter name to search: ")
        found = False
        for contact in contacts:
            if contact[0].lower() == search.lower():
                print(f"Found: {contact[0]} - {contact[1]}")
                found = True
                break
        if not found:
            print("Contact not found!")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")