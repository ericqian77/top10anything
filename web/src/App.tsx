import React, { useState, useEffect } from 'react';
import SearchForm from './components/SearchForm';
import Results from './components/Results';

export interface Item {
  name: string;
  value: number;
}

export default function App() {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const data = params.get('data');
    if (data) {
      try {
        const parsed = JSON.parse(atob(data));
        if (Array.isArray(parsed)) {
          setItems(parsed as Item[]);
        }
      } catch {}
    }
  }, []);

  return (
    <div className="w-full max-w-4xl space-y-4">
      <SearchForm onResult={setItems} />
      {items.length > 0 && <Results items={items} />}
    </div>
  );
}
