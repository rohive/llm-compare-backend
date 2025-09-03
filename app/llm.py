import os, time
from app.models import ModelResponse
import openai
import anthropic
#from dotenv import load_dotenv

# Load variables from .env
#load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY not set in .env")
if not ANTHROPIC_API_KEY:
    print("⚠️ Warning: ANTHROPIC_API_KEY not set. Claude calls will fail.")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


async def call_openai(prompt: str, model: str) -> ModelResponse:
    start = time.time()
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = int((time.time() - start) * 1000)
    text = response.choices[0].message.content
    usage = response.usage
    # Example cost calculation (GPT-4o-mini: $0.00015 / 1k tokens input)
    cost = (usage.total_tokens / 1000) * 0.00015 if usage else None
    return ModelResponse(model=model, text=text, latency_ms=latency, tokens=usage.total_tokens if usage else None, cost=cost)

async def call_claude(prompt: str, model: str) -> ModelResponse:
    log_available_models()
    start = time.time()
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = int((time.time() - start) * 1000)
    text = response.content[0].text if response.content else ""
    return ModelResponse(model=model, text=text, latency_ms=latency, tokens=None, cost=None)

def list_openai_models() -> list[str]:
    try:
        models = openai_client.models.list()
        return [m.id for m in models.data]
    except Exception as e:
        print("Error listing OpenAI models:", e)
        return []


def list_anthropic_models() -> list[str]:
    try:
        models = anthropic_client.models.list()
        return [m.id for m in models.data]
    except Exception as e:
        print("Error listing Anthropic models:", e)
        return []