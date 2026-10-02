# Engage Era website

Static site for eesmm.com: the newsroom (home, news, articles, The Brief), Engage Era Studio, the founder page, and a private results page.

## Structure
- `src/articles.py` holds every article. Newest first.
- `src/build.py` builds all pages, the sitemap, and share images into `public/`.
- `public/` is what gets hosted.

## Add an article
1. Copy an article block in `src/articles.py`, give it a new `slug`, and write it.
2. Run `python3 src/build.py`.
3. Commit and push to GitHub (`git@github.com:engageerasmm-beep/engage-era-site.git`, branch `main`). Netlify deploys automatically in about a minute.
4. Once it's live, run `python3 src/indexnow.py <new article URL>` so Bing crawls it within hours.

## Search and analytics
- Google Search Console and Google Analytics 4 (`G-TDJCPQLEHK`, set in `src/build.py`) live in the engageerasmm@gmail.com account. Search Console is verified by `public/google67206611d6aee710.html`: don't delete it.
- Bing Webmaster Tools was imported from Search Console. IndexNow key file: `public/9f7203028dcf4c8206df05156f7a082f.txt` (don't delete).

Each publish uses 15 of Netlify's 300 free monthly credits, so batch changes: publish 2–3 times a week, not after every edit.

## Pages
| URL | Page | Indexed |
|---|---|---|
| / | Newsroom home | yes |
| /news/ | All stories | yes |
| /news/<slug>/ | Articles | yes |
| /studio/ | Engage Era Studio (send this to clients) | yes |
| /founder/ | Ben Meller | yes |
| /brief/ | Newsletter | yes |
| /results/ | Private results, unlisted | no |

## Forms
The Studio application and newsletter use Netlify Forms. In Netlify: Forms → Form notifications → email ben@eesmm.com.

## Before launch
- Real photos for the founder page and article headers
- Fill the blanks on /results/
- Confirm SoFi and other brand names are OK to show
- Point eesmm.com DNS at Netlify WITHOUT touching the email (MX) records
