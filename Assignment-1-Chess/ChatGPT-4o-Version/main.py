import chess
import chess.engine
import random
import concurrent.futures

NUM_GAMES = 1000  # Number of games to simulate
MINIMAX_DEPTH = 2  # Depth for the minimax algorithm

def random_move(board):
    """Returns a random legal move."""
    return random.choice(list(board.legal_moves))

def minimax(board, depth, is_maximizing):
    """Simple Minimax algorithm with basic material evaluation."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def evaluate_board(board):
    """Basic evaluation function based on material count."""
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}
    score = 0
    for piece, value in piece_values.items():
        score += len(board.pieces(piece, chess.WHITE)) * value
        score -= len(board.pieces(piece, chess.BLACK)) * value
    return score

def play_game(player_white, player_black):
    """Simulates a single chess game."""
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = player_white(board)
        else:
            move = player_black(board)
        board.push(move)
    result = board.result()
    return result

def simulate_games(player_white, player_black, num_games):
    """Simulates multiple games and returns the win rate."""
    results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(play_game, player_white, player_black) for _ in range(num_games)]
        for future in concurrent.futures.as_completed(futures):
            results[future.result()] += 1

    win_rate_white = results["1-0"] / num_games * 100
    win_rate_black = results["0-1"] / num_games * 100
    draw_rate = results["1/2-1/2"] / num_games * 100

    return win_rate_white, win_rate_black, draw_rate

# Run simulations for different cases
print("Simulating Random vs Random...")
win_white, win_black, draw = simulate_games(random_move, random_move, NUM_GAMES)
print(f"Random vs Random - White Win Rate: {win_white:.2f}%, Black Win Rate: {win_black:.2f}%, Draw Rate: {draw:.2f}%\n")

print("Simulating Expert (White) vs Random...")
win_white, win_black, draw = simulate_games(lambda b: minimax(b, MINIMAX_DEPTH, True)[1], random_move, NUM_GAMES)
print(f"Expert (White) vs Random - White Win Rate: {win_white:.2f}%, Black Win Rate: {win_black:.2f}%, Draw Rate: {draw:.2f}%\n")

print("Simulating Random vs Expert (Black)...")
win_white, win_black, draw = simulate_games(random_move, lambda b: minimax(b, MINIMAX_DEPTH, False)[1], NUM_GAMES)
print(f"Random vs Expert (Black) - White Win Rate: {win_white:.2f}%, Black Win Rate: {win_black:.2f}%, Draw Rate: {draw:.2f}%")
