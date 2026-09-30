"""Builds the Engage Era site into ../public. Run: python3 src/build.py"""
import json, os, re, datetime, html
from articles import ARTICLES, INSTAGRAM

SITE = "https://eesmm.com"
IG = "https://www.instagram.com/engageeraco/"
IG_BEN = "https://www.instagram.com/benmeller/"
EMAIL = "ben@eesmm.com"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
FOUNDER_PHOTO = None  # e.g. "ben-backstage.jpg" in public/assets/img/
BRANDS = ["SoFi", "Oil Nut Bay", "Good Molecules", "Rise Above", "Rome", "Better Life Work", "Beardy Brandon"]
FONTS = "https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
LOGO_DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="eeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aaee6"/><stop offset="1" stop-color="#1466ff"/></linearGradient><g id="ee" fill="url(#eeg)"><path d="M51 0H346L297 67H39Z"/><path d="M31 117H261L216 176H20Z"/><path d="M11 227H247L420 0H670L658 67H440L269 293H0Z"/><path d="M466 117H650L640 176H422Z"/><path d="M389 227H631L620 293H342Z"/></g></defs></svg>'
MARK = '<svg class="mark" viewBox="0 0 670 293" aria-hidden="true"><use href="#ee"/></svg>'


def fmt_date(s):
    return datetime.date.fromisoformat(s).strftime("%b %-d, %Y")


def plain(t):
    return re.sub(r"</?r>", "", t)


def red(t):
    return t.replace("<r>", '<span class="r">').replace("</r>", "</span>")


def cover(item, up):
    """The story's Instagram post (saved from Grok) is its cover. Without one, a generated post in the same style."""
    src = f"{up}assets/img/{item['image']}" if item.get("image") else f"{up}assets/posts/{item['slug']}.png"
    return f'<img src="{src}" alt="{html.escape(plain(item["title"]))}" width="1080" height="1350" loading="lazy">'


def page(path, title, desc, body, *, depth, active="", schema=None, noindex=False, og="og/default.png", word_extra=""):
    up = "../" * depth
    canonical = SITE + "/" + (path if path else "")
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ""
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{up}{href}"{current if key == active else ""}>{label}</a>'
        for key, href, label in [("news", "news/index.html", "News"), ("brief", "brief/index.html", "The Brief"), ("studio", "studio/index.html", "Studio"), ("founder", "founder/index.html", "Founder")]
    )
    cta = f'<a class="btn red" href="{up}studio/index.html#apply">Apply</a>' if active == "studio" else f'<a class="btn red" href="{up}studio/index.html">Work with us</a>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Engage Era">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#060819">
<meta name="author" content="Ben Meller">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{LOGO_DEFS}
{body.replace("%UP%", up).replace("%NAV%", nav).replace("%CTA%", cta).replace("%WORD%", word_extra)}
<script src="{up}assets/site.js" defer></script>
</body>
</html>
"""


def masthead(date=True):
    d = '<span class="date" id="today"></span>' if date else ""
    return f"""<header class="mast gut">
  <div class="max">
    <a class="brand" href="%UP%index.html" aria-label="Engage Era home">{MARK}<span class="word">Engage Era%WORD%</span></a>
    <nav class="main" aria-label="Main">%NAV%</nav>
    {d}
    %CTA%
  </div>
</header>"""


def footer():
    return f"""<footer class="site gut">
  <div class="max cols">
    <div>
      <a class="brand" href="%UP%index.html">{MARK}<span class="word">Engage Era</span></a>
      <p class="mute">Marketing news, before it's news. Plus a studio that builds what we cover. Based in Palm Beach, FL.</p>
    </div>
    <div><h4>News</h4><ul><li><a href="%UP%news/index.html">All stories</a></li><li><a href="%UP%brief/index.html">The Brief</a></li><li><a href="{IG}" rel="noopener">@engageeraco</a></li></ul></div>
    <div><h4>Studio</h4><ul><li><a href="%UP%studio/index.html">Services</a></li><li><a href="%UP%studio/index.html#process">Process</a></li><li><a href="%UP%studio/index.html#apply">Apply</a></li></ul></div>
    <div><h4>Company</h4><ul><li><a href="%UP%founder/index.html">Founder</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG_BEN}" rel="noopener">@benmeller</a></li></ul></div>
  </div>
  <div class="legal"><div class="max"><span>© {datetime.date.today().year} Engage Era · Palm Beach, FL</span><span>Marketing news, before it's news.</span></div></div>
</footer>"""


def brief_band(depth_note=""):
    return """<section class="brief gut" id="brief">
  <div class="max">
    <div>
      <span class="kicker plain" style="color:#fff">The Brief · Every weekday</span>
      <h2 style="margin-top:12px">Marketing news.<br>Before it's news.</h2>
      <p class="lede">The platform updates, campaigns and founder moves that matter, in a 3-minute read every weekday morning.</p>
    </div>
    <form name="brief" method="POST" action="%UP%thanks/index.html" data-netlify="true" netlify-honeypot="company-site" novalidate>
      <input type="hidden" name="form-name" value="brief">
      <p class="hp"><label>Leave empty <input name="company-site"></label></p>
      <label class="fine" for="brief-email">Your email</label>
      <div class="row"><input id="brief-email" name="email" type="email" placeholder="you@company.com" autocomplete="email" required><button class="btn" type="submit">Subscribe</button></div>
      <p class="fine formmsg" aria-live="polite">Free. Unsubscribe anytime.</p>
    </form>
  </div>
