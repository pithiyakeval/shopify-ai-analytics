import subprocess
import time
import os


class OllamaClient:
    """
    Wrapper around Ollama CLI for LLM interaction.

    Bonus features:
    - Retry logic
    - Timeout protection
    - Safe UTF-8 handling (Windows compatible)
    - Graceful fallback on failure
    - Cloud-safe mock for Render deployment
    """

    MODEL = "phi3"
    MAX_RETRIES = 2
    TIMEOUT_SECONDS = 20

    @staticmethod
    def ask(prompt: str) -> str:
        """
        Send a prompt to Ollama and return raw text output.

        Local dev  → Uses Ollama
        Render     → Uses mocked deterministic response
        """

        # ✅ CLOUD DEPLOYMENT (Render) — MOCK LLM
        if os.getenv("RENDER") == "true":
            return """
            {
              "intent": "sales",
              "metric": "quantity",
              "time_range_days": 7
            }
            """

        # ✅ LOCAL DEVELOPMENT — REAL OLLAMA
        for attempt in range(1, OllamaClient.MAX_RETRIES + 1):
            try:
                process = subprocess.Popen(
                    ["ollama", "run", OllamaClient.MODEL],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="ignore"
                )

                stdout, stderr = process.communicate(
                    prompt, timeout=OllamaClient.TIMEOUT_SECONDS
                )

                if process.returncode == 0 and stdout:
                    return stdout.strip()

                if __debug__:
                    print(f"[OllamaClient] Attempt {attempt} failed:", stderr)

            except subprocess.TimeoutExpired:
                if __debug__:
                    print(
                        f"[OllamaClient] Timeout on attempt {attempt}, retrying..."
                    )
                process.kill()

            except Exception as e:
                if __debug__:
                    print(
                        f"[OllamaClient] Error on attempt {attempt}: {e}"
                    )

            time.sleep(0.5)

        # ---- FINAL FALLBACK ----
        return ""
