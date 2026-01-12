# src/engine/game_state.py

import chess
import random

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