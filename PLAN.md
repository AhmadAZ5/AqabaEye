# Build Plan — Eye of Aqaba Portal

A volunteer project has one failure mode above all others: it gets 80% built, the
volunteer gets busy, and nothing ever ships. This plan is ordered to make that
impossible — **something real is live and public from day one**, and every phase
after that adds to a site that already works.

---

## Rules for this project

1. **Deploy on day one, not at the end.** A hello-world FastAPI app on a live URL
   before any feature is written. Every phase ends with a deploy.
2. **The site must never require you.** Every content decision goes into the
   spreadsheet, never into the code.
3. **Placeholders are shipped features.** Never block on the client sending content.
4. **No new account, service, or dependency that costs money — ever.**
5. **Commit small, push often.** The repo is the handover.
6. **When unsure between simple and clever, ship simple.** You will not be here to
   maintain clever.

---

## Phase 0 — Alignment (before any code) — DONE

- [x] Scope reconciled: brief's page structure stands, "facilities" = venue
      directory, "tickets" = price/hours + redirect to venue's own site
- [x] Launch venues confirmed: Saraya Aqaba Waterpark, Sindbad Group Jordan, Saraya
      Aqaba Beach Club (content in shared Drive folders)
- [x] Contact form destination: Eyeofaqaba@gmail.com
- [x] Logo: keeping current one
- [ ] Still open (not blockers): domain ownership, who owns Sheet updates post-handover
- [ ] ~15 additional venues sent by client — parked for a later phase, not Phase 1

**Exit:** you know which product you're building. Cleared — move to Phase 1.

---

## Phase 1 — Skeleton and live deploy

- [ ] GitHub repo, public, MIT or similar
- [ ] FastAPI app, Jinja2 templates, static file mount
- [ ] Base layout: header with language toggle, nav, footer
- [ ] All 7 routes exist and return a real page (content can be lorem ipsum)
- [ ] i18n: `locales/ar.json`, `locales/en.json`, a `t()` helper in templates
- [ ] `/` → 302 to `/ar/` or `/en/` via `Accept-Language`, cookie override
- [ ] RTL/LTR switching correct on both sides
- [ ] Mobile-first CSS, no framework
- [ ] Deploy to Render, confirm the live URL loads on a phone
- [ ] Uptime pinger configured (cron-job.org, every 10 minutes)

**Exit:** a stranger can open the URL on their phone in Arabic and click through
seven pages.

---

## Phase 2 — Content pipeline

- [ ] Create the Google Spreadsheet with the four tabs from PRD FR-2
- [ ] Publish each tab to the web as CSV
- [ ] `sheets.py`: fetch, parse, cache with TTL, fall back to last-good, then to a
      committed JSON snapshot
- [ ] Add the 3 confirmed venues as rows: Saraya Aqaba Waterpark, Sindbad Group
      Jordan, Saraya Aqaba Beach Club — pull whatever's usable from their Drive
      folders, placeholder text/images for anything missing
- [ ] Add 3 placeholder blog posts
- [ ] Waterpark directory page renders from the sheet
- [ ] Waterpark detail page renders from the sheet
- [ ] Blog index and post pages render from the sheet
- [ ] `is_published` respected everywhere; unpublished rows 404
- [ ] "Last verified" date visible on every price
- [ ] Edit a value in the sheet, wait for cache expiry, confirm it changes live

**Exit:** you can change the entire site's content without touching code.

---

## Phase 3 — The money feature

This is the part the client's business model actually depends on. Give it real care.

- [ ] CTA button: direct `<a href>` to partner URL with UTM params, `target="_blank"`
- [ ] `sendBeacon` click logging to `/api/click`
- [ ] `/go/{slug}` server-side 302 fallback
- [ ] Google Apps Script webhook writing click rows to a `clicks` tab
- [ ] Verify: a click from a phone appears as a row in the spreadsheet
- [ ] Verify: the partner site opens **instantly**, even when the backend is cold
- [ ] Simple monthly totals so the client can read the numbers without a formula

**Exit:** the client can open a spreadsheet and see how many people they sent to each
operator. That number is what turns a conversation into a commission agreement.

---

## Phase 4 — Interaction and trust

- [ ] Contact form: validation, honeypot, IP rate limit, SMTP send
- [ ] Success and error states in both languages
- [ ] Leaflet map: directory overview, detail marker, contact page marker
- [ ] FAQ section rendered from the sheet
- [ ] Gallery: lazy loading, sized images, bilingual alt text
- [ ] 404 and 500 pages, in both languages

---

## Phase 5 — Polish and launch

- [ ] Bilingual meta titles and descriptions on every page
- [ ] Open Graph tags, JSON-LD on detail pages
- [ ] Generated `sitemap.xml`, `robots.txt`, `hreflang` tags
- [ ] Lighthouse mobile: performance ≥ 85, accessibility ≥ 90
- [ ] Test on a real Android phone on mobile data, in Arabic
- [ ] Swap placeholders for whatever real content has arrived
- [ ] Domain pointed, or free subdomain confirmed

---

## Phase 6 — Handover (the phase everyone skips)

- [ ] Transfer ownership: repo, hosting, spreadsheet, email sender — all to the
      **client's** accounts
- [ ] Write `HANDOVER.md` in Arabic and English: update a price, publish a post, read
      click numbers, redeploy, who to call
- [ ] One live session walking their person through editing the sheet
- [ ] Have them make one real edit while you watch, without touching the keyboard

**Exit:** you could disappear tomorrow and the site would keep working.

---

## What to say no to

The client has zero experience with websites, which means requests will arrive that
sound small and are not. Some that are likely:

| If they ask for | Answer |
|---|---|
| "Can it book and take payment?" | Not in v1 — that needs a payment provider, a merchant account, and legal terms |
| "Can prices update automatically?" | No. Scraping partner sites breaks constantly and may violate their terms. Manual entry, with a visible verified date |
| "Can we add hotels/restaurants/tours too?" | After waterparks are live and working. Same structure, just more rows |
| "Can we add an AI chatbot?" | Costs money per message. FAQ page first — it answers the same questions for free |
| "Can we cover all of Jordan?" | Aqaba first. Prove the model on one city |

None of these are refusals — they're sequencing. Say "yes, after launch," and mean it.
