"""Thin wrapper around Hindsight: retain / recall / reflect."""
import os
from hindsight_client import Hindsight

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "dealmemory")


def _client() -> Hindsight:
    return Hindsight(
        base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
        api_key=os.getenv("HINDSIGHT_API_KEY"),
    )


def retain_interaction(account: str, kind: str, note: str, date: str) -> None:
    """Store one sales interaction. Account name is in the text so Hindsight
    links it to the account entity."""
    _client().retain(
        bank_id=BANK_ID,
        content=f"[{account}] {kind} on {date}: {note}",
        context=f"sales interaction with {account}",
        timestamp=f"{date}T10:00:00Z",
    )


def recall(query: str) -> list[str]:
    """Return the text of memories relevant to the query."""
    result = _client().recall(bank_id=BANK_ID, query=query)
    return [r.text for r in result.results]


def reflect(query: str) -> str:
    """Ask Hindsight to reason over the bank and return an answer."""
    answer = _client().reflect(bank_id=BANK_ID, query=query)
    return answer.text
