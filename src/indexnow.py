"""Tell Bing (and other IndexNow engines) about new or updated pages, so they're crawled within hours.

Run after a deploy is live:
    python3 src/indexnow.py                      # every URL in public/sitemap.xml
    python3 src/indexnow.py https://eesmm.com/news/<slug>/ ...   # just these

The key file public/<KEY>.txt must be live on eesmm.com for submissions to be accepted.
"""
import json, os, re, sys, urllib.request

KEY = "9f7203028dcf4c8206df05156f7a082f"
HOST = "eesmm.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_urls():
    xml = open(os.path.join(ROOT, "public", "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def submit(urls):
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


if __name__ == "__main__":
    urls = sys.argv[1:] or sitemap_urls()
    status = submit(urls)
    # 200 = accepted, 202 = accepted (key pending validation); anything else is a problem
    print(f"IndexNow: submitted {len(urls)} URL(s), HTTP {status}")
    sys.exit(0 if status in (200, 202) else 1)
