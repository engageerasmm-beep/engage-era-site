# Launching eesmm.com

About 30 minutes of clicking, plus waiting for DNS. Your Microsoft email keeps working the whole time as long as you only change the two records named in Part 2.

## Part 1: Put the site on Netlify (10 min)
1. Go to netlify.com and sign up (free).
2. Click **Add new project → Deploy manually**, then drag in `deploy/engage-era-site.zip`.
3. **Project configuration → Change project name** → `engageera`. Your site is now live at `engageera.netlify.app`. Click through it on your phone.
4. **Forms → Enable form detection**, then drag the zip in again (Deploys tab) so Netlify finds the forms.
5. **Forms → Form notifications → Add notification → Email** → `ben@eesmm.com`. Do it for both forms: `apply` (Studio applications) and `brief` (newsletter).

## Part 2: Point eesmm.com at it (10 min + waiting)
6. Netlify: **Domain management → Add a domain** → `eesmm.com` → continue with external DNS.
7. GoDaddy: **My Products → eesmm.com → DNS**. Screenshot the whole records list first as a backup.
8. If GoDaddy's Website Builder is connected to the domain, disconnect it first, or it will put its records back.
9. Change only these:

| Type | Name | Value | Action |
|---|---|---|---|
| A | @ | `75.2.60.5` | Edit the existing @ record. Delete any other A or AAAA records for @. |
| CNAME | www | `engageera.netlify.app` | Edit the existing www record. |

10. **Do not touch** anything else, especially: MX, TXT, `autodiscover`, `lyncdiscover`, `sip`, `enterpriseregistration`, `enterpriseenrollment`, and SRV records. Those run your Microsoft email.
11. Wait. Usually minutes, sometimes up to 24 hours. Then in Netlify: **Domain management → HTTPS → Verify DNS configuration**, and let it issue the free SSL certificate.
12. Send yourself a test email to ben@eesmm.com and reply to it to confirm email still works.
13. Once the site loads at eesmm.com, cancel the GoDaddy Website Builder plan.

## Part 3: Tell Google (15 min)
14. Google Search Console → add **eesmm.com** as a Domain property. It gives you a TXT record to add at GoDaddy (adding a TXT record is safe for email). Then submit `https://eesmm.com/sitemap.xml`.
15. Create a Google Business Profile for Engage Era Studio in Palm Beach, linking to `https://eesmm.com/studio/`.

## Updating the site later
Claude rebuilds the site and gives you a new zip. In Netlify: **Deploys → drag the zip in**. Live in about 30 seconds.
