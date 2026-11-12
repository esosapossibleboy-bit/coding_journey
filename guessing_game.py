import random

def check_guess(secret_number, player_guess):
    # Keep your working code here!
    if player_guess < secret_number:
        return "Too low!"
    elif player_guess > secret_number:
        return "Too high!"
    else:
        return "You win!"

def play_game():
    secret = random.randint(1, 20)
    print("🎲 I am thinking of a secret number between 1 and 20!")
    
    result = ""
    while result != "You win!":
        guess = int(input("Take a guess: "))
        result = check_guess(secret, guess)
        print(result)

if __name__ == "__main__":
    play_game()
