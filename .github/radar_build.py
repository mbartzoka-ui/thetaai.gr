#!/usr/bin/env python3
"""Χτίζει τις στατικές σελίδες του radar για SEO και GEO.

ΓΙΑΤΙ ΥΠΑΡΧΕΙ (23/10/2026): οι ιστορίες του radar ζούσαν ΜΟΝΟ μέσα στο
`const ITEMS = [...]` και τις ζωγράφιζε η JavaScript. Οι crawlers των AI
μοντέλων (GPTBot, ClaudeBot, PerplexityBot) δεν τρέχουν JavaScript, άρα
έβλεπαν μια σχεδόν άδεια σελίδα. Επιπλέον κάθε ιστορία χανόταν από το
web μόλις έβγαινε από το κυλιόμενο παράθυρο των 40, και καμία δεν είχε
δική της διεύθυνση για να παρατεθεί ως πηγή.

ΤΙ ΚΑΝΕΙ, κάθε φορά που τρέχει (μετά τον radar, πριν το commit):
1. Διαβάζει τα ITEMS της ελληνικής και της αγγλικής σελίδας.
2. Τα ενώνει με το μόνιμο μητρώο `radar/stories.json`. Μια ιστορία που
   εμφανίστηκε μία φορά δεν διαγράφεται ποτέ από εκεί.
3. Γράφει μία σελίδα ανά ιστορία, σε `radar/<slug>/` και
   `en/radar/<slug>/`, με NewsArticle schema και τις πηγές της.
4. Γράφει τις ιστορίες ως κανονικό HTML μέσα στο `<main id="feed">` των
   δύο σελίδων radar. Η JavaScript τις ξαναζωγραφίζει στον browser όπως
   πριν· ο crawler τις βλέπει χωρίς αυτήν.
5. Γράφει σελίδες αρχείου ανά μήνα και ενημερώνει το sitemap.xml.

ΤΙ ΔΕΝ ΚΑΝΕΙ: δεν αγγίζει το ITEMS, το GENERATED, τη γραμμή «upd» ούτε
τα αρχεία του knowledge/. Δεν καλεί κανένα AI. Είναι ντετερμινιστικό:
ίδια είσοδος, ίδια έξοδος, οπότε δεν γεμίζει το ιστορικό με άσκοπα diffs.

Χρήση:  python3 .github/radar_build.py
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

SITE = "https://thetaai.gr"
PAGES = {"el": Path("radar/index.html"), "en": Path("en/radar/index.html")}
PREFIX = {"el": "/radar/", "en": "/en/radar/"}
REGISTRY = Path("radar/stories.json")
SITEMAP = Path("sitemap.xml")
OG_IMAGE = f"{SITE}/og-image-v2.png"
BRAND = "θeta ai"

TOPICS = ["AI Act", "AI Security", "Standards", "Incidents", "General"]
BADGE = {"AI Act": "b-act", "AI Security": "b-sec", "Standards": "b-std",
         "Incidents": "b-inc", "General": "b-gen"}
GROUP_LABEL = {"AI Act": "AI Act & Regulation", "AI Security": "AI Security",
               "Standards": "Standards (ISO / NIST)",
               "Incidents": "Incidents & Data", "General": "General"}

MONTHS = {
    "el": ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαΐ", "Ιουν", "Ιουλ", "Αυγ", "Σεπ",
           "Οκτ", "Νοε", "Δεκ"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
           "Oct", "Nov", "Dec"],
}
MONTHS_FULL = {
    "el": ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος",
           "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος",
           "Νοέμβριος", "Δεκέμβριος"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
}
T = {
    "el": {
        "sources": "Πηγές", "archive": "Αρχείο", "all_stories": "Όλες οι ιστορίες του radar",
        "archive_title": "Αρχείο AI Security Radar",
        "archive_desc": "Όλες οι ιστορίες του AI Security Radar της θeta ai, ανά μήνα: EU AI Act, ασφάλεια AI, περιστατικά και πρότυπα.",
        "archive_h1": "Αρχείο του AI Security Radar",
        "archive_sub": "Κάθε ιστορία που πέρασε από το radar, με την ημερομηνία και τις πηγές της. Οι πιο πρόσφατες είναι στη σελίδα του radar.",
        "permalink": "Μόνιμος σύνδεσμος", "back": "Όλες οι πρόσφατες ιστορίες",
        "disclosure": ("Η περίληψη συντάχθηκε αυτόματα με AI από τις δημόσιες πηγές "
                       "που αναφέρονται παραπάνω και ελέγχθηκε από ανεξάρτητο AI ελεγκτή "
                       "πριν δημοσιευτεί. Για όλες τις λεπτομέρειες, διάβασε την αρχική πηγή."),
        "stories": "ιστορίες",
    },
    "en": {
        "sources": "Sources", "archive": "Archive", "all_stories": "All radar stories",
        "archive_title": "AI Security Radar Archive",
        "archive_desc": "Every story from θeta ai's AI Security Radar, by month: EU AI Act, AI security, incidents and standards.",
        "archive_h1": "AI Security Radar archive",
        "archive_sub": "Every story that went through the radar, with its date and sources. The latest ones are on the radar page.",
        "permalink": "Permalink", "back": "All recent stories",
        "disclosure": ("This summary was written automatically with AI from the public "
                       "sources listed above and checked by an independent AI reviewer "
                       "before publication. For full details, read the original source."),
        "stories": "stories",
    },
}

STATIC_START, STATIC_END = "<!-- RADAR-STATIC:START -->", "<!-- RADAR-STATIC:END -->"
ARCH_START, ARCH_END = "<!-- RADAR-ARCHIVE-LINK:START -->", "<!-- RADAR-ARCHIVE-LINK:END -->"


# ---------------------------------------------------------------- helpers

def esc(s):
    return html.escape(str(s), quote=True)


def norm_url(u):
    u = u.strip().lower().split("#", 1)[0].split("?", 1)[0]
    return u.rstrip("/")


def slugify(text, limit=70):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    if len(text) > limit:
        text = text[:limit].rsplit("-", 1)[0]
    return text or "story"


def fmt_date(d, lang):
    y, m, day = d.split("-")
    return f"{int(day)} {MONTHS[lang][int(m) - 1]} {y}"


def read_items(path):
    text = path.read_text(encoding="utf-8")
    idx = text.index("const ITEMS = ")
    items, _ = json.JSONDecoder().raw_decode(text, idx + len("const ITEMS = "))
    gen = re.search(r'const GENERATED = "(\d{4}-\d{2}-\d{2})"', text)
    return text, items, gen.group(1) if gen else None


def sources_of(item):
    srcs = item.get("sources")
    if isinstance(srcs, list) and srcs:
        return [{"name": s["name"], "url": s["url"]} for s in srcs if s.get("url")]
    if item.get("url"):
        return [{"name": item.get("source", "Source"), "url": item["url"]}]
    return []


# --------------------------------------------------------------- registry

def merge_registry(registry, gr_items, en_items, generated):
    """Merge today's items into the permanent registry. Returns the
    records for today's items, in page order."""
    by_url = {}
    for rec in registry:
        for u in rec["urls"]:
            by_url[u] = rec
    used_slugs = {rec["slug"] for rec in registry}
    today = []
    for gr, en in zip(gr_items, en_items):
        srcs = sources_of(gr) or sources_of(en)
        urls = [norm_url(s["url"]) for s in srcs]
        rec = next((by_url[u] for u in urls if u in by_url), None)
        if rec is None:
            base = f"{gr['date']}-{slugify(en.get('title') or gr['title'])}"
            slug, n = base, 2
            while slug in used_slugs:
                slug, n = f"{base}-{n}", n + 1
            used_slugs.add(slug)
            rec = {"slug": slug, "urls": [], "first_seen": generated}
            registry.append(rec)
        # Text and metadata follow the radar's current version of the story.
        rec.update({
            "date": gr["date"], "topic": gr["topic"],
            "el": {"title": gr["title"], "summary": gr["summary"]},
            "en": {"title": en["title"], "summary": en["summary"]},
            "sources": srcs,
        })
        for u in urls:
            if u not in rec["urls"]:
                rec["urls"].append(u)
            by_url[u] = rec
        today.append(rec)
    registry.sort(key=lambda r: (r["date"], r["slug"]), reverse=True)
    return today


