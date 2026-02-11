// Constants
const WINDOW_WIDTH = 400;
const WINDOW_HEIGHT = 600;
const BLOCK_HEIGHT = 50;
const INITIAL_BLOCK_WIDTH = 150;
const BLOCK_SPEED = 50;
const BG_COLOR = "#000000";
const BLOCK_COLOR = "#FFFFFF";

// Get canvas and context
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Global variables
let block_x = WINDOW_WIDTH / 2 - INITIAL_BLOCK_WIDTH / 2;
let block_y = WINDOW_HEIGHT - BLOCK_HEIGHT;
let block_width = INITIAL_BLOCK_WIDTH;
let block_direction = 1;
let last_block = null;
let current_block = null; // Current block data
let game_over_flag = false;
let speed = BLOCK_SPEED;

// Storage for all blocks (for drawing)
let all_blocks = [];

// === Funktions ===

function create_block() {
    const block = {
        x: block_x,
        y: block_y,
        width: block_width,
        height: BLOCK_HEIGHT
    };
    all_blocks.push(block);
    return block;
}

function draw() {
    // Clear canvas
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);
    
    // Draw all blocks
    all_blocks.forEach(block => {
        ctx.fillStyle = BLOCK_COLOR;
        ctx.fillRect(block.x, block.y, block.width, block.height);
    });
}

function move_block() {
    if (game_over_flag || speed === 0) {
        return;
    }
    
    // Update block position
    block_x += block_direction * speed;
    
    // Direction change
    if (block_x <= 0) {
        block_x = 0;
        block_direction = 1;
    } else if (block_x + block_width >= WINDOW_WIDTH) {
        block_x = WINDOW_WIDTH - block_width;
        block_direction = -1;
    }
    
    // Coords update (update current block data)
    if (current_block) {
        current_block.x = block_x;
        current_block.y = block_y;
        current_block.width = block_width;
    }
    
    // Draw everything
    draw();
    
    // window.after(100, move_block) → setTimeout
    setTimeout(move_block, 100);
}

function game_over() {
    game_over_flag = true;
    speed = 0;
    
    // Game over text
    ctx.fillStyle = "red";
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Game Over", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50);
    
    show_restart_buttons();
}

function victory() {
    game_over_flag = true;
    speed = 0;
    
    // Victory text
    ctx.fillStyle = "green";
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Victory!", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50);
    
    show_restart_buttons();
}

function show_restart_buttons() {
    // Play again text
    ctx.fillStyle = "white";
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Play again?", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20);
    
    // Create buttons (html elements)
    const buttonContainer = document.getElementById('buttonContainer');
    buttonContainer.innerHTML = ''; // Clear previous buttons if any
    
    const yesButton = document.createElement('button');
    yesButton.textContent = 'Yes';
    yesButton.style.backgroundColor = 'green';
    yesButton.style.color = 'white';
    yesButton.style.fontSize = '14px';
    yesButton.style.padding = '10px 20px';
    yesButton.style.margin = '5px';
    yesButton.style.cursor = 'pointer';
    yesButton.onclick = reset_game;
    
    const noButton = document.createElement('button');
    noButton.textContent = 'No';
    noButton.style.backgroundColor = 'red';
    noButton.style.color = 'white';
    noButton.style.fontSize = '14px';
    noButton.style.padding = '10px 20px';
    noButton.style.margin = '5px';
    noButton.style.cursor = 'pointer';
    noButton.onclick = () => window.close();
    
    buttonContainer.appendChild(yesButton);
    buttonContainer.appendChild(noButton);
    buttonContainer.style.display = 'block';
}

function last_block_check() {
    // First block check
    if (last_block === null) {
        return true;
    }
    
    // Coords of last block : [x1, y1, x2, y2]
    const last_block_coords = [
        last_block.x,
        last_block.y,
        last_block.x + last_block.width,
        last_block.y + last_block.height
    ];
    
    // No overlap check
    if (block_x + block_width < last_block_coords[0] || block_x > last_block_coords[2]) {
        game_over();
        return false;
    }
    
    // Check for cutting on the left side
    if (block_x < last_block_coords[0]) {
        const cut_amount = last_block_coords[0] - block_x;
        block_x = last_block_coords[0];
        block_width -= cut_amount;
    }
    // Check for cutting on the right side
    else if (block_x + block_width > last_block_coords[2]) {
        block_width -= (block_x + block_width) - last_block_coords[2];
    }
    
    return true;
}

function place() {
    if (game_over_flag) {
        return;
    }
    
    // Check if the block is placed correctly on the last one
    if (!last_block_check()) {
        return;
    }
    
    // If everything is fine, we fix the block in place
    current_block.x = block_x;
    current_block.y = block_y;
    current_block.width = block_width;
    
    // Save current block as last block for the next one
    last_block = current_block;
    
    // Victory check
    if (block_y - BLOCK_HEIGHT <= 0) {
        victory();
        return;
    }
    
    // New block
    block_x = 0;
    block_y -= BLOCK_HEIGHT;
    current_block = create_block();
}

function reset_game() {
    // Reset variables
    block_x = WINDOW_WIDTH / 2 - INITIAL_BLOCK_WIDTH / 2;
    block_y = WINDOW_HEIGHT - BLOCK_HEIGHT;
    block_width = INITIAL_BLOCK_WIDTH;
    block_direction = 1;
    last_block = null;
    game_over_flag = false;
    speed = BLOCK_SPEED;
    
    // Clear canvas and start new game
    all_blocks = [];
    
    // Hide buttons
    document.getElementById('buttonContainer').style.display = 'none';
    
    current_block = create_block();
    move_block();
}

// Keybind
document.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
        event.preventDefault(); // Delete space scroll
        place();
    }
});

// Start game
current_block = create_block();
move_block();