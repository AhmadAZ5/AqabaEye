# Claude Code prompt

Put `PRD.md` and `PLAN.md` in the repo root first, then paste the block below.

---

Read `PRD.md` and `PLAN.md` in this directory before writing any code. They are the
source of truth — if anything I say here contradicts them, follow them and tell me.

Build **Phase 1 only** (see PLAN.md). Do not build Phases 2–6 yet. I want to review
and deploy before we go further.

## What this is

A bilingual (Arabic/English) tourism portal for Aqaba, Jordan. Server-rendered
FastAPI + Jinja2. It lists attractions and redirects visitors to operators' own
websites. It takes no payments and stores no user accounts.

## Hard constraints

- **Python + FastAPI + Jinja2, server-rendered HTML.** No React, no Next, no SPA.
  This site lives or dies on SEO and it must work with JS disabled.
- **No build step.** Plain CSS and vanilla JS served as static files. No npm, no
  bundler, no Tailwind CLI, no PostCSS.
- **No paid service, no service requiring a credit card, no API key that costs money.**
- **Mobile-first.** Most visitors are on a phone in Arabic on mobile data.
- **Arabic is a first-class language, not an afterthought.** Full RTL layout, not a
  mirrored hack. Test that the Arabic side looks intentional.
- Keep dependencies minimal: `fastapi`, `uvicorn`, `jinja2`, `httpx`,
  `python-multipart`. Justify anything else before adding it.

## Phase 1 deliverables

**Project structure**

```
app/
  main.py            # FastAPI app, routes
  i18n.py            # translation loader + t() helper
  config.py          # settings from env vars
  templates/
    base.html
    home.html  waterparks.html  waterpark_detail.html
    explore.html  post.html  about.html  contact.html
    partials/  (header, footer, lang_toggle, card)
  static/
    css/main.css
    js/main.js
    img/
locales/
  ar.json
  en.json
requirements.txt
render.yaml
.env.example
README.md
```

**Routing**
- `/` → 302 to `/ar/` or `/en/` based on the `Accept-Language` header. A `lang`
  cookie, if present, takes priority over the header.
- All seven pages from PRD section 5 exist under both `/ar/` and `/en/` and return
  real rendered HTML.
- Language toggle in the header switches language while staying on the same page.

**i18n**
- `locales/ar.json` and `locales/en.json` hold every UI string. No hardcoded
  user-facing text in templates.
- A `t(key)` helper available in all templates.
- `<html lang dir>` set correctly. Arabic gets an appropriate font stack (system
  Arabic fonts — do not pull a webfont from a CDN that may be slow in Jordan).
- `<link rel="alternate" hreflang>` tags on every page.

**Content for now**
- Hardcode placeholder data in a single `app/placeholder_data.py` module, shaped
  **exactly** like the Google Sheets schema in PRD FR-2. Phase 2 will swap the data
  source without touching the templates, so keep that seam clean.
- Use these 3 real confirmed venue names as the entries (real names, placeholder
  everything else — description, price, hours, images):
  1. Saraya Aqaba Waterpark
  2. Sindbad Group Jordan
  3. Saraya Aqaba Beach Club
- For `partner_url` on each, leave a clearly marked placeholder
  (e.g. `"https://example.com/PLACEHOLDER-saraya-waterpark"`) — real links come later.
- Use free-licence placeholder images or plain CSS gradient blocks. Do not hotlink
  images from sites that may block us.
- Contact form destination (for later phase, but note it in config now):
  `Eyeofaqaba@gmail.com`.

**Styling**
- One `main.css`, CSS custom properties for colours and spacing, logical properties
  (`margin-inline-start`, not `margin-left`) so RTL works without a second stylesheet.
- Give it an actual visual identity — Red Sea and desert palette, generous spacing,
  real typographic hierarchy. It should not look like an unstyled Bootstrap template.
- No CSS framework.

**Deployment**
- `render.yaml` for Render free tier.
- `README.md`: local run instructions, env vars, deploy steps.

## How to work

- Start by showing me the file tree and your CSS colour/type choices before writing
  the bulk of the code.
- Build in small commits I can follow.
- When you hit an ambiguity, ask instead of inventing a requirement.
- Do not add features from later phases, however tempting. No contact form logic, no
  Google Sheets integration, no click tracking, no map yet.
- At the end, tell me exactly what to run to see it locally, and what is stubbed.