# ------------------------------------------------------------ page chrome

def chrome(index_text):
    """Reuse the radar page's own head assets, header, CTA and footer, so
    story pages always match the site's current look."""
    head = index_text[:index_text.index("</head>")]
    styles = "\n".join(re.findall(r"<style>.*?</style>", head, re.S))
    fonts = "\n".join(re.findall(r'<link[^>]+(?:fonts\.googleapis|fonts\.gstatic)[^>]*>', head))
    icon = "\n".join(re.findall(r'<link[^>]+rel="icon"[^>]*>', head))
    header = re.search(r"<header>.*?</header>", index_text, re.S).group(0)
    cta = re.search(r'<div class="cta">.*?</div>', index_text, re.S)
    footer = re.search(r"<footer>.*?</footer>", index_text, re.S).group(0)
    return {"styles": styles, "fonts": fonts, "icon": icon, "header": header,
            "cta": cta.group(0) if cta else "", "footer": footer}


EXTRA_CSS = """<style>
.crumbs{font-size:.85rem;margin:28px 0 8px;color:var(--stone,#6b7280)}
.crumbs a{color:inherit}
.story{padding:8px 0 24px}
.story h1{font-size:clamp(1.6rem,3.2vw,2.3rem);line-height:1.2;margin:14px 0 18px}
.story .lead{font-size:1.08rem;line-height:1.75;max-width:760px}
.story h2{font-size:1.05rem;margin:30px 0 10px}
.story ul{padding-left:1.2em;line-height:1.8}
.story .disc{margin-top:26px}
.story time{font-size:.85rem;opacity:.75}
.arch-month{margin:34px 0 8px;font-size:1.15rem}
.arch-list{list-style:none;padding:0;margin:0}
.arch-list li{padding:9px 0;border-bottom:1px solid rgba(29,40,70,.08);display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.arch-list time{font-size:.8rem;opacity:.7;min-width:90px}
.radar-archive-link{margin:10px 0 40px;font-weight:600}
h2.group-h,h3.it-title{font-size:inherit;margin:0}
</style>"""


