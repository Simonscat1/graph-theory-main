class Game:
    def __init__(self):
        self.board = [[[['_'] * 3 for _ in range(3)] for _ in range(3)] for _ in range(3)]  # Инициализация доски игры
        self.current_player = 'X'  # Установка текущего игрока
        self.next_board = None  # Установка следующей доски

    def make_move(self, board, cell):  # Функция для выполнения хода
        board_row, board_col = board  # Получение координат доски
        button_row, button_col = cell  # Получение координат клетки
        # Проверка, можно ли сделать ход на данной доске
        if self.next_board is not None and self.next_board != (board_row, board_col):
            return False
        try:
            # Проверка, свободна ли клетка
            if self.board[board_row][board_col][button_row][button_col] != '_':
                return False
            # Выполнение хода
            self.board[board_row][board_col][button_row][button_col] = self.current_player
            self.next_board = (button_row, button_col)
            # Переключение игрока
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        except IndexError:
            pass

    def check_winner(self, player):  # Функция для проверки, выиграл ли игрок
        for board_row in range(3):
            for board_col in range(3):
                for i in range(3):
                    # Проверка строк и столбцов на выигрыш
                    if self.board[board_row][board_col][i][0] == self.board[board_row][board_col][i][1] == \
                            self.board[board_row][board_col][i][2] == player:
                        return True
                    if self.board[board_row][board_col][0][i] == self.board[board_row][board_col][1][i] == \
                            self.board[board_row][board_col][2][i] == player:
                        return True
                # Проверка диагоналей на выигрыш
                if self.board[board_row][board_col][0][0] == self.board[board_row][board_col][1][1] == \
                        self.board[board_row][board_col][2][2] == player:
                    return True
                if self.board[board_row][board_col][0][2] == self.board[board_row][board_col][1][1] == \
                        self.board[board_row][board_col][2][0] == player:
                    return True
        return False

    def game_over(self):  # Функция для проверки, окончена ли игра
        # Проверяем, выиграл ли кто-нибудь
        if self.check_winner('X'):
            return 'X'
        if self.check_winner('O'):
            return 'O'
        # Проверяем, есть ли еще доступные ходы
        for board_row in range(3):
            for board_col in range(3):
                for button_row in range(3):
                    for button_col in range(3):
                        if self.board[board_row][board_col][button_row][button_col] == '_':
                            return None
        # Если ни один из игроков не выиграл и нет доступных ходов, игра закончена
        return 'Draw'


