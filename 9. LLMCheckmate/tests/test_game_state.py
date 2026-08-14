import random
import unittest

import chess

from src.engine import (
    apply_move,
    get_fen,
    get_legal_moves,
    is_game_over,
    new_game,
    result,
    shortlist_legal_moves,
)


def state_from_fen(fen):
    return {
        "board": chess.Board(fen),
        "move_history": [],
    }


class GameStateTests(unittest.TestCase):
    def test_new_games_have_independent_initial_state(self):
        first = new_game()
        second = new_game()

        self.assertEqual(chess.STARTING_FEN, get_fen(first))
        self.assertEqual(chess.STARTING_FEN, get_fen(second))
        self.assertEqual([], first["move_history"])
        self.assertEqual([], second["move_history"])

        self.assertTrue(apply_move(first, "e2e4"))
        self.assertNotEqual(get_fen(first), get_fen(second))
        self.assertEqual([], second["move_history"])

    def test_initial_legal_moves_are_returned_as_uci(self):
        legal_moves = get_legal_moves(new_game())

        self.assertEqual(20, len(legal_moves))
        self.assertEqual(len(legal_moves), len(set(legal_moves)))
        self.assertIn("e2e4", legal_moves)
        self.assertTrue(all(isinstance(move, str) for move in legal_moves))

    def test_apply_move_updates_board_and_normalized_history(self):
        state = new_game()

        self.assertTrue(apply_move(state, "  e2e4\n"))

        self.assertEqual(["e2e4"], state["move_history"])
        self.assertEqual(chess.BLACK, state["board"].turn)
        self.assertEqual(chess.PAWN, state["board"].piece_type_at(chess.E4))
        self.assertIsNone(state["board"].piece_at(chess.E2))

    def test_apply_move_rejects_invalid_input_without_mutation(self):
        invalid_moves = (
            None,
            "",
            "   ",
            "not-a-move",
            "e2e5",
            "e7e5",
            "e2e4 extra-text",
            123,
        )

        for invalid_move in invalid_moves:
            with self.subTest(invalid_move=invalid_move):
                state = new_game()
                fen_before = get_fen(state)

                self.assertFalse(apply_move(state, invalid_move))
                self.assertEqual(fen_before, get_fen(state))
                self.assertEqual([], state["move_history"])
                self.assertEqual([], state["board"].move_stack)

    def test_apply_move_supports_castling(self):
        state = state_from_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        self.assertTrue(apply_move(state, "e1g1"))

        self.assertEqual(chess.KING, state["board"].piece_type_at(chess.G1))
        self.assertEqual(chess.ROOK, state["board"].piece_type_at(chess.F1))
        self.assertEqual(["e1g1"], state["move_history"])

    def test_apply_move_supports_en_passant(self):
        state = state_from_fen("8/8/8/3pP3/8/8/8/4K2k w - d6 0 1")

        self.assertTrue(apply_move(state, "e5d6"))

        self.assertEqual(chess.PAWN, state["board"].piece_type_at(chess.D6))
        self.assertIsNone(state["board"].piece_at(chess.D5))
        self.assertEqual(["e5d6"], state["move_history"])

    def test_apply_move_supports_promotion(self):
        state = state_from_fen("7k/P7/8/8/8/8/8/7K w - - 0 1")

        self.assertTrue(apply_move(state, "a7a8q"))

        self.assertEqual(chess.QUEEN, state["board"].piece_type_at(chess.A8))
        self.assertEqual(["a7a8q"], state["move_history"])