</section>"""


def article_card(a, up):
    return f"""<a class="card" data-c="{a['cat']}" href="{up}news/{a['slug']}/index.html">
  <div class="post">{cover(a, up)}</div>
  <h3 class="sr">{plain(a['title'])}</h3>
  <span class="meta">{a['cat_label']} · {fmt_date(a['date'])} · {a['read']}</span>
  <p>{a['dek']}</p>
</a>"""


def ig_card(s):
    return f"""<a class="card ig" data-c="{s['cat']}" href="{IG}" rel="noopener">
  <div class="post">{cover(s, "%UP%")}</div>
  <h3 class="sr">{plain(s['title'])}</h3>
  <span class="meta">{s['cat_label']} · On Instagram</span>
</a>"""


ORG = {"@type": "NewsMediaOrganization", "@id": SITE + "/#org", "name": "Engage Era", "url": SITE, "logo": SITE + "/assets/logo.png",
       "email": EMAIL, "sameAs": [IG], "founder": {"@type": "Person", "@id": SITE + "/founder/#ben", "name": "Ben Meller"},
       "description": "Engage Era is a marketing news outlet with an in-house studio, Engage Era Studio, based in Palm Beach, Florida."}
BEN = {"@type": "Person", "@id": SITE + "/founder/#ben", "name": "Ben Meller", "jobTitle": "Founder", "worksFor": {"@id": SITE + "/#org"},
       "url": SITE + "/founder/", "sameAs": [IG_BEN], "address": {"@type": "PostalAddress", "addressLocality": "Palm Beach", "addressRegion": "FL", "addressCountry": "US"}}


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)


# ---------- Home ----------
def build_home():
    up = ""
    lead, rest = ARTICLES[0], ARTICLES[1:]
    ticker_items = [plain(a["title"]) for a in ARTICLES] + [plain(s["title"]) for s in INSTAGRAM] + ["The Brief: marketing news every weekday"]
    track = "".join(f"<span>{t}</span>" for t in ticker_items) * 2
    latest = "".join(
        f'<a class="item" href="news/{a["slug"]}/index.html"><span class="t">{datetime.date.fromisoformat(a["date"]).strftime("%b %-d")}</span><div><span class="kicker">{a["cat_label"]}</span><h3>{plain(a["title"])}</h3></div></a>'
        for a in ARTICLES
    ) + "".join(
        f'<a class="item" href="{IG}" rel="noopener"><span class="t">IG</span><div><span class="kicker">{s["cat_label"]}</span><h3>{plain(s["title"])}</h3></div></a>' for s in INSTAGRAM
    )
    cards = "".join(article_card(a, up) for a in rest) + "".join(ig_card(s) for s in INSTAGRAM)
    body = f"""<div class="ticker" aria-label="Latest headlines"><b>Latest</b><div class="track">{track}</div></div>
<div class="studiobar gut"><div class="max"><span>Engage Era Studio: we grow founders, artists and brands.</span><a href="studio/index.html">See the Studio →</a></div></div>
{masthead()}
<main id="main">
  <div class="gut">
    <div class="max front">
      <article class="lead split">
        <a href="news/{lead['slug']}/index.html" class="post" tabindex="-1">{cover(lead, up)}</a>
        <div class="lead-copy">
          <span class="kicker">{lead['cat_label']}</span>
          <h1><a href="news/{lead['slug']}/index.html">{red(lead['title'])}</a></h1>
          <p class="dek">{lead['dek']}</p>
          <div class="byline"><b>Ben Meller</b><span>·</span><span>{fmt_date(lead['date'])}</span><span>·</span><span>{lead['read']}</span></div>
        </div>
      </article>
      <aside class="side" aria-label="Latest">
        <h2>Latest <span>● Live</span></h2>
        {latest}
      </aside>
    </div>
  </div>
  <section class="gut" id="news">
    <div class="max">
      <div class="sec-title"><h2>The news</h2><a class="kicker plain" href="news/index.html">All stories →</a></div>
      <div class="grid">{cards}</div>
    </div>
  </section>
  {brief_band()}
  <section class="teaser gut">
    <div class="max">
      <div class="head">
        <div><span class="kicker">Engage Era Studio</span><h2 style="margin-top:14px">We cover what works.<br><span class="r">Then we build it.</span></h2></div>
        <p>The same team that reports on marketing every day runs social for founders, artists and brands with something to say. We work with a small number of partners at a time.</p>
      </div>
      <div class="services">
        <div class="svc"><span class="n">01</span><h3>Strategy</h3><p>Brand Blueprints and growth audits. Who you are online and exactly what to post.</p></div>
        <div class="svc"><span class="n">02</span><h3>Content</h3><p>Shoots, edits and founder content built for how each platform works right now.</p></div>
        <div class="svc"><span class="n">03</span><h3>Social &amp; paid</h3><p>Full social management, organic growth and paid social on Meta and TikTok.</p></div>
        <div class="svc"><span class="n">04</span><h3>Search</h3><p>SEO and AEO content that ranks on Google and gets recommended by AI.</p></div>
      </div>
      <div class="roster"><span class="kicker">Brands we've created for</span>{"".join(f'<span class="name">{b}</span>' for b in BRANDS)}<p>We don't publish client results. We walk through them on the call.</p></div>
      <div class="cta-row"><div><h3>Work with Engage Era Studio</h3><p>Services, process and applications live on the Studio page.</p></div><a class="btn red" href="studio/index.html">See the Studio →</a></div>
    </div>
  </section>
