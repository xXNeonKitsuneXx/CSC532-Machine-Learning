import chess
import chess.engine
import random
from collections import Counter

def random_move(board):
    """Plays a random legal move."""
    return random.choice(list(board.legal_moves))

def minimax_move(board, depth=2):
    """Minimax algorithm with a basic evaluation function."""
    if board.is_game_over():
        return None
    
    best_move = None
    best_value = float('-inf') if board.turn else float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, float('-inf'), float('inf'), not board.turn)
        board.pop()
        
        if board.turn:  # White (maximizing)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        else:  # Black (minimizing)
            if move_value < best_value:
                best_value = move_value
                best_move = move
    
    return best_move

def minimax(board, depth, alpha, beta, maximizing):
    """Minimax with alpha-beta pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval_value = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_value = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:
                break
        return min_eval

def evaluate_board(board):
    """Simple evaluation function using material count."""
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000}
    
    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    
    return score

def play_game(white_player, black_player):
    """Plays a single game between the given players."""
    board = chess.Board()
    while not board.is_game_over():
        move = white_player(board) if board.turn else black_player(board)
        board.push(move)
    return board.result()  # "1-0", "0-1", or "1/2-1/2"

def simulate_games(n, white_strategy, black_strategy):
    """Simulates n games and counts results."""
    results = Counter(play_game(white_strategy, black_strategy) for _ in range(n))
    
    win_rate = {
        'White Win %': (results['1-0'] / n) * 100,
        'Black Win %': (results['0-1'] / n) * 100,
        'Draw %': (results['1/2-1/2'] / n) * 100
    }
    return win_rate

# Simulating games
num_games = 1000
results_random_vs_random = simulate_games(num_games, random_move, random_move)
results_expert_vs_random = simulate_games(num_games, minimax_move, random_move)
results_random_vs_expert = simulate_games(num_games, random_move, minimax_move)

# Displaying results
print("Random vs Random:", results_random_vs_random)
print("Expert (White) vs Random (Black):", results_expert_vs_random)
print("Random (White) vs Expert (Black):", results_random_vs_expert)
