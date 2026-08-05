# AQABA EYE
Hi, I'm Eng Awni. This is Aqaba Eye, a bilingual (Arabic/English) portal for Aqaba, Jordan, built as volunteer work for EntroGate.

The idea is simple: one place to see Aqaba's waterparks and attractions with real prices and hours, then get sent straight to the operator's own site to actually book. No middleman payments, no bookings held here, just a clean directory that points you the right way.

Live at [aqabaeye.onrender.com](https://aqabaeye.onrender.com/).

## How it's built

Server-rendered, no build step, no framework bloat. I wanted something fast to ship and easy to keep maintaining without a whole toolchain in the way.

- **Backend:** FastAPI (Python)
- **Templates:** Jinja2, rendered server-side
- **Frontend:** Plain HTML, CSS, and JS, no framework
- **i18n:** JSON locale files (`ar.json` / `en.json`) with a small `t()` helper, full RTL/LTR support
- **Images:** committed to this repo, served through jsDelivr's CDN
- **Hosting:** Render, free tier
