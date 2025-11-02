"""LLM Vision Service for analyzing mushroom images.

This module provides optional LLM-based image analysis to help users
quickly fill in mushroom attributes based on uploaded images.
"""

import os

from pydantic import BaseModel, Field

from ..attributes import ATTRIBUTES


class MushroomAttributes(BaseModel):
    """Structured output model for mushroom attribute analysis."""

    odor: str | None = Field(None, description="Mushroom odor code")
    gill_color: str | None = Field(None, description="Gill color code")
    spore_print_color: str | None = Field(None, description="Spore print color code")
    stalk_color_below_ring: str | None = Field(
        None, description="Stalk color below ring code"
    )
    stalk_color_above_ring: str | None = Field(
        None, description="Stalk color above ring code"
    )
    stalk_root: str | None = Field(None, description="Stalk root type code")
    population: str | None = Field(None, description="Population code")
    habitat: str | None = Field(None, description="Habitat code")
    ring_type: str | None = Field(None, description="Ring type code")
    ring_number: str | None = Field(None, description="Ring number code")
    cap_shape: str | None = Field(None, description="Cap shape code")
    cap_color: str | None = Field(None, description="Cap color code")
    stalk_shape: str | None = Field(None, description="Stalk shape code")
    gill_spacing: str | None = Field(None, description="Gill spacing code")


class LLMVisionService:
    """Service for analyzing mushroom images using LLM vision APIs."""

    def __init__(self):
        """Initialize the LLM vision service."""
        self.enabled: bool = False
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = os.getenv("LLM_VISION_MODEL", "gemini-2.0-flash")

        if self.api_key:
            self.enabled = True
            print("✓ LLM Vision service enabled (Gemini)")
        else:
            print("ℹ LLM Vision service disabled (no API key found)")

    def is_enabled(self) -> bool:
        """Check if the LLM vision service is enabled."""
        return self.enabled

    async def analyze_mushroom_image(self, image_data: bytes) -> dict[str, str]:
        """
        Analyze a mushroom image and return suggested attribute values.

        Args:
            image_data: The image data as bytes
            image_format: The image format (jpeg, png, etc.)

        Returns:
            Dictionary mapping attribute names to their suggested values
        """
        if not self.enabled:
            return {}

        try:
            import io

            from google import genai
            from PIL import Image

            # Configure Gemini
            client = genai.Client(api_key=self.api_key)

            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))

            # Create the prompt with all available attributes
            prompt = self._create_analysis_prompt()

            # Generate content with structured output
            response = client.models.generate_content(
                model=self.model,
                contents=[prompt, image],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": MushroomAttributes,
                },
            )

            # Parse the structured response
            parsed_response: MushroomAttributes = response.parsed
            return self._validate_and_convert_response(parsed_response)

        except ImportError:
            print(
                "⚠️  Google Generative AI library not installed. Install with: pip install google-generativeai pillow"
            )
            return {}
        except Exception as e:
            print(f"⚠️  Error analyzing image: {e}")
            return {}

    def _create_analysis_prompt(self) -> str:
        """Create a detailed prompt for the LLM to analyze the mushroom."""
        prompt = """Analyze this mushroom image and identify visible attributes.
Only provide values you are confident about based on what you can see in the image.
Leave attributes as null if you cannot determine them from the image.

Use ONLY the exact codes from the following valid options:

"""

        # Add all attributes and their options
        for attr_name, attr_info in ATTRIBUTES.items():
            prompt += f"\n{attr_name}:\n"
            for code, description in attr_info["options"]:
                prompt += f"  {code} = {description}\n"

        prompt += """

Important:
- Only include attributes you can confidently determine from the image
- Use ONLY the exact codes provided above (not the descriptions)
- Visual attributes like cap_color, gill_color, cap_shape are usually visible
- Odor and spore_print_color are typically NOT determinable from images alone
- Return null for any attribute you cannot see or determine
"""

        return prompt

    def _validate_and_convert_response(
        self, parsed_response: MushroomAttributes
    ) -> dict[str, str]:
        """
        Validate and convert the Pydantic model response to a dictionary.

        Args:
            parsed_response: The parsed Pydantic model from Gemini

        Returns:
            Dictionary mapping attribute names to their validated values
        """
        results = {}

        if not parsed_response:
            return results

        # Convert Pydantic model to dict and validate each attribute
        response_dict = parsed_response.model_dump(exclude_none=True)

        for attr_name, value in response_dict.items():
            # Validate that the attribute exists in our system
            if attr_name in ATTRIBUTES:
                # Validate that the value is valid for this attribute
                valid_codes = [code for code, _ in ATTRIBUTES[attr_name]["options"]]
                if value in valid_codes:
                    results[attr_name] = value
                else:
                    print(
                        f"⚠️  Invalid value '{value}' for attribute '{attr_name}', skipping"
                    )

        return results


# Global singleton instance
_llm_vision_service: LLMVisionService | None = None


def get_llm_vision_service() -> LLMVisionService:
    """Get or create the LLM vision service singleton."""
    global _llm_vision_service
    if _llm_vision_service is None:
        _llm_vision_service = LLMVisionService()
    return _llm_vision_service
