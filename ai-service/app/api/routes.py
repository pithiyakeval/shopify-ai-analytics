from fastapi import APIRouter
from fastapi.routing import APIRouter
from app.schemas.question import QuestionRequest
from app.agents.analytics_agent import AnalyticsAgent

router = APIRouter()

@router.post("/ask")
def ask_question(payload: QuestionRequest):
    agent = AnalyticsAgent()
    return agent.handle(payload.store_id,payload.question)

@router.get("/health")
def health_check():
    return{
        "status":"ok",
        "service":"ai-service"
    }
