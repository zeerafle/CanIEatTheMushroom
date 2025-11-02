"""Rule engine for mushroom classification expert system."""

from dataclasses import dataclass


@dataclass
class Rule:
    """Represents a single classification rule."""

    name: str
    target: str  # "edible" or "poisonous"
    conditions: dict[str, str]  # attribute -> value mapping
    description: str


class RulesEngine:
    """Expert system rule engine."""

    def __init__(self):
        self.rules: list[Rule] = self._initialize_rules()

    def _initialize_rules(self) -> list[Rule]:
        """Initialize all rules from the CLIPS file."""
        return [
            # Poisonous rules
            Rule("poisonous_odor_f", "poisonous", {"odor": "f"}, "Poisonous: odor=f"),
            Rule(
                "poisonous_gill_color_b",
                "poisonous",
                {"gill_color": "b"},
                "Poisonous: gill_color=b",
            ),
            Rule("poisonous_odor_p", "poisonous", {"odor": "p"}, "Poisonous: odor=p"),
            Rule("poisonous_odor_c", "poisonous", {"odor": "c"}, "Poisonous: odor=c"),
            Rule(
                "poisonous_spore_print_color_r",
                "poisonous",
                {"spore_print_color": "r"},
                "Poisonous: spore_print_color=r",
            ),
            Rule("poisonous_odor_m", "poisonous", {"odor": "m"}, "Poisonous: odor=m"),
            Rule(
                "poisonous_stalk_color_below_ring_y",
                "poisonous",
                {"stalk_color_below_ring": "y"},
                "Poisonous: stalk_color_below_ring=y",
            ),
            Rule(
                "poisonous_stalk_color_below_ring_n_stalk_root_MISSING",
                "poisonous",
                {"stalk_color_below_ring": "n", "stalk_root": "MISSING"},
                "Poisonous: stalk_color_below_ring=n AND stalk_root=MISSING",
            ),
            # Edible rules
            Rule(
                "edible_stalk_color_above_ring_g",
                "edible",
                {"stalk_color_above_ring": "g"},
                "Edible: stalk_color_above_ring=g",
            ),
            Rule("edible_odor_a", "edible", {"odor": "a"}, "Edible: odor=a"),
            Rule("edible_odor_l", "edible", {"odor": "l"}, "Edible: odor=l"),
            Rule(
                "edible_stalk_color_below_ring_g",
                "edible",
                {"stalk_color_below_ring": "g"},
                "Edible: stalk_color_below_ring=g",
            ),
            Rule(
                "edible_population_a",
                "edible",
                {"population": "a"},
                "Edible: population=a",
            ),
            Rule(
                "edible_stalk_color_above_ring_o",
                "edible",
                {"stalk_color_above_ring": "o"},
                "Edible: stalk_color_above_ring=o",
            ),
            Rule("edible_habitat_w", "edible", {"habitat": "w"}, "Edible: habitat=w"),
            Rule(
                "edible_population_n",
                "edible",
                {"population": "n"},
                "Edible: population=n",
            ),
            Rule(
                "edible_ring_type_f",
                "edible",
                {"ring_type": "f"},
                "Edible: ring_type=f",
            ),
            Rule(
                "edible_cap_shape_s",
                "edible",
                {"cap_shape": "s"},
                "Edible: cap_shape=s",
            ),
            Rule(
                "edible_odor_n_stalk_shape_t",
                "edible",
                {"odor": "n", "stalk_shape": "t"},
                "Edible: odor=n AND stalk_shape=t",
            ),
            Rule(
                "edible_ring_number_t_spore_print_color_w",
                "edible",
                {"ring_number": "t", "spore_print_color": "w"},
                "Edible: ring_number=t AND spore_print_color=w",
            ),
            Rule(
                "edible_cap_color_c_odor_n",
                "edible",
                {"cap_color": "c", "odor": "n"},
                "Edible: cap_color=c AND odor=n",
            ),
            Rule(
                "edible_odor_n_stalk_root_e",
                "edible",
                {"odor": "n", "stalk_root": "e"},
                "Edible: odor=n AND stalk_root=e",
            ),
            Rule(
                "edible_gill_spacing_w_cap_color_n",
                "edible",
                {"gill_spacing": "w", "cap_color": "n"},
                "Edible: gill_spacing=w AND cap_color=n",
            ),
        ]

    def check_rules(self, facts: dict[str, str]) -> tuple[str, Rule] | None:
        """
        Check if any rule matches the current facts.
        Returns (target, rule) if a rule matches, None otherwise.
        """
        for rule in self.rules:
            if self._rule_matches(rule, facts):
                return (rule.target, rule)
        return None

    def _rule_matches(self, rule: Rule, facts: dict[str, str]) -> bool:
        """Check if a rule's conditions are satisfied by the facts."""
        for attr, value in rule.conditions.items():
            if facts.get(attr) != value:
                return False
        return True

    def get_next_question(self, answered: dict[str, str]) -> str | None:
        """
        Determine the next attribute to ask about.
        Uses a simple strategy: prioritize attributes that appear in more rules.
        """
        # Count which attributes appear in rules we haven't satisfied yet
        attribute_importance = {}

        for rule in self.rules:
            # Check if this rule could still fire
            can_fire = True
            for attr, value in rule.conditions.items():
                if attr in answered and answered[attr] != value:
                    can_fire = False
                    break

            if can_fire:
                for attr in rule.conditions.keys():
                    if attr not in answered:
                        attribute_importance[attr] = (
                            attribute_importance.get(attr, 0) + 1
                        )

        # Return the most important unanswered attribute
        if attribute_importance:
            return max(attribute_importance.items(), key=lambda x: x[1])[0]
        return None
