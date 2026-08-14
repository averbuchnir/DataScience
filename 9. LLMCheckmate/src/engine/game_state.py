"""Functional helpers for managing an LLMCheckmate chess game."""

import random

import chess


_DEFAULT_QUIET_MOVE_SEED = 0


def new_game():
    """Create and return a new game state as a plain dictionary."""
    return {
        "board": chess.Board(),
        "move_history": [],
    }


def get_fen(state):
    """Return the current FEN."""
    return state["board"].fen()


def get_legal_moves(state):
    """Return all legal moves in UCI format."""
    board = state["board"]
    return [move.uci() for move in board.legal_moves]


def shortlist_legal_moves(
    board: chess.Board,
    quiet_k: int = 8,
    seed: int | None = None,
) -> list[str]:
    """Return a deterministic shortlist that retains every tactical move.

    The shortlist includes all checking moves, captures (including en passant),
    and promotions, followed by up to ``quiet_k`` quiet moves. Promotions use a
    dedicated bucket, so checking or capturing promotions are included once.

    Quiet moves are sampled with a local random-number generator. Omitting
    ``seed`` uses a fixed seed, so identical positions produce identical
    shortlists without reading or modifying Python's global random state.

    Raises:
        TypeError: If ``quiet_k`` is not an integer.
        ValueError: If ``quiet_k`` is negative.
    """
    if isinstance(quiet_k, bool) or not isinstance(quiet_k, int):
        raise TypeError("quiet_k must be an integer")
    if quiet_k < 0:
        raise ValueError("quiet_k must be non-negative")

    effective_seed = _DEFAULT_QUIET_MOVE_SEED if seed is None else seed
    rng = random.Random(effective_seed)

    checking_moves: list[str] = []
    capture_moves: list[str] = []
    promotion_moves: list[str] = []
    quiet_moves: list[str] = []

    for move in board.legal_moves:
        move_uci = move.uci()

        # Keep promotions in one bucket so capture promotions are not duplicated.
        if move.promotion is not None:
            promotion_moves.append(move_uci)
        elif board.gives_check(move):
            checking_moves.append(move_uci)
        elif board.is_capture(move):
            capture_moves.append(move_uci)
        else:
            quiet_moves.append(move_uci)

    # The mutually exclusive buckets make duplicates unlikely; ``seen`` also
    # protects the public contract if classification changes later.
    seen: set[str] = set()
    ordered: list[str] = []
    for group in (checking_moves, capture_moves, promotion_moves):
        for move_uci in group:
            if move_uci not in seen:
                seen.add(move_uci)
                ordered.append(move_uci)

    if quiet_k > 0 and quiet_moves:
        for move_uci in rng.sample(quiet_moves, min(quiet_k, len(quiet_moves))):
            if move_uci not in seen:
                seen.add(move_uci)
                ordered.append(move_uci)

    return ordered


def apply_move(state, uci):
    """Apply one complete legal UCI move without mutating state on failure."""
    board = state["board"]

    if not isinstance(uci, str):
        return False

    uci_str = uci.strip()
    if not uci_str:
        return False

    try:
        move = chess.Move.from_uci(uci_str)
    except ValueError:
        return False

    if not board.is_legal(move):
        return False

    board.push(move)
    state["move_history"].append(uci_str)
    return True


def is_game_over(state):
    """Return whether the game ended without requiring a player draw claim.

    With ``claim_draw=False``, python-chess includes automatic endings such as
    checkmate, stalemate, insufficient material, fivefold repetition, and the
    75-move rule. Claimable threefold repetition and the 50-move rule alone do
    not end the tournament game.
    """
    return state["board"].is_game_over(claim_draw=False)


def result(state):
    """Return the result without requiring a player draw claim."""
    return state["board"].result(claim_draw=False)
