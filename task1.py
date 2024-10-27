import random
from enum import Enum

class LetterState(Enum):
    HIT = "\033[32m"      # HIT - Green color for correct letter, correct position
    PRESENT = "\033[33m"  # PRESENT - Yellow color for correct letter, wrong position
    MISS = "\033[0m"      # MISS - Default color for letter not in word

def load_dictionary(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f]

class Wordle:
    def __init__(self, guesses, answers):
        self.guesses = [word.lower() for word in guesses]
        self.answer = random.choice(answers).lower()
        self.attempts = 0
        self.max_attempts = 6
        self.game_over = False

    def is_valid_guess(self, guess):
        return len(guess) == 5 and guess.lower() in self.guesses

    def evaluate_guess(self, guess):
        result = ""
        guess = guess.lower()
        
        for i in range(5):
            if guess[i] == self.answer[i]:
                result += LetterState.HIT.value + guess[i]
            elif guess[i] in self.answer:
                result += LetterState.PRESENT.value + guess[i]
            else:
                result += LetterState.MISS.value + guess[i]
        
        return result + LetterState.MISS.value

    def play(self):
        print("Welcome to Wordle! Guess a 5-letter word in 6 attempts")
        
        while self.attempts < self.max_attempts and not self.game_over:
            guess = input(f"Enter Guess #{self.attempts + 1}: ").lower()
            
            if not self.is_valid_guess(guess):
                print("Invalid guess. Please enter a valid 5-letter word.")
                continue
            
            if guess == self.answer:
                print(f"Congratulations! You Won!!, You guessed the word: {self.answer} in {self.attempts} attempts")
                self.game_over = True
                break
            
            self.attempts += 1
            feedback = self.evaluate_guess(guess)
            print(feedback)
        
        if not self.game_over:
            print(f"Game over, You lost!!. The word was: {self.answer}")

def main():
    guesses = load_dictionary("guesses.txt")
    answers = load_dictionary("answers.txt")
    game = Wordle(guesses, answers)
    game.play()

if __name__ == "__main__":
    main()