def lang_switch(header, lang, el_path, en_path):
    """Point the header's EL/EN switch at this page's counterpart."""
    target = en_path if lang == "el" else el_path
    return re.sub(r'(<span class="lang">.*?<a href=")[^"]*(")',
                  lambda m: m.group(1) + target + m.group(2), header, count=1, flags=re.S)


def page(lang, c, *, title, desc, path, el_path, en_path, body, jsonld,
         og_type="article"):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="el" href="{SITE}{el_path}">
<link rel="alternate" hreflang="en" href="{SITE}{en_path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{el_path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:locale" content="{'el_GR' if lang == 'el' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
{c['icon']}
{c['fonts']}
{c['styles']}
{EXTRA_CSS}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
{lang_switch(c['header'], lang, el_path, en_path)}
<div class="wrap">
{body}
{c['cta']}
{c['footer']}
</div>
</body>
</html>
"""


def org():
    return {"@type": "Organization", "name": BRAND, "alternateName": "Theta AI",
            "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": OG_IMAGE}}


def desc_of(summary, limit=158):
    s = re.sub(r"\s+", " ", summary).strip()
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "…"


# ------------------------------------------------------------ story pages

def story_page(rec, lang, c):
    t = T[lang]
    txt = rec[lang]
    el_path, en_path = f"/radar/{rec['slug']}/", f"/en/radar/{rec['slug']}/"
    path = el_path if lang == "el" else en_path
    radar = PREFIX[lang]
    srcs = "\n".join(
        f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["name"])}</a></li>'
        for s in rec["sources"])
    body = f"""<nav class="crumbs" aria-label="breadcrumb"><a href="{radar}">AI Security Radar</a> › <a href="{radar}archive/">{t['archive']}</a></nav>
<article class="story">
<div class="it-top"><span class="badge {BADGE.get(rec['topic'], 'b-gen')}">{esc(rec['topic'])}</span> <time datetime="{rec['date']}">{fmt_date(rec['date'], lang)}</time></div>
<h1>{esc(txt['title'])}</h1>
<p class="lead">{esc(txt['summary'])}</p>
<h2>{t['sources']}</h2>
<ul>
{srcs}
</ul>
<p class="disc">{t['disclosure']}</p>
<p><a href="{radar}">← {t['back']}</a></p>
</article>"""
    jsonld = [
        {"@context": "https://schema.org", "@type": "NewsArticle",
         "headline": txt["title"][:110], "description": desc_of(txt["summary"], 300),
         "datePublished": rec["date"], "dateModified": rec["date"],
         "inLanguage": lang, "url": SITE + path, "mainEntityOfPage": SITE + path,
         "image": OG_IMAGE, "articleSection": rec["topic"],
         "author": org(), "publisher": org(),
         "isPartOf": {"@type": "CollectionPage", "name": "AI Security Radar",
                      "url": SITE + radar},
         "citation": [{"@type": "CreativeWork", "name": s["name"], "url": s["url"]}
                      for s in rec["sources"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "AI Security Radar", "item": SITE + radar},
             {"@type": "ListItem", "position": 2, "name": txt["title"][:110], "item": SITE + path}]},
    ]
    return page(lang, c, title=f"{txt['title']} | AI Security Radar · {BRAND}",
                desc=desc_of(txt["summary"]), path=path, el_path=el_path,
                en_path=en_path, body=body, jsonld=jsonld)


def archive_page(registry, lang, c):
    t = T[lang]
    radar = PREFIX[lang]
    el_path, en_path = "/radar/archive/", "/en/radar/archive/"
    path = el_path if lang == "el" else en_path
    months, parts = {}, []
    for rec in registry:
        months.setdefault(rec["date"][:7], []).append(rec)
    for ym in sorted(months, reverse=True):
        y, m = ym.split("-")
        rows = "\n".join(
            f'<li><time datetime="{r["date"]}">{fmt_date(r["date"], lang)}</time>'
            f'<a href="{radar}{r["slug"]}/">{esc(r[lang]["title"])}</a></li>'
            for r in months[ym])
        parts.append(f'<h2 class="arch-month">{MONTHS_FULL[lang][int(m) - 1]} {y} · {len(months[ym])} {t["stories"]}</h2>\n<ul class="arch-list">\n{rows}\n</ul>')
    body = f"""<nav class="crumbs" aria-label="breadcrumb"><a href="{radar}">AI Security Radar</a> › {t['archive']}</nav>
