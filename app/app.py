import reflex as rx

from .components.question_form import question_form
from .components.result_display import result_display
from .state_clips import MushroomExpertState


def index() -> rx.Component:
    """Main page of the mushroom expert system."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Can I Eat The Mushroom? 🍄", size="9"),
            rx.text(
                "Answer questions about the mushroom to determine if it's edible or poisonous.",
                size="4",
                color="gray",
                margin_bottom="30px",
            ),
            # Show question form or result based on completion status
            rx.cond(
                MushroomExpertState.is_complete,
                result_display(),
                question_form(),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
        size="3",
    )


app = rx.App()
app.add_page(index)
