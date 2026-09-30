import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const notes = await getCollection('notes');
  return rss({
    title: 'hoanhi — Technical Artist',
    description: 'Notes about tech art, mobile games, shaders, and more.',
    site: context.site!,
    items: notes
      .filter((note) => !note.data.draft)
      .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
      .map((note) => ({
        title: note.data.title,
        pubDate: note.data.pubDate,
        description: note.data.description,
        link: `/notes/${note.slug}/`,
      })),
  });
}