</main>
{footer()}"""
    schema = [{"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "@id": SITE + "/#site", "name": "Engage Era", "url": SITE, "publisher": {"@id": SITE + "/#org"}}]}]
    write("index.html", page("", "Engage Era | Marketing News, Before It's News",
                             "Marketing news for brands and founders: platform updates, campaigns and founder stories, every weekday. Plus Engage Era Studio, a social media and content agency in Palm Beach.",
                             body, depth=0, schema=schema))


# ---------- News index ----------
def build_news():
    up = "../"
    cats = [("all", "All"), ("platforms", "Platforms"), ("founders", "Founder stories"), ("ai", "AI"), ("guides", "Guides"), ("campaigns", "Campaigns"), ("creators", "Creators")]
    used = {a["cat"] for a in ARTICLES} | {x["cat"] for x in INSTAGRAM}
    cats = [(k, l) for k, l in cats if k == "all" or k in used]
    chips = "".join(f'<button class="chip" aria-pressed="{"true" if k == "all" else "false"}" data-f="{k}">{l}</button>' for k, l in cats)
    cards = "".join(article_card(a, up) for a in ARTICLES) + "".join(ig_card(s) for s in INSTAGRAM)
    body = f"""{masthead()}
<main id="main">
  <div class="page-hero gut" style="padding-bottom:32px"><div class="max"><span class="kicker">Engage Era News</span><h1>The news</h1><p class="sub">Platform updates, campaigns, AI and founder stories. What changed, who it hits, and what to do about it.</p></div></div>
  <section class="gut"><div class="max">
    <div class="cats" role="group" aria-label="Filter stories">{chips}</div>
    <div class="grid">{cards}</div>
  </div></section>
  {brief_band()}
</main>
{footer()}"""
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Engage Era News", "url": SITE + "/news/", "isPartOf": {"@id": SITE + "/#site"}}]
    write("news/index.html", page("news/", "Marketing News: Platforms, AI, Campaigns | Engage Era",
                                  "The latest marketing news for brands and founders: Instagram, TikTok, Meta and Google updates, AI search, campaigns and founder stories.",
                                  body, depth=1, active="news", schema=schema))


# ---------- Articles ----------
def build_articles():
    for i, a in enumerate(ARTICLES):
        up = "../../"
        path = f"news/{a['slug']}/"
        faq = "".join(f"<h3>{q}</h3><p>{ans}</p>" for q, ans in a["faq"])
        others = [o for o in ARTICLES if o["slug"] != a["slug"]][:2]
        more = "".join(article_card(o, up) for o in others)
        body = f"""{masthead(date=False)}
<main id="main">
  <div class="gut">
    <nav class="crumbs max" aria-label="Breadcrumb" style="max-width:880px"><a href="{up}index.html">Home</a><span>/</span><a href="{up}news/index.html">News</a><span>/</span><span>{a['cat_label']}</span></nav>
    <header class="article-head split">
      <figure class="cover-fig"><div class="post">{cover(a, up)}</div>{f'<figcaption>{a["image_credit"]}</figcaption>' if a.get("image_credit") else ""}</figure>
      <div class="lead-copy">
        <span class="kicker">{a['cat_label']}</span>
        <h1>{red(a['title'])}</h1>
        <p class="dek">{a['dek']}</p>
        <div class="byline"><b><a href="{up}founder/index.html">Ben Meller</a></b><span>·</span><time datetime="{a['date']}">{fmt_date(a['date'])}</time><span>·</span><span>{a['read']}</span></div>
      </div>
    </header>
    <article class="prose">
      <div class="tldr"><b class="kicker">The short version</b>{a['tldr']}</div>
      {a['body']}
      <h2>FAQ</h2>
      {faq}
    </article>
    <div class="author"><div class="av" aria-hidden="true">BM</div><p><b>Ben Meller</b> is the founder of Engage Era and Engage Era Studio. He works with founders, artists and brands on social, content and growth. <a href="{up}founder/index.html" style="color:var(--sky)">More about Ben →</a></p></div>
    <div class="article-cta cta-row"><div><h3>Want this done for you?</h3><p>Engage Era Studio builds what we cover.</p></div><a class="btn red" href="{up}studio/index.html">See the Studio →</a></div>
  </div>
  {brief_band()}
  <section class="gut" style="padding-top:64px"><div class="max"><div class="sec-title"><h2>More from Engage Era</h2><a class="kicker plain" href="{up}news/index.html">All stories →</a></div><div class="grid">{more}</div></div></section>
