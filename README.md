# Tetris Game

A Python implementation of the classic Tetris game using tkinter.

## Features

- Classic Tetris gameplay
- Configurable settings (preview count, fall speed, rotation direction)
- Ranking/Score system
- Menu system with How To Play guide
- Pause functionality

## Requirements

- Python 3.7 or higher
- tkinter (included with Python standard library)

## Installation

### Option 1: Direct Run

```bash
python main.py
```

### Option 2: Install as Package

```bash
pip install -e .
tetris
```

## Usage

Run the game:
```bash
python main.py
```

## File Structure

```
tetris/
├── main.py              # Entry point
├── game.py              # Main game logic
├── piece.py             # Tetromino piece definitions
├── constants.py         # Game constants and colors
├── ranking.py           # Score/ranking system
├── tetris_rankings.json # Saved rankings data
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## License

MIT License - see LICENSE file for details

## Author

Your Name
