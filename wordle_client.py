import socket
import json
from datetime import datetime
from config import MAX_ATTEMPTS, HOST, PORT

# class to setup the client and establish the connection to server
class WordleClient:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_attempt = 0

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"[{datetime.now().isoformat()}] Connected to server")
            return True
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Connection failed: {e}")
            return False

    def display_response_from_server(self, feedback):
        result = ""
        for item in feedback:
            result += item["state"] + item["letter"]
        result += "\033[0m"  # Reset color
        print(f"Round {self.current_attempt}/{MAX_ATTEMPTS}: {result}")

    def play(self):
        if not self.connect():
            return

        print("Welcome to Wordle! Guess a 5-letter word in 6 attempts")
        
        try:
            while True:
                guess = input("Enter your guess: ").lower()
                
                # Send guess to server
                self.socket.send(json.dumps({"guess": guess}).encode())
                
                # Receive response
                response = json.loads(self.socket.recv(1024).decode())
                
                if not response["valid"]:
                    print(response["message"])
                    continue
                
                self.current_attempt = response["attempts"]
                self.display_response_from_server(response["feedback"])
                
                if "game_over" in response:
                    print(response["message"])
                    break

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Error during game: {e}")
        finally:
            self.socket.close()
            print(f"[{datetime.now().isoformat()}] Connection closed")

if __name__ == "__main__":
    client = WordleClient()
    client.play()