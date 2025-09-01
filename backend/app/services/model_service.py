import requests
from app.core.config import settings
from typing import Optional

class ModelService:
    """
    A service class to interact with the chosen LLM (default: LLaMA via Ollama).
    """

    def __init__(self, model: str = None, base_url: str = "http://localhost:11434"):
        self.model = model or settings.llm_model
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a prompt to the LLM and return the generated response.
        """
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except Exception as e:
            return f"⚠️ Error contacting model service: {str(e)}"

    def rag_generate(
        self,
        query: str,
        context_chunks: list[str],
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Retrieval-Augmented Generation (RAG):
        Combines retrieved context with the query before sending to LLM.
        """
        context_text = "\n\n".join(context_chunks)
        rag_prompt = (
            f"Use the following context to answer the question.\n\n"
            f"Context:\n{context_text}\n\n"
            f"Question: {query}\n\n"
            f"Answer concisely and cite sources if possible."
        )

        return self.generate(prompt=rag_prompt, system_prompt=system_prompt)
