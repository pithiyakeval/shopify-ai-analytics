🧠 AI Service – Shopify Analytics Agent

This service is the AI-powered analytics engine for the Shopify Analytics App.
It is responsible for understanding natural-language business questions, converting them into structured analytics plans, generating ShopifyQL queries, and returning clear, business-friendly insights.

The service is implemented using FastAPI and a local LLM (Ollama), and is designed to work as a standalone microservice consumed by a Rails API gateway.

✨ Key Responsibilities

Accept natural-language questions from the backend

Use an LLM to infer intent and parameters

Generate ShopifyQL queries deterministically

Execute analytics queries (mocked for now)

Convert raw results into layman-friendly explanations

Handle malformed or hallucinated LLM output safely

🏗️ High-Level Architecture
Rails API
   │
   │  (POST /api/v1/questions)
   ▼
FastAPI (AI Service)
   │
   ├── LLM Planning (Ollama / Phi-3)
   │
   ├── Agent Logic
   │     ├── Intent detection
   │     ├── Time-range extraction
   │     ├── Validation & fallbacks
   │
   ├── ShopifyQL Generation
   │
   ├── Query Execution (Mocked)
   │
   └── Business-Friendly Explanation

🤖 Why LLM Is Used (Important Design Choice)

The LLM is NOT used to generate data or numbers.

Instead, it is used only for planning:

Classifying intent (sales, inventory, customers)

Extracting parameters (metrics, time range)

All critical logic (query generation, validation, execution) is deterministic, ensuring:

No hallucinated analytics

Predictable behavior

Production safety

This design prevents common LLM failures and is suitable for real-world analytics systems.

🧩 Agent Workflow (Step-by-Step)

Receive Question

Example:
“What were my top selling products last week?”

LLM Planning

Prompted to return:

{
  "intent": "sales",
  "metric": "quantity",
  "time_range_days": 7
}


Sanitization & Validation

Malformed or extra LLM output is ignored

Missing values fall back to deterministic defaults

ShopifyQL Generation

Query is generated based on validated plan

Query Execution

Currently mocked

Can be replaced with real Shopify Analytics API calls

Explanation Layer

Raw metrics converted into simple business language

📂 Folder Structure
ai-service/
│
├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI endpoints
│   │
│   ├── agents/
│   │   ├── analytics_agent.py # Core agent logic
│   │   └── prompts.py         # LLM prompt templates
│   │
│   ├── llm/
│   │   └── ollama_client.py   # Ollama LLM wrapper
│   │
│   └── main.py                # FastAPI app entry point
│
├── requirements.txt
└── README.md

🧠 Core Agent Logic

The AnalyticsAgent is responsible for:

Interpreting user intent

Validating LLM output

Generating ShopifyQL

Returning business-friendly insights

Safety Mechanisms

Extracts only the first valid JSON block from LLM output

Ignores hallucinated or irrelevant text

Applies deterministic fallbacks

Never executes unvalidated queries

📊 Example ShopifyQL Generated
1️⃣ Sales Analytics
FROM sales
SHOW sum(quantity) AS total_sold
GROUP BY product_title
SINCE -7d
ORDER BY total_sold DESC
LIMIT 5

2️⃣ Inventory Risk
FROM inventory_levels
SHOW available
ORDER BY available ASC

3️⃣ Repeat Customers
FROM customers
SHOW count(id)
WHERE orders_count > 1
SINCE -90d

🔌 API Endpoint
POST /ask

Request

{
  "store_id": "demo-store.myshopify.com",
  "question": "What were my top selling products last week?"
}


Response

{
  "answer": "Your top selling product in the last 7 days is Product A with around 120 units sold.",
  "confidence": "medium",
  "debug": {
    "plan": {
      "intent": "sales",
      "metric": "quantity",
      "time_range_days": 7
    },
    "shopifyql": "FROM sales ..."
  }
}

⚙️ LLM Configuration

Provider: Ollama (local)

Model: phi3

Reason:

Free & local

Good enough for intent classification

Demonstrates model-agnostic architecture

The model can be swapped without changing agent logic.

🧪 Error Handling Strategy

Invalid JSON → fallback logic

Partial responses → defaults applied

LLM instability → deterministic execution

Encoding issues → UTF-8 enforced at subprocess level

🚧 Current Limitations (Intentional)

ShopifyQL execution is mocked

Shopify OAuth handled by Rails API

No persistent conversation memory (optional future improvement)

These trade-offs were made to prioritize design clarity and correctness, as per assignment guidance.

🚀 How to Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000


Open API docs:

http://127.0.0.1:8000/docs

✅ Summary

This AI service demonstrates:

Clean agentic workflow design

Safe and constrained LLM usage

Clear separation of concerns

Real-world analytics reasoning

Production-minded error handling

It is designed to integrate seamlessly with a Rails-based backend and can be extended to support real Shopify Analytics APIs with minimal changes.