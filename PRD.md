# PRD — Eye of Aqaba Portal (عين العقبة)

**Version:** 0.1 (draft, pending client sign-off)
**Owner:** Awni (volunteer developer)
**Client:** Aqaba Eye / شركة عين العقبة السياحية
**Replaces:** https://eyeofaqaba.mystrikingly.com

---

## 0. Scope decision (confirmed)

The written brief and the meeting were reconciled: the brief's page/section list
stands, but two sections work differently than a literal reading suggests:

| Brief section | How it actually works |
|---|---|
| المرافق والخدمات (facilities & services) | This is the venue directory — starts as waterparks, expandable to other Aqaba activities |
| قسم حجز التذاكر / الأسعار وأوقات الزيارة (tickets/prices) | Not a real booking flow. Shows price + hours, then redirects the visitor to the venue's own site to actually book and pay |

Business model: Eye of Aqaba is the **referral portal**, not the venue. Revenue comes
from commission deals with listed venues, negotiated using click-through evidence the
site collects (see FR-4).

**Confirmed launch venues (Phase 1, content supplied via Drive folders):**
1. Saraya Aqaba Waterpark
2. Sindbad Group Jordan
3. Saraya Aqaba Beach Club

More venues (~15 additional companies) have been sent by the client and are under
consideration for a later phase — not part of the initial build.

---

## 1. Overview

A bilingual (AR/EN) web portal positioning itself as **"one gate to explore Aqaba."**
It aggregates attractions — starting with waterparks — showing current prices and
visiting hours, then redirects visitors to the operator's own website to book and pay.
The portal takes no payments and holds no bookings. Revenue comes from referral
agreements with the listed operators.

Alongside the listings, the site publishes blog content about Aqaba and places to
visit, which is what drives organic traffic to the listings.

## 2. Goals

1. Replace the current Strikingly site with a self-hosted, self-owned site.
2. Publish a working waterpark directory with prices, hours, and outbound links.
3. **Count and store every outbound click** — this is the evidence the client needs
   to negotiate commission deals with operators.
4. Give the client full ability to update prices, hours, and blog posts **without a
   developer**.
5. Rank for Aqaba tourism searches in Arabic and English.
6. Cost: **0 JOD/month**, excluding an optional domain.

## 3. Non-goals (explicitly out of scope for v1)

- Payment processing, cart, or checkout of any kind
- User accounts, login, or profiles
- Real-time price scraping from partner websites
- AI chatbot
- Native mobile app
- Multi-city coverage (Aqaba only)
- Operator self-service portal ("Add your listing")

## 4. Users

| User | Need |
|---|---|
| Tourist planning an Aqaba trip | Compare attractions, see prices, decide where to go |
| Jordanian family (Arabic-first, mobile) | Prices and hours in Arabic, fast on 4G |
| Client staff (non-technical) | Update a price without calling the developer |
| Partner operator | Proof the portal sends them real traffic |

**Mobile-first is not optional.** Assume the majority of traffic is a phone on
mobile data.

## 5. Pages (7)

| # | Route | Purpose |
|---|---|---|
| 1 | `/{lang}/` | Hero, what the portal is, featured waterparks, latest posts |
| 2 | `/{lang}/waterparks` | Directory: cards with price, hours, CTA |
| 3 | `/{lang}/waterparks/{slug}` | Detail: gallery, description, price table, hours, map, CTA |
| 4 | `/{lang}/explore` | Blog index — places to visit in Aqaba |
| 5 | `/{lang}/explore/{slug}` | Blog post |
| 6 | `/{lang}/about` | The project, the mission, the team |
| 7 | `/{lang}/contact` | Contact info, interactive map, inquiry form, FAQ |

Plus non-page routes:
- `/` → 302 to `/ar/` or `/en/` based on `Accept-Language`
- `/go/{slug}` → 302 to partner URL, logs the click
- `/sitemap.xml`, `/robots.txt`

## 6. Functional requirements

### FR-1 — Language handling
- Every page exists at `/ar/...` and `/en/...`
- `/` inspects `Accept-Language`; Arabic → `/ar/`, anything else → `/en/`
- Language choice stored in a cookie; the cookie wins over the header on return visits
- `dir="rtl"` + Arabic font stack on `/ar/`, `dir="ltr"` on `/en/`
- Visible language toggle in the header that preserves the current page
- `<link rel="alternate" hreflang="...">` on every page

### FR-2 — Content management (Google Sheets)
The client edits one Google Spreadsheet. Tabs:

- **`waterparks`** — slug, name_ar, name_en, summary_ar, summary_en, description_ar,
  description_en, price_adult, price_child, currency, hours, lat, lng, partner_url,
  image_urls, is_featured, is_published, last_verified
- **`posts`** — slug, title_ar, title_en, body_ar, body_en, cover_image, published_at,
  is_published
- **`faq`** — question_ar, question_en, answer_ar, answer_en, sort_order
- **`settings`** — key, value_ar, value_en (phone, email, address, social links)

