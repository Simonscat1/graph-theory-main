import threading

import pygame as pg
import sys
from game import Game
from minimax import Minimax

pg.init()  # Инициализация Pygame
margin = 5  # Отступ
board_size = 180  # Размер доски
button_size = 55  # Размер кнопки
width = height = board_size * 3 + margin * 4  # Размеры окна
size_window = (width, height)  # Размер окна
screen = pg.display.set_mode(size_window)  # Создание окна
pg.display.set_caption("Сложные крестики нолики")  # Установка заголовка окна

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

game = Game()  # Создание новой игры


def run_minimax(game):  # Функция для запуска алгоритма Minimax
    alg_minimax = Minimax(game, 100)  # Создание экземпляра алгоритма Minimax
    _, best_move = alg_minimax.minimax(0, False, -float('inf'), float('inf'))  # Выполнение алгоритма Minimax
    if best_move is not None:  # Если найден лучший ход
        if game.make_move(alg_minimax.next_game_board, best_move):  # Если ход возможен
            # Вывод информации о сделанном ходе
            print(
                f"Компьютер сделал ход на доске"
                f" {alg_minimax.next_game_board[0] * 3 + alg_minimax.next_game_board[1] + 1} "
                f"в ячейке {best_move[0] + 1}, {best_move[1] + 1}")
            print(f"Следующий ход на доске {game.next_board[0] * 3 + game.next_board[1] + 1}")


def draw_endgame_message(result):  # Функция для отображения сообщения о конце игры
    if result == 'X':
        message = "Победили крестики!"
    elif result == 'O':
        message = "Победили нолики!"
    else:
        message = "Ничья!"
    font = pg.font.Font(None, 50)  # Создание шрифта
    text = font.render(message, True, (0, 0, 0))  # Создание текста
    # Отображение текста в центре экрана
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))


def reset_game():  # Функция для сброса игры
    global game
    game = Game()  # Создание новой игры



while True:  # Главный цикл игры
    for event in pg.event.get():  # Обработка событий
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)  # Завершение работы программы
        if event.type == pg.MOUSEBUTTONDOWN:  # Если событие - нажатие кнопки мыши
            x, y = pg.mouse.get_pos()  # Получение координат мыши
            board_col = x // board_size  # Определение столбца доски
            board_row = y // board_size  # Определение строки доски
            button_col = (x % board_size) // button_size  # Определение столбца кнопки
            button_row = (y % board_size) // button_size  # Определение строки кнопки
            if game.make_move((board_row, board_col), (button_row, button_col)):  # Если ход возможен
                # Вывод информации о сделанном ходе
                print(f"Ход сделан на доске {board_row * 3 + board_col + 1} в ячейке {button_row + 1},{button_col + 1}")
                print(f"Следующий ход на доске {game.next_board[0] * 3 + game.next_board[1] + 1}")
                if game.current_player == 'O':  # Если текущий игрок - 'O'
                    minimax_thread = threading.Thread(target=run_minimax, args=(game,))  # Создание потока для алгоритма Minimax
                    minimax_thread.start()  # Запуск потока
                    minimax_thread.join()  # Ожидание завершения потока
            if game.game_over():  # Если игра окончена
                result = game.game_over()  # Получение результата игры
                draw_endgame_message(result)  # Отображение сообщения о конце игры
                pg.display.update()  # Обновление дисплея
                pg.time.wait(2000)  # Задержка в 2 секунды
                reset_game()  # Сброс игры
            else:  # Если ход невозможен
                print(f"Ход невозможен")

    font = pg.font.Font(None, 24)  # Создание шрифта
    for board_row in range(3):  # Для каждой строки доски
        for board_col in range(3):  # Для каждого столбца доски
            for row in range(3):  # Для каждой строки клетки
                for col in range(3):  # Для каждого столбца клетки
                    x = (col * button_size + (col + 1) * margin) + (
                            board_col * (board_size + margin))  # Вычисление координаты x клетки
                    y = (row * button_size + (row + 1) * margin) + (
                            board_row * (board_size + margin))  # Вычисление координаты y клетки
                    cell_row = row % 3  # Определение строки клетки
                    cell_col = col % 3  # Определение столбца клетки
                    symbol = game.board[board_row][board_col][cell_row][cell_col]  # Получение символа клетки
                    if symbol == 'X':  # Если символ - 'X'
                        color = GREEN  # Цвет клетки - зеленый
                    elif symbol == 'O':  # Если символ - 'O'
                        color = RED  # Цвет клетки - красный
                    else:  # Если клетка пуста
                        color = WHITE  # Цвет клетки - белый
                    pg.draw.rect(screen, color, (x, y, button_size, button_size))  # Отрисовка клетки
                    if symbol != '_':  # Если клетка не пуста
                        font = pg.font.Font(None, 36)  # Создание шрифта
                        text = font.render(symbol, True, BLACK)  # Создание текста
                        text_rect = text.get_rect(center=(x + button_size // 2, y + button_size // 2))  # Создание прямоугольника для текста
                        screen.blit(text, text_rect)  # Отрисовка текста
    pg.display.update()  # Обновление дисплея

