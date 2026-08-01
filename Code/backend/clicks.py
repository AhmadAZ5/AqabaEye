"""
Phase 3 click tracking. Builds the UTM url the CTA actually points at, and
fires the click row at the Apps Script webhook in the background. Logging a
click should never be able to break the redirect or the page itself, so any
failure here just gets swallowed.
"""

from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import httpx

from config import settings


def with_utm(url: str, slug: str) -> str:
    parts = urlparse(url)
    query = dict(parse_qsl(parts.query))
    query.update({
        "utm_source": "eyeofaqaba",
        "utm_medium": "referral",
        "utm_campaign": slug,
    })
    return urlunparse(parts._replace(query=urlencode(query)))


# turns a full user agent string into something short like "mobile-chrome"
# instead of storing the whole raw string in the spreadsheet
def coarse_ua(user_agent: str) -> str:
    ua = user_agent.lower()
    if "ipad" in ua or "tablet" in ua:
        device = "tablet"
    elif "mobile" in ua or "android" in ua or "iphone" in ua:
        device = "mobile"
    else:
        device = "desktop"

    if "edg" in ua:
        browser = "edge"
    elif "chrome" in ua:
        browser = "chrome"
    elif "firefox" in ua:
        browser = "firefox"
    elif "safari" in ua:
        browser = "safari"
    else:
        browser = "other"

    return f"{device}-{browser}"


async def log_click(slug: str, lang: str, referrer: str, user_agent: str) -> None:
    if not settings.clicks_webhook_url:
        return
    row = {
        "slug": slug,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lang": lang,
        "referrer": referrer,
        "user_agent": coarse_ua(user_agent),
    }
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            await client.post(settings.clicks_webhook_url, json=row)
    except Exception:
        pass