</main>
{footer()}"""
        schema = [{"@context": "https://schema.org", "@graph": [
            {"@type": "NewsArticle", "headline": plain(a["title"]), "description": a["description"], "datePublished": a["date"], "dateModified": a["date"],
             "author": {"@id": SITE + "/founder/#ben", "@type": "Person", "name": "Ben Meller", "url": SITE + "/founder/"},
             "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + "/" + path, "image": SITE + f"/assets/posts/{a['slug']}.png", "articleSection": a["cat_label"]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "News", "item": SITE + "/news/"},
                {"@type": "ListItem", "position": 3, "name": plain(a["title"]), "item": SITE + "/" + path}]}]}]
        write(path + "index.html", page(path, a["seo_title"] + " | Engage Era", a["description"], body, depth=2, active="news", schema=schema, og=f"og/{a['slug']}.png"))


# ---------- Studio ----------
STUDIO_FAQ = [
    ("How much does a social media agency cost?", "We work on monthly retainers scoped to each brand, plus The Blueprint as a one-time strategy project. We share investment on a call after your application, once we understand what you need."),
    ("What's included in social media management?", "Strategy, content planning, production and editing, posting, community management and monthly reporting. Full Production adds shoots, paid social, launches and search content."),
    ("Do you only work with businesses in Palm Beach?", "No. We're based in Palm Beach and Jupiter, Florida, and work with founders, artists and brands across the US."),
    ("What is AEO?", "Answer engine optimization: making your brand easy for AI tools like ChatGPT, Gemini and Perplexity to find, understand and recommend."),
    ("How long does it take to see results?", "We plan in 90-day cycles, and partnerships start with a three-month minimum so the work has time to compound."),
    ("Do you publish client results?", "No. We keep client numbers private and walk through relevant results on the call."),
]


def build_studio():
    wall = "".join(f'<span>{b}</span><span class="dot">/</span>' for b in BRANDS)
    wall_dup = "".join(f'<span aria-hidden="true">{b}</span><span class="dot" aria-hidden="true">/</span>' for b in BRANDS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in STUDIO_FAQ)
    body = f"""{masthead(date=False)}
