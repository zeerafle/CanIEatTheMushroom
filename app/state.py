from typing import Any

import reflex as rx

from .attributes import get_attribute_info
from .rules_engine import RulesEngine

# Create a single instance of the rules engine
_rules_engine = RulesEngine()


class MushroomExpertState(rx.State):
    """State for the mushroom expert system."""

    # User's answers so far
    answers: dict[str, str] = {}

    # Current question attribute
    current_attribute: str = "odor"  # Start with odor

    # Result
    prediction: str = ""
    matched_rule: str = ""
    is_complete: bool = False

    # Progress tracking
    questions_asked: int = 0

    def handle_answer(self, form_data: dict[str, Any]):
        """Handle user's answer to current question."""
        if "answer" not in form_data:
            return

        answer_code = str(form_data["answer"])

        # Store the answer
        self.answers[self.current_attribute] = answer_code
        self.questions_asked += 1

        # Check if any rule matches
        result = _rules_engine.check_rules(self.answers)

        if result:
            # We have a match!
            target, rule = result
            self.prediction = target
            self.matched_rule = rule.description
            self.is_complete = True
        else:
            # Get next question
            next_attr = _rules_engine.get_next_question(self.answers)

            if next_attr:
                self.current_attribute = next_attr
            else:
                # No more questions and no rule matched
                self.prediction = "unknown"
                self.matched_rule = "No matching rule found"
                self.is_complete = True

    def reset_form(self):
        """Reset the expert system."""
        self.answers = {}
        self.current_attribute = "odor"
        self.prediction = ""
        self.matched_rule = ""
        self.is_complete = False
        self.questions_asked = 0

    @rx.var
    def get_current_question(self) -> str:
        """Get the current question text."""
        attr_info = get_attribute_info(self.current_attribute)
        return attr_info.get("question", "")

    @rx.var
    def get_current_options(self) -> list[tuple[str, str]]:
        """Get options for current question."""
        attr_info = get_attribute_info(self.current_attribute)
        return attr_info.get("options", [])

    @rx.var
    def get_answered_count(self) -> int:
        """Get number of questions answered."""
        return len(self.answers)


# Keep the old state for compatibility
class FormRadioState(rx.State):
    form_data: dict[str, Any] = {}

    def handle_submit(self, form_data: dict[str, Any]):
        """Handle the form submit."""
        self.form_data = form_data
