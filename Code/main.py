import tkinter as tk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 150
BLOCK_SPEED = 25
BG_COLOR = "#000000"
BLOCK_COLOR = "#FFFFFF"

window = tk.Tk()
window.title("Beta")
window.resizable(False, False)

block_x = 0
block_y = WINDOW_HEIGHT - BLOCK_HEIGHT - 1
block_direction = 1



def create_block():
    block = canvas.create_rectangle(
        block_x, 
        block_y, 
        block_x + BLOCK_WIDTH, 
        block_y + BLOCK_HEIGHT, 
        fill=BLOCK_COLOR, 
        outline=BLOCK_COLOR
    )
    return block

def move_block():
    global block_x, block_direction
    if block_x <= 0:
        block_direction = 1
    if block_x + BLOCK_WIDTH >= WINDOW_WIDTH:
        block_direction = -1
    canvas.move(block, BLOCK_SPEED * block_direction, 0)
    window.after(100, move_block)




canvas = tk.Canvas(
    window, 
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    bg=BG_COLOR
)
canvas.pack()

block = create_block()
move_block()

window.mainloop()

