from fastapi import APIRouter, HTTPException
import traceback

from llm.service import LLMService

router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)

@router.get("/recommendation")
def get_recommendation():
    try:
        return LLMService.recommend()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))