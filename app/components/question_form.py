import reflex as rx

from ..state import MushroomExpertState


def question_form() -> rx.Component:
    """Render the current question with radio options."""
    return rx.card(
        rx.vstack(
            rx.heading(
                MushroomExpertState.get_current_question,
                size="6",
                margin_bottom="10px",
            ),
            # Show LLM suggestion for current question if available
            rx.cond(
                MushroomExpertState.llm_suggestions.get(
                    MushroomExpertState.current_attribute
                ),
                rx.callout(
                    rx.hstack(
                        rx.text(
                            "AI suggestion available for this question",
                            size="2",
                        ),
                        rx.button(
                            "Auto-fill from AI",
                            size="1",
                            variant="soft",
                            on_click=lambda _: MushroomExpertState.apply_llm_suggestion(
                                MushroomExpertState.current_attribute
                            ),
                        ),
                        spacing="3",
                        align="center",
                    ),
                    icon="sparkles",
                    color_scheme="blue",
                    size="1",
                    margin_bottom="15px",
                ),
            ),
            rx.flex(
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
                # Attribute description
                rx.cond(
                    MushroomExpertState.get_current_description != "",
                    rx.text(
                        MushroomExpertState.get_current_description,
                        size="2",
                        color="gray",
                        margin_bottom="20px",
                    ),
                ),
                spacing="2",
            ),
            rx.divider(margin_top="20px", margin_bottom="20px"),
            rx.text(
                MushroomExpertState.get_progress,
                size="2",
                color="gray",
            ),
            width="100%",
            spacing="4",
        ),
        width="100%",
        max_width="600px",
    )
