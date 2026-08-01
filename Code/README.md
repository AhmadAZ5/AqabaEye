# Eye of Aqaba Portal

Bilingual (Arabic/English) FastAPI + Jinja2 site. Server-rendered, no build step,
no paid services. See `../Files/PRD.md` and `../Files/PLAN.md` for the full spec.

```
backend/   FastAPI app (main.py, config.py, i18n.py, sheets.py, snapshot.json)
frontend/  Jinja2 templates + static CSS/JS (rendered by the backend, no build step)
locales/   ar.json / en.json, every UI string, shared by backend and frontend
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

Open `http://127.0.0.1:8000/`, it redirects to `/ar/` or `/en/` based on your
browser's language, then the toggle in the header switches manually.

## Env vars

| Variable | Purpose |
|---|---|
| `CONTACT_EMAIL` | Where contact-form submissions will go once Phase 4 wires it up |
| `ENV` | `development` / `production` |
| `SHEET_CSV_WATERPARKS` | Published-to-web CSV url for the `waterparks` tab, optional |
| `SHEET_CSV_ATTRACTIONS` | Published-to-web CSV url for the `attractions` tab, optional |
| `SHEET_CSV_POSTS` | Published-to-web CSV url for the `posts` tab, optional |
| `SHEET_CSV_FAQ` | Published-to-web CSV url for the `faq` tab, optional |
| `SHEET_CSV_SETTINGS` | Published-to-web CSV url for the `settings` tab, optional |
| `CLICKS_WEBHOOK_URL` | Apps Script web app url that logs a click, optional, see `Files/apps_script_clicks_webhook.gs` |

Leave any of the sheet vars blank and that tab falls back to `backend/snapshot.json`
instead, the site never breaks just because a url is missing or a sheet edit went bad.

## Content pipeline

Content comes from one Google Sheet with 5 tabs: `waterparks`, `attractions`,
`posts`, `faq`, `settings`. Each tab gets published to web as CSV (File > Share >
Publish to web > pick the tab > CSV > Publish), and the resulting url goes into the
matching `SHEET_CSV_*` env var. `backend/sheets.py` fetches each tab, caches it in
memory for 10 minutes, and falls back to the last good copy, then to
`backend/snapshot.json`, if a fetch ever fails.

Column shapes, matching PRD FR-2:

- `waterparks` / `attractions`: slug, name_ar, name_en, summary_ar, summary_en,
  description_ar, description_en, price_adult, price_child, currency, hours, lat,
  lng, partner_url, image_urls (pipe-separated, `url1|url2`), is_featured,
  is_published (`TRUE`/`FALSE`), last_verified (`YYYY-MM-DD`)
- `posts`: slug, title_ar, title_en, body_ar, body_en, cover_image, published_at,
  is_published
- `faq`: question_ar, question_en, answer_ar, answer_en, sort_order
- `settings`: key, value_ar, value_en (rows: `phone`, `email`, `address`, `lat`, `lng`, the last two are for the contact page map pin)

## Click tracking

The CTA on every waterpark/attraction detail page points straight at the partner
url (with `utm_source`/`utm_medium`/`utm_campaign` params appended) and fires
`navigator.sendBeacon('/api/click', ...)` in the background on click, so the
outbound link opens instantly even if the backend is cold. `/go/{slug}` is a
server-side 302 fallback for the same url, used when the link is shared outside
the site (an ad, a WhatsApp message), since there's no page loaded to fire a
beacon from. Both paths log to the `clicks` tab via the Apps Script webhook in
`CLICKS_WEBHOOK_URL`, see `Files/apps_script_clicks_webhook.gs` for the script
and setup steps, including a `QUERY` formula for monthly totals.

## Deploy (Render free tier)

1. Push this repo to GitHub.
2. New Web Service on Render, pointed at this repo.
3. **Root Directory: `Code/backend`** (that's where `requirements.txt` and
   `render.yaml` live, it reaches into `../frontend` for templates and static files).
4. Render reads `render.yaml` for the build/start commands automatically.
5. Set up a free uptime pinger (e.g. cron-job.org) hitting the live URL every
   ~10 minutes so the free-tier instance doesn't cold-start on the first visitor.

## What's stubbed

- **Contact form** renders fully (fields, FAQ, honeypot field) but does not
  submit anywhere yet, the submit button is disabled. Phase 4 adds validation,
  rate limiting, and SMTP sending.
- **Click tracking**: waterpark and attraction CTAs link straight to the
  `partner_url` from the sheet. No `sendBeacon`, no `/go/{slug}`, no click logging
  yet, that's Phase 3.
- **SEO extras**: `sitemap.xml`, `robots.txt`, Open Graph tags, and JSON-LD are
  Phase 5.

## What's real right now

- All pages, both languages, real server-rendered HTML.
- `/` redirects by `Accept-Language`, with a `lang` cookie override.
- RTL/LTR layout via CSS logical properties (`margin-inline-start`, not
  `margin-left`), no separate stylesheet needed for Arabic.
- `hreflang` alternate tags and a working language toggle that preserves the
  current page.
- "Last verified" date on every price, with a muted warning past 30 days.
- Real venue photos, committed to this repo and served through jsDelivr's CDN.
- Content pipeline described above, currently running on `snapshot.json` until the
  live Google Sheet is published and its urls are set.
- Leaflet + OpenStreetMap map (no API key) on the waterpark/attraction directory
  and detail pages, plus the contact page pin. Venues without lat/lng just get
  skipped instead of breaking the map.
