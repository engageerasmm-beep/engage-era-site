# Engage Era website

Static site for eesmm.com: the newsroom (home, news, articles, The Brief), Engage Era Studio, the founder page, and a private results page.

## Structure
- `src/articles.py` holds every article. Newest first.
- `src/build.py` builds all pages, the sitemap, and share images into `public/`.
- `public/` is what gets hosted.

## Add an article
1. Copy an article block in `src/articles.py`, give it a new `slug`, and write it.
2. Run `python3 src/build.py`.
3. Deploy (push to GitHub, or drag `public/` into Netlify).

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
