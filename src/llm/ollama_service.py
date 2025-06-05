"""Ollama LLM Service for LLM Fixpoints Explorer."""

import ollama

class OllamaLLMService:
    """Service for interacting with Ollama language models."""

    def __init__(self, model_name: str = "llama3.2:latest"):
        """Initialize the service with a specific model."""
        self.model_name = model_name
        print(f"Initializing Ollama LLM Service with model: {model_name}")

    def generate_story(self, prompt: str) -> str:
        """Generate a story based on a prompt."""
        print(f"Generating story from prompt: {prompt[:50]}...")
        response = ollama.generate(self.model_name, prompt)
        return response['response']

    def retell_story(self, story: str) -> str:
        """Retell an existing story."""
        print("Retelling story...")
        prompt = f"Please retell this story in your own words. Make it engaging.\n\n<STORY>{story}</STORY>"
        response = ollama.generate(self.model_name, prompt)
        return response['response']