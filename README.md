# AI Support Automation

An AI-assisted customer support workflow built with n8n, FastAPI,
PostgreSQL, Groq, and Discord.

The system receives customer support requests through a webhook,
classifies them with an LLM, and routes them to deterministic backend
actions.

## Features

- AI classification of support requests
- Structured LLM output
- Confidence-based escalation
- Automatic support ticket creation
- Automatic order status lookup
- Validation of customers and order ownership
- Human escalation through Discord
- PostgreSQL persistence
- Centralized API error handling
- Dockerized local development environment

## Architecture

```text
Client
  │
  ▼
n8n Webhook
  │
  ▼
Normalize Input
  │
  ▼
LLM Classification (Groq)
  │
  ▼
Confidence Check
  │
  ▼
Action Router
  │
  ├── create_ticket
  │      │
  │      ▼
  │   FastAPI → PostgreSQL
  │
  ├── get_order_status
  │      │
  │      ▼
  │   FastAPI → PostgreSQL
  │
  └── escalate
         │
         ▼
      Create Ticket
         │
         ▼
      Discord Notification
```

The LLM is only responsible for interpreting the user's intent.

Business actions, validation, database access, and error handling remain
deterministic.

## AI Routing

The classifier produces structured output:

```json
{
  "category": "delivery_issue",
  "action": "create_ticket",
  "requires_order": true,
  "confidence": 0.95
}
```

Supported actions:

| Action | Description |
| --- | --- |
| `create_ticket` | Creates a support ticket |
| `get_order_status` | Retrieves an existing order |
| `escalate` | Sends the request to human support |

Requests with low classification confidence are automatically escalated
instead of executing an uncertain action.

## Tech Stack

- **n8n** — workflow orchestration
- **FastAPI** — REST API and business logic
- **PostgreSQL** — persistent application data
- **Groq** — LLM inference
- **Discord Bot API** — human support notifications
- **Docker Compose** — local infrastructure

## Project Structure

```text
ai-support-automation/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── customers.py
│   │   │   ├── orders.py
│   │   │   └── tickets.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   └── init.sql
├── n8n/
│   └── workflows/
├── compose.yaml
├── .env.example
└── README.md
```

## Running Locally

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Configure the required credentials and start the stack:

```powershell
docker compose up -d --build
```

Services:

```text
n8n       http://localhost:5678
FastAPI   http://localhost:8000
API Docs  http://localhost:8000/docs
Postgres  localhost:5432
```

## Example Request

```json
{
  "customer_id": "CUST-001",
  "order_id": "ORD-002",
  "message": "Where is my order?"
}
```

The LLM identifies the request as an order status lookup and n8n routes
it to the corresponding FastAPI endpoint.

An unclear request is instead escalated:

```text
Customer request
→ Low confidence / escalation decision
→ Support ticket created
→ Discord notification sent to operator
→ Client receives HTTP 202
```

## Design Decisions

The LLM does not directly modify application data.

It only chooses a predefined action from structured output. The actual
operations are performed by deterministic n8n workflows and FastAPI
endpoints.

This reduces the risk of hallucinated actions and keeps business logic
testable and predictable.

## Status

Current MVP supports:

- ticket creation
- order status lookup
- AI intent classification
- low-confidence fallback
- human escalation

Possible future improvements include authentication, retries,
observability, database migrations, and knowledge-base assisted answers.
