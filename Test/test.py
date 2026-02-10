import tkinter as tk

# === НАСТРОЙКИ ===
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BLOCK_HEIGHT = 30
INITIAL_BLOCK_WIDTH = 150  # Начальная ширина (3 "блока")
SPEED = 3
BG_COLOR = "#2C3E50"
BLOCK_COLOR = "#E74C3C"

# === ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ===
block_x = 0
block_y = WINDOW_HEIGHT - BLOCK_HEIGHT
block_width = INITIAL_BLOCK_WIDTH
direction = 1  # 1 = вправо, -1 = влево
level = 0
game_over = False
fallen_blocks = []  # Список упавших блоков: [(x, y, width), ...]

# === СОЗДАНИЕ ОКНА ===
window = tk.Tk()
window.title("Stacker Game")
window.resizable(False, False)

canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR)
canvas.pack()

# Текст для счёта уровней
score_text = canvas.create_text(WINDOW_WIDTH//2, 30, text=f"Уровень: {level}", 
                                fill="white", font=("Arial", 16, "bold"))

# Первый блок (стартовая платформа)
base_block = canvas.create_rectangle(
    WINDOW_WIDTH//2 - INITIAL_BLOCK_WIDTH//2,  # x1
    WINDOW_HEIGHT - BLOCK_HEIGHT,              # y1
    WINDOW_WIDTH//2 + INITIAL_BLOCK_WIDTH//2,  # x2
    WINDOW_HEIGHT,                              # y2
    fill="#3498DB", outline=""
)

# Сохраняем первый блок в список
fallen_blocks.append((WINDOW_WIDTH//2 - INITIAL_BLOCK_WIDTH//2, 
                      WINDOW_HEIGHT - BLOCK_HEIGHT, 
                      INITIAL_BLOCK_WIDTH))

# Движущийся блок (начинаем со второго уровня)
block_y = WINDOW_HEIGHT - 2 * BLOCK_HEIGHT
moving_block = canvas.create_rectangle(
    block_x, block_y,
    block_x + block_width, block_y + BLOCK_HEIGHT,
    fill=BLOCK_COLOR, outline=""
)

# === ФУНКЦИЯ ДВИЖЕНИЯ ===
def move_block():
    global block_x, direction
    
    if game_over:
        return
    
    # Двигаем блок
    block_x += direction * SPEED
    
    # Отскок от краёв
    if block_x <= 0:
        block_x = 0
        direction = 1
    elif block_x + block_width >= WINDOW_WIDTH:
        block_x = WINDOW_WIDTH - block_width
        direction = -1
    
    # Обновляем позицию на canvas
    canvas.coords(moving_block, block_x, block_y,
                  block_x + block_width, block_y + BLOCK_HEIGHT)
    
    # Повторяем через 20мс
    window.after(20, move_block)

# === ФУНКЦИЯ ОСТАНОВКИ БЛОКА ===
def stop_block(event):
    global block_y, block_width, level, game_over, moving_block
    
    if game_over:
        return
    
    # Получаем данные предыдущего блока
    prev_x, prev_y, prev_width = fallen_blocks[-1]
    
    # Проверяем перекрытие
    overlap = check_overlap(block_x, block_width, prev_x, prev_width)
    
    if overlap == 0:
        # GAME OVER
        game_over = True
        canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2,
                          text="GAME OVER!", fill="white",
                          font=("Arial", 32, "bold"))
        canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40,
                          text=f"Уровней пройдено: {level}", fill="white",
                          font=("Arial", 16))
        canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80,
                          text="Нажми R для рестарта", fill="white",
                          font=("Arial", 14))
        return
    
    # Блок упал успешно!
    # Вычисляем новую позицию (по центру перекрытия)
    new_x = max(block_x, prev_x)
    new_width = overlap
    
    # Фиксируем блок
    canvas.coords(moving_block, new_x, block_y,
                  new_x + new_width, block_y + BLOCK_HEIGHT)
    canvas.itemconfig(moving_block, fill="#3498DB")
    
    # Добавляем в список
    fallen_blocks.append((new_x, block_y, new_width))
    
    # Следующий уровень
    level += 1
    canvas.itemconfig(score_text, text=f"Уровень: {level}")
    
    # Уменьшаем ширину каждые 3 уровня
    if level % 3 == 0 and block_width > 50:
        block_width = new_width - 30
    else:
        block_width = new_width
    
    # Новый блок
    block_y -= BLOCK_HEIGHT
    moving_block = canvas.create_rectangle(
        0, block_y, block_width, block_y + BLOCK_HEIGHT,
        fill=BLOCK_COLOR, outline=""
    )

# === ПРОВЕРКА ПЕРЕКРЫТИЯ ===
def check_overlap(new_x, new_width, prev_x, prev_width):
    """Возвращает ширину перекрытия"""
    new_left = new_x
    new_right = new_x + new_width
    
    prev_left = prev_x
    prev_right = prev_x + prev_width
    
    # Нет перекрытия?
    if new_right <= prev_left or new_left >= prev_right:
        return 0
    
    # Есть перекрытие - вычисляем
    overlap_left = max(new_left, prev_left)
    overlap_right = min(new_right, prev_right)
    
    return overlap_right - overlap_left

# === РЕСТАРТ ИГРЫ ===
def restart_game(event):
    global block_x, block_y, block_width, level, game_over, fallen_blocks, moving_block, direction
    
    if not game_over:
        return
    
    # Очищаем canvas
    canvas.delete("all")
    
    # Сбрасываем переменные
    block_x = 0
    block_y = WINDOW_HEIGHT - BLOCK_HEIGHT
    block_width = INITIAL_BLOCK_WIDTH
    direction = 1
    level = 0
    game_over = False
    fallen_blocks = []
    
    # Пересоздаём интерфейс
    canvas.create_text(WINDOW_WIDTH//2, 30, text=f"Уровень: {level}",
                      fill="white", font=("Arial", 16, "bold"), tags="score")
    
    # Базовый блок
    canvas.create_rectangle(
        WINDOW_WIDTH//2 - INITIAL_BLOCK_WIDTH//2,
        WINDOW_HEIGHT - BLOCK_HEIGHT,
        WINDOW_WIDTH//2 + INITIAL_BLOCK_WIDTH//2,
        WINDOW_HEIGHT,
        fill="#3498DB", outline=""
    )
    fallen_blocks.append((WINDOW_WIDTH//2 - INITIAL_BLOCK_WIDTH//2,
                         WINDOW_HEIGHT - BLOCK_HEIGHT,
                         INITIAL_BLOCK_WIDTH))
    
    # Новый движущийся блок
    block_y = WINDOW_HEIGHT - 2 * BLOCK_HEIGHT
    moving_block = canvas.create_rectangle(
        block_x, block_y, block_x + block_width, block_y + BLOCK_HEIGHT,
        fill=BLOCK_COLOR, outline=""
    )
    
    move_block()

# === ПРИВЯЗКА КЛАВИШ ===
window.bind("<space>", stop_block)
window.bind("<r>", restart_game)
window.bind("<R>", restart_game)

# === ЗАПУСК ===
move_block()
window.mainloop()