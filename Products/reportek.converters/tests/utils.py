import os
import json


def _mime_types():
    mime_types = _load_json("mime_types.json")
    return mime_types


def _extensions():
    mime_types = _load_json("mime_types.json")
    extensions = dict()
    for ext, mimes in mime_types.items():
        for mime in mimes:
            extensions.update({mime: ext})
    return extensions


def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)


mime_types = _mime_types()
extensions = _extensions()