<main id="main">
  <div class="page-hero gut" style="padding-top:88px">
    <div class="max">
      <span class="kicker">Engage Era Studio · Palm Beach</span>
      <h1 style="font-size:clamp(56px,10vw,136px)">We cover what works.<br><span class="r">Then we build it.</span></h1>
      <div class="hero-sub">
        <p>A social media and content production agency for <b>founders, artists and brands</b> with something to say. Based in Palm Beach. Working everywhere.</p>
        <div class="ctas"><a class="btn red" href="#apply">Apply to work with us</a><a class="btn ghost" href="#services">What we do</a></div>
      </div>
    </div>
  </div>
  <div class="wall gut" aria-label="Brands we've created for">
    <div class="max">
      <div class="top"><span class="kicker">Brands we've created for</span><p>We don't publish client results. We walk through them on the call.</p></div>
      <div class="marquee"><div class="track">{wall}{wall_dup}</div></div>
    </div>
  </div>
  <section class="band gut" id="why">
    <div class="max">
      <div class="head"><span class="kicker">Why a newsroom runs a studio</span><h2>We see it first. <span class="r">You use it first.</span></h2></div>
      <div class="why">
        <div><h3>We report daily</h3><p>Engage Era covers platform changes, campaigns and founder moves every weekday. Our partners act on what we learn before it's common knowledge.</p></div>
        <div><h3>We build like publishers</h3><p>Audiences grow from a publishing rhythm, not random posts. We run your accounts the way a media company runs its channels.</p></div>
        <div><h3>We stay small</h3><p>We partner with a limited number of brands each quarter, so every account gets senior attention.</p></div>
      </div>
      <p class="entity"><b>Engage Era Studio</b> is a social media management and content production agency based in Palm Beach and Jupiter, Florida. Founded by Ben Meller, it works with founders, artists and brands across the US on strategy, content, organic growth, paid social and search.</p>
    </div>
  </section>
  <section class="band gut" id="services">
    <div class="max">
      <div class="head"><span class="kicker">What we do</span><h2>Full production. <span class="r">One team.</span></h2><p>Strategy through execution, under one roof. Take one area or all five.</p></div>
      <div class="svc5">
        <article><span class="n">01 · Strategy</span><h3>Strategy</h3><ul><li><b>Brand Blueprint</b><span>Positioning, visual world, content system and launch plan.</span></li><li><b>Growth audit</b><span>A teardown of your accounts and a plan for the next level.</span></li></ul></article>
        <article><span class="n">02 · Content</span><h3>Content</h3><ul><li><b>Content production</b><span>Shoots, editing, reels and photo, built for each platform.</span></li><li><b>Founder content</b><span>Making the person behind the brand the reason people follow.</span></li></ul></article>
        <article><span class="n">03 · Social</span><h3>Social</h3><ul><li><b>Social media management</b><span>Planning, posting, community and monthly reporting.</span></li><li><b>Organic growth</b><span>Engagement, collaborations and reach strategy.</span></li></ul></article>
        <article><span class="n">04 · Paid</span><h3>Paid</h3><ul><li><b>Paid social</b><span>Meta and TikTok campaigns, creative and management.</span></li><li><b>Launches</b><span>Drops, releases, tours and openings, run as campaigns.</span></li></ul></article>
        <article><span class="n">05 · Search</span><h3>Search</h3><ul><li><b>SEO content</b><span>Blogs and articles that rank on Google.</span></li><li><b>AEO</b><span>Getting your brand found and recommended by AI tools.</span></li></ul></article>
      </div>
    </div>
  </section>
  <section class="band gut" id="packages">
    <div class="max">
      <div class="head"><span class="kicker">How to work with us</span><h2>Three ways in</h2></div>
      <div class="pk">
        <article><span class="type">One-time project</span><h3>The Blueprint</h3><p>The strategy behind everything: who you are online, what your world looks like, and exactly what to post.</p><ul><li>Positioning and brand world</li><li>Visual rules and content system</li><li>90-day launch plan</li></ul></article>
        <article class="feat"><span class="type">Monthly partnership</span><h3>Growth</h3><p>We run your social. Strategy, content and growth, handled every month.</p><ul><li>Full social media management</li><li>Content production and editing</li><li>Organic growth and reporting</li></ul></article>
        <article><span class="type">Monthly partnership</span><h3>Full Production</h3><p>Everything we do, for brands that want to operate like a media company.</p><ul><li>Everything in Growth</li><li>Shoots, paid social and launches</li><li>SEO and AEO content, founder brand</li></ul></article>
      </div>
      <p class="pk-note">Most partners start with The Blueprint. Investment is shared on the call after you apply.</p>
    </div>
  </section>
  <section class="band gut" id="process">
    <div class="max">
      <div class="head"><span class="kicker">Process</span><h2>From application to growth</h2></div>
      <ol class="steps">
        <li><span class="n">1</span><h3>Apply</h3><p>Tell us about your brand and goals. We reply within 48 hours.</p></li>
        <li><span class="n">2</span><h3>Call</h3><p>A 30-minute conversation. We walk through relevant results and see if we're a fit.</p></li>
        <li><span class="n">3</span><h3>Blueprint</h3><p>We map your positioning, content system and 90-day plan.</p></li>
        <li><span class="n">4</span><h3>Build</h3><p>We produce, publish and grow, with monthly reporting and 90-day planning cycles.</p></li>
      </ol>
    </div>
  </section>
  <section class="band gut" id="who">
    <div class="max">
      <div class="head"><span class="kicker">Who we work with</span><h2>Built for brands with <span class="r">something to say</span></h2></div>
      <div class="who"><span><b>Founders</b> &amp; personal brands</span><span><b>Artists</b> &amp; musicians</span><span><b>Luxury</b> &amp; hospitality</span><span><b>Consumer</b> brands</span><span><b>Real estate</b> &amp; private clubs</span><span><b>Palm Beach</b> &amp; Jupiter businesses</span></div>
    </div>
  </section>
  <section class="band gut" id="faq">
    <div class="max"><div class="head"><span class="kicker">Questions</span><h2>FAQ</h2></div><div class="faq">{faq}</div></div>
  </section>
  <section class="band apply gut" id="apply">
    <div class="max">
      <div class="side-copy">
        <span class="kicker">Apply</span>
        <h2 style="margin-top:14px">Let's build <span class="r">your era.</span></h2>
        <p>We take on a limited number of partners each quarter. Tell us where you are and where you want to go. We reply to every application within 48 hours.</p>
        <div class="contact"><span>Direct</span><b>{EMAIL}</b><span style="margin-top:10px">Based in</span><b>Palm Beach · Jupiter, FL</b></div>
      </div>
      <form class="form" name="apply" method="POST" action="../thanks/index.html" data-netlify="true" netlify-honeypot="company-site" novalidate>
        <input type="hidden" name="form-name" value="apply">
        <p class="hp"><label>Leave empty <input name="company-site"></label></p>
        <div class="row2">
          <div class="f"><label for="a-name">Name</label><input id="a-name" name="name" type="text" autocomplete="name" required></div>
          <div class="f"><label for="a-email">Email</label><input id="a-email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="row2">
          <div class="f"><label for="a-brand">Brand or company</label><input id="a-brand" name="brand" type="text" required></div>
          <div class="f"><label for="a-link">Website or Instagram</label><input id="a-link" name="link" type="text" placeholder="@yourbrand"></div>
        </div>
        <fieldset><legend>What do you need?</legend>
          <div class="checks">
            <label><input type="checkbox" name="needs[]" value="Strategy"> Strategy</label><label><input type="checkbox" name="needs[]" value="Content"> Content</label><label><input type="checkbox" name="needs[]" value="Social management"> Social management</label><label><input type="checkbox" name="needs[]" value="Paid social"> Paid social</label><label><input type="checkbox" name="needs[]" value="SEO / AEO"> SEO / AEO</label><label><input type="checkbox" name="needs[]" value="Not sure"> Not sure yet</label>
          </div>
        </fieldset>
        <div class="row2">
          <div class="f"><label for="a-budget">Monthly investment</label>
            <select id="a-budget" name="budget" required><option value="">Select a range</option><option>$3,000 – $5,000 / month</option><option>$5,000 – $10,000 / month</option><option>$10,000+ / month</option><option>One-time project (The Blueprint)</option></select></div>
          <div class="f"><label for="a-time">Timeline</label><select id="a-time" name="timeline"><option>As soon as possible</option><option>Within 1–3 months</option><option>Just exploring</option></select></div>
        </div>
        <div class="f"><label for="a-msg">Where are you now, and where do you want to be?</label><textarea id="a-msg" name="message"></textarea></div>
        <button class="btn red" type="submit">Submit application</button>
        <p class="formmsg" aria-live="polite"></p>
      </form>
    </div>
  </section>
