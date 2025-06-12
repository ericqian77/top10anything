import React, { useState } from 'react';
import { Item } from '../App';

interface Props {
  onResult: (items: Item[]) => void;
}

export default function SearchForm({ onResult }: Props) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (res.ok) {
        onResult(data.items);
      } else {
        alert(data.error || 'Error');
      }
    } catch (err) {
      alert('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-2">
      <input
        className="flex-1 p-2 border rounded dark:bg-gray-700"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Top 10 ..."
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleSearch}
        disabled={loading}
      >
        {loading ? 'Loading...' : '查询'}
      </button>
    </div>
  );
}
