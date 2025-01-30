import chess
import collections
import random

# Piece Values
PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100
}

TERMINATIONS = ['is_stalemate', 'is_insufficient_material', 'is_checkmate',
                'can_claim_fifty_moves', 'can_claim_threefold_repetition']


def get_termination(board):
    """Check how the game ended."""
    for termination in TERMINATIONS:
        method = getattr(board, termination)
        if method():
            return termination
    return None


def evaluate_board(board):
    """Improved Evaluation: Material, Mobility, King Safety"""
    if board.is_checkmate():
        return -1000 if board.turn else 1000  # Negative if current player is in checkmate
    if board.is_stalemate() or board.is_insufficient_material():
        return 0  # Draw
    
    score = 0
    for piece_type in PIECE_VALUES.keys():
        score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

    # Number of legal moves
    score += 0.1 * len(list(board.legal_moves)) if board.turn == chess.WHITE else -0.1 * len(list(board.legal_moves))

    # King safety: Encourage castling
    if board.has_castling_rights(chess.WHITE):
        score += 0.5
    if board.has_castling_rights(chess.BLACK):
        score -= 0.5

    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax with Alpha-Beta Pruning (Depth 3)"""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def best_move(board, depth=3):
    """Find the best move using Minimax (Depth 3)"""
    best_eval = float('-inf') if board.turn else float('inf')
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, float('-inf'), float('inf'), not board.turn)
        board.pop()

        if (board.turn and eval > best_eval) or (not board.turn and eval < best_eval):
            best_eval = eval
            best_move = move

    return best_move


def random_move(board):
    """Play a smarter random move: Prefer captures, avoid repetition"""
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)

    # Prefer captures over random moves
    capture_moves = [move for move in legal_moves if board.is_capture(move)]
    return random.choice(capture_moves) if capture_moves else random.choice(legal_moves)


def play_game(white_strategy, black_strategy):
    """Simulate a chess game with different strategies."""
    board = chess.Board()

    while not board.is_game_over():
        move = white_strategy(board) if board.turn == chess.WHITE else black_strategy(board)
        board.push(move)

    result = board.result(claim_draw=True)
    termination = get_termination(board)
    
    return result, termination


def run_simulation(num_games, white_strategy, black_strategy):
    """Run multiple games and summarize the results."""
    stats = collections.Counter()

    for _ in range(num_games):
        result, termination = play_game(white_strategy, black_strategy)
        if termination == 'is_checkmate':
            stats[result] += 1
        else:
            stats[termination] += 1

    return stats


def calculate_win_rate(stats):
    """Compute win rates from simulation results."""
    white_wins = stats['1-0']
    black_wins = stats['0-1']
    draws = sum(stats[term] for term in stats if term not in ['1-0', '0-1'])

    total_games = white_wins + black_wins + draws
    white_win_rate = (white_wins / total_games) * 100
    black_win_rate = (black_wins / total_games) * 100
    draw_rate = (draws / total_games) * 100

    return white_win_rate, black_win_rate, draw_rate


# Number of simulations per case
NUM_GAMES = 1000

# Run simulations
print("Running Case 1: Random VS Random")
stats1 = run_simulation(NUM_GAMES, random_move, random_move)
w1, b1, d1 = calculate_win_rate(stats1)

print("Running Case 2: Expert (Minimax) VS Random")
stats2 = run_simulation(NUM_GAMES, best_move, random_move)
w2, b2, d2 = calculate_win_rate(stats2)

print("Running Case 3: Random VS Expert (Minimax)")
stats3 = run_simulation(NUM_GAMES, random_move, best_move)
w3, b3, d3 = calculate_win_rate(stats3)

# Display results
print("\n=== Simulation Results (Win Rates) ===")
print(f"Case 1 (Random vs. Random): White Win: {w1:.2f}%, Black Win: {b1:.2f}%, Draw: {d1:.2f}%")
print(f"Case 2 (Minimax vs. Random): White Win: {w2:.2f}%, Black Win: {b2:.2f}%, Draw: {d2:.2f}%")
print(f"Case 3 (Random vs. Minimax): White Win: {w3:.2f}%, Black Win: {b3:.2f}%, Draw: {d3:.2f}%")
