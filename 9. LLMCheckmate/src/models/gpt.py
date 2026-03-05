
import os
import json
import ast
from openai import OpenAI
from .prompts import build_move_prompt,build_strategy_prompt,build_move_prompt_simple
from ..utils import get_current_time_display
from dotenv import load_dotenv
import re
load_dotenv()


_client = None

def _get_client():
    global _client
    if _client is not None:
        return _client
    
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    _client = OpenAI(api_key=api_key)
    return _client

# general function to get response from GPT called "call_gpt_model"
def _call_gpt_model(model_name, prompt):
    client = _get_client()
    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return resp.choices[0].message.content





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


## function to get move from GPT
def get_move_gpt(tier,fen, side, legal_moves=None, move_history=None, model_name=None):
    """
        return move, confidence, reason, strategy from GPT model.
    """
    client = _get_client()
    Flag_Advanced_Move_Prompt = True
    if Flag_Advanced_Move_Prompt:
        print(f"{get_current_time_display()} - GPT Advanced Move Prompt")
        strategy_prompt = build_strategy_prompt(fen, side, legal_moves, move_history)
        print(f"{get_current_time_display()} - GPT Strategy Reasoning")
        gpt_strategy_response = _call_gpt_model(model_name, strategy_prompt)
        gpt_strategy_response = _extract_json_strategy(gpt_strategy_response)
        strategy_str = gpt_strategy_response.get("strategy", "balanced") if isinstance(gpt_strategy_response, dict) else "balanced"
        print(f"{get_current_time_display()} - GPT Move Reasoning (Advanced-Flow)")
        prompt = build_move_prompt(fen, side, legal_moves, move_history=move_history, strategy=strategy_str)
        get_gpt_move_response = _call_gpt_model(model_name, prompt)
        get_gpt_move_response = _extract_json_move(get_gpt_move_response)
    else:
        print(f"{get_current_time_display()} - GPT Simple Move Prompt")
        prompt = build_move_prompt_simple(fen, side, legal_moves)
        print(f"{get_current_time_display()} - GPT Move Reasoning (Simple-Flow)")
        get_gpt_move_response = _call_gpt_model(model_name, prompt)
        get_gpt_move_response = _extract_json_move(get_gpt_move_response)
        # create a default strategy dict for return values
        gpt_strategy_response = {
            "strategy": "balanced (simple prompt mode)",
            "confidence": get_gpt_move_response.get("confidence", 0.5),
            "reason": "Simple prompt mode - no strategy reasoning"
        }


    # print the move, confidence, reason, strategy
    # print(f"{get_current_time_display()} - Move: {_extract_uci_move(get_gpt_move_response.get('move'))}")
    # print(f"{get_current_time_display()} - Confidence: {get_gpt_move_response.get('confidence')}")
    # print(f"{get_current_time_display()} - Reason: {get_gpt_move_response.get('reason')}")
    # print(f"{get_current_time_display()} - Strategy: {gpt_strategy_response.get('strategy')}")
    # a = input("Press Enter to continue...")
    return _extract_uci_move(get_gpt_move_response.get("move")),get_gpt_move_response.get("confidence"),get_gpt_move_response.get("reason"),gpt_strategy_response.get("strategy")

    
    
    
