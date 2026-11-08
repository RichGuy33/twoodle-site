import json, os, re, sys
from html.parser import HTMLParser
root = sys.argv[1]
errors = []
pages = []
for d, _, fs in os.walk(root):
    for f in fs:
        if f.endswith(".html"):
            pages.append(os.path.join(d, f))
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ld=[]; s._ld=False; s.title=False; s.t=""
    def handle_starttag(s, tag, a):
        a=dict(a)
        if tag in ("a","link") and a.get("href"): s.links.append(a["href"])
        if tag=="script" and a.get("type")=="application/ld+json": s._ld=True
        if tag=="title": s.title=True
    def handle_endtag(s, tag):
        if tag=="script": s._ld=False
        if tag=="title": s.title=False
    def handle_data(s, data):
        if s._ld: s.ld.append(data)
        if s.title: s.t+=data
for p in sorted(pages):
    h = open(p, encoding="utf-8").read()
    ps = P(); ps.feed(h)
    rel = os.path.relpath(p, root)
    for j in ps.ld:
        try: json.loads(j)
        except Exception as e: errors.append(f"{rel}: bad JSON-LD: {e}")
    for l in ps.links:
        if l.startswith("/") and not l.startswith("//"):
            path = l.split("#")[0].split("?")[0]
            cand = os.path.join(root, path.lstrip("/"))
            if not (os.path.isfile(cand) or os.path.isfile(os.path.join(cand, "index.html"))):
                errors.append(f"{rel}: broken internal link {l}")
        elif l.startswith("mailto:") or l.startswith("https://"):
            pass
        else:
            errors.append(f"{rel}: odd link {l}")
    print(f"{rel}: title={ps.t.strip()!r} links={len(ps.links)} jsonld={len(ps.ld)}")
print("ERRORS:" if errors else "no errors"); [print(" ", e) for e in errors]
