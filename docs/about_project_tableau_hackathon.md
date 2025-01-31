# Top10 Anything - Project Story

## Inspiration

The inspiration for Top10 Anything came from two key insights during our exploration of AI and BI integration:

1. **TopX Information Seeking Pattern**: I noticed how frequently people search for "Top X" rankings across various domains - from technology choices to consumer products. This universal pattern of seeking curated, ranked information revealed an opportunity to create something interesting using AI capabilities.

2. **AI Agents Meet BI Tools**: While experimenting with AI agent frameworks, I was inspired by their ability to produce structured outputs. This led to an exciting realization: we could bridge the gap between Large Language Models' analytical capabilities and Tableau's visualization power. By combining these technologies, we could transform unstructured web data into meaningful, interactive visualizations automatically.


## What it does

Top10 Anything is an AI-powered system that:

1. **Generates Rankings**: Users can input any topic (e.g., "Best Electric Cars 2024", "Top Programming Languages") and get AI-analyzed rankings.

2. **Provides Deep Analysis**: For each ranked item, AI agents(with LLM and web search) provide comprehensive analysis:
   - Calculates comprehensive scores
   - Identifies key advantages
   - Extracts quantitative metrics
   - References authoritative sources

3. **Automates Visualization**: The system:
   - Converts AI analysis into Tableau-ready data
   - Automatically updates Tableau dashboards
   - Provides interactive visualizations


## How we built it

The development process involved several key components:

1. **AI Agent Architecture**:
   - Built using Pydantic-AI framework
   - Implemented DuckDuckGo search integration
   - Developed ranking using LLM and web search
   - Created data validation models

2. **Tableau Integration**:
   - Used Tableau Hyper API for data source generation
   - Implemented REST API and TSC for cloud publishing
   - Created embedded dashboard interface
   - Built update mechanism

3. **Web Interface**:
   - Developed FastAPI backend
   - Created simple frontend web page
   - Integrated Tableau embedding
   - Implemented progress tracking

## Challenges we ran into

1. **System Design**:
   - Designing a system that can handle virtually any ranking topic
   - design the workflow of the system
   - Balancing the scope of the system with the complexity of the topic
   - Ensuring the system can handle the data from the web search

2. **Data Consistency**:
   - Ensuring consistent ranking criteria across different topics
   - Handling varying data availability
   - Maintaining data quality standards

3. **Technical Integration**:
   - Coordinating between AI analysis and Tableau updates
   - Managing asynchronous operations
   - Ensuring reliable data pipeline


## Accomplishments that we're proud of

1. **Seamless Integration**: Successfully bridged the gap between AI analysis and Tableau visualization

2. **Flexibility**: Created a system that can handle virtually (almost) any ranking topic 
   
3. **Automation**: Built an end-to-end pipeline requiring minimal user intervention

4. Finishing it in a short period of time 2-3 days


## What we learned

   - Best practices for AI agent development
   - Tableau API integration patterns
   - better work with AI powered IDEs (cursor)

## What's next for Top10 Anything

1. **Enhanced AI Capabilities**:
   - Multiple specialized agents (reasoning, search, scoring)
   - Advanced reasoning with newer models (Claude-3, GPT-4)
   - Improved source validation

2. **Tableau Integration**:
   - Multi-table data models
   - Enhanced visualization templates

3. **User Features**:
   - Human-in-the-loop validation