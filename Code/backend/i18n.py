import json
from functools import lru_cache
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"
SUPPORTED_LANGS = ("ar", "en")
DEFAULT_LANG = "en"


@lru_cache
def _load(lang: str) -> dict:
    path = LOCALES_DIR / f"{lang}.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def get_translation(lang: str):
    strings = _load(lang)

    def t(key: str) -> str:
        node = strings
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return key
            node = node[part]
        return node

    return t
