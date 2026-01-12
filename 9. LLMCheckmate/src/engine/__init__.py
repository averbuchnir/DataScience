# src/engine/__init__.py
"""
Engine module for LLMCheckmate.
Provides a functional game state wrapper for chess.
Useful for LLM-based chess engines.

"""

from .game_state import (
    new_game,
    get_fen,
    get_legal_moves,
    shortlist_legal_moves,
    apply_move,
    is_game_over,
    result,
)
