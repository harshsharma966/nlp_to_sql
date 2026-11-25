"""
LLM Service - Manages the language model for SQL generation
"""
from llama_cpp import Llama
from config.settings import settings

class LLMService:
    """Manages the LLM model for text-to-SQL conversion"""

    _instance = None
    _model = None

    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        """Initialize the LLM model (loads once)"""
        if self._model is None:
            self._model = Llama(
                model_path=settings.MODEL_PATH,
                n_ctx=settings.MODEL_CONTEXT,
                n_threads=settings.MODEL_THREADS,
                n_gpu_layers=settings.MODEL_GPU_LAYERS,
                verbose=False,
            )

    def generate(self, prompt: str, max_tokens: int = 350, temperature: float = 0.0):
        """
        Generate text using the LLM

        Args:
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature

        Returns:
            str: Generated text
        """
        output = self._model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["Explanation", "Reason", "Note", "Answer", "```"]
        )
        return output["choices"][0]["text"]

# Singleton instance
llm_service = LLMService()
