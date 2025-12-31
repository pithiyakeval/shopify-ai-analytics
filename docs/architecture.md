# System Architecture

This project implements an AI-powered Shopify Analytics platform using a
two-service architecture designed for clarity, safety, and scalability.

## High-Level Components

### 1. Rails API (Gateway Layer)
- Acts as the public-facing backend
- Handles Shopify OAuth (design-level)
- Validates incoming requests
- Forwards analytics questions to the AI service
- Formats and returns responses

### 2. Python AI Service (Analytics Engine)
- Implements an agentic workflow
- Uses an LLM (Ollama + Phi-3) for intent planning
- Generates ShopifyQL queries
- Executes queries (mocked)
- Converts results into business-friendly explanations

## Why This Architecture?

- Clear separation of concerns
- LLM is isolated from execution logic
- Rails remains Shopify-focused
- AI service remains analytics-focused
- Easy to extend with real Shopify APIs

## Data Flow

Client → Rails API → AI Service → (Mock Shopify) → AI Explanation → Rails → Client

## Key Design Principle

LLMs are used **only for planning**, never for execution or data generation.
All analytics execution is deterministic and validated.
