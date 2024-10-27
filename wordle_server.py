import socket
import random
from enum import Enum
import json
from datetime import datetime
import threading
from config import MAX_ATTEMPTS, HOST, PORT

class LetterState(Enum):
    HIT = "\033[32m"      # Green color - HIT
    PRESENT = "\033[33m"  # Yellow color - PRESENT
    MISS = "\033[0m"      # Default color/Reset - MISS

def load_dictionary(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f]

# Separate class to deal with main logic of wordle - compare the guess word to the selectec secret word
class WordleGame:
    def __init__(self, guesses, answers):
        self.guesses = [word.lower() for word in guesses]
        self.answer = random.choice(answers).lower()
        self.attempts = 0
        self.max_attempts = MAX_ATTEMPTS
        self.game_over = False
        self.start_time = datetime.now()

    def is_valid_guess(self, guess):
        return len(guess) == 5 and guess.lower() in self.guesses

    def evaluate_guess(self, guess):
        result = []
        guess = guess.lower()
        
        for i in range(5):
            if guess[i] == self.answer[i]:
                result.append({"letter": guess[i], "state": LetterState.HIT.value})
            elif guess[i] in self.answer:
                result.append({"letter": guess[i], "state": LetterState.PRESENT.value})
            else:
                result.append({"letter": guess[i], "state": LetterState.MISS.value})
        
        return result

    def process_guess(self, guess): #prepare payload for sending back to client
        if not self.is_valid_guess(guess):
            return {
                "valid": False,
                "message": "Invalid guess. Please enter a valid 5-letter word.",
                "timestamp": datetime.now().isoformat()
            }

        self.attempts += 1
        feedback = self.evaluate_guess(guess)
        
        response = {
            "valid": True,
            "feedback": feedback,
            "attempts": self.attempts,
            "timestamp": datetime.now().isoformat()
        }

        if guess == self.answer:
            response["game_over"] = True
            response["won"] = True
            response["message"] = f"Congratulations! You won in {self.attempts} attempts!"
            self.game_over = True
        elif self.attempts >= self.max_attempts:
            response["game_over"] = True
            response["won"] = False
            response["message"] = f"Game over. The word was: {self.answer}"
            self.game_over = True
        
        return response


# class to deal with sockets, client request handling
class WordleServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.guesses = load_dictionary("guesses.txt")
        self.answers = load_dictionary("answers.txt")
        self.active_games = {}

    def handle_client(self, client_socket, addr):
        print(f"[{datetime.now().isoformat()}] New connection from {addr}")
        
        game = WordleGame(self.guesses, self.answers)
        self.active_games[addr] = game
        
        try:
            while not game.game_over:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                guess = json.loads(data)["guess"]
                response = game.process_guess(guess)
                client_socket.send(json.dumps(response).encode())

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Error handling client {addr}: {e}")
        finally:
            if addr in self.active_games:
                del self.active_games[addr]
            client_socket.close()
            print(f"[{datetime.now().isoformat()}] Connection closed for {addr}")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[{datetime.now().isoformat()}] Server started on {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
        except KeyboardInterrupt:
            print(f"[{datetime.now().isoformat()}] Server shutting down...")
        finally:
            server.close()

if __name__ == "__main__":
    server = WordleServer()
    server.start()