class ShortlistTests(unittest.TestCase):
    @staticmethod
    def tactical_moves(board):
        return {
            move.uci()
            for move in board.legal_moves
            if move.promotion is not None
            or board.gives_check(move)
            or board.is_capture(move)
        }

    @staticmethod
    def quiet_moves(board):
        return {
            move.uci()
            for move in board.legal_moves
            if move.promotion is None
            and not board.gives_check(move)
            and not board.is_capture(move)
        }

    def test_default_shortlist_is_repeatable_and_does_not_use_global_rng(self):
        board = chess.Board()
        fen_before = board.fen()
        move_stack_before = list(board.move_stack)

        random.seed(1729)
        expected_next_random = random.random()
        random.seed(1729)
        first = shortlist_legal_moves(board, quiet_k=8)
        actual_next_random = random.random()
        second = shortlist_legal_moves(board, quiet_k=8)

        self.assertEqual(first, second)
        self.assertEqual(first, shortlist_legal_moves(board, quiet_k=8, seed=0))
        self.assertEqual(expected_next_random, actual_next_random)
        self.assertEqual(8, len(first))
        self.assertEqual(len(first), len(set(first)))
        self.assertTrue(set(first).issubset(set(get_legal_moves({"board": board}))))
        self.assertEqual(fen_before, board.fen())
        self.assertEqual(move_stack_before, board.move_stack)

    def test_explicit_seed_is_repeatable(self):
        board = chess.Board()

        first = shortlist_legal_moves(board, quiet_k=8, seed=23)
        second = shortlist_legal_moves(board, quiet_k=8, seed=23)

        self.assertEqual(first, second)

    def test_shortlist_includes_all_tactical_moves_before_quiet_moves(self):
        tactical_positions = (
            "4k3/8/8/8/3r4/8/3Q4/4K3 w - - 0 1",
            "8/8/8/3pP3/8/8/8/4K2k w - d6 0 1",
            "1r5k/P7/8/8/8/8/8/7K w - - 0 1",
        )

        for fen in tactical_positions:
            with self.subTest(fen=fen):
                board = chess.Board(fen)
                expected_tactical = self.tactical_moves(board)
                shortlist = shortlist_legal_moves(board, quiet_k=3)

                self.assertTrue(expected_tactical)
                self.assertEqual(
                    expected_tactical,
                    set(shortlist[: len(expected_tactical)]),
                )
                self.assertLessEqual(len(shortlist) - len(expected_tactical), 3)
                self.assertTrue(
                    set(shortlist[len(expected_tactical) :]).issubset(
                        self.quiet_moves(board)
                    )
                )
                self.assertEqual(len(shortlist), len(set(shortlist)))

    def test_quiet_limit_zero_and_above_available_moves(self):
        board = chess.Board()

        self.assertEqual([], shortlist_legal_moves(board, quiet_k=0))
        self.assertEqual(
            set(get_legal_moves({"board": board})),
            set(shortlist_legal_moves(board, quiet_k=100)),
        )

    def test_invalid_quiet_limit_is_rejected(self):
        board = chess.Board()

        for invalid_limit in (True, 1.5, "8"):
            with self.subTest(invalid_limit=invalid_limit):
                with self.assertRaises(TypeError):
                    shortlist_legal_moves(board, quiet_k=invalid_limit)

        with self.assertRaises(ValueError):
            shortlist_legal_moves(board, quiet_k=-1)

    def test_terminal_position_has_empty_shortlist(self):
        board = chess.Board("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")

        self.assertTrue(board.is_checkmate())
        self.assertEqual([], shortlist_legal_moves(board))


class GameTerminationTests(unittest.TestCase):
    def test_checkmate_and_stalemate_are_automatic_endings(self):
        checkmate = state_from_fen("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")
        stalemate = state_from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")

        self.assertTrue(is_game_over(checkmate))
        self.assertEqual("1-0", result(checkmate))
        self.assertTrue(is_game_over(stalemate))
        self.assertEqual("1/2-1/2", result(stalemate))

    def test_claimable_fifty_move_draw_does_not_end_tournament_game(self):
        state = state_from_fen("8/8/8/8/8/8/6k1/4K2R w - - 100 1")
        board = state["board"]

        self.assertTrue(board.can_claim_fifty_moves())
        self.assertTrue(board.is_game_over(claim_draw=True))
        self.assertFalse(is_game_over(state))
        self.assertEqual("*", result(state))

    def test_seventy_five_move_draw_is_automatic(self):
        state = state_from_fen("8/8/8/8/8/8/6k1/4K2R w - - 150 1")

        self.assertTrue(state["board"].is_seventyfive_moves())
        self.assertTrue(is_game_over(state))
        self.assertEqual("1/2-1/2", result(state))

    def test_threefold_is_claimable_but_fivefold_is_automatic(self):
        state = new_game()
        repetition_cycle = ("g1f3", "g8f6", "f3g1", "f6g8")

        for _ in range(2):
            for move in repetition_cycle:
                self.assertTrue(apply_move(state, move))

        self.assertTrue(state["board"].can_claim_threefold_repetition())
        self.assertTrue(state["board"].is_game_over(claim_draw=True))
        self.assertFalse(is_game_over(state))
        self.assertEqual("*", result(state))

        for _ in range(2):
            for move in repetition_cycle:
                self.assertTrue(apply_move(state, move))

        self.assertTrue(state["board"].is_fivefold_repetition())
        self.assertTrue(is_game_over(state))
        self.assertEqual("1/2-1/2", result(state))


if __name__ == "__main__":
    unittest.main()
