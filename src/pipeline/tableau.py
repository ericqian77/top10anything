from pydantic import BaseModel, Field
from datetime import datetime
import json
from typing import List
from src.models.ranking import RankingResult

class TableauDataRow(BaseModel):
    """Represents a single row in the Tableau dataset"""
    topic: str = Field(..., description="Ranking topic")
    generated_at: datetime = Field(..., description="Generation timestamp in UTC")
    rank: int = Field(..., ge=1, le=10, description="Position in ranking")
    item_name: str = Field(..., description="Name of the ranked item")
    score: float = Field(..., ge=0, le=10, description="Item's score")
    advantages: str = Field(..., description="JSON string of advantages")
    metrics: str = Field(..., description="JSON string of metrics")
    sources: str = Field(..., description="JSON string of source URLs")
    methodology: str = Field(..., description="Analysis methodology")
    batch_id: str = Field(..., description="Unique batch identifier")

class TableauDataConverter:
    """Converts RankingResult to Tableau-friendly format"""
    
    @staticmethod
    def generate_batch_id(topic: str, timestamp: datetime) -> str:
        """Generate a unique batch ID for tracking"""
        return f"{topic}_{timestamp.strftime('%Y%m%d%H%M%S')}"
    
    @classmethod
    def convert(cls, ranking: RankingResult) -> List[TableauDataRow]:
        """Convert a RankingResult into a list of TableauDataRows"""
        batch_id = cls.generate_batch_id(ranking.topic, ranking.generated_at)
        
        return [
            TableauDataRow(
                topic=ranking.topic,
                generated_at=ranking.generated_at,
                rank=item.rank,
                item_name=item.name,
                score=item.score or 0.0,
                advantages=json.dumps(item.advantages),
                metrics=json.dumps(item.metrics),
                sources=json.dumps(ranking.sources),
                methodology=ranking.methodology,
                batch_id=batch_id
            )
            for item in ranking.items
        ] 