import json
from typing import Dict, List, Tuple

def parse_llm_json(raw_text: str) -> Dict:
    """
    Safely parse the LLM output expected as JSON.
    """
    raw_text = raw_text.strip()
    # Handle potential leading/trailing text by finding first '{' and last '}'
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("LLM did not return valid JSON.")
    snippet = raw_text[start:end+1]
    return json.loads(snippet)

def compute_accuracy(confidence: float, description: str, short_description: str, chosen_definition: str) -> float:
    """
    Map LLM confidence to a user-facing accuracy score.
    Optionally weight by simple keyword overlap to stabilize.
    """
    # Simple heuristic: confidence weighted by keyword overlap
    def tokens(s: str) -> set:
        return set(t.lower() for t in s.split() if t.isalpha())

    ticket_tokens = tokens(description) | tokens(short_description)
    def_tokens = tokens(chosen_definition)
    overlap = len(ticket_tokens & def_tokens)
    norm = max(1, len(def_tokens))
    overlap_ratio = overlap / norm  # 0..1

    base = max(0.0, min(1.0, confidence))
    blended = 0.7 * base + 0.3 * overlap_ratio
    return round(blended * 100, 2)  # percentage
