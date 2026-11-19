# Newsletter subscribe endpoint

`worker.js` is a Cloudflare Worker that takes the email from the newsletter card and the
inline comparison-page block (`js/swk-newsletter-prompt.js`) and adds it to Beehiiv.
The Beehiiv API key lives in Cloudflare, never in the site's files.

Beehiiv's free Launch plan includes the API (everything except the Send API, which this
does not use). Cloudflare Workers' free plan covers 100,000 requests a day.

**Live since Nov 15, 2026:** `https://swk-subscribe.keith-pence.workers.dev`
(Cloudflare Worker `swk-subscribe`; `BEEHIIV_PUB_ID` is a plain variable,
`BEEHIIV_API_KEY` a secret; Beehiiv key named "Website signup (Cloudflare Worker)").
The dashboard copy was typed in as one compacted line; `worker.js` here is the readable
source of truth. Paste it over the dashboard copy if it ever needs changing.

## One-time setup (about 10 minutes)

1. **Beehiiv API key.** Beehiiv > Settings > Integrations > API > Create new key.
   Copy the key (shown once) and the **Publication ID** on the same page (starts `pub_`).
2. **Cloudflare Worker.** In the Cloudflare dashboard: Workers & Pages > Create >
   Create Worker. Name it `swk-subscribe`, Deploy, then Edit code. Replace everything
   with the contents of `worker.js` and Deploy again.
3. **Secrets.** Worker > Settings > Variables and Secrets > Add, type **Secret**:
   - `BEEHIIV_API_KEY` = the key from step 1
   - `BEEHIIV_PUB_ID` = the Publication ID from step 1
4. **Turn it on.** Copy the Worker's URL (`https://swk-subscribe.<subdomain>.workers.dev`)
   into `endpointUrl` at the top of `js/swk-newsletter-prompt.js`. Until that is filled
   in, the script falls back to the Beehiiv embed.

## Checking it

- Open any page with `?swk-newsletter=preview`, subscribe with a test address, and
  confirm it appears in Beehiiv > Audience with UTM source `website`, medium
  `slide-in` or `inline`, campaign `swk-newsletter-prompt`.
- Errors from Beehiiv show in Worker > Logs ("beehiiv error ...").

## Notes

- Only suiteswithkeith.com, www, the github.io address and localhost may call it.
- The form has a hidden `website` honeypot field; anything that fills it is answered
  with success and not sent to Beehiiv.
- `send_welcome_email: true` sends Beehiiv's welcome email if one is set up there.
