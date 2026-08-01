"""
Phase 2 content pipeline. Each tab of the client's Google Sheet gets published
to web as CSV, we fetch it here, cache it for a while, and if anything goes
wrong (sheet down, bad edit, no url configured yet) we just fall back to the
last good copy we had, and if we never had one, to the committed snapshot.json.
The site should never go down just because someone fat-fingered a spreadsheet.
"""

import csv
import io
import json
import time
from pathlib import Path

import httpx

from config import settings

BACKEND_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = BACKEND_DIR / "snapshot.json"
CACHE_TTL_SECONDS = 600

_cache: dict[str, tuple[float, list[dict]]] = {}


def _snapshot() -> dict:
    with SNAPSHOT_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _to_bool(value: str) -> bool:
    return str(value).strip().upper() in ("TRUE", "1", "YES")


def _fetch_rows(tab: str, url: str) -> list[dict] | None:
    now = time.time()
    cached = _cache.get(tab)
    if cached and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    if url:
        try:
            response = httpx.get(url, timeout=5, follow_redirects=True)
            response.raise_for_status()
            rows = list(csv.DictReader(io.StringIO(response.text)))
            _cache[tab] = (now, rows)
            return rows
        except Exception:
            pass

    return cached[1] if cached else None


def _parse_venue_row(row: dict) -> dict:
    return {
        "slug": row["slug"].strip(),
        "name_ar": row["name_ar"],
        "name_en": row["name_en"],
        "summary_ar": row["summary_ar"],
        "summary_en": row["summary_en"],
        "description_ar": row["description_ar"],
        "description_en": row["description_en"],
        "price_adult": int(row["price_adult"] or 0),
        "price_child": int(row["price_child"] or 0),
        "currency": row["currency"],
        "hours": row["hours"],
        "lat": float(row["lat"]) if row["lat"] else None,
        "lng": float(row["lng"]) if row["lng"] else None,
        "partner_url": row["partner_url"],
        "image_urls": [u.strip() for u in row["image_urls"].split("|") if u.strip()],
        "is_featured": _to_bool(row["is_featured"]),
        "is_published": _to_bool(row["is_published"]),
        "last_verified": row["last_verified"].strip(),
    }


def _parse_post_row(row: dict) -> dict:
    return {
        "slug": row["slug"].strip(),
        "title_ar": row["title_ar"],
        "title_en": row["title_en"],
        "body_ar": row["body_ar"],
        "body_en": row["body_en"],
        "cover_image": row["cover_image"],
        "published_at": row["published_at"].strip(),
        "is_published": _to_bool(row["is_published"]),
    }


def _parse_faq_row(row: dict) -> dict:
    return {
        "question_ar": row["question_ar"],
        "question_en": row["question_en"],
        "answer_ar": row["answer_ar"],
        "answer_en": row["answer_en"],
        "sort_order": int(row["sort_order"] or 0),
    }


def _parse_settings_rows(rows: list[dict]) -> dict:
    result = {}
    for row in rows:
        key = row["key"].strip()
        if key == "address":
            result["address_ar"] = row["value_ar"]
            result["address_en"] = row["value_en"]
        elif key in ("lat", "lng"):
            value = row["value_en"] or row["value_ar"]
            result[key] = float(value) if value else None
        else:
            result[key] = row["value_en"] or row["value_ar"]
    return result


def get_waterparks() -> list[dict]:
    rows = _fetch_rows("waterparks", settings.sheet_csv_waterparks)
    return [_parse_venue_row(r) for r in rows] if rows is not None else _snapshot()["waterparks"]


def get_attractions() -> list[dict]:
    rows = _fetch_rows("attractions", settings.sheet_csv_attractions)
    return [_parse_venue_row(r) for r in rows] if rows is not None else _snapshot()["attractions"]


def get_posts() -> list[dict]:
    rows = _fetch_rows("posts", settings.sheet_csv_posts)
    return [_parse_post_row(r) for r in rows] if rows is not None else _snapshot()["posts"]


def get_faq() -> list[dict]:
    rows = _fetch_rows("faq", settings.sheet_csv_faq)
    return [_parse_faq_row(r) for r in rows] if rows is not None else _snapshot()["faq"]


def get_settings() -> dict:
    rows = _fetch_rows("settings", settings.sheet_csv_settings)
    return _parse_settings_rows(rows) if rows is not None else _snapshot()["settings"]
