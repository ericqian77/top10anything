import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const query = (req.query.q as string) || '';
  if (!query) {
    return res.status(400).json({ error: 'Missing query' });
  }
  try {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent('top 10 ' + query)}&format=json&no_redirect=1&no_html=1`;
    const resp = await fetch(url);
    const data = await resp.json();
    const results = (data.RelatedTopics || []).map((t: any) => ({
      title: t.Text,
      link: t.FirstURL,
    }));
    return res.status(200).json({ results });
  } catch (err: any) {
    return res.status(500).json({ error: 'Search error', detail: err.message });
  }
}
