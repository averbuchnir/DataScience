# src/engine/game_state.py

def new_game():
    """
    Create and return a new game state.
    State is a plain dict.
    """
    return {
        "board": chess.Board(),
        "move_history": []
    }

  

def get_fen(state):
    """Return the current FEN."""
    return state["board"].fen()



def get_legal_moves(state):
    """
    Return all legal moves in UCI format.
    Example: ['e2e4', 'g8f6']
    """
    board = state["board"]
    return [m.uci() for m in board.legal_moves]


import random
import chess

def shortlist_legal_moves(board: chess.Board, quiet_k: int = 8, seed: int | None = None) -> list[str]:
    """
    Return a shortlist of legal moves prioritizing tactical moves.

    Includes:
    - All checking moves
    - All captures (including en passant)
    - All promotions (including capture promotions)
    - + K quiet moves (randomly sampled)

    Returns:
        list[str] of UCI moves
    """
    rng = random.Random(seed) if seed is not None else random

    checking_moves: list[str] = []
    capture_moves: list[str] = []
    promotion_moves: list[str] = []
    quiet_moves: list[str] = []

    for move in board.legal_moves:
        move_uci = move.uci()

        # Promotions first (promotion captures should be treated as promotions)
        if move.promotion is not None:
            promotion_moves.append(move_uci)
            continue

        # Checks
        if board.gives_check(move):
            checking_moves.append(move_uci)
            continue

        # Captures (includes en passant)
        if board.is_capture(move):
            capture_moves.append(move_uci)
            continue

        # Quiet
        quiet_moves.append(move_uci)

    # Deduplicate while preserving priority order
    seen: set[str] = set()
    ordered: list[str] = []
    for group in (checking_moves, capture_moves, promotion_moves):
        for mv in group:
            if mv not in seen:
                seen.add(mv)
                ordered.append(mv)

    # Add K quiet moves (random sample)
    if quiet_k > 0 and quiet_moves:
        k = min(quiet_k, len(quiet_moves))
        for mv in rng.sample(quiet_moves, k):
            if mv not in seen:
                seen.add(mv)
                ordered.append(mv)

    return ordered



def apply_move(state, uci):
    """
    Apply a UCI move to the board.
    Returns True if applied, False if illegal or invalid.
    """
    board = state["board"]

    # Safely extract first token, handling empty strings
    uci_str = (uci or "").strip()
    if not uci_str:
        return False
    
    split_result = uci_str.split()
    if not split_result:
        return False
    
    uci = split_result[0]

    try:
        move = chess.Move.from_uci(uci)
    except ValueError:
        return False

    if move not in board.legal_moves:
        return False

    board.push(move)
    state["move_history"].append(uci)
    return True

def is_game_over(state):
    """
    Return True if the game is finished.
    Includes checkmate, stalemate, repetition, 50-move rule, insufficient material.
    """
    return state["board"].is_game_over(claim_draw=True)


def result(state):
    """
    Return game result:
    '1-0', '0-1', '1/2-1/2', or '*'
    """
    return state["board"].result(claim_draw=True)