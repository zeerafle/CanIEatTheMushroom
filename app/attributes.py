"""Mushroom attribute definitions and options."""

from typing import TypedDict


class AttributeInfo(TypedDict):
    question: str
    options: list[tuple[str, str]]


# Attribute display names and their possible values
ATTRIBUTES: dict[str, AttributeInfo] = {
    "odor": {
        "question": "What is the odor of the mushroom?",
        "options": [
            ("a", "Almond"),
            ("l", "Anise"),
            ("c", "Creosote"),
            ("f", "Foul"),
            ("m", "Musty"),
            ("n", "None"),
            ("p", "Pungent"),
            ("s", "Spicy"),
            ("y", "Fishy"),
        ],
    },
    "gill_color": {
        "question": "What is the gill color?",
        "options": [
            ("b", "Buff"),
            ("n", "Brown"),
            ("g", "Gray"),
            ("p", "Pink"),
            ("w", "White"),
            ("h", "Chocolate"),
            ("u", "Purple"),
            ("e", "Red"),
            ("y", "Yellow"),
            ("o", "Orange"),
            ("k", "Black"),
        ],
    },
    "spore_print_color": {
        "question": "What is the spore print color?",
        "options": [
            ("w", "White"),
            ("n", "Brown"),
            ("k", "Black"),
            ("h", "Chocolate"),
            ("r", "Green"),
            ("o", "Orange"),
            ("u", "Purple"),
            ("y", "Yellow"),
            ("b", "Buff"),
        ],
    },
    "stalk_color_below_ring": {
        "question": "What is the stalk color below the ring?",
        "options": [
            ("w", "White"),
            ("p", "Pink"),
            ("g", "Gray"),
            ("n", "Brown"),
            ("b", "Buff"),
            ("e", "Red"),
            ("y", "Yellow"),
            ("o", "Orange"),
            ("c", "Cinnamon"),
        ],
    },
    "stalk_color_above_ring": {
        "question": "What is the stalk color above the ring?",
        "options": [
            ("w", "White"),
            ("p", "Pink"),
            ("g", "Gray"),
            ("n", "Brown"),
            ("b", "Buff"),
            ("e", "Red"),
            ("y", "Yellow"),
            ("o", "Orange"),
            ("c", "Cinnamon"),
        ],
    },
    "stalk_root": {
        "question": "What is the stalk root type?",
        "options": [
            ("b", "Bulbous"),
            ("c", "Club"),
            ("e", "Equal"),
            ("r", "Rooted"),
            ("MISSING", "Missing/Not visible"),
        ],
    },
    "population": {
        "question": "What is the population?",
        "options": [
            ("a", "Abundant"),
            ("c", "Clustered"),
            ("n", "Numerous"),
            ("s", "Scattered"),
            ("v", "Several"),
            ("y", "Solitary"),
        ],
    },
    "habitat": {
        "question": "What is the habitat?",
        "options": [
            ("d", "Woods"),
            ("g", "Grasses"),
            ("l", "Leaves"),
            ("m", "Meadows"),
            ("p", "Paths"),
            ("u", "Urban"),
            ("w", "Waste"),
        ],
    },
    "ring_type": {
        "question": "What is the ring type?",
        "options": [
            ("e", "Evanescent"),
            ("f", "Flaring"),
            ("l", "Large"),
            ("n", "None"),
            ("p", "Pendant"),
        ],
    },
    "ring_number": {
        "question": "How many rings?",
        "options": [
            ("n", "None"),
            ("o", "One"),
            ("t", "Two"),
        ],
    },
    "cap_shape": {
        "question": "What is the cap shape?",
        "options": [
            ("b", "Bell"),
            ("c", "Conical"),
            ("f", "Flat"),
            ("k", "Knobbed"),
            ("s", "Sunken"),
            ("x", "Convex"),
        ],
    },
    "cap_color": {
        "question": "What is the cap color?",
        "options": [
            ("n", "Brown"),
            ("b", "Buff"),
            ("c", "Cinnamon"),
            ("g", "Gray"),
            ("r", "Green"),
            ("p", "Pink"),
            ("u", "Purple"),
            ("e", "Red"),
            ("w", "White"),
            ("y", "Yellow"),
        ],
    },
    "stalk_shape": {
        "question": "What is the stalk shape?",
        "options": [
            ("e", "Enlarging"),
            ("t", "Tapering"),
        ],
    },
    "gill_spacing": {
        "question": "What is the gill spacing?",
        "options": [
            ("c", "Close"),
            ("w", "Crowded"),
        ],
    },
}


def get_attribute_info(attr_name: str) -> AttributeInfo:
    """Get the question and options for a given attribute."""
    return ATTRIBUTES.get(
        attr_name,
        {"question": f"What is the {attr_name.replace('_', ' ')}?", "options": []},
    )
