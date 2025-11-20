from typing import List, Dict

SYSTEM_PROMPT = """You are a classification expert. 
Given a user ticket with Description and Short Description, and a catalog of definitions, 
select the single best matching row and provide a structured JSON with:
- assignment_group
- service
- service_offering
- reasoning: brief justification tied to the definitions
Also compute a confidence score between 0 and 1 based on semantic match quality.
Be accurate and avoid fabricating values not present in the catalog."""

def build_user_prompt(description: str, short_description: str, catalog: List[Dict]) -> str:
    # Pack catalog definitions into a compact list
    lines = []
    for i, row in enumerate(catalog):
        lines.append(
            f"ID={i}; AG={row['Assignment Group']}; Service={row['Service']}; Offering={row['Service Offering']}; Def={row['Definition']}"
        )
    catalog_text = "\n".join(lines)

    return f"""Ticket:
- Description: {description}
- Short Description: {short_description}

Catalog:
{catalog_text}

Task:
1) Choose the best matching ID (only one).
2) Return JSON EXACTLY in this format:
{{
  "assignment_group": "...",
  "service": "...",
  "service_offering": "...",
  "confidence": 0.0,
  "reasoning": "..."
}}
Notes:
- Only use values from the chosen catalog row.
- confidence in [0,1]; 1 is perfect definition match.
- Do not include extra fields."""
