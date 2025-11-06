import reflex as rx

from ..state import MushroomExpertState


def result_display() -> rx.Component:
    """Display the final result."""
    return rx.card(
        rx.vstack(
            rx.heading(MushroomExpertState.ui_result_title, size="7"),
            rx.cond(
                MushroomExpertState.prediction == "edible",
                rx.vstack(
                    rx.callout(
                        MushroomExpertState.ui_result_edible,
                        icon="circle-check",
                        color="green",
                        size="3",
                    ),
                    rx.text(
                        MushroomExpertState.ui_result_matched_rule,
                        size="2",
                        color="gray",
                    ),
                    spacing="2",
                ),
                rx.cond(
                    MushroomExpertState.prediction == "poisonous",
                    rx.vstack(
                        rx.callout(
                            MushroomExpertState.ui_result_poisonous,
                            icon="triangle-alert",
                            color="red",
                            size="3",
                        ),
                        rx.text(
                            MushroomExpertState.ui_result_matched_rule,
                            size="2",
                            color="gray",
                        ),
                        spacing="2",
                    ),
                    rx.callout(
                        MushroomExpertState.ui_result_unknown,
                        icon="circle-help",
                        color="orange",
                        size="3",
                    ),
                ),
            ),
            rx.divider(margin_top="20px", margin_bottom="20px"),
            rx.text(
                MushroomExpertState.ui_progress,
                size="2",
                color="gray",
            ),
            rx.button(
                MushroomExpertState.ui_button_start_over,
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
