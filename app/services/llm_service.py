"""LLM Service wrapper for backwards compatibility and convenience."""

from .llm_vision import get_llm_vision_service


class LLMService:
    """Main LLM service that wraps all LLM-based functionality."""

    def __init__(self):
        """Initialize the LLM service."""
        self.vision = get_llm_vision_service()

    def is_enabled(self) -> bool:
        """Check if any LLM service is enabled."""
        return self.vision.is_enabled()


def is_llm_available() -> bool:
    """Check if LLM services are available."""
    service = LLMService()
    return service.is_enabled()


# Global singleton
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
