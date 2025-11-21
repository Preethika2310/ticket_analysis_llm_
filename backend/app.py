from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Settings
from excel_loader import load_catalog
from prompt import SYSTEM_PROMPT, build_user_prompt
from matching import parse_llm_json, compute_accuracy
import requests

app = Flask(__name__)
CORS(app)

try:
    CATALOG = load_catalog(Settings.EXCEL_PATH)
except Exception as e:
    print(f"Failed to load Excel catalog: {e}")
    CATALOG = []

def call_azure_openai(system_prompt: str, user_prompt: str) -> str:
    url = f"{Settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/{Settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-08-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": Settings.AZURE_OPENAI_API_KEY,
    }
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "top_p": 0.9,
        "max_tokens": 150,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "catalog_loaded": len(CATALOG) > 0})

@app.route("/analyze", methods=["POST"])
def analyze():
    body = request.get_json(force=True)
    description = (body.get("description") or "").strip()
    short_description = (body.get("short_description") or "").strip()

    if not description and not short_description:
        return jsonify({"error": "Provide Description or Short Description"}), 400

    if not CATALOG:
        return jsonify({"error": "Catalog not loaded"}), 500

    user_prompt = build_user_prompt(description, short_description, CATALOG)
    try:
        llm_text = call_azure_openai(SYSTEM_PROMPT, user_prompt)
        parsed = parse_llm_json(llm_text)
    except Exception as e:
        return jsonify({"error": f"LLM call/parsing failed: {str(e)}"}), 500

    assignment_group = parsed.get("assignment_group", "")
    service = parsed.get("service", "")
    service_offering = parsed.get("service_offering", "")
    confidence = float(parsed.get("confidence", 0.0))
    reasoning = parsed.get("reasoning", "")

    chosen_def = ""
    routing_reason = ""
    for row in CATALOG:
        if (row["Assignment Group"] == assignment_group and
            row["Service"] == service and
            row["Service Offering"] == service_offering):
            chosen_def = row["Definition"]
            routing_reason = row["Routing Reason"]
            break

    accuracy = compute_accuracy(confidence, description, short_description, chosen_def)

    return jsonify({
        "accuracy": accuracy,
        "assignment_group": assignment_group,
        "service": service,
        "service_offering": service_offering,
        "routing_reason": routing_reason,
        "reasoning": reasoning
    })

if __name__ == "__main__":
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
