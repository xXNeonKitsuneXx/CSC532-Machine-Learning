import chess
import random
import collections

# Piece values for evaluation
PIECE_SCORES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Conditions for game termination
DRAW_CONDITIONS = ['is_stalemate', 'is_insufficient_material', 'can_claim_fifty_moves', 'can_claim_threefold_repetition']

def evaluate_position(board):
    if board.is_checkmate():
        return -1 if board.turn else 1  # Negative if Black wins, positive if White wins
    if any(getattr(board, condition)() for condition in DRAW_CONDITIONS):
        return 0  # Draw scenario
    
    score = sum((len(board.pieces(p, chess.WHITE)) - len(board.pieces(p, chess.BLACK))) * PIECE_SCORES[p] for p in PIECE_SCORES)
    return score / 10000  # Normalize for stability

# Minimax with Alpha-Beta Pruning
def minimax_search(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_position(board), None
    
    best_move = None
    possible_moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)  # Prioritize captures

    if is_maximizing:
        max_score = float('-inf')
        for move in possible_moves:
            board.push(move)
            score, _ = minimax_search(board, depth - 1, alpha, beta, False)
            board.pop()
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Prune search
        return max_score, best_move
    else:
        min_score = float('inf')
        for move in possible_moves:
            board.push(move)
            score, _ = minimax_search(board, depth - 1, alpha, beta, True)
            board.pop()
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break  # Prune search
        return min_score, best_move

# Simulation functions
def random_vs_random():
    board = chess.Board()
    while not board.is_game_over():
        move = random.choice(list(board.legal_moves))
        board.push(move)
    return determine_winner(board)

def expert_vs_random():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn:
            _, move = minimax_search(board, 2, float('-inf'), float('inf'), True)
        else:
            move = random.choice(list(board.legal_moves))
        board.push(move)
    return determine_winner(board)

def random_vs_expert():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn:
            move = random.choice(list(board.legal_moves))
        else:
            _, move = minimax_search(board, 2, float('-inf'), float('inf'), False)
        board.push(move)
    return determine_winner(board)

def determine_winner(board):
    if board.is_checkmate():
        return "1-0" if board.turn == False else "0-1"
    return "1/2-1/2"

def run_experiments(simulation, iterations=1000):
    results = collections.Counter()
    for _ in range(iterations):
        outcome = simulation()
        results[outcome] += 1
    return results

def main():
    matchups = {
        "Random vs Random": random_vs_random,
        "Expert (White) vs Random (Black)": expert_vs_random,
        "Random (White) vs Expert (Black)": random_vs_expert
    }
    
    for title, func in matchups.items():
        stats = run_experiments(func, 1000)
        print(f"=== {title} ===")
        print(f"Total Games: 1000")
        print(f"White Wins: {stats['1-0']} ({stats['1-0'] / 10:.2f}%)")
        print(f"Black Wins: {stats['0-1']} ({stats['0-1'] / 10:.2f}%)")
        print(f"Draws: {stats['1/2-1/2']} ({stats['1/2-1/2'] / 10:.2f}%)\n")

if __name__ == "__main__":
    main()
