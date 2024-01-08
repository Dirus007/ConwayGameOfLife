import tkinter as tk
from tkinter import Button, Canvas, Scale
from PIL import Image, ImageTk
import cv2
import numpy as np
from game_of_life import GameOfLife

class GameOfLifeGUI:
    def __init__(self, root, game_of_life):
        self.root = root
        self.game_of_life = game_of_life
        self.paused = True
        self.zoom_level = 1

        self.canvas = Canvas(root, width=game_of_life.width, height=game_of_life.height)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.click)

        self.pause_button = Button(root, text="Start", command=self.toggle_pause)
        self.pause_button.pack(side="left")

        self.quit_button = Button(root, text="Quit", command=root.destroy)
        self.quit_button.pack(side="right")

        self.zoom_slider = Scale(root, from_=1, to=10, orient="horizontal", label="Zoom", command=self.zoom)
        self.zoom_slider.set(1)
        self.zoom_slider.pack(side="bottom")

        self.update_canvas()

    def update_canvas(self):
        if not self.paused:
            self.game_of_life.update_grid()

        img = self.draw_grid()
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor="nw", image=imgtk)
        self.root.after(8000, self.update_canvas)

    def draw_grid(self):
        # Create a blank image array
        img = np.zeros((self.game_of_life.height, self.game_of_life.width, 3), dtype=np.uint8)

        # Draw each cell
        for y in range(self.game_of_life.grid_height):
            for x in range(self.game_of_life.grid_width):
                if self.game_of_life.grid[y][x]:
                    x_start = x * self.game_of_life.cell_size
                    y_start = y * self.game_of_life.cell_size
                    x_end = x_start + self.game_of_life.cell_size
                    y_end = y_start + self.game_of_life.cell_size
                    img[y_start:y_end, x_start:x_end] = [255, 255, 255]  # White for alive cells

        # Draw grid lines
        for x in range(0, self.game_of_life.width, self.game_of_life.cell_size):
            img[:, x:x+1] = [200, 200, 200]  # Light grey for vertical grid lines
        for y in range(0, self.game_of_life.height, self.game_of_life.cell_size):
            img[y:y+1, :] = [200, 200, 200]  # Light grey for horizontal grid lines

        if self.zoom_level > 1:
            img = cv2.resize(img, (self.game_of_life.width * self.zoom_level, self.game_of_life.height * self.zoom_level), interpolation=cv2.INTER_NEAREST)

        return img

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Pause" if not self.paused else "Start")
        if not self.paused:
            self.update_game()

    def click(self, event):
        if self.paused:
            x, y = event.x // (self.game_of_life.cell_size * self.zoom_level), event.y // (self.game_of_life.cell_size * self.zoom_level)
            if 0 <= x < self.game_of_life.grid_width and 0 <= y < self.game_of_life.grid_height:
                self.game_of_life.toggle_cell(x, y)
                self.update_canvas()

    def zoom(self, val):
        self.zoom_level = int(val)
        self.update_canvas()

    def update_game(self):
        self.game_of_life.update_grid()
        self.update_canvas()
        if not self.paused:
            self.root.after(100, self.update_game)
