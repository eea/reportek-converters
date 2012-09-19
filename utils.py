import os
import json

def mime_type(ext):
    mime_types = _load_json("mime_types.json")
    return mime_types.get(ext)

def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)
