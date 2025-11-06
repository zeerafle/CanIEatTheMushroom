"""Image upload component for LLM-powered mushroom analysis."""

import reflex as rx

from ..state import MushroomExpertState


def image_upload_section() -> rx.Component:
    """Render the optional image upload section for LLM analysis."""
    return rx.cond(
        MushroomExpertState.llm_enabled,
        rx.card(
            rx.vstack(
                rx.heading(
                    MushroomExpertState.ui_image_upload_title,
                    size="5",
                    margin_bottom="10px",
                ),
                rx.text(
                    MushroomExpertState.ui_image_upload_desc,
                    size="2",
                    color="gray",
                    margin_bottom="15px",
                ),
                # Upload area
                rx.cond(
                    ~MushroomExpertState.image_uploaded,
                    rx.vstack(
                        rx.upload(
                            rx.vstack(
                                rx.button(
                                    rx.icon("upload", size=20),
                                    MushroomExpertState.ui_button_upload,
                                    size="3",
                                    variant="soft",
                                ),
                                rx.text(
                                    MushroomExpertState.ui_drag_and_drop,
                                    size="2",
                                    color="gray",
                                ),
                            ),
                            id="mushroom_image_upload",
                            accept={
                                "image/png": [".png"],
                                "image/jpeg": [".jpg", ".jpeg"],
                            },
                            max_files=1,
                            border="2px dashed var(--accent-9)",
                            padding="30px",
                            border_radius="8px",
                        ),
                        rx.hstack(
                            rx.foreach(
                                rx.selected_files("mushroom_image_upload"),
                                lambda file: rx.text(file),
                            ),
                        ),
                        rx.cond(
                            MushroomExpertState.get_analyzing_status,
                            rx.button(MushroomExpertState.ui_button_analyze, loading=True, size="2"),
                            rx.button(
                                MushroomExpertState.ui_button_analyze,
                                on_click=lambda: MushroomExpertState.handle_image_upload(
                                    rx.upload_files(upload_id="mushroom_image_upload")
                                ),
                                size="2",
                            ),
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    # Show suggestions after upload
                    rx.vstack(
                        rx.hstack(
                            rx.icon("check-circle", color="green", size=20),
                            rx.text(
                                MushroomExpertState.ui_analysis_complete,
                                size="3",
                                weight="bold",
                                color="green",
                            ),
                            spacing="2",
                        ),
                        rx.divider(),
                        # Show suggestions list if not yet applied
                        rx.cond(
                            ~MushroomExpertState.llm_suggestions_applied,
                            rx.vstack(
                                rx.text(
                                    MushroomExpertState.ui_ai_suggestions,
                                    size="3",
                                    weight="bold",
                                    margin_top="10px",
                                ),
                                # Display suggestions
                                rx.vstack(
                                    rx.foreach(
                                        MushroomExpertState.llm_suggestions.items(),
                                        lambda item: rx.card(
                                            rx.hstack(
                                                rx.vstack(
                                                    rx.text(
                                                        item[0]
                                                        .replace("_", " ")
                                                        .title(),
                                                        size="2",
                                                        weight="bold",
                                                    ),
                                                    rx.text(
                                                        "Value: ",
                                                        item[1],
                                                        size="2",
                                                        color="gray",
                                                    ),
                                                    align="start",
                                                    spacing="1",
                                                ),
                                                rx.spacer(),
                                                rx.button(
                                                    MushroomExpertState.ui_button_apply,
                                                    size="1",
                                                    variant="soft",
                                                    on_click=MushroomExpertState.apply_llm_suggestion(
                                                        item[0]
                                                    ),
                                                ),
                                                width="100%",
                                                align="center",
                                            ),
                                            size="1",
                                        ),
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.button(
                                        MushroomExpertState.ui_button_apply_all,
                                        size="2",
                                        on_click=MushroomExpertState.apply_all_llm_suggestions,
                                        variant="solid",
                                    ),
                                    rx.button(
                                        MushroomExpertState.ui_button_upload_different,
                                        size="2",
                                        variant="outline",
                                        on_click=MushroomExpertState.clear_llm_suggestions,
                                    ),
                                    spacing="2",
                                    width="100%",
                                    margin_top="15px",
                                ),
                                width="100%",
                                spacing="3",
                                align="start",
                            ),
                            # Show message after suggestions applied
                            rx.vstack(
                                rx.callout(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon("check-circle-2", size=20),
                                            rx.text(
                                                MushroomExpertState.ui_suggestions_applied,
                                                size="3",
                                                weight="bold",
                                            ),
                                            spacing="2",
                                        ),
                                        rx.cond(
                                            ~MushroomExpertState.is_complete,
                                            rx.text(
                                                MushroomExpertState.ui_fill_remaining,
                                                size="2",
                                                margin_top="5px",
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    icon="info",
                                    color_scheme="blue",
                                    size="2",
                                    margin_top="10px",
                                ),
                                rx.button(
                                    MushroomExpertState.ui_button_upload_different,
                                    size="2",
                                    variant="outline",
                                    on_click=MushroomExpertState.clear_llm_suggestions(),
                                    margin_top="10px",
                                ),
                                width="100%",
                                spacing="2",
                                align="start",
                            ),
                        ),
                        width="100%",
                        spacing="3",
                        align="start",
                    ),
                ),
                # Error message
                rx.cond(
                    MushroomExpertState.llm_error != "",
                    rx.callout(
                        MushroomExpertState.llm_error,
                        icon="alert-circle",
                        color_scheme="red",
                        size="1",
                        margin_top="10px",
                    ),
                ),
                width="100%",
                spacing="4",
                align="start",
            ),
            width="100%",
            max_width="600px",
            margin_bottom="20px",
        ),
    )
