# DealMemory

A sales copilot that remembers every call, objection, stakeholder and promise
across a deal, and briefs you before the next conversation.

Built with [Hindsight](https://github.com/vectorize-io/hindsight) agent memory,
Groq, and Streamlit.

## The problem

Reps lose hours re-reading CRM notes before calls, and still miss things:
the promise nobody followed up on, the CFO's pricing objection from three
weeks ago, the competitor mentioned twice.

## How Hindsight memory is used

| Operation | Where | What it does |
|---|---|---|
| `retain` | `memory.retain_interaction` | Stores every call, email and meeting as it happens, with date and account context |
| `recall` | `memory.recall` | Before the chat agent answers, fetches memories relevant to the question |
| `reflect` | `memory.reflect` | Powers "Brief me": reasons over the whole bank to produce a briefing |

A sidebar toggle turns memory off so you can compare the same question answered
with and without Hindsight.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in keys
streamlit run app.py
```

1. Click "Load demo history into memory".
2. Click "Brief me for my next call" with memory OFF, then ON.
