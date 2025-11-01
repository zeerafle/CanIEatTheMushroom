import reflex as rx
from rxconfig import config

from .components.radio_form import radio_form

from .state import FormRadioState


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Mantar yiyebilir miyim? 🍄", size="9"),
            rx.box(
                radio_form("How is the odor?"),
                margin_top="10px",
            ),
            rx.badge(
                rx.text(FormRadioState.form_data)
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


app = rx.App()
app.add_page(index)
