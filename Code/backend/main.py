from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from i18n import DEFAULT_LANG, SUPPORTED_LANGS, get_translation
from sheets import get_attractions, get_faq, get_posts, get_settings, get_waterparks

BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
LANG_COOKIE = "lang"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

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
    verified_date = datetime.strptime(last_verified, "%Y-%m-%d").date()
    return (date.today() - verified_date).days > 30


def render(request: Request, template_name: str, lang: str, **context):
    if lang not in SUPPORTED_LANGS:
        raise HTTPException(status_code=404)

    other_lang = "ar" if lang == "en" else "en"
    current_path = request.url.path
    alt_path = f"/{other_lang}{current_path[3:]}" if current_path.startswith(f"/{lang}") else f"/{other_lang}/"

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
    posts = get_posts()
    featured = [w for w in waterparks if w["is_published"] and w["is_featured"]]
    latest_posts = [p for p in posts if p["is_published"]][:3]
    return render(request, "home.html", lang, featured=featured, latest_posts=latest_posts)


@app.get("/{lang}/waterparks", response_class=HTMLResponse)
async def waterparks_list(request: Request, lang: str):
    published = [w for w in get_waterparks() if w["is_published"]]
    return render(request, "waterparks.html", lang, waterparks=published, is_stale=is_stale)


@app.get("/{lang}/waterparks/{slug}", response_class=HTMLResponse)
async def waterpark_detail(request: Request, lang: str, slug: str):
    match = next((w for w in get_waterparks() if w["slug"] == slug and w["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    return render(request, "waterpark_detail.html", lang, waterpark=match, is_stale=is_stale)


@app.get("/{lang}/attractions", response_class=HTMLResponse)
async def attractions_list(request: Request, lang: str):
    published = [a for a in get_attractions() if a["is_published"]]
    return render(request, "attractions.html", lang, attractions=published, is_stale=is_stale)


@app.get("/{lang}/attractions/{slug}", response_class=HTMLResponse)
async def attraction_detail(request: Request, lang: str, slug: str):
    match = next((a for a in get_attractions() if a["slug"] == slug and a["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    return render(request, "attraction_detail.html", lang, attraction=match, is_stale=is_stale)


@app.get("/{lang}/explore", response_class=HTMLResponse)
async def explore_list(request: Request, lang: str):
    published = [p for p in get_posts() if p["is_published"]]
    return render(request, "explore.html", lang, posts=published)


@app.get("/{lang}/explore/{slug}", response_class=HTMLResponse)
async def post_detail(request: Request, lang: str, slug: str):
    match = next((p for p in get_posts() if p["slug"] == slug and p["is_published"]), None)
    if match is None:
        raise HTTPException(status_code=404)
    return render(request, "post.html", lang, post=match)


@app.get("/{lang}/about", response_class=HTMLResponse)
async def about(request: Request, lang: str):
    return render(request, "about.html", lang)


@app.get("/{lang}/contact", response_class=HTMLResponse)
async def contact(request: Request, lang: str):
    return render(request, "contact.html", lang, faq=get_faq(), contact_settings=get_settings())
