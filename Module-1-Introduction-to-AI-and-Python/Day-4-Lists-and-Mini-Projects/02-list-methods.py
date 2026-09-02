tasks = []

# Adding items
tasks.append("Study Python")
tasks.append("Push to GitHub")
tasks.append("Write notes")
print("After append:", tasks)

# Insert at position
tasks.insert(1, "Eat lunch")
print("After insert:", tasks)

# Remove item
tasks.remove("Eat lunch")
print("After remove:", tasks)

# Pop (remove last)
last = tasks.pop()
print("Popped:", last)
print("After pop:", tasks)

# Sort
numbers = [5, 2, 8, 1, 9]
numbers.sort()
print("Sorted:", numbers)

numbers.reverse()
print("Reversed:", numbers)