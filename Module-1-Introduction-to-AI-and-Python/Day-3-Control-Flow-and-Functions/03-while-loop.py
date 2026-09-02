# Countdown
count = 5
print("Countdown:")
while count > 0:
    print(count)
    count -= 1
print("Blast off! 🚀")

# User validation
password = ""
while password != "python":
    password = input("\nEnter password: ")
    if password != "python":
        print("Wrong! Try again.")
print("Access granted! ✅")