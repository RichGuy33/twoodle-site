#!/usr/bin/env python3
"""Generate plain-Markdown copies of every guide plus llms.txt (same content as the HTML, not a different version).
Run after i18n.py:  python3 scripts/make_md.py .   (needs beautifulsoup4)
- writes <guide-dir>/index.md next to each guide's index.html (English + translated)
- adds <link rel="alternate" type="text/markdown"> to each guide's <head>
- writes /llms.txt (index of guides, English first, translations grouped)
"""
import os, re, sys, json
from bs4 import BeautifulSoup, NavigableString
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SITE = "https://twoodle.app"
FOLDERS = {"": "guides", "es": "guias", "pt": "guias", "fr": "guides", "de": "ratgeber"}

def md_inline(node):
    out = ""
    for c in node.children:
        if isinstance(c, NavigableString): out += str(c)
        elif c.name in ("strong", "b"): out += f"**{md_inline(c).strip()}**"
        elif c.name in ("em", "i"): out += f"*{md_inline(c).strip()}*"
        elif c.name == "a":
            href = c.get("href", ""); href = SITE + href if href.startswith("/") else href
            out += f"[{md_inline(c).strip()}]({href})"
        elif c.name == "br": out += "\n"
        elif c.get("class") and "en" in c.get("class"): out += md_inline(c)
        else: out += md_inline(c)
    return re.sub(r"[ \t]+", " ", out)

def md_block(el, depth=0):
    lines = []
    for c in el.children:
        if isinstance(c, NavigableString): continue
        n = c.name
        if n in ("h1", "h2", "h3", "h4"): lines.append("#" * int(n[1]) + " " + md_inline(c).strip() + "\n")
        elif n == "p":
            t = md_inline(c).strip()
            if t: lines.append(t + "\n")
        elif n in ("ul", "ol"):
            for i, li in enumerate(c.find_all("li", recursive=False), 1):
                lines.append((f"{i}. " if n == "ol" else "- ") + md_inline(li).strip())
            lines.append("")
        elif n == "table":
            rows = [[md_inline(x).strip().replace("|", "/") for x in r.find_all(["th", "td"])] for r in c.find_all("tr")]
            if rows:
                lines.append("| " + " | ".join(rows[0]) + " |"); lines.append("|" + "---|" * len(rows[0]))
                for r in rows[1:]: lines.append("| " + " | ".join(r) + " |")
                lines.append("")
        elif n == "div":
            if c.get("class") and "cta" in c.get("class"):
                h = c.find("h3"); p = c.find("p"); a = c.find("a")
                lines.append(f"> **{h.get_text(strip=True) if h else ''}** {p.get_text(' ', strip=True) if p else ''} [{a.get_text(strip=True)}]({a['href']})\n" if a else "")
            elif c.get("class") and "note" in c.get("class"): lines.append("> " + md_inline(c).strip() + "\n")
            else: lines += md_block(c, depth + 1)
        elif n in ("section", "article"): lines += md_block(c, depth + 1)
    return lines

pages = []  # (lang, dir)
for lang, folder in FOLDERS.items():
    base = os.path.join(ROOT, lang, folder) if lang else os.path.join(ROOT, folder)
    if not os.path.isdir(base): continue
    for d in sorted(os.listdir(base)):
        if os.path.isfile(os.path.join(base, d, "index.html")): pages.append((lang, folder, d))

info = {}
for lang, folder, slug in pages:
    p = os.path.join(ROOT, lang, folder, slug, "index.html") if lang else os.path.join(ROOT, folder, slug, "index.html")
    html = open(p, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    art = soup.find("article")
    if not art: continue
    url = f"{SITE}/{lang + '/' if lang else ''}{folder}/{slug}/"
    desc = (soup.find("meta", attrs={"name": "description"}) or {}).get("content", "")
    h1 = art.find("h1").get_text(strip=True)
    body = [l for l in md_block(art.find("div") or art)]
    text = "\n".join(body)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"^# .*\n+", "", text) if False else text
    md = f"---\ntitle: {json.dumps(h1, ensure_ascii=False)}\nurl: {url}\nlanguage: {lang or 'en'}\npublisher: Taking Flight, Inc.\n---\n\n{text}\n"
    open(p[:-len("index.html")] + "index.md", "w", encoding="utf-8").write(md)
    link = f'<link rel="alternate" type="text/markdown" href="{url}index.md">\n'
    html2 = re.sub(r'<link rel="alternate" type="text/markdown"[^>]*>\n?', "", html)
    html2 = re.sub(r'(<link rel="canonical" href="[^"]*">\n)', lambda m: m.group(1) + link, html2, count=1)
    if html2 != html: open(p, "w", encoding="utf-8").write(html2)
    info[(lang, slug)] = (h1, desc, url)

lines = ["# Twoodle", "",
 "> Twoodle (Twoodle: Couples Widgets) is a couples app by Taking Flight, Inc. that lets couples send doodles to each other's Home Screen widget, with Lock Screen widgets for love notes and days together. Available for iPhone (iOS 18+) and Android; widget details here describe the iPhone app. Free to download; Twoodle Pro unlocks pairing.",
 "", f"About (publisher and sources): https://twoodle.app/about/", "",
 "App Store: https://apps.apple.com/us/app/twoodle-couples-widgets/id6789469881","", "Google Play: https://play.google.com/store/apps/details?id=app.rork.nvhca9qbywihzi01pvnox&hl=en_US", "",
 "Each guide is available as plain Markdown (same content as the HTML page) by appending index.md to its URL.", "",
 "## Video", "", "- [I Tested 6 Couple Widget Apps, and Only One Does This (iPhone 2026)](https://www.youtube.com/watch?v=zZiUwmBjRcw): 6 min 25 s video version of the best couples widget apps guide (English).", "", "## Guides (English)", ""]
for (lang, slug), (h1, desc, url) in info.items():
    if lang == "": lines.append(f"- [{h1}]({url}index.md): {desc}")
for lang, name in [("es", "Español"), ("pt", "Português"), ("fr", "Français"), ("de", "Deutsch")]:
    items = [(h1, desc, url) for (l, s), (h1, desc, url) in info.items() if l == lang]
    if items:
        lines += ["", f"## {name}", ""] + [f"- [{h1}]({url}index.md): {desc}" for h1, desc, url in items]
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("md pages:", len(info))
