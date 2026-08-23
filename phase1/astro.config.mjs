import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://suiteswithkeith.com',
  trailingSlash: 'ignore',
  build: { format: 'file' },
});
