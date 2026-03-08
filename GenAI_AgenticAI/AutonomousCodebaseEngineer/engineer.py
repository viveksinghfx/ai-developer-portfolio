from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.codebase_engineer import run_codebase_engineer

router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class EngineerRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class EngineerResponse(BaseModel):
    response: str


@router.post("/engineer", response_model=EngineerResponse)
async def engineer(req: EngineerRequest):
    """
    Give a public GitHub repo URL + task in plain English.
    The agent will analyse the codebase and return a full implementation.

    Example message:
        https://github.com/tiangolo/fastapi  Add rate limiting to all API endpoints
    """
    try:
        history = [{"role": m.role, "content": m.content} for m in (req.history or [])]
        response = await run_codebase_engineer(req.message, history)
        return EngineerResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