Backend fetches each tab as published CSV, caches in memory with a ~10 minute TTL.
On fetch failure, serve the last good cache; if none, serve a committed JSON snapshot.
**The site must never go down because a spreadsheet was edited badly.**

### FR-3 — Price honesty
Every price displays a **"Last verified: {date}"** label from `last_verified`.
If the date is older than 30 days, show a muted "prices may have changed" note.
No scraping. Prices are entered by hand — there are only a handful of relevant
operators in Aqaba, so this is entirely tractable.

### FR-4 — Outbound redirect and click tracking
- CTA renders as a real `<a href>` pointing **directly** at the partner URL with UTM
  params appended (`utm_source=eyeofaqaba&utm_medium=referral&utm_campaign={slug}`),
  `target="_blank" rel="noopener"`
- On click, fire `navigator.sendBeacon('/api/click', {...})` — non-blocking
- `/go/{slug}` also exists as a server-side 302 fallback for links shared elsewhere
- Every click stores: slug, timestamp, language, referrer, coarse user agent
- **No user waits on our backend to reach a partner site.** The direct href means a
  cold-started free-tier server never blocks the one action that earns money.

**Storage:** append click rows to a `clicks` tab in the same Google Spreadsheet via a
Google Apps Script webhook. Free, durable across redeploys, and the client can read
their own numbers in a spreadsheet. (Upgrade path: Supabase free Postgres.)

### FR-5 — Contact form
- Fields: name, email, phone (optional), message, honeypot anti-spam field
- Server-side validation; rate limit by IP
- Sends via SMTP to the client's inbox
- Success and error states rendered in the active language

### FR-6 — Map
Leaflet + OpenStreetMap tiles. No API key, no billing account. Markers for each
published waterpark on the directory page; single marker on detail and contact pages.

### FR-7 — Gallery
Images referenced by URL from the sheet. Lazy loading, explicit width/height to avoid
layout shift, `alt` text in the active language. Placeholder images (free-licence
stock) until the client supplies real photography.

### FR-8 — SEO
Server-rendered HTML (not client-side JS rendering). Per-page `<title>` and
description in both languages, Open Graph tags, `LocalBusiness`/`TouristAttraction`
JSON-LD on detail pages, generated `sitemap.xml`.

## 7. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI (Python) | Chosen by developer; fast to write |
| Templating | Jinja2, server-rendered | SEO — a content site rendered in JS will not rank |
| Frontend | Plain HTML/CSS/vanilla JS | No build step, no framework to maintain after handover |
| i18n | Jinja2 + `ar.json` / `en.json` dictionaries | No library needed |
| Map | Leaflet + OSM | Free, keyless |
| Content store | Google Sheets (published CSV) | Client already knows spreadsheets |
| Click log | Google Apps Script webhook → Sheets | Free, survives redeploys, client-readable |
| Email | SMTP (Gmail app password or Resend free tier) | No DB needed for enquiries |
| Hosting | Render free tier + free uptime pinger | One deploy; pinger defeats the 15-min spin-down |
| Repo | GitHub, public | Handover, and Render deploys from it |

**Deliberately rejected:** n8n (hosting burden, solves a problem this project does not
have), React/Next (build step and framework churn for a 7-page content site),
scraping (fragile, hostile to partners, unnecessary at this scale).

## 8. Success metrics

- Site live on a real URL, all 7 pages, both languages
- Lighthouse mobile performance ≥ 85, accessibility ≥ 90
- Client updates a price themselves, unassisted, at least once before handover
- Outbound clicks recorded and visible to the client
- No monthly cost

## 9. Risks

| Risk | Mitigation |
|---|---|
| Scope mismatch (section 0) | Written sign-off before Phase 1 ends |
| Client never supplies real content | Ship with placeholders; site works regardless |
| Client can't maintain it after handover | Sheets CMS + written guide + one live training session |
| Free tier cold starts | Uptime pinger; outbound CTAs bypass the backend entirely |
| No partner deals exist yet | Click log from day one gives them the negotiating evidence |
| Volunteer leaves | Public repo, plain stack, no proprietary services, written docs |

## 10. Open questions for the client

Resolved:
- ~~Brief version or portal version?~~ → Reconciled, see section 0
- ~~Which waterparks go in the first launch?~~ → Saraya Aqaba Waterpark, Sindbad Group Jordan, Saraya Aqaba Beach Club
- ~~Who receives the contact form emails?~~ → Eyeofaqaba@gmail.com
- ~~Logo?~~ → Keeping the current one as-is

Still open:
1. Do you own a domain, or should the site launch on a free subdomain?
2. Are any partner/commission agreements signed, or is that still ahead?
3. Who on your side will own updating the spreadsheet after handover?
4. The ~15 additional venues sent by the client — which of these (if any) join
   later phases, and in what order?

## 11. Handover requirements

Launch is not the finish line. Handover includes:
- Public GitHub repo, with the client added as an owner or admin
- All accounts (hosting, email sender, spreadsheet) owned by the **client's** email,
  not the developer's
- `HANDOVER.md`: how to update a price, publish a post, read the click numbers,
  redeploy
- One live walkthrough session with whoever will maintain it
