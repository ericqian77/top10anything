from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import os
import logging
from ..services.ranking_service import RankingService
from pipeline.tableau_cloud import TableauCloudPublisher

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter()

class TopicRequest(BaseModel):
    """Request model for topic analysis"""
    topic: str

class AnalysisResponse(BaseModel):
    """Response model for analysis status"""
    status: str
    message: str
    timestamp: datetime
    details: Dict[str, Any]

async def get_ranking_service() -> RankingService:
    """Dependency to get RankingService instance"""
    publisher = TableauCloudPublisher(
        server_url=os.getenv('TABLEAU_SERVER_URL'),
        site_name=os.getenv('TABLEAU_SITE_NAME'),
        token_name=os.getenv('TABLEAU_TOKEN_NAME'),
        token_value=os.getenv('TABLEAU_TOKEN_VALUE'),
        datasource_name=os.getenv('TABLEAU_DATASOURCE_NAME')
    )
    return RankingService(publisher)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_topic(
    request: TopicRequest,
    service: RankingService = Depends(get_ranking_service)
) -> AnalysisResponse:
    """
    Endpoint to trigger topic analysis and ranking generation
    """
    try:
        result = await service.generate_and_update(request.topic)
        return AnalysisResponse(
            status=result["status"],
            message=result["message"],
            timestamp=result["details"]["timestamp"],
            details=result["details"]
        )
    except Exception as e:
        logger.error(f"Error in analyze_topic: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 