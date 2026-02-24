from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Импортируем ОБНОВЛЕННЫЙ модуль с MCP
from finance_tools import run_agent, tools

load_dotenv()

app = FastAPI(title="FinGuard AI API with MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    text: str
    session_id: Optional[str] = "default"

class AgentResponse(BaseModel):
    response: str
    session_id: str
    tools_used: list

@app.post("/agent/run")
async def run_agent_endpoint(request: AgentRequest):
    try:
        print(f"📝 Received: {request.text}")
        result = run_agent(request.text, request.session_id)
        return AgentResponse(
            response=result,
            session_id=request.session_id,
            tools_used=[tool.name for tool in tools]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "FinGuard AI with MCP"}

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)