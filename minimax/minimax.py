import time


class Minimax:
    def __init__(self, game, max_depth):
        self.game_boards = game.board  # Инициализация доски игры
        self.next_game_board = game.next_board  # Инициализация следующей доски
        self.max_depth = max_depth  # Установка максимальной глубины
        self.start_time = time.time()  # Установка начального времени

    def evaluate(self, player, depth):  # Функция оценки
        score = 0  # Инициализация счета
        opponent = 'O' if player == 'X' else 'X'  # Определение противника

        for board_row in range(3):  # Для каждой строки доски
            for board_col in range(3):  # Для каждого столбца доски
                for i in range(3):  # Для каждой строки клетки
                    # Проверяем строки и столбцы
                    for line in [self.game_boards[board_row][board_col][i],
                                 [self.game_boards[board_row][board_col][j][i] for j in range(3)]]:
                        if line.count(player) == 2 and line.count('_') == 1:
                            score += 10 / depth  # Близость к победе
                        if line.count(opponent) == 2 and line.count('_') == 1:
                            score -= 20 / depth  # Угроза

                # Проверяем диагонали
                for diag in [[self.game_boards[board_row][board_col][i][i] for i in range(3)],
                             [self.game_boards[board_row][board_col][i][2 - i] for i in range(3)]]:
                    if diag.count(player) == 2 and diag.count('_') == 1:
                        score += 30 / depth  # Близость к победе
                    if diag.count(opponent) == 2 and diag.count('_') == 1:
                        score -= 20 / depth  # Угроза

                # Центральные клетки
                if self.game_boards[board_row][board_col][1][1] == player:
                    score += 1

                # Угловые клетки
                for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                    if self.game_boards[board_row][board_col][i][j] == player:
                        score += 1

                # Блокирование противника
                for i in range(3):
                    for j in range(3):
                        if self.game_boards[board_row][board_col][i][j] == player and any(
                                line.count(opponent) == 1 and line.count('_') == 2 for line in
                                [self.game_boards[board_row][board_col][i],
                                 [self.game_boards[board_row][board_col][k][j] for k in range(3)],
                                 [self.game_boards[board_row][board_col][k][k] for k in range(3)],
                                 [self.game_boards[board_row][board_col][k][2 - k] for k in range(3)]]):
                            score += 5  # Блокирование противника

        return score, None  # Возвращение оценки

    def minimax(self, depth, isMaximizing, alpha, beta):
        # Если достигнута максимальная глубина или превышено время, возвращаем оценку текущего состояния игры
        if depth == self.max_depth or time.time() - self.start_time > 10:
            return self.evaluate('X' if isMaximizing else 'O', depth)

        board_row, board_col = self.next_game_board  # Получаем координаты следующей доски

        if isMaximizing:  # Если текущий игрок максимизирует оценку
            best = -1000  # Инициализация лучшего значения
            best_move = None  # Инициализация лучшего хода

            for i in range(3):  # Перебор всех клеток на доске
                for j in range(3):
                    if self.game_boards[board_row][board_col][i][j] == '_':  # Если клетка свободна
                        self.game_boards[board_row][board_col][i][j] = 'X'  # Совершаем ход
                        original_next_board = self.next_game_board  # Сохраняем оригинальную следующую доску
                        self.next_game_board = (i, j)  # Обновляем следующую доску
                        score, _ = self.minimax(depth + 1, not isMaximizing, alpha, beta)  # Рекурсивный вызов minimax
                        self.game_boards[board_row][board_col][i][j] = '_'  # Отменяем ход
                        self.next_game_board = original_next_board  # Восстанавливаем следующую доску

                        if score > best:  # Если новый счет лучше предыдущего лучшего
                            best = score  # Обновляем лучший счет
                            best_move = (i, j)  # Обновляем лучший ход

                        alpha = max(alpha, best)  # Обновляем значение alpha
                        if beta <= alpha:  # Если beta меньше или равно alpha, прерываем цикл
                            break

            return best, best_move  # Возвращаем лучший счет и лучший ход

        else:  # Если текущий игрок минимизирует оценку
            best = 1000  # Инициализация лучшего значения
            best_move = None  # Инициализация лучшего хода

            for i in range(3):  # Перебор всех клеток на доске
                for j in range(3):
                    if self.game_boards[board_row][board_col][i][j] == '_':  # Если клетка свободна
                        self.game_boards[board_row][board_col][i][j] = 'O'  # Совершаем ход
                        original_next_board = self.next_game_board  # Сохраняем оригинальную следующую доску
                        self.next_game_board = (i, j)  # Обновляем следующую доску
                        score, _ = self.minimax(depth + 1, not isMaximizing, alpha, beta)  # Рекурсивный вызов minimax
                        self.game_boards[board_row][board_col][i][j] = '_'  # Отменяем ход
                        self.next_game_board = original_next_board  # Восстанавливаем следующую доску

                        if score < best:  # Если новый счет лучше предыдущего лучшего
                            best = score  # Обновляем лучший счет
                            best_move = (i, j)  # Обновляем лучший ход

                        beta = min(beta, best)  # Обновляем значение beta
                        if beta <= alpha:  # Если beta меньше или равно alpha, прерываем цикл
                            break

            return best, best_move  # Возвращаем лучший счет и лучший ход

