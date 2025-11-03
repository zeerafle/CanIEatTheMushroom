import reflex as rx

from .components.image_upload import image_upload_section
from .components.question_form import question_form
from .components.result_display import result_display
from .state import MushroomExpertState


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
                rx.vstack(
                    # Optional AI-powered image upload
                    image_upload_section(),
                    # Question form
                    question_form(),
                    spacing="5",
                    width="100%",
                    align="center",
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
        size="3",
    )


app = rx.App()
app.add_page(index, on_load=MushroomExpertState.on_load, title="Can I Eat The Mushroom")
