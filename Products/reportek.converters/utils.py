import os
import json

def mime_type(ext):
    mime_types = _load_json("mime_types.json")
    return mime_types.get(ext)

def extension(mime_type):
    mime_types = _load_json("mime_types.json")
    extensions = dict()
    for ext, mimes in mime_types.items():
        for mime in mimes:
            extensions.update({mime: ext})
    return extensions.get(mime_type)

def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)
