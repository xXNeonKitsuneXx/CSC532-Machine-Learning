import chess
import random
import collections


def get_termination(board):
    """Check how the game ended."""
    if board.is_checkmate():
        return "checkmate"
    elif board.is_stalemate():
        return "stalemate"
    elif board.is_insufficient_material():
        return "insufficient_material"
    elif board.can_claim_fifty_moves():
        return "fifty_moves"
    elif board.can_claim_threefold_repetition():
        return "threefold_repetition"
    return "in_progress"


def minimax(board, depth, maximizing):
    """Simple Minimax implementation without Stockfish."""
    if depth == 0 or board.is_game_over():
        if board.is_checkmate():
            return -100 if board.turn else 100
        return 0

    if maximizing:
        best_value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            best_value = max(best_value, minimax(board, depth - 1, False))
            board.pop()
        return best_value
    else:
        best_value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            best_value = min(best_value, minimax(board, depth - 1, True))
            board.pop()
        return best_value


def get_best_move(board, depth=2):
    """Select the best move using Minimax."""
    best_move = None
    best_value = -float('inf')
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, False)
        board.pop()
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move


def play_random_game():
    """Simulates a game where both players make random moves."""
    board = chess.Board()
    while not board.is_game_over():
        move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.result(), get_termination(board)


def play_minimax_game(minimax_first=True):
    """Simulates a game where one player uses minimax and the other plays randomly."""
    board = chess.Board()
    while not board.is_game_over():
        if (board.turn == chess.WHITE and minimax_first) or (board.turn == chess.BLACK and not minimax_first):
            move = get_best_move(board, depth=2)
        else:
            move = random.choice(list(board.legal_moves))
        board.push(move)
    return board.result(), get_termination(board)


def simulate_games(n=1):
    """Runs simulations for both random and minimax-based games."""
    random_stats = collections.Counter()
    minimax_first_stats = collections.Counter()
    minimax_second_stats = collections.Counter()

    for _ in range(n):
        result, termination = play_random_game()
        random_stats[result] += 1

        result, termination = play_minimax_game(minimax_first=True)
        minimax_first_stats[result] += 1

        result, termination = play_minimax_game(minimax_first=False)
        minimax_second_stats[result] += 1

    return random_stats, minimax_first_stats, minimax_second_stats


# Run simulations
random_results, minimax_first_results, minimax_second_results = simulate_games(1000)

# Display results
print("Random vs Random:", random_results)
print("Minimax First vs Random:", minimax_first_results)
print("Minimax Second vs Random:", minimax_second_results)


def calculate_win_rates(stats):
    """Calculate win percentages from simulation results."""
    total_games = sum(stats.values())
    white_wins = stats.get("1-0", 0) / total_games * 100
    black_wins = stats.get("0-1", 0) / total_games * 100
    draws = stats.get("1/2-1/2", 0) / total_games * 100
    return {
        "White Win %": white_wins,
        "Black Win %": black_wins,
        "Draw %": draws,
    }


print("Random Strategy Win Rates:", calculate_win_rates(random_results))
print("Minimax First Strategy Win Rates:", calculate_win_rates(minimax_first_results))
print("Minimax Second Strategy Win Rates:", calculate_win_rates(minimax_second_results))