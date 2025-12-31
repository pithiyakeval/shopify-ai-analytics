🚪 Rails API – Shopify Analytics Gateway

This service is the backend gateway for the Shopify AI Analytics application.
It is responsible for handling authentication, request validation, and orchestration between the client and the AI service.

The Rails API does not perform analytics or AI reasoning itself.
Instead, it acts as a secure, scalable middleware layer between Shopify and the Python AI service.

✨ Key Responsibilities

Expose REST APIs for analytics questions

Validate incoming requests

Handle Shopify store context

Forward requests to the AI service (FastAPI)

Return formatted, user-friendly responses

(Optional) Persist logs and analytics metadata

🏗️ High-Level Architecture
Client / Frontend
        │
        │ POST /api/v1/questions
        ▼
Rails API (Gateway)
        │
        │ Forward Question
        ▼
FastAPI AI Service
        │
        ▼
LLM + Agent + ShopifyQL

🧠 Why Rails Is Used Here

Rails is used as an API-only gateway for:

Clean REST API design

Shopify OAuth integration

Secure token handling

Centralized validation and logging

Separation of AI concerns from business logic

This keeps the system modular and maintainable.

📂 Folder Structure
rails-api/
│
├── app/
│   ├── controllers/
│   │   └── api/
│   │       └── v1/
│   │           └── questions_controller.rb
│   │
│   ├── services/
│   │   └── ai_service_client.rb
│   │
│   └── models/
│
├── config/
│   ├── routes.rb
│   └── database.yml
│
├── db/
├── Gemfile
└── README.md

🔌 API Endpoints
POST /api/v1/questions

Accepts a natural-language analytics question and forwards it to the AI service.

Request
{
  "store_id": "example-store.myshopify.com",
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
    }
  }
}

🔁 Request Flow

Client sends a question to Rails API

Rails validates input (store_id, question)

Rails forwards the request to the AI service

AI service returns structured analytics insight

Rails returns a clean response to the client

Rails never executes analytics logic itself.

🤝 Rails ↔ FastAPI Integration

Rails communicates with the AI service via HTTP using a dedicated service class.

AiServiceClient

Responsibilities:

Build request payload

Send request to FastAPI

Parse response

Handle AI service downtime gracefully

This allows the AI service to be:

Independently scalable

Language-agnostic

Easily replaceable

🔐 Shopify OAuth (Design Explanation)

Shopify OAuth is handled by Rails, not the AI service.

OAuth Flow (Planned)

Merchant installs the app from Shopify

Shopify redirects to Rails OAuth endpoint

Rails exchanges authorization code for access token

Token is securely stored (encrypted)

Token is used to query Shopify APIs

Why OAuth Is in Rails

Secure token storage

Centralized authentication logic

Industry-standard Shopify app architecture

OAuth implementation is intentionally mocked for this assignment to focus on system design and agent reasoning.

🧪 Validation & Error Handling

Rails handles:

Missing or invalid parameters

AI service unavailability

Timeout or connection errors

Example fallback response:

{
  "answer": "AI service unavailable at the moment.",
  "confidence": "low"
}

🗃️ Database Usage (Optional)

PostgreSQL can be used for:

Storing request logs

Tracking analytics queries

Saving Shopify store metadata

Database usage is optional and not required for core functionality.

🚀 Running the Rails API Locally
bundle install
rails db:create
rails server


Server runs at:

http://127.0.0.1:3000

🧠 Design Philosophy

Rails = Gateway & Security

Python = Intelligence & Analytics

LLM = Planning, not execution

Deterministic logic for safety

Clear separation of concerns

This mirrors real-world SaaS analytics platforms.

✅ Summary

This Rails API provides:

Clean REST interface

Shopify-ready architecture

Secure service orchestration

AI-agnostic backend design

Production-oriented separation of concerns

It is designed to work seamlessly with the FastAPI AI service and can be extended to support full Shopify OAuth and real analytics execution.