# Private client proposals

This folder holds **unlisted** proposal pages — one per client. Each is a normal HTML
page hosted on the live site, but it is only discoverable by someone who has the exact
link. Nothing here is linked from the site's navigation, and none of these pages are
listed in `sitemap.xml`.

## The privacy model (read this)

GitHub Pages is a **public** static host — there is no login. "Private" here means
**unlisted**, the same idea as a Google Doc set to "anyone with the link" or an unlisted
YouTube video:

- The filename is a long, random string, so the URL is effectively impossible to guess.
- Each page carries `<meta name="robots" content="noindex, nofollow">`, so search
  engines will not index it.
- The page is not linked from anywhere and is not in the sitemap, so it won't be crawled
  or discovered.

**Caveat:** anyone the client forwards the link to can open it. This is fine for travel
proposals. If a specific proposal ever needs true access control (password / login),
tell Keith — that's a different setup (client-side encryption or Cloudflare Access).

## Adding a new client proposal

1. Start from `sample-proposal.html` in the site root — it's the master template
   (cover → overview → itinerary spreads → comparison → closing).
2. Fill in the real content, resort photos (drop them in `images/proposals/` or a
   per-client subfolder), dates and pricing.
3. Remove the `.pr-sample-note` bar at the top, and set the cover's "Prepared For" name
   to the real client.
4. Confirm the page has this in its `<head>`:
   ```html
   <meta name="robots" content="noindex, nofollow">
   ```
   (The public sample does **not** have this — private ones **must**.)
5. Save it here with a random filename, e.g.:
   ```
   proposals/8f3a9c2e7b1d4a6f.html
   ```
   Generate a random slug with:
   ```
   openssl rand -hex 8
   ```
6. Do **not** add it to `sitemap.xml` and do **not** link it from any page.
7. Commit + push. The private link to send the client is then:
   ```
   https://suiteswithkeith.com/proposals/8f3a9c2e7b1d4a6f.html
   ```

## Workflow with Claude

Keith designs each proposal, then shares the finished version. Claude converts it into an
unlisted page here (following the steps above) and hands back the link to send.
