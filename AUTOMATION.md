# Automated publishing run (Mon / Wed / Fri 9 AM)

This is the playbook the scheduled Claude task follows. Ben approved **automatic publishing**: stories that pass every check go live without asking. Anything that fails a check is **held, not published**, and reported to Ben.

## 0. Setup
- Project folder: `~/Documents/Engage Era/engage-era-site` (git repo, remote `origin` = `git@github.com:engageerasmm-beep/engage-era-site.git`, branch `main`).
- Start with `git pull --ff-only origin main`. If that fails, stop and notify Ben.
- Netlify deploys automatically on every push to `main`. Each push costs 15 of 300 free monthly credits, so push **once per run at most**.

## 1. Find new stories
- Drive Inbox folder ID: `1b5R93_5dA9Q_IBZp4anHRnPtwKTyxNwJ` (in the engageerasmm@gmail.com / ben@eesmm.com Drive, shared by link).
- List its subfolders with the Google Drive connector: search query `parentId = '1b5R93_5dA9Q_IBZp4anHRnPtwKTyxNwJ'` (paginate with the page token until empty).
- Skip any folder whose ID is in `src/processed.json` → `published`.
- For each new folder, list its files (`parentId = '<folderId>'`). Expect `post.jpg` and `packet.txt`. Ignore files starting with `OLD-`.
- Download files with curl (the folder is link-shared):
  `curl -sL "https://drive.google.com/uc?export=download&id=<fileId>" -o <file>`
  If the connector's download tool works, that's fine too (text comes back base64).
- A folder with no `packet.txt` or no `post.jpg` is incomplete: hold it with reason "missing files".

## 2. Check every story (hold on any failure)
Read `packet.txt` (format in GROK.md) and look at `post.jpg`.
1. **Headline match:** the headline on the image must make the same claim as `HEADLINE:` in the packet. Extra claims on the image ("now", "two of them", numbers not in KEY FACTS) → hold.
2. **Facts:** open the source links with WebFetch and confirm each KEY FACT, and confirm any quote word for word. Drop any fact you can't confirm. If the core claim of the story can't be confirmed → hold. If a source is paywalled or unreachable, a second reputable source confirming it is enough; otherwise hold.
3. **Images:** no AI-generated or AI-edited images of real people. Real people must come from official sources (press kit, newsroom, the brand's or person's own site/social). Photos credited to Getty, AP, Reuters or news outlets → hold.
4. **Category:** must be one of Platforms, AI, Founder stories, Campaigns, Creators, Guides.
5. **Guides** (CATEGORY: Guides) are covers for articles Claude already wrote: if an article with a matching headline exists in `src/articles.py`, just attach the image (step 3b). If none exists, hold with reason "guide cover without an article".

## 3. Publish the stories that passed
a. **Cover:** save `post.jpg` optimized to `public/assets/img/<slug>.jpg`
   (`python3 -c "from PIL import Image; Image.open('post.jpg').convert('RGB').save('public/assets/img/<slug>.jpg', quality=82, optimize=True, progressive=True)"`).
   Slug = the folder's short name (lowercase, dashes).
b. **Article:** add a new block at the **top** of `ARTICLES` in `src/articles.py`, matching the existing news entries exactly (keys: slug, cat, cat_label, date, read, image, image_credit, title, seo_title, description, dek, tldr, faq, body).
   - `title`: the packet headline, Title Case, red word wrapped in `<r>…</r>`.
   - `date`: today's date. `read`: honest estimate.
   - `body`: 400–700 words, plain and direct, sections: what happened, the details, why brands should care, what to do. Link each fact to its source inline. End with a `<h2>Sources</h2>` list.
   - `faq`: 3 questions people would actually search, answered in 1–2 sentences using only confirmed facts.
   - Match the voice of the existing articles. No hype, no invented numbers.
   - `cat` keys: platforms, ai, founders, campaigns, creators, guides.
c. Run `python3 src/build.py`. It must finish without errors.
d. Sanity check: `public/news/<slug>/index.html` exists and contains the headline.
e. Add each published folder ID to `src/processed.json` → `published`. Add held ones to `held` as `{"<folderId>": "<folder name>: <reason>"}` (they'll be retried next run; remove from `held` once published).

## 4. Ship
- If nothing new passed, don't push. Still update `held` if needed (commit locally).
- Otherwise: `git add -A && git commit -m "Publish: <slugs>"` (end the message with `Co-Authored-By: Claude <noreply@anthropic.com>`), then `git push origin main`.
- Wait ~90 seconds, then confirm with curl that `https://eesmm.com/news/<slug>/` returns 200. Report if not.

## 5. Report to Ben
Send one short notification (PushNotification if available), e.g.:
`Engage Era: published 3 stories (meta-one, bloom, …). Held 1: musk-ad (image headline says "two", packet says Meta only).`
If nothing was in the Inbox: `Engage Era: no new stories in the Inbox.`
Also leave the same summary as the final message of the run.

## Never
- Never publish a story that failed a check.
- Never delete anything in Drive or in the repo's history.
- Never change site design, the Studio page, pricing, or brand names during an automated run.
- Never push more than once per run.
