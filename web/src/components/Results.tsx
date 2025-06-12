import React, { useRef } from 'react';
import html2canvas from 'html2canvas';
import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis, ResponsiveContainer } from 'recharts';
import { Item } from '../App';

interface Props {
  items: Item[];
}

export default function Results({ items }: Props) {
  const chartRef = useRef<HTMLDivElement>(null);

  const share = async (platform: 'twitter' | 'wechat' | 'weibo') => {
    const url = new URL(window.location.href);
    url.searchParams.set('data', btoa(JSON.stringify(items)));

    if (chartRef.current) {
      const canvas = await html2canvas(chartRef.current);
      url.searchParams.set('img', canvas.toDataURL('image/png'));
    }

    const shareUrl = encodeURIComponent(url.toString());

    if (platform === 'twitter') {
      window.open(`https://twitter.com/intent/tweet?url=${shareUrl}`);
    } else if (platform === 'weibo') {
      window.open(`https://service.weibo.com/share/share.php?url=${shareUrl}`);
    } else {
      await navigator.clipboard.writeText(url.toString());
      alert('URL copied, share it in WeChat');
    }
  };

  return (
    <div className="space-y-4">
      <table className="min-w-full text-sm border">
        <thead>
          <tr className="bg-gray-200 dark:bg-gray-700">
            <th className="px-2 py-1 text-left">Rank</th>
            <th className="px-2 py-1 text-left">Item</th>
            <th className="px-2 py-1 text-right">Value</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, idx) => (
            <tr key={idx} className="odd:bg-gray-50 dark:odd:bg-gray-800">
              <td className="px-2 py-1">{idx + 1}</td>
              <td className="px-2 py-1">{item.name}</td>
              <td className="px-2 py-1 text-right">{item.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="h-64 w-full" ref={chartRef}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={items} layout="vertical" margin={{ left: 40 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" width={100} />
            <Tooltip />
            <Bar dataKey="value" fill="#60a5fa" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => share('twitter')}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          Twitter
        </button>
        <button
          onClick={() => share('wechat')}
          className="bg-green-600 text-white px-3 py-1 rounded"
        >
          WeChat
        </button>
        <button
          onClick={() => share('weibo')}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Weibo
        </button>
      </div>
    </div>
  );
}