<section class="intro"><h1>{t['archive_h1']}</h1><p class="sub">{t['archive_sub']}</p></section>
{''.join(parts)}"""
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage",
              "name": t["archive_title"], "url": SITE + path, "inLanguage": lang,
              "publisher": org(),
              "hasPart": [{"@type": "NewsArticle", "headline": r[lang]["title"][:110],
                           "url": f"{SITE}{radar}{r['slug']}/", "datePublished": r["date"]}
                          for r in registry]}
    return page(lang, c, title=f"{t['archive_title']} | {BRAND}", desc=t["archive_desc"],
                path=path, el_path=el_path, en_path=en_path, body=body,
                jsonld=jsonld, og_type="website")


# ------------------------------------------------------ radar index edits

def static_feed(records, items, lang):
    """The same grouping and order as render(), as plain HTML."""
    t = T[lang]
    radar = PREFIX[lang]
    pairs = list(zip(items, records))
    out = []
    for topic in TOPICS:
        group = sorted([p for p in pairs if p[0]["topic"] == topic],
                       key=lambda p: p[0]["date"], reverse=True)
        if not group:
            continue
        arts = []
        for item, rec in group:
            refs = " · ".join(
                f'<a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer nofollow">{esc(s["name"])}</a>'
                for s in sources_of(item))
            arts.append(
                f'<article class="item"><div class="it-top"><span class="badge {BADGE[topic]}">{esc(topic)}</span>'
                f'<time class="it-src" datetime="{item["date"]}">{fmt_date(item["date"], lang)}</time></div>'
                f'<h3 class="it-title"><a class="it-title-link" href="{radar}{rec["slug"]}/">{esc(item["title"])}</a></h3>'
                f'<p class="it-sum">{esc(item["summary"])}</p>'
                f'<div class="it-refs">{t["sources"]}: {refs}</div></article>')
        out.append(f'<section class="group"><h2 class="group-h">{GROUP_LABEL[topic]} · {len(group)}</h2>\n'
                   + "\n".join(arts) + "\n</section>")
    return "\n".join(out)


def patch_index(text, records, items, lang):
    radar = PREFIX[lang]
    t = T[lang]
    # 1. Static stories inside <main id="feed">. render() replaces them in
    #    the browser; crawlers without JavaScript read them as they are.
    feed = f'<main id="feed">{STATIC_START}\n{static_feed(records, items, lang)}\n{STATIC_END}</main>'
    text, n = re.subn(r'<main id="feed">.*?</main>', lambda m: feed, text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"{lang}: <main id=\"feed\"> not found")

    # 2. Archive link right after the feed, outside it so render() keeps it.
    link = (f'{ARCH_START}<p class="radar-archive-link"><a href="{radar}archive/">'
            f'{t["all_stories"]} → {t["archive"]}</a></p>{ARCH_END}')
    text = re.sub(r"\n?" + re.escape(ARCH_START) + r".*?" + re.escape(ARCH_END), "", text, flags=re.S)
    text = text.replace(f"{STATIC_END}</main>", f"{STATIC_END}</main>\n{link}", 1)

    # 3. Story URLs for render(): window.RADAR_SLUGS maps a source URL to
    #    its story page, so the JavaScript view links to it too.
    slugs = {}
    for item, rec in zip(items, records):
        for s in sources_of(item):
            slugs[norm_url(s["url"])] = rec["slug"]
    slug_tag = f'<script id="radar-slugs">window.RADAR_SLUGS={json.dumps(slugs, ensure_ascii=False)};</script>'
    text = re.sub(r'<script id="radar-slugs">.*?</script>\n?', "", text, flags=re.S)
    text = text.replace("<script>\nconst GENERATED", f"{slug_tag}\n<script>\nconst GENERATED", 1)

    # 4. One-time patch of render(): add a permalink to each story.
    marker = "const refs = srcs.map("
    if "RADAR_SLUGS" not in text.split("function render()", 1)[-1][:2000] and marker in text:
        add = (f"const _sl=(window.RADAR_SLUGS||{{}})[String(srcs[0].url).toLowerCase().split('#')[0].split('?')[0].replace(/\\/+$/,'')];\n"
               f"const perma=_sl?` · <a href=\"{radar}${{_sl}}/\">{t['permalink']}</a>`:'';\n")
        text = text.replace(marker, add + marker, 1)
        text = text.replace("`<div class=\"it-refs\">Sources: ${refs}</div>`",
                            "`<div class=\"it-refs\">Sources: ${refs}${perma}</div>`", 1)

    # 5. ItemList schema of today's stories, for search and AI engines.
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "AI Security Radar", "url": SITE + radar, "inLanguage": lang,
          "publisher": org(),
          "mainEntity": {"@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": n + 1,
               "url": f"{SITE}{radar}{rec['slug']}/", "name": item["title"][:110]}
              for n, (item, rec) in enumerate(zip(items, records))]}}
    ld_tag = f'<script type="application/ld+json" id="radar-ld">{json.dumps(ld, ensure_ascii=False)}</script>'
    text = re.sub(r'<script type="application/ld\+json" id="radar-ld">.*?</script>\n?', "", text, flags=re.S)
    text = text.replace("</head>", f"{ld_tag}\n</head>", 1)
    return text


# ----------------------------------------------------------------- sitemap

def url_block(el_path, en_path, lastmod, changefreq, priority):
    alts = (f'<xhtml:link rel="alternate" hreflang="el" href="{SITE}{el_path}"/>'
            f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{en_path}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{el_path}"/>')
    return "".join(
        f"<url><loc>{SITE}{p}</loc>{alts}<lastmod>{lastmod}</lastmod>"
        f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n"
        for p in (el_path, en_path))


def update_sitemap(registry, generated):
    text = SITEMAP.read_text(encoding="utf-8")
    text = re.sub(r"\s*<url>(?:(?!</url>).)*?<loc>https://thetaai\.gr/(?:en/)?radar/(?:(?!</url>).)*?</url>",
                  "", text, flags=re.S)
    blocks = url_block("/radar/", "/en/radar/", generated, "daily", "0.7")
    blocks += url_block("/radar/archive/", "/en/radar/archive/", generated, "daily", "0.5")
    for r in registry:
        blocks += url_block(f"/radar/{r['slug']}/", f"/en/radar/{r['slug']}/",
                            r["date"], "monthly", "0.5")
    text = text.replace("</urlset>", blocks + "</urlset>", 1)
    return text


# -------------------------------------------------------------------- main

def write_if_changed(path, content):
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main():
    el_text, el_items, generated = read_items(PAGES["el"])
    en_text, en_items, _ = read_items(PAGES["en"])
    if len(el_items) != len(en_items):
        raise RuntimeError("GR and EN pages have different item counts")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else []
    records = merge_registry(registry, el_items, en_items, generated)

    # Everything is computed in memory first; files are written only after
    # nothing above has failed, so a crash never leaves a half-built site.
    out = {}
    c = {"el": chrome(el_text), "en": chrome(en_text)}
    out[PAGES["el"]] = patch_index(el_text, records, el_items, "el")
    out[PAGES["en"]] = patch_index(en_text, records, en_items, "en")
    for rec in registry:
        for lang in ("el", "en"):
            out[Path(PREFIX[lang].strip("/")) / rec["slug"] / "index.html"] = story_page(rec, lang, c[lang])
    for lang in ("el", "en"):
        out[Path(PREFIX[lang].strip("/")) / "archive" / "index.html"] = archive_page(registry, lang, c[lang])
    out[SITEMAP] = update_sitemap(registry, generated)
    out[REGISTRY] = json.dumps(registry, ensure_ascii=False, indent=1) + "\n"

    changed = sum(write_if_changed(p, txt) for p, txt in out.items())
    print(f"radar_build: {len(registry)} stories in registry, "
          f"{len(records)} on the radar page, {changed} files changed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"radar_build FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
