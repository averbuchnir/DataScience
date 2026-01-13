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

def get_move_model(tier,state, side, model, legal_moves=None, move_history=None,model_name=None):
    if model == "gpt":
        return get_move_gpt(tier,state, side, legal_moves, move_history, model_name)
    else:
        return get_move_gemini(tier,state, side, legal_moves, move_history, model_name)




def main():
    for tier in get_tier_keys():
        print(f"Tier: {tier}")
        tier_gpt_model = get_model_names(tier)["gpt"]
        tier_gemini_model = get_model_names(tier)["gemini"]
        print(f"=== performing tournament for {tier} tier ===")
        print("=== {} Vs {} ===".format(tier_gpt_model, tier_gemini_model))
    
        number_of_games = 1  # Number of games to play in each tier
        print("=== LLMCheckmate: Multiple Games Tournament ===")
        print(f"Playing {number_of_games} games...")
        print()
        
        # Track wins for each model
        wins = {"gpt": 0, "gemini": 0, "draw": 0}
        
        for game_num in range(1, number_of_games + 1):
            print(f"\n{'='*60}")
            print(f"GAME {game_num}/{number_of_games}")
            print(f"{'='*60}")
            
            state = new_game()
            print("Initial FEN:")
            print(get_fen(state))
            print("Initial legal move count:", len(get_legal_moves(state)))
            print()

            ## Assign the model to colors
            white_model = random.choice(["gpt", "gemini"])
            black_model = "gemini" if white_model == "gpt" else "gpt"
            print(f"White: {white_model}, Black: {black_model}")

            # Create folder for this game
            game_folder = f"Log/{tier}/game_{game_num:03d}(White={white_model})"
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
            while not is_game_over(state) and ply < max_plies:
                fen_before = get_fen(state)
                side_to_move = "white" if ply % 2 == 0 else "black"
                model = white_model if side_to_move == "white" else black_model
                model_name = tier_gpt_model if model == "gpt" else tier_gemini_model

                legal_moves = get_legal_moves(state)
                legal_moves_shortlist = shortlist_legal_moves(state["board"], quiet_k=8)
                # print the delta of legal moves between shortlist and all legal moves 
                print(f"legal_moves: {len(legal_moves)} | legal_moves_shortlist: {len(legal_moves_shortlist)} | Delta: {len(legal_moves) - len(legal_moves_shortlist)}")
            
                uci = ""
                ok = False
                raw_move = ""
                num_attempts = 0
                for attempt in range(max_retries+1):
                    num_attempts = attempt + 1
                    legal_for_prompt = legal_moves_shortlist  # use shortlist instead of all legal moves
                    
                    recent_moves = state["move_history"][-6:] if state["move_history"] else None  # last 3 full moves (6 plies)

                    raw_move = get_move_model(
                        tier=tier,
                        state=fen_before,
                        side=side_to_move,
                        model=model,
                        legal_moves=legal_moves,
                        # move_history=state["move_history"],
                        move_history=recent_moves 
                        model_name=model_name,
                    )
                    # get the first token of the response
                    uci = (raw_move or "").strip().split()[0] if (raw_move or "").strip() else ""
                    ok = apply_move(state, uci)
                    if ok:
                        break
                    
                    if attempt < max_retries:
                        print(f"  Attempt {attempt + 1} failed: illegal move {uci}, retrying...")
                    # add small delay to avoid rate limiting
                    # time.sleep(0.5)

                # After retry loop: log and print the result
                ply += 1
                fen_after = get_fen(state)
                # store the board position with ply number
                board_positions.append((ply, fen_after))
                # print(f"FEN after: {fen_after}")
       
                # time.sleep(0.3)
                
                # current time for display "HH:MM:SS:MS"
                current_time_display = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                status = "OK" if ok else "ILLEGAL MOVE"
                print(f"{current_time_display} - {ply:03d}. {side_to_move} / {model} -> {uci} [{status}]")
                
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
                    "raw_move": raw_move,
                    "legal": ok,
                    "status": status,
                    "timestamp": current_time_display,
                    "legal_moves_count": len(legal_moves),
                    "attempts": num_attempts
                }
                game_log["moves"].append(move_info)
                
                if not ok:
                    print(f"ERROR: illegal move generated after {max_retries + 1} attempts: {uci}")
                    break
            
            # Save all board images AFTER the game is complete
            print(f"Saving {len(board_positions)} board images...")
            for ply, fen_after in board_positions:
                save_board_png(fen_after, f"{game_folder}/board_{ply:03d}.png")
                
            # Determine winner
            game_result = result(state)
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
            
            print()
            print("Game over:", is_game_over(state))
            print("The Winning Model is:", winning_model)
            print("Result:", game_result)
            print("Total plies:", ply)
            print("Move history:")
            # print(" ".join(state["move_history"]))
            
            # export game log to JSON in game-specific folder
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            log_file = f"{game_folder}/game_log_{timestamp}.json"
            with open(log_file, "w") as f:
                json.dump(game_log, f, indent=4)
            print(f"Game log exported to {log_file}")
            
            # generate a GIF animation from the board images in the game folder
            frame_to_gif(game_folder, f"{game_folder}/game_{timestamp}.gif")
        
        # Print tournament summary
        print()
        print(f"\n{'='*60}")
        print("TOURNAMENT SUMMARY")
        print(f"{'='*60}")
        print(f"Total games played: {number_of_games}")
        print(f"GPT wins: {wins['gpt']}")
        print(f"Gemini wins: {wins['gemini']}")
        print(f"Draws: {wins['draw']}")
        print()
        
        if wins['gpt'] > wins['gemini']:
            print(f"🏆 GPT is the overall winner with {wins['gpt']} wins!")
        elif wins['gemini'] > wins['gpt']:
            print(f"🏆 Gemini is the overall winner with {wins['gemini']} wins!")
        else:
            print("🤝 It's a tie!")



if __name__ == "__main__":
    main()