try:
    from .game import TetrisGame
except ImportError:
    from game import TetrisGame


if __name__ == "__main__":
    TetrisGame().run()
