import os
from google import genai
from .prompts import build_move_prompt
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


import re

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


def get_move_gemini(fen, side, legal_moves=None, move_history=None, model="gemini-3-pro-preview"): # models/gemini-2.5-flash-image"
    """
    return ONE UCI move from Gemini model.
    """
    client = _get_client()
    prompt = build_move_prompt(fen, side, legal_moves, move_history)
    
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    # extract UCI move from the response
    return _extract_uci_move(resp.text)