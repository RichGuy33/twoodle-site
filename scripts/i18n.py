#!/usr/bin/env python3
"""Translation tooling for twoodle.app.

Data: scripts/translations.json  {english_slug: {lang: {"slug","title","desc"}}}
Run `python3 scripts/i18n.py .` after adding/changing translated pages. It:
  1. rewrites /guides/<slug>/ links on translated pages to the translated URL when one exists
  2. (re)writes hreflang <link>s on every page that has translations
  3. regenerates the per-language guides index pages
  4. adds missing translated URLs to sitemap.xml (with hreflang-free simple entries)
Build a new translated page with: build_page() (see PLAYBOOK.md, "Translations").
"""
import json, os, re, sys, datetime, html

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SITE = "https://twoodle.app"
TODAY = datetime.date.today().isoformat()
APP = "https://apps.apple.com/us/app/twoodle-couples-widgets/id6789469881"
PLAY = "https://play.google.com/store/apps/details?id=app.rork.nvhca9qbywihzi01pvnox&amp;hl=en_US"

# folder = URL segment that replaces "guides" in each language
LANGS = {
 "es": dict(name="Español", play="Disponible en Google Play", locale="es", folder="guias", og="es_ES",
   guides="Guías", support="Soporte", privacy="Privacidad", terms="Términos", all="Todas las guías",
   by="Por el equipo de Twoodle", disc="Divulgación", read="Leer la guía", btn="Descargar Twoodle", faq="Preguntas frecuentes",
   foot="Hecho con cariño, para dos.", idx_title="Guías para parejas | Twoodle", idx_h1="Guías para <em>parejas</em>",
   idx_lead="Guías prácticas del equipo de Twoodle.", idx_desc="Guías prácticas para parejas, sobre todo a distancia, del equipo de Twoodle.",
   month="noviembre de 2026", ps="P. D.", more="Otros idiomas", en_note=" (en inglés)"),
 "pt": dict(name="Português", play="Disponível no Google Play", locale="pt", folder="guias", og="pt_BR",
   guides="Guias", support="Suporte", privacy="Privacidade", terms="Termos", all="Todos os guias",
   by="Pela equipe do Twoodle", disc="Transparência", read="Ler o guia", btn="Baixar o Twoodle", faq="Perguntas frequentes",
   foot="Feito com carinho, para dois.", idx_title="Guias para casais | Twoodle", idx_h1="Guias para <em>casais</em>",
   idx_lead="Guias práticos da equipe do Twoodle.", idx_desc="Guias práticos para casais, principalmente à distância, da equipe do Twoodle.",
   month="novembro de 2026", ps="P.S.", more="Outros idiomas", en_note=" (em inglês)"),
 "fr": dict(name="Français", play="Disponible sur Google Play", locale="fr", folder="guides", og="fr_FR",
   guides="Guides", support="Assistance", privacy="Confidentialité", terms="Conditions", all="Tous les guides",
   by="Par l'équipe Twoodle", disc="Transparence", read="Lire le guide", btn="Télécharger Twoodle", faq="Questions fréquentes",
   foot="Fait avec amour, pour deux.", idx_title="Guides pour couples | Twoodle", idx_h1="Guides pour <em>couples</em>",
   idx_lead="Des guides pratiques par l'équipe Twoodle.", idx_desc="Guides pratiques pour les couples, surtout à distance, par l'équipe Twoodle.",
   month="novembre 2026", ps="P.-S.", more="Autres langues", en_note=" (en anglais)"),
 "de": dict(name="Deutsch", play="Jetzt bei Google Play", locale="de", folder="ratgeber", og="de_DE",
   guides="Ratgeber", support="Support", privacy="Datenschutz", terms="Nutzungsbedingungen", all="Alle Ratgeber",
   by="Vom Twoodle-Team", disc="Hinweis", read="Ratgeber lesen", btn="Twoodle laden", faq="Häufige Fragen",
   foot="Mit Liebe gemacht, für zwei.", idx_title="Ratgeber für Paare | Twoodle", idx_h1="Ratgeber für <em>Paare</em>",
   idx_lead="Praktische Ratgeber vom Twoodle-Team.", idx_desc="Praktische Ratgeber für Paare, vor allem in Fernbeziehungen, vom Twoodle-Team.",
   month="November 2026", ps="P.S.", more="Weitere Sprachen", en_note=" (auf Englisch)"),
}
ORDER = ["es", "pt", "fr", "de"]

