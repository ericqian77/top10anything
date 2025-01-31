import os
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add src directory to Python path for imports
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from pipeline.tableau_cloud import TableauCloudPublisher
from agent.ranking_agent import generate_ranking
from pipeline.tableau import TableauDataConverter

async def main():
    """Main function to demonstrate Tableau Cloud data update process"""
    print("\n=== Starting Tableau Cloud Update Process ===")
    
    # Load environment variables
    print("\n1. Loading environment variables...")
    load_dotenv()
    required_env_vars = [
        "TABLEAU_SERVER_URL",
        "TABLEAU_SITE_NAME",
        "TABLEAU_TOKEN_NAME",
        "TABLEAU_TOKEN_VALUE",
        "TABLEAU_DATASOURCE_NAME"
    ]
    
    # Verify all required environment variables are set
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        return
    
    print("✅ Environment variables loaded successfully")
    
    try:
        # Initialize Tableau Cloud connection
        print("\n2. Initializing Tableau Cloud connection...")
        publisher = TableauCloudPublisher(
            server_url=os.getenv('TABLEAU_SERVER_URL'),
            site_name=os.getenv('TABLEAU_SITE_NAME'),
            token_name=os.getenv('TABLEAU_TOKEN_NAME'),
            token_value=os.getenv('TABLEAU_TOKEN_VALUE'),
            datasource_name=os.getenv('TABLEAU_DATASOURCE_NAME')
        )
        print(f"✅ Connected to Tableau Cloud at {os.getenv('TABLEAU_SERVER_URL')}")
        print(f"📊 Using datasource: {os.getenv('TABLEAU_DATASOURCE_NAME')}")
        
        # Generate new ranking data
        print("\n3. Generating ranking data...")
        query = "best universities in the world"
        print(f"🔍 Query: {query}")
        ranking_result = await generate_ranking(query)
        print(f"✅ Generated ranking with {len(ranking_result.items)} items")
        print(f"📝 Topic: {ranking_result.topic}")
        


        # Convert to Tableau format
        print("\n4. Converting data to Tableau format...")
        tableau_data = TableauDataConverter.convert(ranking_result)
        print(f"✅ Converted {len(tableau_data)} rows")
        
        # Create temp directory for Hyper files
        temp_dir = Path("data/temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Update data in Tableau Cloud
        print("\n5. Updating data in Tableau Cloud...")
        job_id = await publisher.update_data(tableau_data, temp_dir)
        print(f"✅ Update job started with ID: {job_id}")
        
        # Wait for job completion
        print("\n6. Waiting for job completion...")
        success = await publisher.wait_for_job_completion(job_id)
        
        if success:
            print("\n✅ Data successfully updated in Tableau Cloud")
            print(f"📊 Updated datasource: {os.getenv('TABLEAU_DATASOURCE_NAME')}")
            print(f"📈 Total rows updated: {len(tableau_data)}")
            print("\nRanking Summary:")
            for item in ranking_result.items:
                print(f"\n{item.rank}. {item.name}")
                print(f"Score: {item.score}")
                print("Advantages:")
                for advantage in item.advantages:
                    print(f"  - {advantage}")
        else:
            print("\n❌ Failed to update data")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nStack trace:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nStarting data update process...")
    asyncio.run(main())
    print("\nProcess completed.") 