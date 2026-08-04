import json
import re
import time
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from clicks import log_click, with_utm
from config import settings
from i18n import DEFAULT_LANG, SUPPORTED_LANGS, get_translation
from mail import send_contact_email
from sheets import (
    get_attractions,
    get_best_time_guide,
    get_car_rentals,
    get_faq,
    get_posts,
    get_settings,
    get_waterparks,
)

BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
LANG_COOKIE = "lang"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CONTACT_RATE_LIMIT_SECONDS = 60

# per-IP cooldown for the contact form, in-memory since this runs as a single
# free-tier instance, resets on deploy and that's fine for this scale
_contact_last_submit: dict[str, float] = {}


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

app = FastAPI()
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")
templates = Jinja2Templates(directory=FRONTEND_DIR / "templates")


def resolve_lang(request: Request) -> str:
    cookie_lang = request.cookies.get(LANG_COOKIE)
    if cookie_lang in SUPPORTED_LANGS:
        return cookie_lang
    accept_language = request.headers.get("accept-language", "")
    if accept_language.lower().startswith("ar"):
        return "ar"
    return DEFAULT_LANG


def is_stale(last_verified: str) -> bool:
    # an unparseable date from a bad sheet row is treated as stale rather than
    # crashing the page
    try:
        verified_date = datetime.strptime(last_verified, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return True
    return (date.today() - verified_date).days > 30


# builds the marker list map.js reads off the page, skips any venue missing
# lat/lng instead of crashing the map over one bad sheet row
def venue_markers(venues: list[dict], lang: str, href_prefix: str | None = None) -> list[dict]:
    markers = []
    for v in venues:
        try:
            lat = float(v.get("lat"))
            lng = float(v.get("lng"))
        except (TypeError, ValueError):
            continue
        if lat == 0 and lng == 0:
            continue
        marker = {
            "lat": lat,
            "lng": lng,
            "title": v["name_ar"] if lang == "ar" else v["name_en"],
        }
        if href_prefix:
            marker["href"] = f"{href_prefix}/{v['slug']}"
        markers.append(marker)
    return markers


def render(request: Request, template_name: str, lang: str, **context):
    if lang not in SUPPORTED_LANGS:
        raise HTTPException(status_code=404)

    other_lang = "ar" if lang == "en" else "en"
    current_path = request.url.path
    alt_path = f"/{other_lang}{current_path[3:]}" if current_path.startswith(f"/{lang}") else f"/{other_lang}/"

    # markers travels as a real list for {% if markers %} checks, markers_json is the
    # string that actually goes in the html attribute, autoescape handles quoting it safely
    if "markers" in context:
        context["markers_json"] = json.dumps(context["markers"], ensure_ascii=False)

    response = templates.TemplateResponse(
        request,
        template_name,
        {
            "lang": lang,
            "other_lang": other_lang,
            "alt_path": alt_path,
            "dir": "rtl" if lang == "ar" else "ltr",
            "t": get_translation(lang),
            "site_name_ar": settings.site_name_ar,
            "site_name_en": settings.site_name_en,
            **context,
        },
    )
    response.set_cookie(LANG_COOKIE, lang, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.get("/")
async def root(request: Request):
    lang = resolve_lang(request)
    response = RedirectResponse(url=f"/{lang}/", status_code=302)
    response.set_cookie(LANG_COOKIE, lang, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.get("/{lang}/", response_class=HTMLResponse)
async def home(request: Request, lang: str):
    waterparks = get_waterparks()
    attractions = get_attractions()
    posts = get_posts()
    featured = [w for w in waterparks if w["is_published"] and w["is_featured"]]
    featured_attractions = [a for a in attractions if a["is_published"] and a["is_featured"]]
    latest_posts = [p for p in posts if p["is_published"]][:3]
    total_venues = len([w for w in waterparks if w["is_published"]]) + len([a for a in attractions if a["is_published"]])
    return render(
        request, "home.html", lang, featured=featured, featured_attractions=featured_attractions,
        latest_posts=latest_posts, total_venues=total_venues,
    )


@app.get("/{lang}/waterparks", response_class=HTMLResponse)
async def waterparks_list(request: Request, lang: str):
    published = [w for w in get_waterparks() if w["is_published"]]
    markers = venue_markers(published, lang, href_prefix=f"/{lang}/waterparks")
    return render(request, "waterparks.html", lang, waterparks=published, is_stale=is_stale, markers=markers)


@app.get("/{lang}/waterparks/{slug}", response_class=HTMLResponse)
async def waterpark_detail(request: Request, lang: str, slug: str):
    match = next((w for w in get_waterparks() if w["slug"] == slug and w["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    cta_url = with_utm(match["partner_url"], slug)
    markers = venue_markers([match], lang)
    return render(
        request, "waterpark_detail.html", lang, waterpark=match, is_stale=is_stale, cta_url=cta_url, markers=markers
    )


@app.get("/{lang}/attractions", response_class=HTMLResponse)
async def attractions_list(request: Request, lang: str):
    published = [a for a in get_attractions() if a["is_published"]]
    markers = venue_markers(published, lang, href_prefix=f"/{lang}/attractions")
    return render(request, "attractions.html", lang, attractions=published, is_stale=is_stale, markers=markers)


@app.get("/{lang}/attractions/{slug}", response_class=HTMLResponse)
async def attraction_detail(request: Request, lang: str, slug: str):
    match = next((a for a in get_attractions() if a["slug"] == slug and a["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    cta_url = with_utm(match["partner_url"], slug)
    markers = venue_markers([match], lang)
    return render(
        request, "attraction_detail.html", lang, attraction=match, is_stale=is_stale, cta_url=cta_url, markers=markers
    )


@app.get("/{lang}/car-rentals", response_class=HTMLResponse)
async def car_rentals_list(request: Request, lang: str):
    published = [c for c in get_car_rentals() if c["is_published"]]
    return render(request, "car_rentals.html", lang, car_rentals=published)


@app.get("/{lang}/car-rentals/{slug}", response_class=HTMLResponse)
async def car_rental_detail(request: Request, lang: str, slug: str):
    match = next((c for c in get_car_rentals() if c["slug"] == slug and c["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    cta_url = with_utm(match["partner_url"], slug)
    return render(request, "car_rental_detail.html", lang, car_rental=match, cta_url=cta_url)


@app.get("/{lang}/explore", response_class=HTMLResponse)
async def explore_list(request: Request, lang: str):
    published = [p for p in get_posts() if p["is_published"]]
    return render(request, "explore.html", lang, posts=published)


@app.get("/{lang}/explore/{slug}", response_class=HTMLResponse)
async def post_detail(request: Request, lang: str, slug: str):
    match = next((p for p in get_posts() if p["slug"] == slug and p["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    if slug == "best-time-to-visit-aqaba":
        return render(request, "best_time_guide.html", lang, post=match, guide=get_best_time_guide())
    return render(request, "post.html", lang, post=match)


@app.get("/{lang}/about", response_class=HTMLResponse)
async def about(request: Request, lang: str):
    return render(request, "about.html", lang)


@app.get("/{lang}/contact", response_class=HTMLResponse)
async def contact(request: Request, lang: str):
    contact_settings = get_settings()
    markers = []
    if contact_settings.get("lat") is not None and contact_settings.get("lng") is not None:
        markers = [{
            "lat": contact_settings["lat"],
            "lng": contact_settings["lng"],
            "title": contact_settings["address_ar"] if lang == "ar" else contact_settings["address_en"],
        }]
    return render(request, "contact.html", lang, faq=get_faq(), contact_settings=contact_settings, markers=markers)


# contact form submit, validates then relays to CONTACT_EMAIL over SMTP,
# a filled honeypot field gets a fake success so bots don't learn anything
@app.post("/api/contact")
async def api_contact(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400)

    if payload.get("company"):
        return {"ok": True}

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone") or "").strip()
    message = (payload.get("message") or "").strip()

    errors = {}
    if not name:
        errors["name"] = True
    if not email or not EMAIL_RE.match(email):
        errors["email"] = True
    if not message:
        errors["message"] = True
    if errors:
        return JSONResponse({"ok": False, "errors": errors}, status_code=400)

    ip = client_ip(request)
    now = time.monotonic()
    last = _contact_last_submit.get(ip)
    if last is not None and now - last < CONTACT_RATE_LIMIT_SECONDS:
        return JSONResponse({"ok": False, "rate_limited": True}, status_code=429)
    _contact_last_submit[ip] = now

    sent = await send_contact_email(name, email, phone, message)
    if not sent:
        return JSONResponse({"ok": False, "server_error": True}, status_code=502)
    return {"ok": True}


# sendBeacon hits this on CTA click, fire and forget, never blocks the user
@app.post("/api/click")
async def api_click(request: Request):
    try:
        payload = await request.json()
    except Exception:
        return Response(status_code=204)

    slug = payload.get("slug", "")
    if slug:
        await log_click(
            slug,
            payload.get("lang", ""),
            request.headers.get("referer", ""),
            request.headers.get("user-agent", ""),
        )
    return Response(status_code=204)


# server-side fallback for links shared outside the site, also the only way
# a click gets logged if the visitor's browser has no sendBeacon or JS is off
@app.get("/go/{slug}")
async def go(request: Request, slug: str):
    match = next(
        (
            v
            for v in get_waterparks() + get_attractions() + get_car_rentals()
            if v["slug"] == slug and v["is_published"]
        ),
        None,
    )
    if match is None:
        raise HTTPException(status_code=404)

    lang = resolve_lang(request)
    await log_click(slug, lang, request.headers.get("referer", ""), request.headers.get("user-agent", ""))
    return RedirectResponse(url=with_utm(match["partner_url"], slug), status_code=302)
