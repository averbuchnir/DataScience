# function for strict side naming "Black" or "White" (case insensitive)
def strict_side_name(side):
    side = (side or "").strip().lower()
    if side == "white":
        return "White"
    if side == "black":
        return "Black"
    raise ValueError("side must be 'white' or 'black'")

def build_move_prompt(fen, side, legal_moves, ascii_board=None):
    side = strict_side_name(side)
    prompt = (
        "Return EXACTLY ONE move in UCI notation\n."
        "No explanation, no Extra Text, Any other text is INVALID.\n"
        "PLAY AS AGGRESSIVELY AS POSSIBLE: prefer tactical, attacking and forcing moves, even if there is risk.\n"
        "1. CHECKMATE (if available)\n"
        "2. CHECK (threaten the king)\n"
        "3. CAPTURE (take enemy pieces, especially valuable ones)\n"
        "4. PROMOTION (advance pawns to promote)\n"
        "5. ATTACK (create threats, fork, pin, skewer)\n"
        "6. DEVELOPMENT (activate pieces, control center)\n"
        "7. ADVANCE (move pieces forward, not backward)\n"
        "AVOID PASSIVE MOVES: Do NOT make passive king shuffles, retreats, or defensive moves unless absolutely necessary.\n"
        "Prefer moves that progress the game toward checkmate rather than maintaining position.\n"
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
    )
    if ascii_board:
        prompt += (f"\nBoard:\n{ascii_board}\n")
    prompt+= "\nLegal moves (UCI) — choose ONE from this list:\n" + " ".join(legal_moves) + "\n"
    return prompt


# prompt for model to perfrom movment
# def build_move_prompt(fen, side, legal_moves=None, move_history=None):
#     """
#     Build a strict prompt that asks for ONE UCI move only.
#     legal_moves: optional list[str] of UCI moves
#     move_history: optional list[str] of previous UCI moves in the game
#     """
#     side = strict_side_name(side)

#     prompt = (
#         f"You are playing chess as {side}.\n"
#         f"Current board position (FEN): {fen}\n"
#     )

#     if move_history:
#         prompt += (
#             "Previous moves in this game (UCI notation):\n"
#             + " ".join(move_history)
#             + "\n\n"
#         )

#     prompt += (
#         "Task: Choose ONE legal move.\n\n"
#         "Output rules:\n"
#         "- Return ONLY ONE move in UCI notation.\n"
#         "- No explanation.\n"
#         "- No commentary.\n"
#         "- No additional text.\n\n"
#         "Valid output examples (choose ONE, do not copy multiple):\n"
#         "e2e4\n"
#         "g8f6\n"
#         "e1g1\n"
#         "g7g8q\n"
#     )

#     if legal_moves:
#         prompt += (
#             "\nLegal moves (UCI) — choose ONE from this list:\n"
#             + " ".join(legal_moves)
#             + "\n"
#         )

#     return prompt
# 