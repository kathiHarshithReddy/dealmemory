"""Groq via its OpenAI-compatible endpoint, with simple retry."""
import os
import time
from openai import OpenAI

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def _client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )


def ask(system: str, user: str, retries: int = 2) -> str:
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = _client().chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return resp.choices[0].message.content
        except Exception as e:  # rate limits, malformed output, etc.
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    return f"(LLM error after retries: {last_err})"
