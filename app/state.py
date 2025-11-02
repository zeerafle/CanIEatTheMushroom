"""State management using CLIPS-based rules engine."""

from typing import Any

import reflex as rx

from .attributes import get_attribute_info
from .engines.clips_engine import CLIPSRulesEngine

# Module-level singleton engine
try:
    _clips_engine = CLIPSRulesEngine()
    print("✓ CLIPS engine initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize CLIPS engine: {e}")
    print("  Falling back to Python-based rules engine")
    from .engines.rules_engine import RulesEngine

    _clips_engine = RulesEngine()


class MushroomExpertState(rx.State):
    """State for the mushroom expert system using CLIPS."""

    # Current answers
    answers: dict[str, str] = {}

    # Current attribute being asked - default to first important attribute
    current_attribute: str = "odor"

    # Prediction result
    prediction: str = ""  # "edible" or "poisonous"
    matched_rule: str = ""
    rule_description: str = ""

    # UI state
    is_complete: bool = False

    def handle_answer(self, form_data: dict[str, Any]):
        """Handle form submission with an answer (matches form component call)."""
        print("\n📝 handle_answer called")
        print(f"   Form data: {form_data}")
        print(f"   Current attribute: {self.current_attribute}")
        print(f"   Current answers: {self.answers}")

        if not self.current_attribute:
            print("   ⚠️  No current attribute set!")
            return

        answer = form_data.get("answer", "")
        if not answer:
            print("   ⚠️  No answer in form data!")
            return

        print(f"   ✓ Answer received: {answer}")

        # Store the answer - create new dict to trigger Reflex reactivity
        new_answers = dict(self.answers)
        new_answers[self.current_attribute] = answer
        self.answers = new_answers
        print(f"   ✓ Updated answers: {self.answers}")

        # Check if any rule matches
        result = _clips_engine.check_rules(self.answers)
        print(f"   🔍 Rule check result: {result}")

        if result:
            # We have a match!
            target, rule_name, description = result
            self.prediction = target
            self.matched_rule = rule_name
            self.rule_description = description
            self.is_complete = True
            print(f"   ✅ MATCH FOUND: {target} - {rule_name}")
        else:
            # Get next question
            next_attr = _clips_engine.get_next_question(self.answers)
            print(f"   ➡️  Next question: {next_attr}")

            if next_attr:
                self.current_attribute = next_attr
            else:
                # No more questions and no match
                self.prediction = "unknown"
                self.matched_rule = "No matching rule found"
                self.rule_description = (
                    "Unable to classify this mushroom with the available rules."
                )
                self.is_complete = True
                print("   ⚠️  No more questions and no match found")

    # Alias for compatibility
    handle_submit = handle_answer

    def reset_form(self):
        """Reset the expert system to start over."""
        print("\n🔄 Resetting form...")
        self.answers = {}
        next_question = _clips_engine.get_next_question({})
        self.current_attribute = next_question if next_question else "odor"
        self.prediction = ""
        self.matched_rule = ""
        self.rule_description = ""
        self.is_complete = False
        print(f"   ✓ Reset complete. First question: {self.current_attribute}")

    @rx.var
    def get_current_question(self) -> str:
        """Get the current question text."""
        if self.current_attribute:
            attr_info = get_attribute_info(self.current_attribute)
            return attr_info["question"]
        return ""

    @rx.var
    def get_current_options(self) -> list[tuple[str, str]]:
        """Get options for the current question."""
        if self.current_attribute:
            attr_info = get_attribute_info(self.current_attribute)
            return attr_info["options"]
        return []

    @rx.var
    def get_answered_count(self) -> int:
        """Get number of questions answered."""
        return len(self.answers)

    @rx.var
    def get_progress(self) -> str:
        """Get progress information."""
        total_answered = len(self.answers)
        return f"Questions answered: {total_answered}"
