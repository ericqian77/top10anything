from datetime import datetime
from pathlib import Path
from typing import Optional
import logging
import asyncio

from src.agent.ranking_agent import generate_ranking
from src.pipeline.tableau import TableauDataConverter
from src.pipeline.tableau_cloud import TableauCloudPublisher
import tableauserverclient as TSC


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RankingService:
    """Service for handling ranking generation and Tableau updates"""
    
    def __init__(self, publisher: TableauCloudPublisher):
        self.publisher = publisher
        self.temp_dir = Path("data/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def generate_and_update(self, topic: str) -> dict:
        """
        Generate ranking for topic and update Tableau
        Returns status information about the process
        """
        try:
            # Generate ranking
            logger.info(f"\n3. Generating ranking data...")
            logger.info(f"🔍 Query: {topic}")
            ranking_result = await generate_ranking(topic)
            logger.info(f"✅ Generated ranking with {len(ranking_result.items)} items")
            logger.info(f"📝 Topic: {ranking_result.topic}")


            # convert data to Tableau format
            logger.info("\n4. Converting data to Tableau format...")
            tableau_data = TableauDataConverter.convert(ranking_result)
            logger.info(f"✅ Converted {len(tableau_data)} rows")
            
            # update Tableau Cloud
            logger.info("\n5. Updating data in Tableau Cloud...")
            job_id = await self.publisher.update_data(tableau_data, self.temp_dir)
            logger.info(f"✅ Update job started with ID: {job_id}")


            # wait for job completion
            logger.info("\n6. Waiting for job completion...")
            try:

                # use TSC built-in wait method
                final_job = await self.publisher.wait_for_job(job_id, timeout=300)
                

                if final_job.finish_code == 0:
                    logger.info("\n✅ Data successfully updated in Tableau Cloud")
                    logger.info(f"📊 Updated datasource: {self.publisher.datasource_name}")
                    logger.info(f"📈 Total rows updated: {len(tableau_data)}")
                    
                    return {
                        "status": "success",
                        "message": "Ranking generated and Tableau updated successfully",
                        "details": {
                            "topic": topic,
                            "items_count": len(ranking_result.items),
                            "job_id": job_id,
                            "timestamp": datetime.utcnow(),
                            "items": [
                                {
                                    "rank": item.rank,
                                    "name": item.name,
                                    "score": item.score,
                                    "advantages": item.advantages
                                }
                                for item in ranking_result.items
                            ]
                        }
                    }
                else:
                    error_msg = f"Tableau update failed with code {final_job.finish_code}"
                    logger.error(f"\n❌ {error_msg}")
                    raise Exception(error_msg)

            except Exception as e:
                logger.error(f"\n❌ Error waiting for job: {str(e)}")
                raise Exception(f"Tableau update failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"\n❌ Error in generate_and_update: {str(e)}")
            logger.error("\nStack trace:", exc_info=True)
            raise Exception(f"Failed to generate ranking: {str(e)}") 