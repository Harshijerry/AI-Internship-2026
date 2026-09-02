import random

secret = random.randint(1, 100)
attempts = 0

print("=== Number Guessing Game ===")
print("Guess a number between 1 and 100")

while True:
    guess = int(input("Your guess: "))
    attempts += 1

    if guess < secret:
        print("Too low! Try higher.")
    elif guess > secret:
        print("Too high! Try lower.")
    else:
        print(f" Correct! You found it in {attempts} attempts!")
        break