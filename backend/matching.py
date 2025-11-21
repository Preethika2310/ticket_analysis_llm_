import json
from typing import Dict

def parse_llm_json(raw_text: str) -> Dict:
    raw_text = raw_text.strip()
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("LLM did not return valid JSON.")
    snippet = raw_text[start:end+1]
    return json.loads(snippet)

def compute_accuracy(confidence: float, description: str, short_description: str, chosen_definition: str) -> float:
    def tokens(s: str) -> set:
        return set(t.lower() for t in s.split() if t.isalpha())

    ticket_tokens = tokens(description) | tokens(short_description)
    def_tokens = tokens(chosen_definition)
    overlap = len(ticket_tokens & def_tokens)
    norm = max(1, len(def_tokens))
    overlap_ratio = overlap / norm

    base = max(0.0, min(1.0, confidence))
    blended = 0.7 * base + 0.3 * overlap_ratio
    return round(blended * 100, 2)
