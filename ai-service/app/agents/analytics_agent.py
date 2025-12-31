import json
import re
from app.llm.ollama_client import OllamaClient
from app.agents.prompts import INTENT_PROMPT


class AnalyticsAgent:
    """
    Agent responsible for:
    - Understanding user intent
    - Planning analytics query
    - Generating ShopifyQL
    - Explaining results
    """

    # ---------- PUBLIC ENTRY POINT ----------

    def handle(self, store_id: str, question: str):
        plan = self._plan_with_llm(question)
        shopifyql = self._build_shopifyql(plan)
        result = self._execute_query(shopifyql)
        answer = self._explain_result(result, plan)

        return {
            "answer": answer,
            "confidence": "medium",
            "debug": {
                "plan": plan,
                "shopifyql": shopifyql
            }
        }

    # ---------- LLM + PLANNING ----------

    def _plan_with_llm(self, question: str) -> dict:
        prompt = INTENT_PROMPT.format(question=question)
        raw_output = OllamaClient.ask(prompt)
        print("LLM raw output:", raw_output)
        parsed = self._extract_json(raw_output)
        return self._validate_plan(parsed, question)

    def _extract_json(self, text: str) -> dict:
        """
        Extract first valid JSON object from LLM output.
        Handles markdown, explanations, and broken responses.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}

        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {}

    def _validate_plan(self, plan: dict, question: str) -> dict:
        """
        Never trust LLM blindly.
        Apply deterministic fallbacks.
        """
        q = question.lower()

        intent = plan.get("intent")
        if intent not in ["sales", "inventory", "customers"]:
            if "stock" in q or "inventory" in q:
                intent = "inventory"
            elif "customer" in q or "repeat" in q:
                intent = "customers"
            else:
                intent = "sales"

        time_range = plan.get("time_range_days")
        if not isinstance(time_range, int):
            time_range = 7

        metric = plan.get("metric")
        if not isinstance(metric, str):
         metric = "quantity"


        return {
            "intent": intent,
            "metric": metric,
            "time_range_days": time_range
        }

    # ---------- SHOPIFYQL ----------

    def _build_shopifyql(self, plan: dict) -> str:
        if plan["intent"] == "sales":
            return f"""
            FROM sales
            SHOW sum(quantity) AS total_sold
            GROUP BY product_title
            SINCE -{plan["time_range_days"]}d
            ORDER BY total_sold DESC
            LIMIT 5
            """

        if plan["intent"] == "inventory":
            return """
            FROM inventory_levels
            SHOW available
            ORDER BY available ASC
            """

        if plan["intent"] == "customers":
            return f"""
            FROM customers
            SHOW count(id)
            WHERE orders_count > 1
            SINCE -{plan["time_range_days"]}d
            """

    # ---------- EXECUTION (MOCK) ----------

    def _execute_query(self, shopifyql: str) -> dict:
        """
        Mock Shopify API execution.
        Real ShopifyQL execution comes later.
        """
        return {
            "rows": [
                {"name": "Product A", "value": 120},
                {"name": "Product B", "value": 90}
            ]
        }

    # ---------- EXPLANATION ----------

    def _explain_result(self, result: dict, plan: dict) -> str:
        if plan["intent"] == "sales":
            top = result["rows"][0]
            return (
                f"Your top selling product in the last {plan['time_range_days']} days "
                f"is {top['name']} with around {top['value']} units sold."
            )

        if plan["intent"] == "inventory":
            return "Some products are running low and may go out of stock soon."

        if plan["intent"] == "customers":
            return "You have customers who placed repeat orders recently."
