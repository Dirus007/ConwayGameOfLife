# main.py
import tkinter as tk
from game_of_life import GameOfLife
from gui import GameOfLifeGUI


def main():
    root = tk.Tk()
    root.title("Conway's Game of Life")

    WIDTH, HEIGHT, CELL_SIZE = 400, 400, 10
    game = GameOfLife(WIDTH, HEIGHT, CELL_SIZE)
    gui = GameOfLifeGUI(root, game)

    root.mainloop()

if __name__ == "__main__":
    main()
