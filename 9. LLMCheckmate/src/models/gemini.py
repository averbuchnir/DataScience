import os

from dotenv import load_dotenv
from google import genai

from .prompts import build_move_prompt
from .response_parsing import (
    extract_uci_move,
    parse_move_response,
    parse_strategy_response,
)
from ..utils import get_current_time_display

load_dotenv()


_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    _client = genai.Client(api_key=api_key)
    return _client


def _call_gemini_model(model_name, prompt):
    client = _get_client()
    resp = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return resp.text


def _extract_uci_move(text):
    """Compatibility wrapper around the shared UCI parser."""
    return extract_uci_move(text)


def _extract_json_strategy(response):
    """Compatibility wrapper around the shared strategy parser."""
    return parse_strategy_response(response)


def _extract_json_move(response):
    """Compatibility wrapper preserving the legacy three-field result."""
    parsed = parse_move_response(response)
    return {
        "move": parsed["move"],
        "confidence": parsed["confidence"],
        "reason": parsed["reason"],
    }


def get_move_gemini(tier, fen, side, legal_moves=None, move_history=None, model_name=None):
    """Return move, confidence, reason, and strategy from one Gemini API call."""
    del tier  # Retained in the public signature for main.py compatibility.
    prompt = build_move_prompt(
        fen=fen,
        side=side,
        legal_moves=legal_moves,
        move_history=move_history,
    )
    print(f"{get_current_time_display()} - Gemini Move Reasoning (Single-Call)")
    response = _call_gemini_model(model_name, prompt)
    parsed = parse_move_response(response, legal_moves=legal_moves)
    return (
        parsed["move"],
        parsed["confidence"],
        parsed["reason"],
        parsed["strategy"],
    )
