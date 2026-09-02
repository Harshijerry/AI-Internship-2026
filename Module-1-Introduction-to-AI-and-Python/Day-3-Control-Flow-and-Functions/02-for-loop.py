# Print 1 to 10
print("Numbers 1 to 10:")
for i in range(1, 11):
    print(i, end=" ")
print()

# Print even numbers
print("\nEven numbers 2 to 20:")
for i in range(2, 21, 2):
    print(i, end=" ")
print()

# Print multiplication table
num = int(input("\nEnter a number for table: "))
print(f"Table of {num}:")
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")