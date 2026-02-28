import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import openai

router = APIRouter()

_client: openai.OpenAI | None = None


def _get_client() -> openai.OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        _client = openai.OpenAI(api_key=api_key)
    return _client


class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)


@router.post("/")
def explain_topic(request: TopicRequest):
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful educational assistant. Explain topics clearly and concisely.",
                },
                {
                    "role": "user",
                    "content": f"Explain the following topic: {request.topic}",
                },
            ],
        )
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded. Please try again later.")
    except openai.APIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")
    explanation = response.choices[0].message.content
    return {"topic": request.topic, "explanation": explanation}
