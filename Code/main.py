import tkinter as tk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
BLOCK_HEIGHT = 25
BLOCK_WIDTH = 75
BLOCK_SPEED = 25
BG_COLOR = "#000000"
BLOCK_COLOR = "#FFFFFF"

window = tk.Tk()
window.title("Beta")
window.resizable(False, False)

block_x = 0
block_y = WINDOW_HEIGHT - BLOCK_HEIGHT
block_direction = 1
last_block = None



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
    block_x += block_direction * BLOCK_SPEED
    if block_x <= 0 or block_x + BLOCK_WIDTH >= WINDOW_WIDTH:
        block_direction *= -1
    canvas.coords(block, block_x, block_y, block_x + BLOCK_WIDTH, block_y + BLOCK_HEIGHT)
    window.after(100, move_block)

def place(event):
    global block_x, block_y, last_block, BLOCK_WIDTH, BLOCK_SPEED
    
    if last_block is None: # If it's the first block, we just place it and move on
        pass
    else:
        last_block_coords = canvas.coords(last_block)
        if block_x + BLOCK_WIDTH < last_block_coords[0] or block_x > last_block_coords[2]: # If the block is completely outside, it's game over
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text="Game Over", fill="red", font=("Arial", 30))
            BLOCK_SPEED = 0
            return
        elif block_x < last_block_coords[0]: # If the block is only outside on the left, we cut it down
            BLOCK_WIDTH -= last_block_coords[0] - block_x
            block_x = last_block_coords[0]
        elif block_x + BLOCK_WIDTH > last_block_coords[2]: # If the block is onlyoutside on the right, we cut it down
            BLOCK_WIDTH -= (block_x + BLOCK_WIDTH)- last_block_coords[2]
            
    last_block = create_block()
    block_x = 0
    block_y -= BLOCK_HEIGHT

window.bind("<space>", place)


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

