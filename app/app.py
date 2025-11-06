import reflex as rx

from .components.image_upload import image_upload_section
from .components.question_form import question_form
from .components.result_display import result_display
from .i18n import AVAILABLE_LANGUAGES
from .state import MushroomExpertState


def language_selector() -> rx.Component:
    """Language selector dropdown."""
    return rx.hstack(
        rx.text("Language:", size="2", weight="medium"),
        rx.select.root(
            rx.select.trigger(placeholder=MushroomExpertState.locale.upper()),
            rx.select.content(
                rx.foreach(
                    MushroomExpertState.get_available_languages,
                    lambda lang: rx.select.item(lang[1], value=lang[0]),
                ),
            ),
            value=MushroomExpertState.locale,
            on_change=MushroomExpertState.set_locale,
        ),
        spacing="2",
        align="center",
    )


def index() -> rx.Component:
    """Main page of the mushroom expert system."""
    return rx.container(
        rx.hstack(
            rx.color_mode.button(position="top-right"),
            language_selector(),
            position="absolute",
            top="20px",
            right="20px",
            spacing="4",
            z_index="100",
        ),
        rx.vstack(
            rx.heading(MushroomExpertState.ui_app_title, size="9"),
            rx.text(
                MushroomExpertState.ui_app_subtitle,
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
