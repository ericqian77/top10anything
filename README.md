# Top10 Anything - AI Agent Powered Ranking Insights with Tableau

A powerful integration between AI agents and Tableau that helps you:

- Generate data-driven Top 10 rankings on any topic using advanced AI analysis
- Automatically convert insights into interactive Tableau visualizations 
- Get detailed scoring breakdowns and comparative metrics for each ranked item
- Leverage both AI intelligence and Tableau's visualization capabilities

![Alt text](https://pub-877d58a8bdbe42a2b5aefa451ed8fc66.r2.dev/top10anything-pic1.jpg)

## Features

- 🧠 **AI Agent Ranking Analysis**: AI agent system for scoring and ranking data insights
- 📊 **Tableau Hyper Pipeline**: Automated conversion of ranking results to Tableau-ready Hyper files
- ☁️ **Tableau Cloud Integration**: Seamless publishing and updating of data sources in Tableau Cloud
- 🔄 **Tableau Embed Integration**: Embedded Tableau dashboard that updates automatically when AI agent generates new rankings
- ⚙️ **Automated Workflow**: End-to-end pipeline from data processing to visualization


## Installation

1. Clone the repository:
```bash
git clone https://github.com/ericqian77/top10anything.git
cd top10anything
```
2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
3. Install the package in editable mode with all dependencies:
```bash
pip install -e .
```

## Configure the project

### 1. Backend Setup
Configure Tableau credentials in `.env`:
```
TABLEAU_SITE_ID=your_site_id
TABLEAU_PROJECT_NAME=your_project
TABLEAU_TOKEN_NAME=your_token_name
TABLEAU_TOKEN_VALUE=your_token_value
```
### 2. Tableau published data source initialization

1. Locate the example Hyper file:
   ```
   data/Initial/initial.hyper.example
   ```

2. Publish this initial Hyper file to Tableau:
   - Open Tableau Desktop
   - Connect to the Hyper file (File > Open > Browse to initial.hyper.example)
   - Publish as Data Source (Server > Publish Data Source)
   - Set a unique name for your data source (e.g., "top10_rankings_yourname")
   - update the **TABLEAU_DATASOURCE_NAME** in the .env file

### 3. Update src\web\static\index.html
   - update the you embedding url in the index.html file to your tableau cloud workbook url

### 4. Access the Dashboard
1. Start the application:
   ```bash
   python -m src.web.run   
   ```
2. Open `http://localhost:8000` in your browser

## Usage

### 5. Analyze Topics
1. Enter a topic in the input field. Example topics:
   - "Best universities in Canada"
   - "Top programming languages 2024"
   - "Best electric cars in the market"

2. Click "Analyze" to start processing
   - The AI ranking agent will search for relevant data sources
   - Analyze and rank results using agent scoring system 
   - Generate detailed metrics and comparisons
   - Process typically takes 30-45 seconds depending on topic complexity

3. View Results
   - Click "Refresh Dashboard" to see new rankings
   - Review detailed scores and comparisons

## Tech Stack & APIs

### AI 
- OpenAI API (gpt-4o) - LLM base model
- Pydantic-AI - AI agent  framework
- DuckDuckGo Search  - Web search

### Tableau Integration
- Tableau TSC
- Tableau REST API - datasource publishing
- Tableau Hyper API  - Data  generation
- Tableau Embedding API v3 - Dashboard embedding and interactivity

### Backend Framework
- FastAPI - Web API framework

### Data Processing
- Pydantic v2 - Data validation and serialization

### Development Tools
- cursor - AI powered IDE

## Future Improvements
- multiple agents (reasoning, search, scoring, review etc.)
- add advanced reasoning capabilities (o1/r1)
- enhanced agentic tools use (RAG,Web search, etc.)
- tableau Data model improvements (multi-table, etc.)
- enhancement for data validation and error handling
- human-in-the-loop for final review and approval


