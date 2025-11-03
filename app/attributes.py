"""Mushroom attribute definitions and options."""

from typing import TypedDict


class AttributeInfo(TypedDict):
    question: str
    description: str
    options: list[tuple[str, str]]


# Attribute display names and their possible values
ATTRIBUTES: dict[str, AttributeInfo] = {
    "odor": {
        "question": "What is the odor of the mushroom?",
        "description": "How the mushroom smells: like almond/anise (licorice‑like), tar/chemical, fishy, foul, musty, no smell, sharp/pungent, or spicy. Example: Some edible Agaricus smell pleasantly like almond or anise; some poisonous ones smell foul or sharply pungent.",
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
        "description": "The color of the gills underneath the cap. Example: Agaricus gills often start pink and turn chocolate‑brown as they mature.",
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
        "description": "If you lay the cap gills‑down on paper, the spores leave a colored “print” (black, brown, chocolate, white, yellow, etc.). Example: Agaricus typically have a chocolate‑brown spore print; many Russula have white prints.",
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
        "description": "The color of the stalk below the ring. Example: A stalk can be white above the ring and brown below it.",
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
        "description": "The color of the stalk above the ring. Example: A white upper stalk stays white; some species have yellowish tint above the ring.",
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
        "description": "What the very bottom of the stalk (in the ground) looks like: a bulb, a club shape, a cup, even width, root‑like strings, or a pointed “root.” Sometimes it’s unknown. Example: Some Amanita have a round bulb at the base.",
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
        "description": "How the mushrooms are growing in an area: very common, in clusters from one spot, lots, scattered around, several together, or single and alone. Example: A tight bunch from the same base is “clustered”; one here and there is “solitary.”",
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
        "description": "Where it’s growing: lawns/grass, leaf litter, meadows, paths, city places, waste areas, or woods. Example: In a lawn is “grass”; in a forest is “woods.”",
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
        "description": "What the ring looks like: cobwebby, fades away, flares outward, large, none, hanging like a skirt, sheathing, or just a colored band. Example: A skirt‑like ring that hangs is “pendant”; a simple band of color is a “zone.”",
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
        "description": "How many rings are on the stalk: none, one, or two. Example: Store‑bought Agaricus usually have one ring; some species have no ring",
        "options": [
            ("n", "None"),
            ("o", "One"),
            ("t", "Two"),
        ],
    },
    "cap_shape": {
        "question": "What is the cap shape?",
        "description": "What the top of the mushroom looks like from the side: like a bell, a cone, a dome, flat, with a little bump, or sunken in the middle. Example: A typical grocery button mushroom has a dome‑shaped cap; a mature parasol can look flat.",
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
        "description": "The main color of the cap (e.g., brown, white, yellow, red, gray, pink, etc.). Example: Button mushroom caps are often white; many field mushrooms are brown",
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
        "description": "Whether the stalk gets wider toward the base or narrower toward the base. Example: A club‑like stalk that swells near the bottom is “wider at base”; a stalk that thins toward the bottom is “narrower at base.”",
        "options": [
            ("e", "Enlarging"),
            ("t", "Tapering"),
        ],
    },
    "gill_spacing": {
        "question": "What is the gill spacing?",
        "description": "How tightly packed the gills are under the cap: close/crowded or more spaced out. Example: Store mushrooms usually have crowded gills; some wild ones have gills that are more widely spaced.",
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
        {
            "question": f"What is the {attr_name.replace('_', ' ')}?",
            "options": [],
            "description": "",
        },
    )
