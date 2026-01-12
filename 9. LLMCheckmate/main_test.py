import random
from src.engine import (
    new_game,
    get_fen,
    get_legal_moves,
    apply_move,
    is_game_over,
    result,
)


def pick_random_legal_move(state):
    moves = get_legal_moves(state)
    return random.choice(moves) if moves else None


def main():
    state = new_game()

    print("=== LLMCheckmate: Engine Sanity Test ===")
    print("Initial FEN:")
    print(get_fen(state))
    print("Initial legal move count:", len(get_legal_moves(state)))
    print()

    ply = 0
    max_plies = 200  # avoid infinite random games

    while not is_game_over(state) and ply < max_plies:
        ply += 1

        move = pick_random_legal_move(state)
        if move is None:
            print("No legal moves found.")
            break

        ok = apply_move(state, move)
        if not ok:
            print("ERROR: illegal move generated:", move)
            break

        print(f"{ply:03d}. {move}")

    print()
    print("Game over:", is_game_over(state))
    print("Result:", result(state))
    print("Total plies:", ply)
    print("Move history:")
    print(" ".join(state["move_history"]))


if __name__ == "__main__":
    main()
