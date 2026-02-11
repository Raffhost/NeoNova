import tkinter as tk

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BLOCK_HEIGHT = 50
INITIAL_BLOCK_WIDTH = 150
BLOCK_SPEED = 50
BG_COLOR = "#000000"
BLOCK_COLOR = "#FFFFFF"

window = tk.Tk()
window.title("Beta")
window.resizable(False, False)

# Global variables
block_x = WINDOW_WIDTH // 2 - INITIAL_BLOCK_WIDTH // 2
block_y = WINDOW_HEIGHT - BLOCK_HEIGHT
block_width = INITIAL_BLOCK_WIDTH
block_direction = 1
last_block = None
current_block = None  # Current block ID
game_over_flag = False
speed = BLOCK_SPEED

canvas = tk.Canvas(
    window, 
    width=WINDOW_WIDTH, 
    height=WINDOW_HEIGHT, 
    bg=BG_COLOR
)
canvas.pack()



def create_block():
    block = canvas.create_rectangle(
        block_x, 
        block_y, 
        block_x + block_width, 
        block_y + BLOCK_HEIGHT, 
        fill=BLOCK_COLOR, 
        outline=BLOCK_COLOR
    )
    return block

def move_block():
    global block_x, block_direction, current_block
    
    if game_over_flag or speed == 0:
        return
    
    block_x += block_direction * speed
    
    # Direction change
    if block_x <= 0:
        block_x = 0
        block_direction = 1
    elif block_x + block_width >= WINDOW_WIDTH:
        block_x = WINDOW_WIDTH - block_width
        block_direction = -1
    
    # Coords update
    canvas.coords(current_block, block_x, block_y, 
                  block_x + block_width, block_y + BLOCK_HEIGHT)
    
    window.after(100, move_block)

def game_over():
    global game_over_flag, speed
    game_over_flag = True
    speed = 0
    
    canvas.create_text(
        WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, 
        text="Game Over", 
        fill="#ae00ff", 
        font=("Arial", 30),
        tags="game_over_text"
    )
    
    show_restart_buttons()

def victory():
    global game_over_flag, speed
    game_over_flag = True
    speed = 0
    
    canvas.create_text(
        WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, 
        text="Victory!", 
        fill="#ff00cc", 
        font=("Arial", 30),
        tags="victory_text"
    )
    
    show_restart_buttons()

def show_restart_buttons():
    canvas.create_text(
        WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20,
        text="Play again?",
        fill="white",
        font=("Arial", 16),
        tags="restart_text"
    )
    
    # Create buttons
    yes_button = tk.Button(window, text="Yes", command=reset_game, 
                       bg="#ae00ff", fg="white", font=("Arial", 14))
    no_button = tk.Button(window, text="No", command=window.destroy,
                      bg="darkgrey", fg="white", font=("Arial", 14))
    
    # Place buttons on canvas
    canvas.create_window(WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 70, 
                        window=yes_button, tags="yes_button")
    canvas.create_window(WINDOW_WIDTH/2 + 50, WINDOW_HEIGHT/2 + 70, 
                        window=no_button, tags="no_button")

def last_block_check():
    global block_x, block_width, last_block
    
    # First block check
    if last_block is None:
        return True
    
    # Coords of last block : [x1, y1, x2, y2]
    last_block_coords = canvas.coords(last_block)
    
    # No overlap check
    if block_x + block_width < last_block_coords[0] or block_x > last_block_coords[2]: 
        game_over()
        return False
    
    # Check for cutting on the left side
    if block_x < last_block_coords[0]: #
        cut_amount = last_block_coords[0] - block_x
        block_x = last_block_coords[0]
        block_width -= cut_amount
    
    # Check for cutting on the right side
    elif block_x + block_width > last_block_coords[2]:
        block_width -= (block_x + block_width) - last_block_coords[2]
    
    return True

def place(event):
    global block_x, block_y, block_width, last_block, current_block
    
    if game_over_flag:
        return
    
    # Check if the block is placed correctly on the last one
    if not last_block_check():
        return  
    
    # If everything is fine, we fix the block in place
    canvas.coords(current_block, block_x, block_y,
                 block_x + block_width, block_y + BLOCK_HEIGHT)
    
    # Save current block as last block for the next one
    last_block = current_block
    
    # Victory check
    if block_y - BLOCK_HEIGHT <= 0:
        victory()
        return
    
    # New block
    block_x = 0
    block_y -= BLOCK_HEIGHT
    current_block = create_block()

def reset_game():
    global block_x, block_y, block_width, last_block, current_block
    global game_over_flag, speed, block_direction
    
    # Reset variables
    block_x = WINDOW_WIDTH // 2 - INITIAL_BLOCK_WIDTH // 2
    block_y = WINDOW_HEIGHT - BLOCK_HEIGHT
    block_width = INITIAL_BLOCK_WIDTH
    block_direction = 1
    last_block = None
    game_over_flag = False
    speed = BLOCK_SPEED
    
    # Clear canvas and start new game
    canvas.delete("all")
    current_block = create_block()
    move_block()

# Keybind 
window.bind("<space>", place)

# Start game
current_block = create_block()
move_block()

window.mainloop()