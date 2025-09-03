# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models import CompareRequest, CompareResponse
from app.llm import call_openai, call_claude, list_openai_models, list_anthropic_models
from app.auth import verify_token
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all. Later restrict to frontend domain.
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/models")
def get_models(user=Depends(verify_token)):
    return {
        "openai": list_openai_models(),
        "anthropic": list_anthropic_models(),
    }


@app.post("/compare", response_model=CompareResponse)
async def compare(request: CompareRequest, user=Depends(verify_token)):
    if not request.models:
        raise HTTPException(status_code=400, detail="No models provided")

    tasks = []
    for model in request.models[:3]:
        if model.startswith("gpt") or model.startswith("o"):  # OpenAI naming
            tasks.append(call_openai(request.prompt, model))
        elif model.startswith("claude"):
            tasks.append(call_claude(request.prompt, model))
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported model: {model}")

    results = await asyncio.gather(*tasks)
    return CompareResponse(results=results)
