import os
import re
import json
import ast
from google import genai
from .prompts import build_move_prompt,build_strategy_prompt,build_move_prompt_simple
from ..utils import get_current_time_display
from dotenv import load_dotenv
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
    """
    Extract a UCI move from the response text.
    Looks for UCI pattern: [a-h][1-8][a-h][1-8][qrnb]?
    Returns the first valid UCI move found, or empty string if none found.
    """
    if not text:
        return ""
    
    text = text.strip()
    # Pattern for UCI move: 4-5 characters matching [a-h][1-8][a-h][1-8][qrnb]?
    uci_pattern = r'\b([a-h][1-8][a-h][1-8][qrnb]?)\b'
    match = re.search(uci_pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).lower()
    
    # Fallback: try to find any 4-5 character sequence that looks like UCI
    # This handles cases where there's no word boundary
    uci_pattern_loose = r'([a-h][1-8][a-h][1-8][qrnb]?)'
    match = re.search(uci_pattern_loose, text, re.IGNORECASE)
    
    if match:
        return match.group(1).lower()
    
    # Last resort: return first token (original behavior)
    return text.split()[0] if text else ""

def _extract_json_strategy(response):
    if not response:
        return {
            "strategy": "balanced",
            "confidence": 0.5,
            "reason": "Failed to parse strategy response"
        }
    
    # Strip markdown code blocks if present
    text = response.strip()
    if text.startswith("```"):
        # Remove markdown code block markers
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    
    try:
        return json.loads(text)
    except Exception:
        try:
            # Try with single quotes converted to double quotes (for Python dict syntax)
            text_single_to_double = text.replace("'", '"')
            return json.loads(text_single_to_double)
        except Exception:
            try:
                return ast.literal_eval(text)
            except Exception:
                return {
                    "strategy": "balanced",
                    "confidence": 0.5,
                    "reason": "Failed to parse strategy response"
                }

def _extract_json_move(response):
    if not response:
        return {
            "move": "",
            "confidence": 0.5,
            "reason": "Failed to parse move response"
        }
    
    # Strip markdown code blocks if present
    text = response.strip()
    if text.startswith("```"):
        # Remove markdown code block markers
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    
    try:
        return json.loads(text)
    except Exception:
        try:
            # Try with single quotes converted to double quotes (for Python dict syntax)
            text_single_to_double = text.replace("'", '"')
            return json.loads(text_single_to_double)
        except Exception:
            try:
                return ast.literal_eval(text)
            except Exception:
                return {
                    "move": "",
                    "confidence": 0.5,
                    "reason": "Failed to parse move response"
                }

# gemini-3-flash-preview
# gemini-3-pro-preview"

def get_move_gemini(tier,fen, side, legal_moves=None, move_history=None, model_name=None):
    """
    return move, confidence, reason, strategy from Gemini model.
    """
    client = _get_client()
    Flag_Advanced_Move_Prompt = False
    if Flag_Advanced_Move_Prompt:
        print(f"{get_current_time_display()} - Gemini Advanced Move Prompt")
        strategy_prompt = build_strategy_prompt(fen, side, legal_moves, move_history)
        print(f"{get_current_time_display()} - Gemini Strategy Reasoning")
        gemini_strategy_response = _call_gemini_model(model_name, strategy_prompt)
        gemini_strategy_response = _extract_json_strategy(gemini_strategy_response)
        strategy_str = gemini_strategy_response.get("strategy", "balanced") if isinstance(gemini_strategy_response, dict) else "balanced"
        print(f"{get_current_time_display()} - Gemini Move Reasoning (Advanced-Flow)")
        prompt = build_move_prompt(fen, side, legal_moves, move_history=move_history, strategy=strategy_str)
        gemini_move_response = _call_gemini_model(model_name, prompt)
        gemini_move_response = _extract_json_move(gemini_move_response)
    else:
        print(f"{get_current_time_display()} - Gemini Simple Move Prompt")
        prompt = build_move_prompt_simple(fen, side, legal_moves)
        print(f"{get_current_time_display()} - Gemini Move Reasoning (Simple-Flow)")
        gemini_move_response = _call_gemini_model(model_name, prompt)
        gemini_move_response = _extract_json_move(gemini_move_response)
        # create a default strategy dict for return values
        gemini_strategy_response = {
            "strategy": "balanced",
            "confidence": gemini_move_response.get("confidence", 0.5),
            "reason": "Simple prompt mode - no strategy reasoning"
        }

    # print the move, confidence, reason, strategy
    # print(f"{get_current_time_display()} - Gemini-Move: {_extract_uci_move(gemini_move_response.get('move'))}")
    # print(f"{get_current_time_display()} - Gemini-Confidence: {gemini_strategy_response.get('confidence')}")
    # print(f"{get_current_time_display()} - Gemini-Reason: {gemini_strategy_response.get('reason')}")
    # print(f"{get_current_time_display()} - Gemini-Strategy: {gemini_strategy_response.get('strategy')}")

    return _extract_uci_move(gemini_move_response.get("move")),gemini_move_response.get("confidence"),gemini_move_response.get("reason"),gemini_strategy_response.get("strategy")
    # a = input("From gemini.py: Press Enter to continue...")





# def get_move_gemini(tier,fen, side, legal_moves=None, move_history=None, model_name=None):
#     """
#     return ONE UCI move from Gemini model.
#     """


#     client = _get_client()
#     prompt = build_move_prompt(fen, side, legal_moves, move_history)

#     # Use model_name if provided, otherwise fallback to default
#     model = model_name if model_name else "gemini-3-flash-preview"

#     resp = client.models.generate_content(
#         model=model,
#         contents=prompt,
#     )
#     # extract UCI move from the response
#     return _extract_uci_move(resp.text)