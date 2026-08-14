VALID_STRATEGIES = ("aggressive", "defensive", "balanced", "random")


def strict_side_name(side):
    """Return the canonical chess side name."""
    side = (side or "").strip().lower()
    if side == "white":
        return "White"
    if side == "black":
        return "Black"
    raise ValueError("side must be 'white' or 'black'")


def _format_moves(moves, empty_text):
    if not moves:
        return empty_text
    if isinstance(moves, str):
        return moves.strip() or empty_text
    return " ".join(str(move).strip() for move in moves if str(move).strip()) or empty_text


def build_strategy_prompt(fen, side, legal_moves, move_history):
    """Build the legacy strategy-only prompt retained for compatibility."""
    side = strict_side_name(side)
    legal_text = _format_moves(legal_moves, "(none)")
    history_text = _format_moves(move_history, "(none; this is the first move)")
    return (
        "You are a chess expert selecting a strategy for the current position.\n"
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
        f"Recent moves, oldest to newest (UCI): {history_text}\n"
        f"Legal moves (UCI): {legal_text}\n"
        "Choose one strategy: aggressive, defensive, balanced, or random.\n"
        "Return only a JSON object with this shape:\n"
        '{"strategy":"<aggressive|defensive|balanced|random>",'
        '"confidence":<number from 0 to 1>,"reason":"<short explanation>"}'
    )


def build_move_prompt(fen, side, legal_moves, move_history=None, strategy=None):
    """Build a compact, history-aware prompt for one legal chess move."""
    side = strict_side_name(side)
    legal_text = _format_moves(legal_moves, "(none)")
    history_text = _format_moves(move_history, "(none; this is the first move)")
    normalized_strategy = strategy.strip().lower() if isinstance(strategy, str) else ""

    if normalized_strategy in VALID_STRATEGIES:
        strategy_instruction = f'Use the "{normalized_strategy}" strategy.'
    else:
        strategy_instruction = (
            "Choose the most appropriate strategy: aggressive, defensive, balanced, or random."
        )

    return (
        "You are a chess expert choosing one move. Play sound chess and convert a winning "
        "advantage efficiently.\n"
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
        f"Recent moves, oldest to newest (UCI): {history_text}\n"
        f"{strategy_instruction}\n"
        "Choose exactly one move from the following allowed legal moves. Do not invent a move.\n"
        f"Allowed legal moves (UCI): {legal_text}\n"
        "Return only a JSON object with this shape:\n"
        '{"move":"<one allowed UCI move>","confidence":<number from 0 to 1>,'
        '"reason":"<short explanation>",'
        '"strategy":"<aggressive|defensive|balanced|random>"}'
    )


def build_move_prompt_simple(fen, side, legal_moves, ascii_board=None, strategy=None):
    """Build the legacy simple prompt, using the same response contract."""
    prompt = build_move_prompt(
        fen=fen,
        side=side,
        legal_moves=legal_moves,
        move_history=None,
        strategy=strategy,
    )
    if not ascii_board:
        return prompt

    board_section = f"Board:\n{ascii_board}\n"
    return prompt.replace("Return only a JSON object", board_section + "Return only a JSON object", 1)
