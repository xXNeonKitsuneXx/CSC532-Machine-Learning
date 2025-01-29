import chess
import random


def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    legal_moves = list(board.legal_moves)
    if maximizing:
        best_value = float('-inf')
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, False)
            board.pop()
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, True)
            board.pop()
            best_value = min(best_value, value)
        return best_value


def get_best_move(board, depth=2):
    best_move = None
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, False)
        board.pop()
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move


def evaluate_board(board):
    if board.is_checkmate():
        return float('-inf') if board.turn else float('inf')
    return sum(piece_value(piece) for piece in board.piece_map().values())


def piece_value(piece):
    values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    return values[piece.piece_type] if piece.color == chess.WHITE else -values[piece.piece_type]


def play_minimax_vs_random(minimax_first=True):
    board = chess.Board()
    while not board.is_game_over():
        if (board.turn == chess.WHITE and minimax_first) or (board.turn == chess.BLACK and not minimax_first):
            move = get_best_move(board)
        else:
            move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.result()


def simulate_games(n):
    random_vs_random_results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
    minimax_first_results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
    minimax_second_results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
    for _ in range(n):
        board = chess.Board()
        while not board.is_game_over():
            move = random.choice(list(board.legal_moves))
            board.push(move)
        random_vs_random_results[board.result()] += 1
        result = play_minimax_vs_random(minimax_first=True)
        minimax_first_results[result] += 1
        result = play_minimax_vs_random(minimax_first=False)
        minimax_second_results[result] += 1
    return random_vs_random_results, minimax_first_results, minimax_second_results


def calculate_win_rate(results, n):
    win_rate = {
        "Win %": (results["1-0"] / n) * 100,
        "Loss %": (results["0-1"] / n) * 100,
        "Draw %": (results["1/2-1/2"] / n) * 100
    }
    return win_rate


if __name__ == "__main__":
    n = 1000
    random_results, minimax_first_results, minimax_second_results = simulate_games(n)
    print("Random vs Random Results:", random_results, "Win Rate:", calculate_win_rate(random_results, n))
    print("Minimax First vs Random Results:", minimax_first_results, "Win Rate:",
          calculate_win_rate(minimax_first_results, n))
    print("Minimax Second vs Random Results:", minimax_second_results, "Win Rate:",
          calculate_win_rate(minimax_second_results, n))