// General client praise for Keith, shown in the book-through-me sections of
// hotel pages that have no review of their own. Each page gets one quote,
// picked from its slug so it never changes between builds. Keep this list
// and its order in sync with js/swk-book.js (comparison pages).
export const clientQuotes = [
  { quote: '&ldquo;I love booking hotels through you. I&rsquo;m going to spread the word to everyone.&rdquo;', cite: 'C&amp;J &middot; SWK Clients' },
  { quote: '&ldquo;Worth its weight in gold. I won&rsquo;t ever book a stay without Keith again.&rdquo;', cite: 'Caitlin M. &middot; SWK Client' },
  { quote: '&ldquo;Keith made me believe in using travel agents again. He carefully put together thoughtful options and called out why he would choose each.&rdquo;', cite: 'Stephanie F. &middot; SWK Client' },
  { quote: '&ldquo;He handled everything, from booking to communications, and I didn&rsquo;t have to worry about a thing.&rdquo;', cite: 'Nida T. &middot; SWK Client' },
  { quote: '&ldquo;Luxury hotels naturally have many guests competing for attention, but having Keith in our corner made us feel like a priority throughout the entire experience.&rdquo;', cite: 'Tyler &amp; Spencer C. &middot; SWK Clients' },
];

// C&J stayed at Passalacqua through Keith, so its pages always carry their quote.
export function clientQuoteFor(slug) {
  if (/passalacqua/.test(slug)) return clientQuotes[0];
  let h = 0;
  for (let i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) >>> 0;
  return clientQuotes[h % clientQuotes.length];
}