</main>
{footer()}"""
    schema = [{"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": SITE + "/studio/#studio", "name": "Engage Era Studio", "url": SITE + "/studio/", "email": EMAIL,
         "image": SITE + "/assets/og/studio.png", "parentOrganization": {"@id": SITE + "/#org"}, "founder": {"@id": SITE + "/founder/#ben"},
         "description": "Social media management and content production agency for founders, artists and brands, based in Palm Beach and Jupiter, Florida.",
         "address": {"@type": "PostalAddress", "addressLocality": "Palm Beach", "addressRegion": "FL", "addressCountry": "US"},
         "areaServed": [{"@type": "City", "name": "Palm Beach"}, {"@type": "City", "name": "Jupiter"}, {"@type": "City", "name": "West Palm Beach"}, {"@type": "Country", "name": "United States"}],
         "knowsAbout": ["Social media management", "Content production", "Brand strategy", "Organic social growth", "Paid social advertising", "SEO", "Answer engine optimization"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in STUDIO_FAQ]}]}]
    write("studio/index.html", page("studio/", "Social Media & Content Production Agency in Palm Beach | Engage Era Studio",
                                    "Engage Era Studio is a social media and content production agency for founders, artists and brands. Based in Palm Beach and Jupiter, FL, working nationwide.",
                                    body, depth=1, active="studio", schema=schema, og="og/studio.png", word_extra="<small>Studio</small>"))


# ---------- Founder ----------
def build_founder():
    body = f"""{masthead(date=False)}
<main id="main">
  <section class="page-hero gut">
    <div class="max founder-grid">
      <div class="post">{cover({"slug": "founder", "title": "Ben Meller", "image": FOUNDER_PHOTO}, "../")}</div>
      <div class="copy">
        <span class="kicker">Founder</span>
        <h1>Ben Meller</h1>
        <div class="tag">The entrepreneur's entrepreneur.</div>
        <p>Ben is the founder of Engage Era, a marketing news outlet, and Engage Era Studio, its in-house social media and content agency. He started Engage Era to cover marketing the way it actually happens: fast, from the inside, with the people making it.</p>
        <p>He works alongside founders, artists and brands building audiences, and has created for names including SoFi, Oil Nut Bay, Good Molecules, Rise Above and Rome. He's based in Palm Beach and Jupiter, Florida, and spends a lot of time on the road with the people he works with.</p>
        <div class="links"><a href="{IG_BEN}" rel="noopener">@benmeller</a><a href="../studio/index.html">Work with Ben</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      </div>
    </div>
  </section>
</main>
{footer()}"""
    schema = [{"@context": "https://schema.org", "@graph": [dict(BEN, description="Founder of Engage Era and Engage Era Studio.", knowsAbout=["Social media marketing", "Content production", "Founder brands", "Brand strategy"]),
                                                            {"@type": "ProfilePage", "mainEntity": {"@id": SITE + "/founder/#ben"}, "url": SITE + "/founder/"}]}]
    write("founder/index.html", page("founder/", "Ben Meller, Founder of Engage Era",
                                     "Ben Meller is the founder of Engage Era, a marketing news outlet, and Engage Era Studio, a social media and content agency based in Palm Beach, FL.",
                                     body, depth=1, active="founder", schema=schema))


# ---------- The Brief ----------
def build_brief():
    body = f"""{masthead(date=False)}
<main id="main">
  <div class="page-hero gut"><div class="max"><span class="kicker">Newsletter</span><h1>The <span class="r">Brief</span></h1><p class="sub">Every weekday morning: the platform updates, campaigns and founder moves that matter for brands, in about three minutes. <b>Free.</b></p></div></div>
  {brief_band()}
  <section class="band gut"><div class="max"><div class="why">
    <div><h3>What changed</h3><p>Instagram, TikTok, Meta, Google and AI tools. The updates that affect brands, without the noise.</p></div>
    <div><h3>What worked</h3><p>Campaigns and founder moves worth stealing from, and why they worked.</p></div>
    <div><h3>What to do</h3><p>One practical takeaway in every issue you can use the same day.</p></div>
  </div></div></section>
</main>
{footer()}"""
    write("brief/index.html", page("brief/", "The Brief: Daily Marketing News Newsletter | Engage Era",
                                   "The Brief is Engage Era's free weekday newsletter: platform updates, campaigns and founder moves that matter for brands, in three minutes.",
                                   body, depth=1, active="brief"))


# ---------- Private results ----------
def build_results():
    names = "".join(f'<span class="name">{b}</span>' for b in BRANDS)
    body = f"""<div class="lockbar gut"><div class="max"><span class="brand">{MARK}<span class="word">Engage Era</span></span><span class="kicker plain">Private · Not for distribution</span></div></div>
