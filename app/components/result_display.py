import reflex as rx

from ..state_clips import MushroomExpertState


def result_display() -> rx.Component:
    """Display the final result."""
    return rx.card(
        rx.vstack(
            rx.heading("🍄 Result", size="7"),
            rx.cond(
                MushroomExpertState.prediction == "edible",
                rx.vstack(
                    rx.callout(
                        "This mushroom is likely EDIBLE! ✅",
                        icon="circle-check",
                        color="green",
                        size="3",
                    ),
                    rx.text(
                        f"Matched rule: {MushroomExpertState.matched_rule}",
                        size="2",
                        color="gray",
                    ),
                    spacing="2",
                ),
                rx.cond(
                    MushroomExpertState.prediction == "poisonous",
                    rx.vstack(
                        rx.callout(
                            "This mushroom is likely POISONOUS! ⚠️",
                            icon="triangle-alert",
                            color="red",
                            size="3",
                        ),
                        rx.text(
                            f"Matched rule: {MushroomExpertState.matched_rule}",
                            size="2",
                            color="gray",
                        ),
                        spacing="2",
                    ),
                    rx.callout(
                        "Could not determine if this mushroom is safe.",
                        icon="circle-help",
                        color="orange",
                        size="3",
                    ),
                ),
            ),
            rx.divider(margin_top="20px", margin_bottom="20px"),
            rx.text(
                MushroomExpertState.get_progress,
                size="2",
                color="gray",
            ),
            rx.button(
                "Start Over",
                on_click=MushroomExpertState.reset_form,
                size="3",
                margin_top="20px",
            ),
            width="100%",
            spacing="4",
            align="center",
        ),
        width="100%",
        max_width="600px",
    )
