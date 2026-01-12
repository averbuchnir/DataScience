import random
import time
import json
import os

from src.engine import (
    new_game,
    get_fen,
    get_legal_moves,
    apply_move,
    is_game_over,
    result,
)
from src.models import get_move_gpt, get_move_gemini
from src.FEN_to_Image import frame_to_gif,save_board_png

def get_move_model(state, side, model, legal_moves=None, move_history=None):
    if model == "gpt":
        return get_move_gpt(state, side, legal_moves, move_history)
    else:
        return get_move_gemini(state, side, legal_moves, move_history)


def main():
    state = new_game()
    print("=== LLMCheckmate: Engine Test ===")
    print("Initial FEN:")
    print(get_fen(state))
    print("Initial legal move count:", len(get_legal_moves(state)))
    print()

    ## Assign the model to colors
    white_model = random.choice(["gpt", "gemini"])
    black_model = "gemini" if white_model == "gpt" else "gpt"
    print(f"White: {white_model}, Black: {black_model}")

    game_log = []
    ply = 0 # number of plies
    max_plies = 100 # avoid infinite random games
    max_retries = 3 # number of retries for each move    
    while not is_game_over(state) and ply < max_plies:
        fen_before = get_fen(state)
        side_to_move = "white" if ply % 2 == 0 else "black"
        model = white_model if side_to_move == "white" else black_model

        legal_moves = get_legal_moves(state)

        uci = ""
        ok = False
        raw_move = ""
        for attempt in range(max_retries+1):
            legal_for_prompt = legal_moves  # always provide legal moves to help LLM

            raw_move = get_move_model(
                state=fen_before,
                side=side_to_move,
                model=model,
                legal_moves=legal_for_prompt,
                move_history=state["move_history"],
            )
            # get the first token of the response
            uci = (raw_move or "").strip().split()[0] if (raw_move or "").strip() else ""
            ok = apply_move(state, uci)
            if ok:
                break
            
            if attempt < max_retries:
                print(f"  Attempt {attempt + 1} failed: illegal move {uci}, retrying...")
            # add small delay to avoid rate limiting
            time.sleep(0.5)

        # After retry loop: log and print the result
        ply += 1
        fen_after = get_fen(state)
        # print(f"FEN after: {fen_after}")
        # save the board image
        save_board_png(fen_after, f"Log/board_{ply:03d}.png")
        # time.sleep(0.3)
        
        game_log.append(
            {
                "ply": ply,
                "side": side_to_move,
                "model": model,
                "uci": uci,
                "fen_before": fen_before,
                "fen_after": fen_after,
                "legal_moves": legal_moves,
                "raw_move": raw_move,
                "ok": ok,
            }
        )
        # current time for display "HH:MM:SS:MS"
        current_time_display = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        status = "OK" if ok else "ILLEGAL MOVE"
        print(f"{current_time_display} - {ply:03d}. {side_to_move} / {model} -> {uci} [{status}]")
        if not ok:
            print(f"ERROR: illegal move generated after {max_retries + 1} attempts: {uci}")
            break
        
    Winning_Model = white_model if result(state) == "1-0" else black_model
    print()
    print("Game over:", is_game_over(state))
    print("The Winning Model is:", Winning_Model)
    print("Result:", result(state))
    print("Total plies:", ply)
    print("Move history:")
    print(" ".join(state["move_history"]))
    print("Game log:")
    # export game log to JSON in Log directory
    os.makedirs("Log", exist_ok=True)
    # Create filename-safe timestamp (no colons, format: HHMMSS)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = f"Log/game_log_{timestamp}.json"
    with open(log_file, "w") as f:
        json.dump(game_log, f, indent=4)
    print(f"Game log exported to {log_file}")
    # generate a GIF animation from the board images
    frame_to_gif("Log", f"Log/game_{timestamp}.gif")



if __name__ == "__main__":
    main()