# Wordle Network Game

A client-server implementation of the popular word-guessing game Wordle using Python sockets.

## Overview

This project implements a networked version of Wordle where multiple clients can connect to a central server and play the game simultaneously. The server maintains separate game instances for each connected client and handles word validation and feedback.

## Architecture

```
Client 1                   Server                   Client 2
┌─────┐                   ┌─────┐                   ┌─────┐
│     │ ───── guess ────► │     │ ◄──── guess ───── │     │
│     │                   │     │                   │     │
│     │ ◄── feedback ───  │     │ ──── feedback ──► │     │
└─────┘                   └─────┘                   └─────┘
```

## Data Exchange Format

```
Client -> Server:
{
    "guess": "word_input_from_user"  // 5-letter word
}

Server -> Client:
{
    "valid": true/false,
    "feedback": "colored_word",  // Using ANSI color codes
    "attempts": number,
    "timestamp": datetime
    "game_over": true/false,    // Optional
    "won": true/false,
    "message": "string"         // Optional
}
```

## Project Structure

```
├── config.py          # Configuration settings
├── wordle_server.py   # Server implementation with main logic (Task 2)
├── wordle_client.py   # Client implementation to create client (Task 2)
├── task1.py           # Basic implementation of wordle game logic
├── answers.txt        # List of possible answers (configurable) - picked up from official website
├── guesses.txt        # List of possible/grammatical correct guesses - picked up from official website
└── README.md          # Documentation 
```

## Configuration

The `config.py` file contains all game settings:
- `MAX_ATTEMPTS`: Maximum number of guesses allowed (default: 6)
- `HOST`: Server host address (default: 'localhost')
- `PORT`: Server port number (default: 8000)

## Features

- Multi-client support using threading
- Real-time colored feedback
- Configurable game parameters
- Simple error handling
- Clean disconnection handling

## Game Flow

```
┌─────────┐          ┌──────────┐          ┌─────────┐
│  Client │          │  Server  │          │   Game  │
└────┬────┘          └────┬─────┘          └────┬────┘
     │    Connect         │                      │
     │───────────────────►│                      │
     │                    │     Create Game      │
     │                    │─────────────────────►│
     │                    │                      │
     │    Send Guess      │                      │
     │───────────────────►│    Process Guess     │
     │                    │─────────────────────►│
     │                    │                      │
     │                    │   Return Feedback    │
     │                    │◄─────────────────────│
     │  Return Feedback   │                      │
     │◄───────────────────│                      │
     │                    │                      │
```

## Installation

1. Clone the repository
2. Ensure you have Python 3.6+ installed
3. Place a word list in `answers.txt` (one word per line)

## Usage

1. Start the server:
```bash
python3 wordle_server.py
```

2. Start client(s):
```bash
python3 wordle_client.py
```

## Game Rules

1. The server selects a random 5-letter word
2. Players have 6 attempts to guess the word
3. After each guess, feedback is provided:
   - Green: Letter is correct and in right position
   - Yellow: Letter is in word but wrong position
   - Gray: Letter is not in word

## Technical Details

- Uses TCP sockets for reliable communication
- JSON for data serialization
- ANSI color codes for terminal output
- Threading for handling multiple clients

## Error Handling

- Invalid word length
- Connection errors
- Client disconnection
- Server shutdown

## Future Improvements

1. Add user authentication
2. Implement scoring system
3. Add game statistics
4. Create web-based front-end with interactive UI/UX
6. Implement difficulty levels


## Screenshots

