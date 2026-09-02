# Simple function
def greet():
    print("Hello from function!")

greet()

# Function with parameter
def greet_user(name):
    print(f"Hello, {name}!")

greet_user("Harshini")

# Function with return
def add(a, b):
    return a + b

result = add(5, 3)
print("5 + 3 =", result)

# Function with default value
def power(base, exponent=2):
    return base ** exponent

print("Square of 4:", power(4))
print("Cube of 2:", power(2, 3))