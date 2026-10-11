import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { rehypeImageCaption } from './src/utils/rehype-caption.mjs';

export default defineConfig({
  site: 'https://hoanhi.vercel.app',
  integrations: [
    mdx({
      rehypePlugins: [rehypeImageCaption],
    }),
    sitemap(),
  ],
  markdown: {
    rehypePlugins: [rehypeImageCaption],
    shikiConfig: {
      theme: 'github-dark',
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
