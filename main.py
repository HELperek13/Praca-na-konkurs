"""
Turtle Snake - uruchom ten plik aby zagrać.
Wymaga Python 3.1+ oraz modułu turtle (standardowa biblioteka).
"""

import sys
import os

# Upewnij się że mamy dostęp do katalogu gry
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import TurtleSnakeGame

if __name__ == "__main__":
    game = TurtleSnakeGame()
    game.run()
