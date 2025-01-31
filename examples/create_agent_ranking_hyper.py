import os
import asyncio
import sys
from pathlib import Path

# Add src directory to PYTHONPATH
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
os.environ["PYTHONPATH"] = src_path

from datetime import datetime
from pipeline.tableau import TableauDataConverter
from pipeline.hyper import HyperFileManager
from agent.ranking_agent import generate_ranking

async def create_and_store_ranking(query: str):
    """Generate ranking using agent and store it in hyper format"""
    try:
        # Generate ranking data using agent
        print(f"\n=== Generating ranking for: {query} ===\n")
        ranking_result = await generate_ranking(query)
        
        print(f"Generated ranking for topic: {ranking_result.topic}")
        print(f"Number of items: {len(ranking_result.items)}")
        
        # Convert to Tableau format
        tableau_data = TableauDataConverter.convert(ranking_result)
        
        # Set output directory
        output_dir = Path("data/hyper")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Hyper file manager
        manager = HyperFileManager(output_dir)
        
        # Generate filename (using timestamp and topic)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = "".join(c for c in ranking_result.topic if c.isalnum() or c in (' ', '-', '_')).strip()
        file_name = f"{sanitized_topic}_{timestamp}"
        
        # Create Hyper file
        hyper_path = manager.create_hyper_file(file_name, tableau_data)
        print(f"\nCreated Hyper file: {hyper_path}")
        
        # Print ranking summary
        print("\nRanking Summary:")
        for item in ranking_result.items:
            print(f"\n{item.rank}. {item.name}")
            print(f"Score: {item.score}")
            print("Advantages:")
            for advantage in item.advantages:
                print(f"  - {advantage}")
            if item.metrics:
                print(f"Metrics: {item.metrics}")
        
    except Exception as e:
        print(f"Error processing ranking: {str(e)}")
        raise

async def main():
    # Test queries
    queries = [
        "Best public high schools in Ottawa based on Fraser rankings",
        # Add more queries here
    ]
    
    for query in queries:
        await create_and_store_ranking(query)

if __name__ == "__main__":
    asyncio.run(main()) 