from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from datetime import datetime, UTC
from typing import List, Dict, Optional
from pydantic_ai import RunContext

class RankingItem(BaseModel):
    """Represents a single item in the ranking"""
    rank: int = Field(..., ge=1, le=10)
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r'^[a-zA-Z0-9\#\+\.\-_ ]+$',
        description="Name of the ranked item (allows letters, numbers, #, +, ., -, _ and spaces)"
    )
    description: str = Field(
        ...,
        min_length=50,
        max_length=500,
        description="Detailed description"
    )
    advantages: List[str] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="Key advantages or features"
    )
    metrics: Dict[str, float] = Field(
        ...,
        description="Quantitative metrics for evaluation"
    )
    score: Optional[float] = Field(
        None,
        ge=0,
        le=10,
        description="Overall score (0-10)"
    )

    @field_validator('advantages')
    @classmethod
    def validate_unique_advantages(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Advantages must be unique')
        return v

class RankingResult(BaseModel):
    """Represents a complete ranking result"""
    topic: str = Field(min_length=3, max_length=50)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    items: List[RankingItem] = Field(min_length=10, max_length=10)
    sources: List[str] = Field(min_length=1)
    methodology: str = Field(
        min_length=100,
        description="Analysis process description"
    )
    year: int

    @field_validator('items')
    @classmethod
    def validate_unique_ranks(cls, v):
        ranks = [item.rank for item in v]
        if len(ranks) != len(set(ranks)):
            raise ValueError('Ranking positions must be unique')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "topic": "Programming Languages",
                "items": [{
                    "rank": 1,
                    "name": "Python",
                    "score": 9.8,
                    "advantages": ["Readability", "Ecosystem", "Versatility"],
                    "description": "General-purpose language with clean syntax and extensive libraries",
                    "metrics": {"popularity": 9.8, "growth": 8.5}
                }],
                "sources": ["https://example.com/rankings"],
                "methodology": "Combined analysis of GitHub activity, Stack Overflow trends, and industry adoption rates."
            }]
        },
        # Custom serialization for datetime
        json_encoders={
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S UTC")
        }
    ) 