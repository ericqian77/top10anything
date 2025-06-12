import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { query } = req.body as { query?: string };
  if (!query) {
    return res.status(400).json({ error: 'Missing query' });
  }
  try {
    const resp = await fetch(process.env.AGENT_API_URL || '', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await resp.json();
    return res.status(resp.status).json(data);
  } catch (err: any) {
    return res.status(500).json({ error: 'Proxy error', detail: err.message });
  }
}
