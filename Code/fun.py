from machine import Pin
from time import sleep as pause
import sys

# Пины для LED
fun_game_over = Pin(23, Pin.OUT)   # FUN


while True:
    # Читаем команду от Python
    command = sys.stdin.readline().strip()
    
    if command == 'GAME_OVER':
        fun_game_over.value(1)  # Включаем красный
        pause(2)  # Держим включенным 2 секунды
        fun_game_over.value(0)