<main id="main">
  <div class="page-hero gut"><div class="max"><span class="kicker">Prepared for <span class="fill">Client name</span></span><h1>Studio <span class="r">results</span></h1><p class="sub">Engage Era reports on marketing every weekday. <b>Engage Era Studio</b> uses what we learn to grow founders, artists and brands. Here's what that looks like in practice.</p></div></div>
  <section class="band gut"><div class="max"><div class="roster"><span class="kicker">Brands we've created for</span>{names}</div></div></section>
  <section class="band gut"><div class="max" style="display:grid;gap:24px">
    <div class="head" style="margin-bottom:12px"><span class="kicker">Case studies</span><h2>The work</h2></div>
    <article class="case">
      <div class="top"><span class="kicker">Full social media management</span><div class="whoname">Rise Above with Kevin Lanning</div><div class="num"><div class="big">+70K</div><div class="unit">followers<br>in 3 months</div></div></div>
      <div class="stats"><div><span>Starting point</span><b><span class="fill">__ followers</span></b></div><div><span>Total views</span><b><span class="fill">__</span></b></div><div><span>Engagement</span><b><span class="fill">__%</span></b></div></div>
      <div class="did"><div><h3>Strategy</h3><p><span class="fill">Positioning + pillars</span></p></div><div><h3>Content</h3><p><span class="fill">Formats + volume</span></p></div><div><h3>Publishing</h3><p><span class="fill">Rhythm + platforms</span></p></div><div><h3>Community</h3><p><span class="fill">Engagement + collabs</span></p></div></div>
    </article>
    <article class="case soon"><div class="top"><span class="kicker">Content · Social</span><div class="whoname">Rome</div><div class="big" style="font-size:clamp(40px,6vw,72px)"><span class="fill">Headline result</span></div></div></article>
  </div></section>
  <section class="band gut"><div class="max">
    <div class="head"><span class="kicker">Ways to work together</span><h2>Three ways in</h2><p>Most partners start with The Blueprint.</p></div>
    <div class="pk">
      <article><span class="type">One-time project</span><h3>The Blueprint</h3><p>Positioning, brand world, content system and a 90-day plan.</p><p><b><span class="fill">$__</span></b></p></article>
      <article class="feat"><span class="type">Monthly partnership</span><h3>Growth</h3><p>Full social management, content production, organic growth and reporting.</p><p><b><span class="fill" style="color:#fff;border-color:#fff">$__ / month</span></b></p></article>
      <article><span class="type">Monthly partnership</span><h3>Full Production</h3><p>Everything in Growth, plus shoots, paid social, launches, SEO and AEO.</p><p><b><span class="fill">$__ / month</span></b></p></article>
    </div>
  </div></section>
  <section class="band gut"><div class="max"><div class="head"><span class="kicker">How we work</span><h2>What happens next</h2></div>
    <ol class="steps"><li><span class="n">1</span><h3>Call</h3><p>We walk through these results and your goals.</p></li><li><span class="n">2</span><h3>Proposal</h3><p>A scoped plan and investment within 48 hours.</p></li><li><span class="n">3</span><h3>Blueprint</h3><p>Positioning, content system, 90-day plan.</p></li><li><span class="n">4</span><h3>Build</h3><p>We produce, publish and grow. Monthly reporting, 3-month minimum.</p></li></ol>
  </div></section>
  <section class="band apply gut"><div class="max"><div><h2>Let's build<br><span class="r">your era.</span></h2><p style="color:var(--mute);margin-top:14px">{EMAIL} · Palm Beach · Jupiter, FL</p></div></div></section>
</main>"""
    write("results/index.html", page("results/", "Engage Era Studio: Private Results", "Private.", body, depth=1, noindex=True))


# ---------- Utility pages ----------
def build_utility():
    thanks = f"""{masthead(date=False)}
<main id="main"><div class="page-hero gut"><div class="max"><span class="kicker">Received</span><h1>You're <span class="r">in.</span></h1><p class="sub">Thanks. If you applied to the Studio, we'll reply within 48 hours. If you subscribed to The Brief, your first issue lands on the next weekday morning.</p><p style="margin-top:28px"><a class="btn" href="../index.html">Back to the news</a></p></div></div></main>
{footer()}"""
    write("thanks/index.html", page("thanks/", "Thanks | Engage Era", "Thanks for reaching out to Engage Era.", thanks, depth=1, noindex=True))
    nf = f"""{masthead(date=False)}
