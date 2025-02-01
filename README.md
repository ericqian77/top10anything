# Top10 Anything - AI Agent Powered Ranking Insights with Tableau

A powerful integration between AI agents and Tableau that helps you:

- Generate data-driven Top 10 rankings on any topic using advanced AI analysis
- Automatically convert insights into interactive Tableau visualizations 
- Get detailed scoring breakdowns and comparative metrics for each ranked item
- Leverage both AI intelligence and Tableau's visualization capabilities

![Alt text](https://private-user-images.githubusercontent.com/20953543/408751680-a195d255-b19c-44e5-8231-9f37931388e6.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgzNjU0NDMsIm5iZiI6MTczODM2NTE0MywicGF0aCI6Ii8yMDk1MzU0My80MDg3NTE2ODAtYTE5NWQyNTUtYjE5Yy00NGU1LTgyMzEtOWYzNzkzMTM4OGU2LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAxMzElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMTMxVDIzMTIyM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdlNTI4NThkYTRlODJkNTgwNTFmNjgyODM3ODkxYmMxMzZhMGY5NzBiMDZjNjAyYjEzMjEwOTU5MmI0ODZhOGImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.gvoMpJldW8qzvBFOuCp6K-jw6VUk35vlcKEn20GwbhI)

## Features

- 🧠 **AI Agent Ranking Analysis**: AI agent system for scoring and ranking data insights
- 📊 **Tableau Hyper Pipeline**: Automated conversion of ranking results to Tableau-ready Hyper files
- ☁️ **Tableau Cloud Integration**: Seamless publishing and updating of data sources in Tableau Cloud
- 🔄 **Tableau Embed Integration**: Embedded Tableau dashboard that updates automatically when AI agent generates new rankings
- ⚙️ **Automated Workflow**: End-to-end pipeline from data processing to visualization

## Configure environment variables

## Usage

### 1. Backend Setup
Configure Tableau credentials in `.env`:
```
TABLEAU_SITE_ID=your_site_id
TABLEAU_PROJECT_NAME=your_project
TABLEAU_TOKEN_NAME=your_token_name
TABLEAU_TOKEN_VALUE=your_token_value
```

### 2. Access the Dashboard
1. Start the application:
   ```bash
   python -m src.web.run   
   ```
2. Open `http://localhost:8000` in your browser

### 3. Analyze Topics
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
- Tableau REST API - Dashboard publishing and management
- Tableau Hyper API  - Data source generation
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
  
## Contributors
- @ericqian77 - project lead and developer


