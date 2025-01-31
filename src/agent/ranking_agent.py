from dataclasses import dataclass
from pydantic_ai import Agent, RunContext, ModelRetry
from models.ranking import RankingResult, RankingItem
from agent.search import web_search, SearchError
from typing import Any, List, Dict
from datetime import datetime, UTC

@dataclass
class RankingDependencies:
    search_client: Any
    db_connector: Any

class RankingError(Exception):
    """Ranking generation related errors"""
    pass

ranking_agent = Agent(
    'openai:gpt-4o',
    deps_type=RankingDependencies,
    result_type=RankingResult,
    system_prompt=(
        "You are a ranking expert that analyzes web search results to generate authoritative top 10 rankings. "
        "For each topic, carefully evaluate key factors like: "
        "- Overall popularity and adoption "
        "- Expert reviews and professional opinions "
        "- Quality metrics relevant to the domain "
        "- Recent trends and developments "
        "Ensure all rankings are unique, properly ordered, and supported by clear reasoning. "
        "Adapt your analysis criteria based on the specific topic being ranked. "
        "Always include domain-specific terminology and concepts in your analysis. "
        "Make sure to validate and retry if the initial result is not satisfactory."
    ),
)

@ranking_agent.tool
async def analyze_search_results(
    ctx: RunContext[RankingDependencies], 
    query: str
) -> List[Dict]:
    """Fetch and preprocess search results for ranking analysis."""
    try:
        raw_results = await ctx.deps.search_client(query)
        if not raw_results:
            raise ModelRetry(
                "No search results found", 
                max_retries=3  
            )
            
        return [
            {
                "title": r.get("title"),
                "snippet": r.get("snippet"),
                "source": r.get("link")
            }
            for r in raw_results
        ]
    except SearchError as e:
        raise ModelRetry(
            f"Search API error: {str(e)}",
            max_retries=3,
            original_exception=e
        )
    except Exception as e:
        raise RankingError(f"Unexpected search error: {str(e)}") from e

@ranking_agent.system_prompt
async def add_ranking_guidelines(ctx: RunContext[RankingDependencies]) -> str:
    current_time = datetime.now(UTC)
    return f"""
    # General Ranking Analysis Framework ({current_time.strftime('%Y-%m-%d %H:%M UTC')})
    
    ## Core Principles
    1. Identify core dimensions of input topic (technical/cultural/business etc.)
    2. Automatically adapt industry standard evaluation metrics
    3. Balance objective data with expert opinions
    
    ## Evaluation Dimensions (Dynamically adjusted by topic)
    - Core advantages (30-50% weight)
    - Market influence (20-40% weight)
    - Innovation (15-30% weight)
    - Sustainability (10-25% weight)
    - User acceptance (10-20% weight)
    
    ## Analysis Requirements
    1. Each ranking item must include:
       - 3 unique advantages
       - Quantitative metric references
       - Authoritative data sources
    2. Compare analysis from at least 5 reliable sources
    3. Time sensitivity note: Current analysis as of {current_time.strftime('%Y-%m-%d')}
    
    ## Validation Requirements
    - Ensure all rankings have unique positions (1-10)
    - Verify each item has required fields
    - Include domain-specific terminology
    - Add current year in methodology section
    """

async def generate_ranking(query: str) -> RankingResult:
    """Generate rankings for the given query."""
    try:
        deps = RankingDependencies(
            search_client=web_search,
            db_connector=None
        )
        
        result = await ranking_agent.run(
            f"Generate top 10 ranking for: {query}",
            deps=deps
        )
        
        current_year = datetime.now(UTC).year
        if str(current_year) not in result.data.methodology:
            result.data.methodology = (
                f"Analysis performed in {current_year}. " + 
                result.data.methodology
            )
        
        return result.data
                
    except Exception as e:
        raise RankingError(f"Ranking generation failed: {str(e)}") from e 