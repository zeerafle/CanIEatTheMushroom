"""State management using CLIPS-based rules engine."""

from typing import Any

import reflex as rx

from .attributes import get_attribute_info, get_attribute_info_i18n
from .engines.clips_engine import CLIPSRulesEngine
from .i18n import I18nState, load_translations
from .services.llm_vision import get_llm_vision_service

# Module-level singleton engine
try:
    _clips_engine = CLIPSRulesEngine()
    print("✓ CLIPS engine initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize CLIPS engine: {e}")
    print("  Falling back to Python-based rules engine")
    from .engines.rules_engine import RulesEngine

    _clips_engine = RulesEngine()


class MushroomExpertState(I18nState):
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

    # LLM Vision features
    llm_enabled: bool = False
    image_uploaded: bool = False
    analyzing_image: bool = False
    llm_suggestions: dict[str, str] = {}
    llm_error: str = ""
    llm_suggestions_applied: bool = False

    def on_load(self):
        """Initialize state on page load."""
        # Load i18n
        self.on_load_i18n()

        llm_service = get_llm_vision_service()
        self.llm_enabled = llm_service.is_enabled()

    @rx.event
    async def handle_image_upload(self, files: list[rx.UploadFile]):
        """Handle mushroom image upload and analyze with LLM."""
        if not files:
            return

        try:
            self.analyzing_image = True
            self.llm_error = ""

            # Get the first uploaded file
            upload_file = files[0]

            # Read the file data
            image_data = await upload_file.read()

            # Analyze with LLM
            llm_service = get_llm_vision_service()
            suggestions = await llm_service.analyze_mushroom_image(image_data)

            if suggestions:
                self.llm_suggestions = suggestions
                self.image_uploaded = True
                print(
                    f"✓ LLM analysis complete: {len(suggestions)} attributes identified"
                )
            else:
                self.llm_error = (
                    "Could not analyze the image. Please answer questions manually."
                )

        except Exception as e:
            self.llm_error = f"Error processing image: {str(e)}"
            print(f"✗ Error in handle_image_upload: {e}")
        finally:
            self.analyzing_image = False

    @rx.var
    def get_analyzing_status(self) -> bool:
        return self.analyzing_image

    @rx.event
    def apply_llm_suggestion(self, attribute: str):
        """Apply an LLM suggestion for a specific attribute."""
        if attribute in self.llm_suggestions:
            suggested_value = self.llm_suggestions[attribute]

            # Create new answers dict and add the suggestion
            new_answers = dict(self.answers)
            new_answers[attribute] = suggested_value
            self.answers = new_answers

            print(f"✓ Applied LLM suggestion: {attribute} = {suggested_value}")

            # Check if we have a match with current answers
            result = _clips_engine.check_rules(self.answers)

            if result:
                # We have a match!
                target, rule_name, description = result
                self.prediction = target
                self.matched_rule = rule_name
                self.rule_description = description
                self.is_complete = True
                print(f"✅ MATCH FOUND after LLM suggestion: {target} - {rule_name}")
            else:
                # Get next question
                next_attr = _clips_engine.get_next_question(self.answers)
                if next_attr:
                    self.current_attribute = next_attr

    @rx.event
    def apply_all_llm_suggestions(self):
        """Apply all LLM suggestions at once."""
        if not self.llm_suggestions:
            return

        # Merge all suggestions into answers
        new_answers = dict(self.answers)
        new_answers.update(self.llm_suggestions)
        self.answers = new_answers

        # Mark suggestions as applied
        self.llm_suggestions_applied = True

        print(f"✓ Applied all {len(self.llm_suggestions)} LLM suggestions")

        # Check if we have a match
        result = _clips_engine.check_rules(self.answers)

        if result:
            # We have a match!
            target, rule_name, description = result
            self.prediction = target
            self.matched_rule = rule_name
            self.rule_description = description
            self.is_complete = True
            print(
                f"✅ MATCH FOUND after applying all suggestions: {target} - {rule_name}"
            )
        else:
            # Get next question for unanswered attributes
            next_attr = _clips_engine.get_next_question(self.answers)
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

    @rx.event
    def clear_llm_suggestions(self):
        """Clear LLM suggestions and uploaded image."""
        self.llm_suggestions = {}
        self.image_uploaded = False
        self.llm_error = ""
        self.llm_suggestions_applied = False

    @rx.event
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

    @rx.event
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
        self.llm_suggestions = {}
        self.image_uploaded = False
        self.llm_error = ""
        self.analyzing_image = False
        self.llm_suggestions_applied = False
        print(f"   ✓ Reset complete. First question: {self.current_attribute}")

    @rx.var
    def get_current_question(self) -> str:
        """Get the current question text."""
        if self.current_attribute:
            attr_info = get_attribute_info_i18n(self.current_attribute, self.t)
            return attr_info["question"]
        return ""

    @rx.var
    def get_current_options(self) -> list[tuple[str, str]]:
        """Get options for the current question."""
        if self.current_attribute:
            attr_info = get_attribute_info_i18n(self.current_attribute, self.t)
            return attr_info["options"]
        return []

    @rx.var
    def get_current_description(self) -> str:
        """Get the description for the current attribute."""
        if self.current_attribute:
            attr_info = get_attribute_info_i18n(self.current_attribute, self.t)
            return attr_info.get("description", "")
        return ""

    @rx.var
    def get_answered_count(self) -> int:
        """Get number of questions answered."""
        return len(self.answers)

    @rx.var
    def get_progress(self) -> str:
        """Get progress information."""
        total_answered = len(self.answers)
        return f"Questions answered: {total_answered}"

    @rx.var
    def get_llm_suggestions_count(self) -> int:
        """Get the number of LLM suggestions."""
        return len(self.llm_suggestions)

    # UI Text Translations
    @rx.var
    def ui_app_title(self) -> str:
        return self.t("app.title")

    @rx.var
    def ui_app_subtitle(self) -> str:
        return self.t("app.subtitle")

    @rx.var
    def ui_image_upload_title(self) -> str:
        return self.t("image_upload.section_title")

    @rx.var
    def ui_image_upload_desc(self) -> str:
        return self.t("image_upload.section_description")

    @rx.var
    def ui_button_upload(self) -> str:
        return self.t("image_upload.button_upload")

    @rx.var
    def ui_drag_and_drop(self) -> str:
        return self.t("image_upload.drag_and_drop")

    @rx.var
    def ui_button_analyze(self) -> str:
        return self.t("image_upload.button_analyze")

    @rx.var
    def ui_analysis_complete(self) -> str:
        return self.t("image_upload.analysis_complete", count=self.get_llm_suggestions_count)

    @rx.var
    def ui_ai_suggestions(self) -> str:
        return self.t("image_upload.ai_suggestions")

    @rx.var
    def ui_button_apply(self) -> str:
        return self.t("image_upload.button_apply")

    @rx.var
    def ui_button_apply_all(self) -> str:
        return self.t("image_upload.button_apply_all")

    @rx.var
    def ui_button_upload_different(self) -> str:
        return self.t("image_upload.button_upload_different")

    @rx.var
    def ui_suggestions_applied(self) -> str:
        return self.t("image_upload.suggestions_applied")

    @rx.var
    def ui_fill_remaining(self) -> str:
        return self.t("image_upload.fill_remaining")

    @rx.var
    def ui_ai_suggestion_available(self) -> str:
        return self.t("question_form.ai_suggestion_available")

    @rx.var
    def ui_button_autofill(self) -> str:
        return self.t("question_form.button_autofill")

    @rx.var
    def ui_button_submit(self) -> str:
        return self.t("question_form.button_submit")

    @rx.var
    def ui_progress(self) -> str:
        return self.t("question_form.progress", count=self.get_answered_count)

    @rx.var
    def ui_result_title(self) -> str:
        return self.t("result.title")

    @rx.var
    def ui_result_edible(self) -> str:
        return self.t("result.edible")

    @rx.var
    def ui_result_poisonous(self) -> str:
        return self.t("result.poisonous")

    @rx.var
    def ui_result_unknown(self) -> str:
        return self.t("result.unknown")

    @rx.var
    def ui_result_matched_rule(self) -> str:
        return self.t("result.matched_rule", rule=self.matched_rule)

    @rx.var
    def ui_button_start_over(self) -> str:
        return self.t("result.button_start_over")