<main id="main"><div class="page-hero gut"><div class="max"><span class="kicker">404</span><h1>Story <span class="r">not found.</span></h1><p class="sub">That page moved or never existed.</p><p style="margin-top:28px"><a class="btn" href="/index.html">Back to the news</a></p></div></div></main>
{footer()}"""
    write("404.html", page("404", "Page not found | Engage Era", "Page not found.", nf, depth=0, noindex=True))
    urls = ["", "news/", "studio/", "founder/", "brief/"] + [f"news/{a['slug']}/" for a in ARTICLES]
    today = datetime.date.today().isoformat()
    sm = "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("_headers", "/results/*\n  X-Robots-Tag: noindex, nofollow\n/thanks/*\n  X-Robots-Tag: noindex\n/assets/*\n  Cache-Control: public, max-age=604800\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /results/\nDisallow: /thanks/\n\nSitemap: {SITE}/sitemap.xml\n")
    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -208 710 710"><rect x="-20" y="-208" width="710" height="710" rx="140" fill="#060819"/><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aaee6"/><stop offset="1" stop-color="#1466ff"/></linearGradient></defs><g fill="url(#g)"><path d="M51 0H346L297 67H39Z"/><path d="M31 117H261L216 176H20Z"/><path d="M11 227H247L420 0H670L658 67H440L269 293H0Z"/><path d="M466 117H650L640 176H422Z"/><path d="M389 227H631L620 293H342Z"/></g></svg>')


# ---------- Share images (1200x630) ----------
def build_og():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("PIL missing: skipped share images"); return
    impact = "/System/Library/Fonts/Supplemental/Impact.ttf"
    mono = "/System/Library/Fonts/SFNSMono.ttf"
    if not os.path.exists(impact):
        print("Impact font missing: skipped share images"); return
    polys = [[(51,0),(346,0),(297,67),(39,67)],[(31,117),(261,117),(216,176),(20,176)],[(11,227),(247,227),(420,0),(670,0),(658,67),(440,67),(269,293),(0,293)],[(466,117),(650,117),(640,176),(422,176)],[(389,227),(631,227),(620,293),(342,293)]]

    def logo(img, x, y, scale):
        d = ImageDraw.Draw(img)
        top, bot = (90, 174, 230), (20, 102, 255)
        mask = Image.new("L", img.size, 0); md = ImageDraw.Draw(mask)
        for p in polys: md.polygon([(x + a * scale, y + b * scale) for a, b in p], fill=255)
        grad = Image.new("RGB", img.size)
        gd = ImageDraw.Draw(grad)
        h = 293 * scale
        for i in range(int(h) + 1):
            t = i / max(h, 1)
            gd.line([(0, y + i), (img.size[0], y + i)], fill=tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3)))
        img.paste(grad, (0, 0), mask)

    def card(fname, kicker, headline, redword=None):
        W, H = 1200, 630
        img = Image.new("RGB", (W, H), (6, 8, 25))
        d = ImageDraw.Draw(img)
        for r in range(420, 0, -6):  # blue glow
            a = int(60 * (1 - r / 420))
            d.ellipse([W - 260 - r, 120 - r, W - 260 + r, 120 + r], fill=(6 + a // 4, 8 + a // 2, 25 + a))
        d.rectangle([0, H - 10, W, H], fill=(228, 38, 44))
        logo(img, 64, 56, 0.16)
        d.text((190, 58), "ENGAGE ERA", font=ImageFont.truetype(impact, 34), fill=(244, 245, 250))
        d.rectangle([64, 150, 94, 153], fill=(228, 38, 44))
        d.text((106, 140), kicker.upper(), font=ImageFont.truetype(mono, 22), fill=(154, 161, 194))
        f = ImageFont.truetype(impact, 76)
        words, lines, cur = headline.upper().split(), [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if d.textlength(test, font=f) > W - 128: lines.append(cur); cur = w
            else: cur = test
        lines.append(cur)
        y = 190
        rw = redword.upper().split() if redword else []
        for line in lines[:5]:
            x = 64
            for w in line.split():
                d.text((x, y), w, font=f, fill=(228, 38, 44) if w.strip(".,?") in rw else (244, 245, 250))
                x += d.textlength(w + " ", font=f)
            y += 84
        os.makedirs(os.path.join(ROOT, "assets/og"), exist_ok=True)
        img.save(os.path.join(ROOT, "assets/og", fname), optimize=True)

    card("default.png", "Marketing news", "Marketing news. Before it's news.", "news.")
    card("studio.png", "Engage Era Studio · Palm Beach", "We cover what works. Then we build it.", "then we build it.")
    for a in ARTICLES:
        m = re.search(r"<r>(.*?)</r>", a["title"])
        card(f"{a['slug']}.png", a["cat_label"], plain(a["title"]), m.group(1) if m else None)

    from PIL import ImageFilter

    def post(slug, kicker, headline, redword=None):
        """Fallback cover in the @engageeraco post style (1080x1350), used until the real Grok post is saved."""
        W, H = 1080, 1350
        glow = Image.new("RGB", (W, H), (6, 8, 25))
        g = ImageDraw.Draw(glow)
        g.ellipse([W * 0.15, -H * 0.15, W * 1.15, H * 0.62], fill=(22, 60, 170))
        im = glow.filter(ImageFilter.GaussianBlur(140))
        d = ImageDraw.Draw(im)
        logo(im, 64, 64, 0.2)
        size = 104
        while True:
            f = ImageFont.truetype(impact, size)
            words, lines, cur = headline.upper().split(), [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if d.textlength(t, font=f) > W - 128: lines.append(cur); cur = w
                else: cur = t
            lines.append(cur)
            if len(lines) <= 5 or size <= 70: break
            size -= 6
        lh = int(size * 1.02)
        y = H - 90 - lh * len(lines)
        d.rectangle([64, y - 52, 100, y - 47], fill=(228, 38, 44))
        d.text((114, y - 64), kicker.upper(), font=ImageFont.truetype(mono, 24), fill=(200, 205, 225))
        rw = [w.strip(".,?!") for w in (redword or "").upper().split()]
        for line in lines:
            x = 64
            for w in line.split():
                d.text((x, y), w, font=f, fill=(228, 38, 44) if w.strip(".,?!") in rw else (244, 245, 250))
                x += d.textlength(w + " ", font=f)
            y += lh
        os.makedirs(os.path.join(ROOT, "assets/posts"), exist_ok=True)
        im.save(os.path.join(ROOT, "assets/posts", f"{slug}.png"), optimize=True)

    for a in ARTICLES + INSTAGRAM:
        if a.get("image"): continue
        m = re.search(r"<r>(.*?)</r>", a["title"])
        post(a["slug"], a["cat_label"], plain(a["title"]), m.group(1) if m else None)
    # founder placeholder until the real photo arrives
    fim = Image.new("RGB", (1080, 1350), (6, 8, 25))
    fg = ImageDraw.Draw(fim); fg.ellipse([0, 200, 1080, 1150], fill=(20, 40, 110))
    fim = fim.filter(ImageFilter.GaussianBlur(160)); logo(fim, 290, 590, 0.75)
    fim.save(os.path.join(ROOT, "assets/posts", "founder.png"), optimize=True)
    # square logo for schema
    img = Image.new("RGB", (600, 600), (6, 8, 25)); logo(img, 65, 153, 0.7); img.save(os.path.join(ROOT, "assets/logo.png"))


if __name__ == "__main__":
    build_home(); build_news(); build_articles(); build_studio(); build_founder(); build_brief(); build_results(); build_utility(); build_og()
    print("Built into", os.path.abspath(ROOT))
