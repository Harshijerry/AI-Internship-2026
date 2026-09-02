# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [10, 20, 30, 40, 50]
mixed = [1, "hello", 3.14, True]

print("Fruits:", fruits)
print("Numbers:", numbers)
print("Mixed:", mixed)

# Indexing (starts from 0)
print("\nFirst fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# Slicing
print("\nFirst two numbers:", numbers[0:2])
print("Last three numbers:", numbers[-3:])

# Length
print("\nTotal fruits:", len(fruits))

# Modifying
fruits[1] = "mango"
print("After change:", fruits)