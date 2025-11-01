import reflex as rx
from ..state import FormRadioState

def radio_form(title: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title),
            rx.form.root(
                rx.vstack(
                    rx.radio_group(
                        ["Almond", "Anise", "Creosote", "Fishy", "Foul", "Musty", "None", "Pungent", "Spicy"],
                        name="radio_choice",
                        direction="row",
                    ),
                    rx.button("Submit", type="submit"),
                    width="100%",
                    spacing="4",
                    align_items="center",
                ),
                on_submit=FormRadioState.handle_submit,
                reset_on_submit=True,
            ),
            align_items="center",
            width="100%",
            spacing="4",
        ),
    )
