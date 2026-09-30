# Engage Era publishing workflow

## Rhythm
| Channel | How often | What |
|---|---|---|
| Instagram @engageeraco | Daily | Fast news posts (Grok) |
| Website articles | 2–3 per week | The biggest stories, expanded |
| Weekly roundup | Fridays | "Everything that changed this week" covering the smaller posts |

## Ben (about 2 minutes per story)
1. Give Grok the story. It returns the Instagram post and the packet (see GROK.md).
2. Save them to `Engage Era Website/Inbox/<date> <short-name>/` in Google Drive.
3. Post to Instagram.
4. Tell Claude "new stories in the inbox" (or let the scheduled check pick them up).
5. Review the preview link Claude sends and reply "approve" or with changes.

## Claude (per batch)
1. Read the Inbox folder in Drive.
2. Check every fact against its source; flag anything unconfirmed or any image that isn't safe to publish.
3. Write the article: 600–900 words, short-version box, FAQ, sources, author box. Pick a slug and SEO title.
4. Add `post.jpg` to `public/assets/img/` and set `image` on the article. It becomes the cover everywhere; without one, a generated post in the same style is used.
5. Rebuild the site, send Ben a preview.
6. On "approve": publish (push to GitHub, Netlify deploys automatically), then move the Drive folder to `Published/`.

## Later: fully hands-free intake
Switch @engageeraco to an Instagram Business account, then connect Zapier or Make: "New Instagram post" → save image + caption to the Drive Inbox. Posting to Instagram alone then feeds the website queue.
