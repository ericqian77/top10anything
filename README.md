# Top10 Anything - Web Native Edition

This project now provides a completely browser-based experience powered by React and serverless functions on Vercel. You can query "Top 10" style questions in English or Chinese and instantly view tabular and charted results.

Original Tableau integration files remain in the repo for reference, but the default UI no longer depends on Tableau.

![Alt text](https://pub-877d58a8bdbe42a2b5aefa451ed8fc66.r2.dev/top10anything-pic1.jpg)

## Features

- 🧠 **AI Agent Ranking Analysis**: type a natural-language "Top 10" question and let the agent compile results
- 📈 **Table and Chart**: view a sortable table and interactive bar chart of the results
- 🌗 **Dark Mode**: UI follows your system preference automatically
- 📤 **Share Links**: copy shareable URLs with data embedded for Twitter/WeChat/Weibo


## Installation

1. Clone the repository:
```bash
git clone https://github.com/ericqian77/top10anything.git
cd top10anything
```
2. Install Node dependencies and start the dev server:
```bash
npm install
npm run dev
```
The app will be available at `http://localhost:5173` by default.

Legacy Python/Tableau tooling remains available in the repository but is optional.

## Configuration

Create a `.env` file by copying `.env.example` and set `AGENT_API_URL` to the endpoint of your AI ranking backend.

## Usage

Run the dev server and open `http://localhost:5173`:

```bash
npm run dev
```

Enter your "Top 10" question in English or Chinese and the results table and chart will appear. Use the share buttons to post the chart to Twitter or Weibo, or copy a link for WeChat.


