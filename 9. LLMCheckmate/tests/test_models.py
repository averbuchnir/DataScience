import unittest
from unittest.mock import patch

from src.models import gemini, gpt
from src.models.prompts import build_move_prompt, build_move_prompt_simple
from src.models.response_parsing import parse_move_response, parse_strategy_response


class MovePromptTests(unittest.TestCase):
    def test_move_prompt_includes_history_and_legal_moves_once(self):
        prompt = build_move_prompt(
            fen="test-fen",
            side="white",
            legal_moves=["g1f3", "f1c4"],
            move_history=["e2e4", "e7e5"],
        )

        self.assertIn("Side to move: White", prompt)
        self.assertEqual(prompt.count("e2e4 e7e5"), 1)
        self.assertEqual(prompt.count("g1f3 f1c4"), 1)
        self.assertIn('"strategy":"<aggressive|defensive|balanced|random>"', prompt)

    def test_move_prompt_marks_empty_history(self):
        prompt = build_move_prompt(
            fen="test-fen",
            side="black",
            legal_moves=["e7e5"],
            strategy={"unexpected": "value"},
        )

        self.assertIn("Side to move: Black", prompt)
        self.assertIn("(none; this is the first move)", prompt)
        self.assertIn("Choose the most appropriate strategy", prompt)

    def test_simple_prompt_preserves_ascii_board(self):
        prompt = build_move_prompt_simple(
            fen="test-fen",
            side="white",
            legal_moves=["e2e4"],
            ascii_board="board diagram",
            strategy="aggressive",
        )

        self.assertIn("Board:\nboard diagram", prompt)
        self.assertIn('Use the "aggressive" strategy.', prompt)


class ResponseParsingTests(unittest.TestCase):
    def test_parses_fenced_json_and_normalizes_values(self):
        response = """```json
        {"move":"E7E8Q","confidence":"0.9","reason":"Promote", "strategy":"Aggressive"}
        ```"""

        parsed = parse_move_response(response, legal_moves=["e7e8q"])

        self.assertEqual(
            parsed,
            {
                "move": "e7e8q",
                "confidence": 0.9,
                "reason": "Promote",
                "strategy": "aggressive",
            },
        )

    def test_parses_simple_uci_response(self):
        parsed = parse_move_response("My move: e2e4", legal_moves=["e2e4", "d2d4"])

        self.assertEqual(parsed["move"], "e2e4")
        self.assertEqual(parsed["strategy"], "balanced")
        self.assertEqual(parsed["confidence"], 0.5)

    def test_parses_json_embedded_in_extra_text(self):
        response = (
            'Choice: {"move":"g1f3","confidence":0.7,'
            '"reason":"Develop", "strategy":"balanced"} Done.'
        )

        parsed = parse_move_response(response, legal_moves=["g1f3"])

        self.assertEqual(parsed["move"], "g1f3")
        self.assertEqual(parsed["reason"], "Develop")

    def test_rejects_structured_move_outside_supplied_legal_moves(self):
        response = (
            '{"move":"a2a5","confidence":0.8,'
            '"reason":"I also considered e2e4", "strategy":"aggressive"}'
        )

        parsed = parse_move_response(response, legal_moves=["e2e4"])

        self.assertEqual(parsed["move"], "")
        self.assertEqual(parsed["reason"], "Model returned no move from the supplied legal moves")

    def test_handles_malformed_types_without_raising(self):
        parsed = parse_move_response(
            {"move": 1234, "confidence": True, "reason": [], "strategy": {}},
            legal_moves=["e2e4"],
        )

        self.assertEqual(parsed["move"], "")
        self.assertEqual(parsed["confidence"], 0.5)
        self.assertEqual(parsed["strategy"], "balanced")

    def test_parses_legacy_strategy_response_defensively(self):
        parsed = parse_strategy_response(
            "{'strategy':'defensive','confidence':0.6,'reason':'King safety'}"
        )

        self.assertEqual(parsed["strategy"], "defensive")
        self.assertEqual(parsed["confidence"], 0.6)


class ProviderAdapterTests(unittest.TestCase):
    @patch("src.models.gpt._call_gpt_model")
    def test_gpt_uses_one_call_and_preserves_return_contract(self, call_model):
        call_model.return_value = (
            '{"move":"e2e4","confidence":0.8,'
            '"reason":"Controls the center", "strategy":"balanced"}'
        )

        result = gpt.get_move_gpt(
            tier="Fast",
            fen="test-fen",
            side="white",
            legal_moves=["e2e4", "d2d4"],
            move_history=["g8f6"],
            model_name="configured-gpt-model",
        )

        self.assertEqual(result, ("e2e4", 0.8, "Controls the center", "balanced"))
        call_model.assert_called_once()
        model_name, prompt = call_model.call_args.args
        self.assertEqual(model_name, "configured-gpt-model")
        self.assertIn("g8f6", prompt)

    @patch("src.models.gemini._call_gemini_model")
    def test_gemini_uses_one_call_and_preserves_return_contract(self, call_model):
        call_model.return_value = (
            '{"move":"d2d4","confidence":0.75,'
            '"reason":"Controls the center", "strategy":"aggressive"}'
        )

        result = gemini.get_move_gemini(
            tier="Fast",
            fen="test-fen",
            side="white",
            legal_moves=["e2e4", "d2d4"],
            move_history=["g8f6"],
            model_name="configured-gemini-model",
        )

        self.assertEqual(result, ("d2d4", 0.75, "Controls the center", "aggressive"))
        call_model.assert_called_once()
        model_name, prompt = call_model.call_args.args
        self.assertEqual(model_name, "configured-gemini-model")
        self.assertIn("g8f6", prompt)


if __name__ == "__main__":
    unittest.main()
