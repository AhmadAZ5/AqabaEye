# Eye of Aqaba Portal — Phase 1

Bilingual (Arabic/English) FastAPI + Jinja2 site. Server-rendered, no build step,
no paid services. See `../Files/PRD.md` and `../Files/PLAN.md` for the full spec.

```
backend/   FastAPI app (main.py, config.py, i18n.py, placeholder_data.py)
frontend/  Jinja2 templates + static CSS/JS (rendered by the backend, no build step)
locales/   ar.json / en.json — every UI string, shared by backend and frontend
```

## Run locally

```
cd Code/backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
copy .env.example .env        # or: cp .env.example .env
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/` — it redirects to `/ar/` or `/en/` based on your
browser's language, then the toggle in the header switches manually.

## Env vars

| Variable | Purpose |
|---|---|
| `CONTACT_EMAIL` | Where contact-form submissions will go once Phase 4 wires it up |
| `ENV` | `development` / `production` |

## Deploy (Render free tier)

1. Push this repo to GitHub.
2. New Web Service on Render, pointed at this repo.
3. **Root Directory: `Code/backend`** (that's where `requirements.txt` and
   `render.yaml` live; it reaches into `../frontend` for templates and static files).
4. Render reads `render.yaml` for the build/start commands automatically.
5. Set up a free uptime pinger (e.g. cron-job.org) hitting the live URL every
   ~10 minutes so the free-tier instance doesn't cold-start on the first visitor.

## What's stubbed in Phase 1

- **Content** — `backend/placeholder_data.py` hardcodes the 3 confirmed venues and 3
  blog posts, shaped exactly like the Google Sheets schema in PRD FR-2. Phase 2
  replaces this module with a live sheet fetch; templates don't need to change.
- **Contact form** — renders fully (fields, FAQ, honeypot field) but does not
  submit anywhere yet; the submit button is disabled. Phase 4 adds validation,
  rate limiting, and SMTP sending.
- **Click tracking** — waterpark CTAs link straight to placeholder partner URLs
  (`https://example.com/PLACEHOLDER-...`). No `sendBeacon`, no `/go/{slug}`, no
  click logging yet — that's Phase 3.
- **Map** — no Leaflet yet (Phase 4). Lat/lng already exist in the placeholder data.
- **Images** — no real photography yet, so cards/detail pages show a CSS gradient
  block instead of hotlinking placeholder stock. Swap in real `<img>` tags plus
  `image_urls` handling when photography arrives.
- **SEO extras** — `sitemap.xml`, `robots.txt`, Open Graph tags, and JSON-LD are
  Phase 5.

## What's real right now

- All 7 pages, both languages, real server-rendered HTML.
- `/` → 302 redirect by `Accept-Language`, with a `lang` cookie override.
- RTL/LTR layout via CSS logical properties (`margin-inline-start`, not
  `margin-left`) — no separate stylesheet needed for Arabic.
- `hreflang` alternate tags and a working language toggle that preserves the
  current page.
- "Last verified" date on every price, with a muted warning past 30 days.
