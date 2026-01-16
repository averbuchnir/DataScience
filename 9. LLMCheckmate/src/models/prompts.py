

# function for strict side naming "Black" or "White" (case insensitive)
def strict_side_name(side):
    side = (side or "").strip().lower()
    if side == "white":
        return "White"
    if side == "black":
        return "Black"
    raise ValueError("side must be 'white' or 'black'")


# prompt to choose strategies for playing the game
def build_strategy_prompt(fen,side,legal_moves,move_history):
    """
    build a prompt to choose strategies for playing the game
    fen: the current board position in FEN notation
    side: the side to move (white or black)
    legal_moves: the list of legal moves in UCI notation
    move_history: the list of move history in UCI notation
    return: a prompt to choose strategies for playing the game
    """
    prompt = (
        "You are a chess expert. You are given a board position and a list of legal moves. You need to choose a strategy to play the game."
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
        f"Legal moves (UCI) — choose ONE from this list:\n" + " ".join(legal_moves) + "\n"
        f"Move history (UCI): {move_history}\n"
        "Return the strategy you want to play the game."
        "The strategy should be one of the following: aggressive, defensive, balanced, random"
        "Output format should be in JSON format with the following keys: strategy, confidence, reason (short explanation)\n"
        "IMPORTANT OUTPUT RULES:\n"
        "- Output MUST be valid JSON\n"
        "- Output MUST contain ONLY the JSON object\n"
        "- Do NOT include any extra text\n"
        "- Do NOT use markdown or ```json\n\n"

        "Output format (JSON only):\n"
        '{"strategy":"<aggressive|defensive|balanced|random>","confidence":<number between 0 and 1>,"reason":"<short explanation>"}\n\n'

        "Example output:\n"
        '{"strategy":"aggressive","confidence":0.95,"reason":"The position favors active play and early initiative."}'
    )


    return prompt



def build_move_prompt(fen, side, legal_moves, move_history=None, strategy=None):
    """
    build a prompt to get move from GPT model,
    the model gets FEN,side, legal and strategy to play the game
    it should write a unique prompt for each strategy
    """
    # check if strategy is one of the following: aggressive, defensive, balanced, random (if not use balanced)
    if strategy not in ["aggressive", "defensive", "balanced", "random"]:
        strategy = "balanced"

    prompt = (
        "Return EXACTLY ONE move in UCI notation\n."
        "You are a chess expert. You are given a board position and a list of legal moves. You need to choose a strategy to play the game."
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
        f"Legal moves (UCI) — choose ONE from this list:\n" + " ".join(legal_moves) + "\n"
        f"Move history (UCI): {move_history}\n"
        f"Avoid Repeating the same move: Do NOT repeat the same move twice in a row"
        
    )
    if strategy == "aggressive":
        prompt += (
            "Play as aggressively as possible: prefer tactical, attacking and forcing moves, even if there is risk."
            "Avoid passive moves: Do NOT make passive king shuffles, retreats, or defensive moves unless absolutely necessary."
            "Control the center of the board: try to control the center of the board with your pieces."
            "Develop your pieces: try to develop your pieces to the center of the board."
            "Attack the enemy king: try to attack the enemy king with your pieces."
            "Checkmate the enemy: try to checkmate the enemy."
        )
    elif strategy == "defensive":
        prompt += (
            "Play as defensively as possible: avoid making mistakes and focus on defending your king."
            "Avoid attacking moves: Do NOT make attacking moves unless absolutely necessary."
            "Control the center of the board: try to control the center of the board with your pieces."
            "Develop your pieces: try to develop your pieces to the center of the board."
        )
    elif strategy == "balanced":
        prompt += (
            "Play as balanced as possible: try to control the center of the board with your pieces."
            "Develop your pieces: try to develop your pieces to the center of the board."
        )
    elif strategy == "random":
        prompt += (
            "Play as randomly as possible: choose a move randomly from the list of legal moves."
        )
    
    
    prompt += "\nLegal moves (UCI) — choose ONE from this list:\n" + " ".join(legal_moves) + "\n"
    # the output should be in JSON format with the following keys: move, confidence, reason (short explanation)
    prompt += ("IMPORTANT OUTPUT RULES:\n"
     "- Output MUST be valid JSON\n"
      "- Output MUST contain ONLY the JSON object\n"
      "- Do NOT include any extra text\n"
       "- Do NOT use markdown or ```json\n\n"
    "Output format (JSON only):\n"
    '{"move":"<UCI move>","confidence":<number between 0 and 1>,"reason":"<short explanation>"}\n\n'
    "Example output:\n"
    '{"move":"e2e4","confidence":0.95,"reason":"I think e2e4 is the best move for this board position as im using ' + (strategy or "balanced") + ' strategy"}'
    )
    
    
    # rompt += "Output format should be in JSON format with the following keys: move, confidence, reason (short explanation)"
    # prompt += "Example output:"
    # prompt += '{"move": "e2e4", "confidence": 0.95, "reason": "I think e2e4 is the best move for this board position"}'
    return prompt
    


# simple move prompt for the models 
def build_move_prompt_simple(fen, side, legal_moves, ascii_board=None):
    side = strict_side_name(side)
    prompt = (
        "Return EXACTLY ONE move in UCI notation\n."
        "No explanation, no Extra Text, Any other text is INVALID.\n"
        "PLAY AS AGGRESSIVELY AS POSSIBLE: prefer tactical, attacking and forcing moves, even if there is risk.\n"
        "AVOID PASSIVE MOVES: Do NOT make passive king shuffles, retreats, or defensive moves unless absolutely necessary.\n"
        f"Side to move: {side}\n"
        f"Current board position (FEN): {fen}\n"
    )
    if ascii_board:
        prompt += (f"\nBoard:\n{ascii_board}\n")

    prompt+= "\nLegal moves (UCI) — choose ONE from this list:\n" + " ".join(legal_moves) + "\n"
    prompt += ("IMPORTANT OUTPUT RULES:\n"
     "- Output MUST be valid JSON\n"
      "- Output MUST contain ONLY the JSON object\n"
      "- Do NOT include any extra text\n"
       "- Do NOT use markdown or\n\n"
    "Output format (JSON only):\n"
    '{"move":"<UCI move>","confidence":<number between 0 and 1>,"reason":"<short explanation>"}\n\n'
    "Example output:\n"
    '{"move":"e2e4","confidence":0.95,"reason":"I think e2e4 is the best move for this board position"}'
    )

    return prompt

