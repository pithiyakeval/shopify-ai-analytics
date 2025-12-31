import subprocess
import time


class OllamaClient:
    """
    Wrapper around Ollama CLI for LLM interaction.

    Bonus features:
    - Retry logic
    - Timeout protection
    - Safe UTF-8 handling (Windows compatible)
    - Graceful fallback on failure
    """

    MODEL = "phi3"
    MAX_RETRIES = 2
    TIMEOUT_SECONDS = 20

    @staticmethod
    def ask(prompt: str) -> str:
        """
        Send a prompt to Ollama and return raw text output.

        The LLM is used only for planning (intent + parameters).
        Execution logic is deterministic elsewhere.
        """

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

            time.sleep(0.5)  # small backoff before retry

        # ---- FINAL FALLBACK ----
        # Agent will handle empty response safely
        return ""