def e(s): return html.escape(s, quote=True)
def path(lang, slug): return f"/{lang}/{LANGS[lang]['folder']}/{slug}/"
def read(p): return open(os.path.join(ROOT, p.lstrip("/")), encoding="utf-8").read()
def write(p, s):
    fp = os.path.join(ROOT, p.lstrip("/")); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(s)

def load():
    return json.load(open(os.path.join(ROOT, "scripts/translations.json"), encoding="utf-8"))

def header(lang, L):
    return (f'<header class="site"><div class="wrap">\n  <a class="brand" href="/">Twoo<span>dle</span></a>\n'
            f'  <nav class="site"><a href="/{lang}/{L["folder"]}/">{L["guides"]}</a><a href="/support/">{L["support"]}</a></nav>\n</div></header>')
def footer(lang, L):
    return (f'<footer class="site"><div class="wrap">\n  <div>&copy; 2026 Taking Flight, Inc. {L["foot"]}</div>\n'
            f'  <div class="links"><a href="/{lang}/{L["folder"]}/">{L["guides"]}</a><a href="/support/">{L["support"]}</a><a href="/privacy/">{L["privacy"]}</a>'
            f'<a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" rel="noopener">{L["terms"]}</a></div>\n</div></footer>')

def build_page(lang, en_slug, slug, c):
    """c: dict(title, desc, og_desc, h1, disclosure, intro_html, body_html, faq=[(q,a)], cta1=(h3,p), cta2=(h3,p), ps_html)
    body_html may contain the token {CTA1}. Writes the page and records it in translations.json."""
    L = LANGS[lang]; url = SITE + path(lang, slug)
    faq_ld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]
    art = {"@context": "https://schema.org", "@type": "Article", "headline": c["h1"], "inLanguage": L["locale"],
           "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "Twoodle"},
           "publisher": {"@type": "Organization", "name": "Taking Flight, Inc."}, "mainEntityOfPage": url}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": L["locale"], "mainEntity": faq_ld}
    def cta(t): return (f'<div class="cta">\n    <h3>{t[0]}</h3>\n    <p>{t[1]}</p>\n    <a class="btn" href="{APP}">{L["btn"]}</a>\n    <a class="btn alt" href="{PLAY}">{L["play"]}</a>\n  </div>')
    faq_html = "\n".join(f"  <h3>{q}</h3>\n  <p>{a}</p>" for q, a in c["faq"])
    page = f'''<!doctype html>
<html lang="{L["locale"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(c["title"])}</title>
<meta name="description" content="{e(c["desc"])}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="apple-itunes-app" content="app-id=6789469881">
<meta property="og:type" content="article">
<meta property="og:locale" content="{L["og"]}">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["og_desc"])}">
<meta property="og:url" content="{url}">
<link rel="stylesheet" href="/style.css?v=3">
<script type="application/ld+json">
{json.dumps(art, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, indent=2, ensure_ascii=False)}
</script>
</head>
<body>
{header(lang, L)}

<main>
<article><div class="narrow">
  <h1>{c["h1"]}</h1>
  <p class="meta">{L["by"]} &middot; {L["month"]}</p>

  <div class="note"><strong>{L["disc"]}:</strong> {c["disclosure"]}</div>

{c["body_html"].replace("{CTA1}", cta(c["cta1"]))}

  <h2>{L["faq"]}</h2>
{faq_html}

  {cta(c["cta2"])}

  <p style="margin-top:28px"><strong>{L["ps"]}</strong> {c["ps_html"]}</p>

  <p style="margin-top:28px"><a href="/{lang}/{L["folder"]}/">&larr; {L["all"]}</a></p>
</div></article>
</main>

{footer(lang, L)}
</body>
</html>
'''
    write(path(lang, slug) + "index.html", page)
    t = load(); t.setdefault(en_slug, {})[lang] = {"slug": slug, "title": c["title"], "desc": c["desc"]}
    json.dump(t, open(os.path.join(ROOT, "scripts/translations.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)

def alt_tags(group):
    """group: {lang_or_en: url_path}"""
    out = []
    for k in ["en"] + ORDER:
        if k in group: out.append(f'<link rel="alternate" hreflang="{k}" href="{SITE}{group[k]}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{group["en"]}">')
    return "\n".join(out) + "\n"

def set_alt(page, group):
    s = read(page)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", s)
    s = re.sub(r'(<link rel="canonical" href="[^"]*">\n)', lambda m: m.group(1) + alt_tags(group), s, count=1)
    write(page, s)

def main():
    t = load(); sm = read("/sitemap.xml"); new_urls = []
    langs_present = sorted({l for v in t.values() for l in v}, key=ORDER.index)
    # 1+2: link rewrite and hreflang
    for en, v in t.items():
        group = {"en": f"/guides/{en}/"}
        for l, d in v.items(): group[l] = path(l, d["slug"])
        set_alt(group["en"] + "index.html", group)
        for l, d in v.items():
            set_alt(group[l] + "index.html", group)
    for l in langs_present:
        mp = {f"/guides/{en}/": path(l, v[l]["slug"]) for en, v in t.items() if l in v}
        for v in t.values():
            if l in v:
                p = path(l, v[l]["slug"]) + "index.html"; s = read(p)
                s = re.sub(r'<span class="en">[^<]*</span>', "", s)
                s = re.sub(r'<a href="(/guides/[^"/]+/)">(.*?)</a>',
                           lambda m: (f'<a href="{mp[m.group(1)]}">{m.group(2)}</a>' if m.group(1) in mp
                                      else f'<a href="{m.group(1)}">{m.group(2)}</a><span class="en">{LANGS[l]["en_note"]}</span>'), s)
                s = s.replace('href="/guides/"', f'href="/{l}/{LANGS[l]["folder"]}/"')
                write(p, s)
        # 3: index page
        L = LANGS[l]; cards = []
        for en, v in t.items():
            if l in v:
                cards.append(f'    <div class="card"><h3>{e(v[l]["title"])}</h3><p>{e(v[l]["desc"])}</p><a class="more" href="{path(l, v[l]["slug"])}">{L["read"]}</a></div>')
        idx = path(l, "")[:-1] + "/"
        idx = f"/{l}/{L['folder']}/"
        group = {"en": "/guides/", **{x: f"/{x}/{LANGS[x]['folder']}/" for x in langs_present}}
        page = f'''<!doctype html>
<html lang="{L["locale"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(L["idx_title"])}</title>
<meta name="description" content="{e(L["idx_desc"])}">
<link rel="canonical" href="{SITE}{idx}">
{alt_tags(group)}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="apple-itunes-app" content="app-id=6789469881">
<link rel="stylesheet" href="/style.css?v=3">
</head>
<body>
{header(l, L)}

<main>
<section class="hero"><div class="wrap">
  <h1>{L["idx_h1"]}</h1>
  <p class="lead">{L["idx_lead"]}</p>
</div></section>

<section class="block"><div class="narrow">
  <div class="grid">
{chr(10).join(cards)}
  </div>
</div></section>
</main>

{footer(l, L)}
</body>
</html>
'''
        write(idx + "index.html", page)
        for u in [idx] + [path(l, v[l]["slug"]) for v in t.values() if l in v]:
            if f"<loc>{SITE}{u}</loc>" not in sm: new_urls.append(u)
    # English guides index: hreflang + language links
    gi = read("/guides/index.html")
    gi = re.sub(r'\n?<p class="langs">.*?</p>', "", gi)
    links = " &middot; ".join(f'<a href="/{l}/{LANGS[l]["folder"]}/" hreflang="{l}" lang="{l}">{LANGS[l]["name"]}</a>' for l in langs_present)
    gi = gi.replace("</div></section>\n</main>", f'</div></section>\n<p class="langs" style="text-align:center;margin:0 0 32px">Also in: {links}</p>\n</main>', 1)
    write("/guides/index.html", gi)
    group = {"en": "/guides/", **{x: f"/{x}/{LANGS[x]['folder']}/" for x in langs_present}}
    set_alt("/guides/index.html", group)
    if new_urls:
        add = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in new_urls)
        sm = sm.replace("  <url><loc>https://twoodle.app/support/</loc>", add + "  <url><loc>https://twoodle.app/support/</loc>", 1)
        write("/sitemap.xml", sm)
    print("sitemap added:", new_urls)

if __name__ == "__main__":
    main()
