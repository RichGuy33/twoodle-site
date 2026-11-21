# Twoodle SEO playbook (read this first)

Site: https://twoodle.app (static HTML, no build). Repo root is the site root.
Cloudflare Pages auto-deploys every push to `main`. App: Twoodle, a couples doodle-widget iPhone app by Taking Flight, Inc.
App Store: https://apps.apple.com/us/app/twoodle-couples-widgets/id6789469881

## The daily job: ONE new English guide per run (plus translations, see Translations below)
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

## Translations (added 2026-11-19, Jason's instruction; this OVERRIDES "ONE guide per run")
Languages: es (Spanish, /es/guias/), pt (Portuguese-BR leaning, /pt/guias/), fr (French, /fr/guides/), de (German, /de/ratgeber/).
Every daily run now does BOTH:
1. Publish the new English guide as before, then publish its translation in all 4 languages (5 pages total for the new guide).
2. Catch-up: also translate at least 2 not-yet-translated existing English guides into all 4 languages (oldest first, by the order of the backlog below) until every English guide has all 4 translations. Check `scripts/translations.json` (English slug -> languages done) to see what is missing.
How:
- Do NOT machine-copy: localize. Re-pick the keyword in the target language (search the SERP in that language), adapt idioms, jokes and examples, and use a localized slug (ascii, lowercase, hyphens). Keep the playbook voice, accuracy rules and CTA structure. Same facts: iPhone only, Home Screen doodles, prices in USD (say "US App Store prices, may vary in your country"), no Android, "check the App Store for the languages the app is available in" (we have NOT confirmed the app UI is localized; never claim it is or isn't).
- Build each page with `scripts/i18n.py` -> `build_page(lang, english_slug, localized_slug, content_dict)` (see the function docstring; a worked example of the content dict is any existing page's structure: title, desc, og_desc, h1, disclosure, body_html with the `{CTA1}` token, faq list, cta1, cta2, ps_html). Write your content/build script in the scratchpad, not in the repo.
- Then run `python3 scripts/i18n.py .` (rewrites links to translated versions, adds hreflang to English + translated pages, regenerates the 4 language index pages, adds new URLs to sitemap.xml). Then `python3 scripts/check_site.py .`.
- Links inside translated pages point at English guides until the translation exists; the script adds an "(in English)" note automatically and swaps to the translated page once it is built. Write links in the body as plain `/guides/<english-slug>/`.
- Request indexing in Search Console for the new English URL and as many translated URLs as time allows (URL inspection box at the top of the Overview page; paste URL, Enter, then Request indexing).
- Fonts are latin subset: fine for es/pt/fr/de. Do not add non-latin languages without adding fonts.
- Flag in the final summary that native-speaker review is still advisable.

## Indexing queue (request these first, then delete the lines)
Not yet requested as of 2026-11-21 (Search Console indexing was not attempted this run): /guides/how-often-should-long-distance-couples-talk/, /guides/long-distance-countdown-until-we-meet/, /fr/guides/questions-relation-a-distance/, /de/ratgeber/fragen-fernbeziehung/, all translated URLs of 2026-11-20 and 2026-11-21 (es/pt/fr/de of countdown, draw-on-partners-lock-screen, lovebox-alternative-app, how-often-should-long-distance-couples-talk, best-apps-for-couples-widgets, couple-joy-alternative), and the 4 language index pages.
Tips: after pressing Enter wait up to ~60s for the "Retrieving data" dialog; if it says "Something went wrong", retry once.
Next catch-up (oldest first): noteit-loklok-alternative, days-together-lock-screen-counter (a Spanish query 'como poner los dias de relacion en iphone' already shows impressions), widgetable-alternative, ...

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
- [x] how-to-add-couples-widget-iphone-home-screen (published 2026-11-14)
- [x] long-distance-date-ideas (published 2026-11-16; keyword source: Search Console LDR query cluster)
- [x] how-to-stay-connected-in-a-long-distance-relationship (published 2026-11-16; keyword source: Search Console LDR query cluster + People Also Ask)
- [x] short-love-notes-for-your-partner (published 2026-11-16; keyword source: backlog empty, Search Console tab did not load; chosen from SERP check on couple-widget notes)
- [x] long-distance-relationship-time-zones (published 2026-11-17; keyword source: Search Console LDR query cluster, gap in existing LDR guides; SERP checked)
- [x] long-distance-relationship-gift-ideas (published 2026-11-18; keyword source: Search Console LDR query cluster, all exact queries already covered so chose adjacent LDR gap; SERP not deeply checked)
- [x] long-distance-relationship-questions (published 2026-11-19; keyword source: Search Console LDR query cluster (all exact queries already covered), chose adjacent gap; SERP checked: crowded with 100-500 question lists, so angle is 30 questions sorted by moment)
- [x] long-distance-countdown-until-we-meet (published 2026-11-20; keyword source: Search Console LDR cluster, exact queries covered so chose adjacent gap; SERP not checked)
- [x] how-often-should-long-distance-couples-talk (published 2026-11-21; keyword source: Search Console showed only 16 queries, all already covered, so chose adjacent LDR gap; SERP checked)
- [ ] (backlog empty: add ideas from Search Console queries; note Chrome is always signed in to Search Console, always use it)

When the backlog runs low, add new keyword ideas from Search Console queries or from real People Also Ask results.
