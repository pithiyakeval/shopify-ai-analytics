# Agent Workflow

The AI service uses an explicit agent-based workflow to ensure correctness
and prevent hallucinations.

## Step-by-Step Flow

1. Receive Question
   - Input: natural-language business question
   - Example: "What were my top selling products last week?"

2. Intent Planning (LLM)
   - Classifies intent: sales, inventory, customers
   - Extracts metric and time range
   - Output must be valid JSON

3. Validation Layer
   - Ensures intent is allowed
   - Applies fallback defaults
   - Sanitizes malformed LLM output

4. ShopifyQL Generation
   - Builds deterministic ShopifyQL
   - Uses predefined query templates

5. Query Execution
   - Mocked Shopify API execution
   - Real Shopify API can be plugged in later

6. Explanation Layer
   - Converts raw data into layman-friendly insights
   - Avoids technical terminology

## Safety Guarantees

- LLM output is never trusted blindly
- All execution logic is deterministic
- Broken or partial AI output is handled gracefully
