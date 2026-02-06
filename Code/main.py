import tkinter as tk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
BLOCK_HEIGHT = 50
START_BLOCK_WIDTH = 150
SPEED = 5
BG_COLOR = "#000000"
BLOCK_COLOR = "#FFFFFF"

window = tk.Tk()
window.title("Beta")
window.resizable(False, False)

canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR)
canvas.pack()

canvas.create_rectangle(
    WINDOW_WIDTH//2 - START_BLOCK_WIDTH//2, 
    WINDOW_HEIGHT - BLOCK_HEIGHT,
    WINDOW_WIDTH//2 + START_BLOCK_WIDTH//2,
    WINDOW_HEIGHT+1, 
    fill=BLOCK_COLOR,
    outline=BLOCK_COLOR
)

def move_block():
    
    

window.mainloop()

