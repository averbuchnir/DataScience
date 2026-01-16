import random
import time
import json
import os
from datetime import datetime

from src.engine import (
    new_game,
    get_fen,
    get_legal_moves,
    shortlist_legal_moves,
    apply_move,
    is_game_over,
    result,
)
from src.models import get_move_gpt, get_move_gemini, get_model_names, get_tier_keys
from src.FEN_to_Image import frame_to_gif,save_board_png
from src.utils import get_current_time_display

def get_move_model(tier,state, side, model, legal_moves=None, move_history=None,model_name=None):
    if model == "gpt":
        return get_move_gpt(tier,state, side, legal_moves, move_history, model_name)
    else:
        return get_move_gemini(tier,state, side, legal_moves, move_history, model_name)


def main():
    for tier in get_tier_keys()[::-1]: # reverse the tier keys to start with the highest tier
        print(f"{get_current_time_display()} - Tier: {tier}")
        tier_gpt_model = get_model_names(tier)["gpt"]
        tier_gemini_model = get_model_names(tier)["gemini"]
        print(f"{get_current_time_display()} - === performing tournament for {tier} tier ===")
        print(f"{get_current_time_display()} - === {tier_gpt_model} Vs {tier_gemini_model} ===")
    
        number_of_games = 3  # Number of games to play in each tier
        print(f"{get_current_time_display()} - === LLMCheckmate: Multiple Games Tournament ===")
        print(f"{get_current_time_display()} - Playing {number_of_games} games...")
        print(f"{get_current_time_display()} - ")
        
        # Track wins for each model
        wins = {"gpt": 0, "gemini": 0, "draw": 0}
        
        for game_num in range(1, number_of_games + 1):
            print(f"{get_current_time_display()} - \n{'='*60}")
            print(f"{get_current_time_display()} - GAME {game_num}/{number_of_games}")
            print(f"{get_current_time_display()} - {'='*60}")
            
            state = new_game()
            print(f"{get_current_time_display()} - Initial FEN:")
            print(f"{get_current_time_display()} - {get_fen(state)}")
            print(f"{get_current_time_display()} - Initial legal move count: {len(get_legal_moves(state))}")
            print(f"{get_current_time_display()} - ")

            ## Assign the model to colors
            white_model = random.choice(["gpt", "gemini"])
            black_model = "gemini" if white_model == "gpt" else "gpt"
            print(f"{get_current_time_display()} - White: {white_model}, Black: {black_model}\n")

            # Generate timestamp for this game (used consistently across all files)
            game_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create folder for this game with timestamp to prevent overwriting
            # Use underscores instead of parentheses for better cross-platform compatibility
            game_folder = os.path.join("Log", tier, f"game_{game_num:03d}_White-{white_model}")
            os.makedirs(game_folder, exist_ok=True)

            game_log = {
                "tier": tier,
                "game_number": game_num,
                "white_model": white_model,
                "black_model": black_model,
                "white_model_name": tier_gpt_model if white_model == "gpt" else tier_gemini_model,
                "black_model_name": tier_gpt_model if black_model == "gpt" else tier_gemini_model,
                "initial_fen": get_fen(state),
                "moves": [],
                "result": None,
                "winning_model": None,
                "total_plies": 0,
                "game_start_time": datetime.now().isoformat()
            }
            board_positions = []
            ply = 0 # number of plies
            max_plies = 100 # avoid infinite random games
            max_retries = 3 # number of retries for each move
            illegal_move_failure, failed_side = False, None # Tracking varaible for illegal move failure
            while not is_game_over(state) and ply < max_plies:
                fen_before = get_fen(state)
                side_to_move = "white" if ply % 2 == 0 else "black"
                model = white_model if side_to_move == "white" else black_model
                model_name = tier_gpt_model if model == "gpt" else tier_gemini_model

                legal_moves = get_legal_moves(state)
                legal_moves_shortlist = shortlist_legal_moves(state["board"], quiet_k=8)
                # print the delta of legal moves between shortlist and all legal moves 
                print(f"{get_current_time_display()} - {ply+1:03d}. {side_to_move} / {model} -> Reasoning before making a move...")
                print(f"{get_current_time_display()} - {ply+1:03d}. {side_to_move} / {model} -> legal_moves: {len(legal_moves)} | legal_moves_shortlist: {len(legal_moves_shortlist)} | Delta: {len(legal_moves) - len(legal_moves_shortlist)}")
        
                uci = ""
                ok = False
                # raw_reponse = ""
                num_attempts = 0
                for attempt in range(max_retries+1):
                    num_attempts = attempt + 1
                    legal_for_prompt = legal_moves_shortlist  # use shortlist instead of all legal moves
                    
                    recent_moves = state["move_history"][-6:] if state["move_history"] else None  # last 3 full moves (6 plies)
                    start_time_reasoning = time.time()
                    strategy_response = get_move_model(
                        tier=tier, # tier of the model
                        state=fen_before, # current FEN position
                        side=side_to_move, # side to move
                        model=model, # model to use
                        legal_moves=legal_for_prompt, # legal moves shortlist/all legal moves
                        move_history=recent_moves, # recent moves for context
                        model_name=model_name, # model name
                    )
                    # get move, confidence, reason, strategy
                    end_time_reasoning = time.time()
                    model_move, model_confidence, model_reason, model_strategy = strategy_response 

                    print(f"{get_current_time_display()} - {model}-Move: {model_move}")
                    print(f"{get_current_time_display()} - {model}-Confidence: {model_confidence}")
                    print(f"{get_current_time_display()} - {model}-Reason: {model_reason}")
                    print(f"{get_current_time_display()} - {model}-Strategy: {model_strategy}")
                    reasoning_time_minutes = (end_time_reasoning - start_time_reasoning) / 60
                    print(f"{get_current_time_display()} - {model}-Reasoning Time: {reasoning_time_minutes:.2f} minutes ({end_time_reasoning - start_time_reasoning:.2f} seconds)")
                    # get the first token of the response
                    uci = (model_move or "").strip().split()[0] if (model_move or "").strip() else ""
                    ok = apply_move(state, uci)
                    if ok:
                        break
                    
                    # a = input("From main.py: Press Enter to continue...")
                    if attempt < max_retries:
                        print(f"{get_current_time_display()} -   Attempt {attempt + 1} failed: illegal move {uci}, retrying...")
                    # add small delay to avoid rate limiting
                    # time.sleep(0.5)

                # After retry loop: log and print the result
                ply += 1
                fen_after = get_fen(state)
                # store the board position with ply number
                board_positions.append((ply, fen_after))
                # print(f"FEN after: {fen_after}")
                
       
                # time.sleep(0.3)
                
                status = "OK" if ok else "ILLEGAL MOVE"
                print(f"{get_current_time_display()} - {ply:03d}. {side_to_move} / {model} Played -> {uci} [{status}]")
                print(f"{get_current_time_display()} - ----------------------------------------------------------")
                # save the board position with ply number
                board_image_path = os.path.join(game_folder, f"board_{ply:03d}.png")
                save_board_png(fen_after, board_image_path)
            
                # Add move information to game_log
                move_info = {
                    "ply": ply,
                    "side": side_to_move,
                    "model": model,
                    "model_name": model_name,
                    "fen_before": fen_before,
                    "fen_after": fen_after,
                    "delta_legal_moves": len(legal_moves) - len(legal_moves_shortlist),
                    "uci": uci,
                    "raw_move": model_move,
                    "strategy": model_strategy,
                    "confidence": model_confidence,
                    "reason": model_reason,
                    "legal": ok,
                    "status": status,
                    "timestamp": get_current_time_display(),
                    "legal_moves_count": len(legal_moves),
                    "attempts": num_attempts,
                    "model_reasoning_time": end_time_reasoning - start_time_reasoning
                }
                game_log["moves"].append(move_info)
                
                if not ok:
                    illegal_move_failure = True
                    failed_side = side_to_move
                    print(f"{get_current_time_display()} - ERROR: illegal move generated after {max_retries + 1} attempts: {uci}")
                    break
 
            
            # Save all board images AFTER the game is complete
            print(f"{get_current_time_display()} - Saving {len(board_positions)} board images...")
            for ply, fen_after in board_positions:
                board_image_path = os.path.join(game_folder, f"board_{ply:03d}.png")
                save_board_png(fen_after, board_image_path)
                
            # Determine winner
            game_result = result(state)
            if illegal_move_failure:
                # the OPPONENT WINS due to illegal move failure
                if failed_side == "white":
                    game_result = "0-1"
                    winning_model = black_model
                else:
                    game_result = "1-0"
                    winning_model = white_model
                wins[winning_model] += 1
            else:
                if game_result == "1-0":
                    winning_model = white_model
                    wins[white_model] += 1
                elif game_result == "0-1":
                    winning_model = black_model
                    wins[black_model] += 1
                else:
                    winning_model = "draw"
                    wins["draw"] += 1
            
            # Update game_log with final results
            game_log["result"] = game_result
            game_log["winning_model"] = winning_model
            game_log["total_plies"] = ply
            game_log["game_over"] = is_game_over(state)
            game_log["final_fen"] = get_fen(state)
            game_log["game_end_time"] = datetime.now().isoformat()
            
            print(f"{get_current_time_display()} - ")
            print(f"{get_current_time_display()} - Game over: {is_game_over(state)}")
            print(f"{get_current_time_display()} - The Winning Model is: {winning_model}")
            print(f"{get_current_time_display()} - Result: {game_result}")
            print(f"{get_current_time_display()} - Total plies: {ply}")
            print(f"{get_current_time_display()} - Move history:")
            # print(" ".join(state["move_history"]))
            
            # export game log to JSON in game-specific folder
            log_file = os.path.join(game_folder, f"game_log_{game_timestamp}.json")
            with open(log_file, "w") as f:
                json.dump(game_log, f, indent=4)
            print(f"{get_current_time_display()} - Game log exported to {log_file}")
            
            # generate a GIF animation from the board images in the game folder
            gif_file = os.path.join(game_folder, f"game_{game_num:03d}_White-{white_model}.gif")
            frame_to_gif(game_folder, gif_file)
        
        # Print tournament summary
        print(f"{get_current_time_display()} - ")
        print(f"{get_current_time_display()} - \n{'='*60}")
        print(f"{get_current_time_display()} - TOURNAMENT SUMMARY")
        print(f"{get_current_time_display()} - {'='*60}")
        print(f"{get_current_time_display()} - Total games played: {number_of_games}")
        print(f"{get_current_time_display()} - GPT wins: {wins['gpt']}")
        print(f"{get_current_time_display()} - Gemini wins: {wins['gemini']}")
        print(f"{get_current_time_display()} - Draws: {wins['draw']}")
        print(f"{get_current_time_display()} - ")
        
        if wins['gpt'] > wins['gemini']:
            print(f"{get_current_time_display()} - 🏆 GPT is the overall winner with {wins['gpt']} wins!")
        elif wins['gemini'] > wins['gpt']:
            print(f"{get_current_time_display()} - 🏆 Gemini is the overall winner with {wins['gemini']} wins!")
        else:
            print(f"{get_current_time_display()} - 🤝 It's a tie!")



if __name__ == "__main__":
    main()