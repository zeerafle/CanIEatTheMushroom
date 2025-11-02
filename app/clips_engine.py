"""CLIPS-based rule engine for mushroom classification expert system."""

import os
from pathlib import Path

try:
    import clips

    clips_available = True
except ImportError:
    clips_available = False
    print("Warning: clipspy not installed. Install with: pip install clipspy")


class CLIPSRulesEngine:
    """Expert system rule engine using CLIPS."""

    def __init__(self, rules_file: str | None = None):
        """
        Initialize the CLIPS engine.

        Args:
            rules_file: Path to the .CLP rules file. If None, uses rules.CLP in project root.
        """
        if not clips_available:
            raise ImportError(
                "clipspy is not installed. Install it with: pip install clipspy"
            )

        # Determine rules file path
        if rules_file is None:
            # Assume rules.CLP is in the project root
            current_file = Path(__file__)
            project_root = current_file.parent.parent  # Go up from app/ to project root
            rules_file = str(project_root / "rules.CLP")

        if not os.path.exists(rules_file):
            raise FileNotFoundError(f"Rules file not found: {rules_file}")

        self.rules_file = rules_file
        self.env = None
        self._initialize_clips()

    def _initialize_clips(self):
        """Initialize CLIPS environment and load rules."""
        self.env = clips.Environment()

        # Load the rules file
        try:
            self.env.load(self.rules_file)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load CLIPS rules from {self.rules_file}: {e}"
            )

    def reset_engine(self):
        """Reset the CLIPS environment to its initial state."""
        if self.env:
            self.env.reset()

    def check_rules(self, facts: dict[str, str]) -> tuple[str, str, str] | None:
        """
        Check if any rule matches the current facts.

        Args:
            facts: Dictionary of attribute -> value pairs

        Returns:
            Tuple of (target, rule_name, description) if a rule matches, None otherwise.
        """
        print(f"\n🔍 CLIPS check_rules called with facts: {facts}")

        # Reset environment for fresh inference
        self.env.reset()

        # Assert the case fact with all known attributes
        fact_slots = " ".join([f"({attr} {value})" for attr, value in facts.items()])
        fact_string = f"(case (id case-1) {fact_slots})"

        print(f"   📋 Asserting: {fact_string}")

        try:
            self.env.assert_string(fact_string)
        except Exception as e:
            print(f"   ❌ Error asserting fact: {e}")
            print(f"   Fact string: {fact_string}")
            return None

        # Run the rules
        print("   ⚙️  Running CLIPS inference engine...")
        fired_count = self.env.run()
        print(f"   🔥 {fired_count} rule(s) fired")

        # Check for conclusions
        conclusions_found = []
        for fact in self.env.facts():
            if fact.template.name == "conclusion":
                target = fact["target"]
                rule_name = str(fact["rule"])
                description = self._get_rule_description(rule_name)
                conclusions_found.append((target, rule_name, description))
                print(f"   ✅ Conclusion found: {target} from rule {rule_name}")

        if conclusions_found:
            # Return the first conclusion
            return conclusions_found[0]

        print("   ℹ️  No conclusions found")
        return None

    def _get_rule_description(self, rule_name: str) -> str:
        """Get the description/docstring of a rule."""
        try:
            # Try to find the rule and get its comment/docstring
            for rule in self.env.rules():
                if rule.name == rule_name:
                    # The docstring is typically the first comment in the rule
                    # For now, we'll construct a basic description
                    return f"Rule: {rule_name}"
        except Exception:
            pass
        return f"Rule: {rule_name}"

    def get_next_question(self, answered: dict[str, str]) -> str | None:
        """
        Determine the next attribute to ask about.
        Uses a strategy based on which attributes appear in rules that could still fire.

        Args:
            answered: Dictionary of attributes already answered

        Returns:
            The next attribute name to ask about, or None if no more questions needed
        """
        # This is a heuristic approach since CLIPS doesn't directly tell us
        # what to ask next in a goal-driven manner without backward chaining

        # All possible attributes from the template
        all_attributes = [
            "cap_color",
            "cap_shape",
            "gill_color",
            "gill_spacing",
            "habitat",
            "odor",
            "population",
            "ring_number",
            "ring_type",
            "spore_print_color",
            "stalk_color_above_ring",
            "stalk_color_below_ring",
            "stalk_root",
            "stalk_shape",
        ]

        # Count how many rules could potentially fire for each unanswered attribute
        attribute_importance = {}

        for attr in all_attributes:
            if attr not in answered:
                # This is a simplified heuristic
                # In a more sophisticated system, you might:
                # 1. Parse rule conditions from CLIPS
                # 2. Use uncertainty/probability
                # 3. Implement backward chaining
                attribute_importance[attr] = self._estimate_attribute_importance(
                    attr, answered
                )

        # Return the most important unanswered attribute
        if attribute_importance:
            return max(attribute_importance.items(), key=lambda x: x[1])[0]
        return None

    def _estimate_attribute_importance(
        self, attr: str, answered: dict[str, str]
    ) -> int:
        """
        Estimate the importance of asking about an attribute.
        This is a simplified heuristic - you could make it more sophisticated.
        """
        # Priority order based on your rules (most discriminative first)
        priority_map = {
            "odor": 10,  # Appears in many rules
            "gill_color": 8,
            "spore_print_color": 7,
            "stalk_color_below_ring": 6,
            "stalk_color_above_ring": 6,
            "stalk_root": 5,
            "population": 5,
            "habitat": 4,
            "ring_type": 4,
            "ring_number": 4,
            "cap_shape": 3,
            "cap_color": 3,
            "stalk_shape": 3,
            "gill_spacing": 3,
        }

        return priority_map.get(attr, 1)

    def get_all_attributes(self) -> list[str]:
        """Get all possible attributes from the case template."""
        return [
            "cap_color",
            "cap_shape",
            "gill_color",
            "gill_spacing",
            "habitat",
            "odor",
            "population",
            "ring_number",
            "ring_type",
            "spore_print_color",
            "stalk_color_above_ring",
            "stalk_color_below_ring",
            "stalk_root",
            "stalk_shape",
        ]


# Fallback to Python-based engine if CLIPS is not available
if not clips_available:
    # Import the existing Python-based engine as fallback
    from .rules_engine import RulesEngine as PythonRulesEngine

    class CLIPSRulesEngine(PythonRulesEngine):
        """Fallback to Python-based rules engine when CLIPS is not available."""

        def __init__(self, rules_file: Optional[str] = None):
            print("Using Python-based rules engine (CLIPS not available)")
            super().__init__()
