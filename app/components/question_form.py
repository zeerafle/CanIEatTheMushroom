import reflex as rx

from ..state import MushroomExpertState


def question_form() -> rx.Component:
    """Render the current question with radio options."""
    return rx.card(
        rx.vstack(
            rx.heading(
                MushroomExpertState.get_current_question,
                size="6",
                margin_bottom="20px",
            ),
            rx.form.root(
                rx.vstack(
                    rx.radio_group.root(
                        rx.foreach(
                            MushroomExpertState.get_current_options,
                            lambda option: rx.radio_group.item(
                                rx.text(option[1]),  # Display name
                                value=option[0],  # Code
                            ),
                        ),
                        name="answer",
                        direction="column",
                        spacing="3",
                    ),
                    rx.button(
                        "Submit Answer",
                        type="submit",
                        size="3",
                        margin_top="20px",
                    ),
                    width="100%",
                    spacing="3",
                    align="start",
                ),
                on_submit=MushroomExpertState.handle_answer,
                width="100%",
            ),
            rx.divider(margin_top="20px", margin_bottom="20px"),
            rx.text(
                f"Questions answered: {MushroomExpertState.get_answered_count}",
                size="2",
                color="gray",
            ),
            width="100%",
            spacing="4",
        ),
        width="100%",
        max_width="600px",
    )
