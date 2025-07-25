import os
import json

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def save_template(name, header_mapping, formulas):
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    data = {
        "name": name,
        "header_mapping": header_mapping,
        "formulas": formulas
    }
    with open(os.path.join(TEMPLATE_DIR, f"{name}.json"), "w") as f:
        json.dump(data, f, indent=2)

def load_template(name):
    path = os.path.join(TEMPLATE_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template '{name}' not found.")
    with open(path, "r") as f:
        return json.load(f)

def list_templates():
    if not os.path.exists(TEMPLATE_DIR):
        return []
    return [f[:-5] for f in os.listdir(TEMPLATE_DIR) if f.endswith(".json")]
