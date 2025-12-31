# API Contracts

This document defines the communication between the Rails API
and the Python AI service.

---

## Rails → AI Service

### Endpoint
POST /ask

### Request Body
```json
{
  "store_id": "example-store.myshopify.com",
  "question": "What were my top selling products last week?"
}
