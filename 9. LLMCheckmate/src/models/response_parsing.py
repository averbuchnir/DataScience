import ast
import json
import math
import re

from .prompts import VALID_STRATEGIES


_UCI_PATTERN = re.compile(
    r"(?<![a-z0-9])([a-h][1-8][a-h][1-8][qrbn]?)(?![a-z0-9])",
    re.IGNORECASE,
)
_FENCED_PATTERN = re.compile(
    r"^\s*```(?:json)?\s*(.*?)\s*```\s*$",
    re.IGNORECASE | re.DOTALL,
)


def _strip_fence(text):
    match = _FENCED_PATTERN.match(text)
    return match.group(1).strip() if match else text.strip()


def _parse_mapping(text):
    """Return the first JSON/Python mapping found in text, if one exists."""
    if isinstance(text, dict):
        return text
    if not isinstance(text, str):
        return None

    cleaned = _strip_fence(text)
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(cleaned)
        except (ValueError, SyntaxError, TypeError, json.JSONDecodeError):
            continue
        if isinstance(parsed, dict):
            return parsed

    decoder = json.JSONDecoder()
    for index, character in enumerate(cleaned):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(cleaned[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _normalized_legal_moves(legal_moves):
    if legal_moves is None:
        return None
    return {
        str(move).strip().lower()
        for move in legal_moves
        if str(move).strip()
    }


def extract_uci_move(text, legal_moves=None):
    """Extract the first syntactically valid UCI move allowed by legal_moves."""
    if not isinstance(text, str):
        return ""

    allowed = _normalized_legal_moves(legal_moves)
    for match in _UCI_PATTERN.finditer(_strip_fence(text)):
        move = match.group(1).lower()
        if allowed is None or move in allowed:
            return move
    return ""


def _parse_confidence(value):
    if isinstance(value, bool):
        return 0.5
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.5
    if not math.isfinite(confidence) or not 0 <= confidence <= 1:
        return 0.5
    return confidence


def _parse_strategy(value):
    if not isinstance(value, str):
        return "balanced"
    strategy = value.strip().lower()
    return strategy if strategy in VALID_STRATEGIES else "balanced"


def parse_strategy_response(response):
    """Parse the legacy strategy response without raising on malformed content."""
    parsed = _parse_mapping(response)
    if not parsed:
        return {
            "strategy": "balanced",
            "confidence": 0.5,
            "reason": "Failed to parse strategy response",
        }

    reason = parsed.get("reason")
    return {
        "strategy": _parse_strategy(parsed.get("strategy")),
        "confidence": _parse_confidence(parsed.get("confidence")),
        "reason": reason.strip() if isinstance(reason, str) and reason.strip() else "No reason provided",
    }


def parse_move_response(response, legal_moves=None):
    """Parse one move response and validate it against the supplied legal moves."""
    parsed = _parse_mapping(response)
    response_text = response if isinstance(response, str) else ""

    if parsed is not None:
        raw_move = parsed.get("move")
        move = extract_uci_move(raw_move, legal_moves)
        confidence = _parse_confidence(parsed.get("confidence"))
        reason_value = parsed.get("reason")
        reason = (
            reason_value.strip()
            if isinstance(reason_value, str) and reason_value.strip()
            else "No reason provided"
        )
        strategy = _parse_strategy(parsed.get("strategy"))
    else:
        move = extract_uci_move(response_text, legal_moves)
        confidence = 0.5
        reason = "Parsed move from a non-JSON response" if move else "Failed to parse move response"
        strategy = "balanced"

    if not move and parsed is not None:
        reason = "Model returned no move from the supplied legal moves"

    return {
        "move": move,
        "confidence": confidence,
        "reason": reason,
        "strategy": strategy,
    }
