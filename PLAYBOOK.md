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

## Voice: warm, funny, direct-response email copywriter
Write like a witty friend who happens to write killer sales emails (the Ben Settle / classic email-copywriter school), talking to ONE person about their relationship. Capture the feel, never copy anyone's phrasing.

Do:
- Open with a hook: a tiny story, a confession, a blunt claim, or a funny observation. Never "In today's fast-paced world" or "Whether you're X or Y".
- Short paragraphs. Often one line. Vary rhythm: a long sentence, then a punch.
- Talk to "you". Use contractions. First person plural ("we built...") is fine; Jason is an indie dev, so a little "small team, one very opinionated founder" charm is on-brand.
- Be opinionated and specific. Take a side, then back it up with real detail (what the feature does, what it costs, where it falls short).
- Humor is warm, self-deprecating and observational (couples habits, long-distance absurdity, bad doodle skills). Never mean, never at a partner's expense, never edgy.
- Open loops and curiosity: tease something useful, deliver it a few paragraphs later. Use plain subheads that are fun but still say what the section is about (Google reads them).
- Finish with a P.S. that has the CTA, one line, with personality.
- Tell small true stories or hypotheticals clearly framed as such ("Picture this:"). Never invent a real person, quote or testimonial.

Don't:
- No fake scarcity, fake deadlines, fake social proof, fear-mongering or manipulation. The email-copywriter craft here is the voice and storytelling, not the tricks.
- No hype words (revolutionary, game-changing, unlock, seamless), no emoji walls, no "In conclusion", no listicle filler.
- Do not sacrifice the answer. The guide must still fully answer the search query within the first screen or two; the personality is the delivery, not a delay. Clear steps, tables and FAQ sections stay.
- Do not weaken the Accuracy rules below. Funny never beats correct.

Self-check before pushing: read the intro aloud. If it could be pasted into any other app's blog unchanged, rewrite it. Cut every sentence that doesn't earn its place.

## Entity consistency (helps Google and AI assistants know what Twoodle is)
- Always write the name as "Twoodle" (app: "Twoodle: Couples Widgets"), publisher "Taking Flight, Inc.", and describe it the same way: an iPhone app for couples that sends doodles to a partner's Home Screen widget, with Lock Screen widgets for love notes and days together.
- Link the App Store page the same way every time. Keep the Organization/SoftwareApplication markup on the home page in sync with what the guides say.
- Prefer plain factual sentences that answer a question in the first 2 lines of a section. Those get quoted by search and AI answers.

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
- [x] best-apps-for-couples-widgets (published 2026-11-08; originally: honest roundup of 6-8 apps incl. Twoodle, disclosed, each with real pros/cons and "best for"; check each app's store page; Twoodle must not always come first)
- [x] couple-joy-alternative (published 2026-11-09)
- [x] noteit-loklok-alternative (published 2026-11-10) (widget doodle apps compared)
- [x] days-together-lock-screen-counter (published 2026-11-10) (relationship day counter widget how-to)
- [x] widgetable-alternative (published 2026-11-11)
- [x] best-long-distance-relationship-apps (published 2026-11-12)
- [x] things-to-doodle-for-your-partner (published 2026-11-13)
- [ ] how-to-add-couples-widget-iphone-home-screen (NEXT)
- [ ] long-distance-anniversary / date ideas that use widgets (only if it can be genuinely useful)

When the backlog runs low, add new keyword ideas from Search Console queries or from real People Also Ask results.
