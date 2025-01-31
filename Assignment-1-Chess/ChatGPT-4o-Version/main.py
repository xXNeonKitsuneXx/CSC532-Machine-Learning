import chess
import random
import numpy as np
import pandas as pd

# --- Opening Book ---
opening_book = {
    "e2e4": ["e7e5", "c7c5", "e7e6", "c7c6"],  # Responses to 1. e4
    "d2d4": ["d7d5", "g8f6", "e7e6"],  # Responses to 1. d4
    "c2c4": ["e7e5", "c7c5", "g8f6"],  # Responses to 1. c4 (English)
    "g1f3": ["d7d5", "g8f6", "c7c5"],  # Responses to 1. Nf3
}

def get_opening_move(board):
    """Returns an opening move if available, otherwise None."""
    moves = [move.uci() for move in board.move_stack]  # Convert to UCI format
    if len(moves) == 0:
        return random.choice(["e2e4", "d2d4", "c2c4", "g1f3"])  # First move
    elif len(moves) == 1:
        return random.choice(opening_book.get(moves[0], []))  # Respond if in book
    return None  # No book move

# --- Minimax with Alpha-Beta Pruning ---
piece_values = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

def evaluate_board(board):
    """Evaluate board state, considering material, position, and endgame dynamics."""
    if board.is_checkmate():
        return 100000 if board.turn == chess.BLACK else -100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0  # Draw

    score = sum(
        piece_values.get(board.piece_at(square).piece_type, 0)
        * (1 if board.piece_at(square).color == chess.WHITE else -1)
        for square in chess.SQUARES if board.piece_at(square)
    )
    
    return score + len(list(board.legal_moves)) * 5  # Mobility bonus

def order_moves(board):
    """Orders moves to prioritize captures and checks for better alpha-beta pruning."""
    def move_priority(move):
        if board.gives_check(move):
            return 20
        if board.is_capture(move):
            return 10
        return 1
    return sorted(board.legal_moves, key=move_priority, reverse=True)

def minimax(board, depth, alpha, beta, is_maximizing):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    best_score = -np.inf if is_maximizing else np.inf
    for move in order_moves(board):
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta, not is_maximizing)
        board.pop()
        if is_maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)
        if beta <= alpha:
            break  # Alpha-beta pruning
    return best_score

def best_move_minimax(board, depth=4):
    """Select the best move using Minimax, considering the opening book."""
    if board.fullmove_number <= 2:  # Use opening book for first 2 moves
        move = get_opening_move(board)
        if move:
            return chess.Move.from_uci(move)

    best_score, best_move = -np.inf, None
    alpha, beta = -np.inf, np.inf
    for move in order_moves(board):
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if score > best_score:
            best_score, best_move = score, move
    return best_move

# --- Random Move Selection ---
def random_move(board):
    return random.choice(list(board.legal_moves))

# --- Simulate a Game ---
def play_game(player_white, player_black):
    """Simulates a game between two players."""
    board = chess.Board()
    while not board.is_game_over():
        move = player_white(board) if board.turn == chess.WHITE else player_black(board)
        board.push(move)
    result = board.result()
    return 1 if result == "1-0" else -1 if result == "0-1" else 0

# --- Simulate 1,000 Games ---
num_games = 1000
scenarios = {
    "Random vs. Random": (random_move, random_move),
    "Minimax (White) vs. Random (Black)": (lambda b: best_move_minimax(b, 4), random_move),
    "Random (White) vs. Minimax (Black)": (random_move, lambda b: best_move_minimax(b, 4))
}

# --- Run Simulations ---
results = {scenario: [play_game(white, black) for _ in range(num_games)] for scenario, (white, black) in scenarios.items()}

# --- Summarize Results ---
win_rates = {
    scenario: {
        "White Win Rate": sum(1 for r in results[scenario] if r == 1) / num_games * 100,
        "Black Win Rate": sum(1 for r in results[scenario] if r == -1) / num_games * 100,
        "Draw Rate": sum(1 for r in results[scenario] if r == 0) / num_games * 100
    } for scenario in scenarios
}

# --- Display Results ---
df_results = pd.DataFrame(win_rates).T
print(df_results)
