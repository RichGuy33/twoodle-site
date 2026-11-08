# Twoodle SEO playbook (read this first)

Site: https://twoodle.app (static HTML, no build). Repo root is the site root.
Cloudflare Pages auto-deploys every push to `main`. App: Twoodle, a couples doodle-widget iPhone app by Taking Flight, Inc.
App Store: https://apps.apple.com/us/app/twoodle-couples-widgets/id6789469881

## The daily job: ONE quality guide per run
1. Pick the keyword.
   - If Search Console data is reachable (Chrome, property `sc-domain:twoodle.app`, Performance report, last 28 days), pick the best query with impressions but no dedicated page, or a page ranking 8-30 that deserves a stronger guide.
   - Otherwise take the next unchecked item in the backlog below.
2. Check the live search results with WebSearch (standard mode). Write something more useful and more honest than what ranks.
3. Create `guides/<slug>/index.html` by copying the structure of `guides/lovebox-alternative-app/index.html` (head meta, canonical, Article JSON-LD, FAQPage JSON-LD, footer). 900-1500 words, scannable, real answers.
4. Internal links: link the new guide from `guides/index.html` (new card), from the home page guide cards if it is one of the best, and add 2+ contextual links from existing related guides to it. Link out of it to 2+ related guides.
5. CTA: one inline CTA and one end-of-article CTA to the App Store link.
6. Add the URL to `sitemap.xml` with today's `lastmod`; bump `lastmod` on any page you edited.
7. Run `python3 scripts/check_site.py .` and fix every error.
8. Commit to `main` with a clear message and push. Cloudflare deploys automatically (about a minute).
9. In Search Console (if reachable), use URL inspection -> Request indexing for the new URL.

## Accuracy rules (non-negotiable)
- iPhone only, iOS 18+. Android is NOT available. Free download; Twoodle Pro unlocks pairing: $3.99/week with 3-day trial, or $49.99/year; one subscription covers both partners. Re-verify on the App Store page before quoting prices.
- Doodles go to the partner's **Home Screen widget only** (not the Lock Screen). Lock Screen has widgets: Love Note (Lock or Home Screen), Days Together (Lock Screen), optional Distance widget. Live "draw together" uses a Lock-Screen-styled shared canvas inside the app.
- Other features: Mood, Distance Bubbles, nudges, gallery, important dates. Account is auto-created (no sign-up). Delete via Settings -> Delete my account.
- Privacy: no ads, no selling data, no cross-app tracking. Location only if the Distance widget is enabled.
- Competitor posts must be honest and factual: include "when <competitor> is better", disclose that Twoodle is our app, no invented stats, no fake reviews, no disparagement. Check competitor claims on their store pages.
- Do not claim features Twoodle lacks. If unsure, leave it out.

## Backlog (mark [x] when published)
- [x] draw-on-partners-lock-screen
- [x] lovebox-alternative-app
- [ ] couple-joy-alternative
- [ ] noteit-loklok-alternative (widget doodle apps compared)
- [ ] days-together-lock-screen-counter (relationship day counter widget how-to)
- [ ] best-doodle-apps-for-couples
- [ ] widgetable-alternative (crowded)
- [ ] best-long-distance-relationship-apps (crowded)
- [ ] love-note-widget-ideas / things to doodle for your partner
- [ ] how-to-add-couples-widget-iphone-home-screen
- [ ] long-distance-anniversary / date ideas that use widgets (only if it can be genuinely useful)

When the backlog runs low, add new keyword ideas from Search Console queries or from real People Also Ask results.
