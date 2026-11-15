/**
 * Suites With Keith: newsletter subscribe endpoint (Cloudflare Worker).
 *
 * js/swk-newsletter-prompt.js POSTs { email, source, page, website } as JSON here.
 * This adds the email to Beehiiv with the publication API key, which must never
 * sit in the site's public files.
 *
 * Secrets (Cloudflare > Worker > Settings > Variables and Secrets, type "Secret"):
 *   BEEHIIV_API_KEY   Beehiiv > Settings > Integrations > API > Create new key
 *   BEEHIIV_PUB_ID    the Publication ID shown on that same page (starts "pub_")
 *
 * Responses: 200 { ok: true } | 400 bad email | 403 wrong origin | 502 Beehiiv error
 */

const ALLOWED_ORIGINS = [
  "https://suiteswithkeith.com",
  "https://www.suiteswithkeith.com",
  "https://suiteswithkeith.github.io",
];
// Local previews (any localhost port) are allowed so the form can be tested.
const LOCAL_ORIGIN = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function allowedOrigin(origin) {
  return origin && (ALLOWED_ORIGINS.includes(origin) || LOCAL_ORIGIN.test(origin));
}

function reply(body, status, origin) {
  const headers = { "Content-Type": "application/json", "Vary": "Origin" };
  if (allowedOrigin(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
    headers["Access-Control-Allow-Methods"] = "POST, OPTIONS";
    headers["Access-Control-Allow-Headers"] = "Content-Type";
    headers["Access-Control-Max-Age"] = "86400";
  }
  return new Response(body === null ? null : JSON.stringify(body), { status, headers });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") return reply(null, allowedOrigin(origin) ? 204 : 403, origin);
    if (request.method !== "POST") return reply({ ok: false, error: "method" }, 405, origin);
    if (!allowedOrigin(origin)) return reply({ ok: false, error: "origin" }, 403, origin);

    let data;
    try { data = await request.json(); } catch (e) { return reply({ ok: false, error: "json" }, 400, origin); }

    // Honeypot: the form has a hidden "website" field people never see. Bots fill it.
    // Answer as if it worked so they don't retry.
    if (data.website) return reply({ ok: true }, 200, origin);

    const email = String(data.email || "").trim().toLowerCase();
    if (!EMAIL_RE.test(email) || email.length > 254) return reply({ ok: false, error: "email" }, 400, origin);

    const source = String(data.source || "website").slice(0, 40);
    const page = String(data.page || "/").slice(0, 200);

    const res = await fetch(
      `https://api.beehiiv.com/v2/publications/${env.BEEHIIV_PUB_ID}/subscriptions`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.BEEHIIV_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          reactivate_existing: false,
          send_welcome_email: true,
          utm_source: "website",
          utm_medium: source,          // "slide-in" or "inline"
          utm_campaign: "swk-newsletter-prompt",
          referring_site: `https://suiteswithkeith.com${page}`,
        }),
      }
    );

    if (!res.ok) {
      console.log("beehiiv error", res.status, (await res.text()).slice(0, 300));
      return reply({ ok: false, error: "upstream" }, 502, origin);
    }
    return reply({ ok: true }, 200, origin);
  },
};
