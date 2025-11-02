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
                    "🤖 Quick Fill with AI (Optional)",
                    size="5",
                    margin_bottom="10px",
                ),
                rx.text(
                    "Upload a photo of the mushroom to automatically fill in visible attributes using AI vision.",
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
                                    "Choose Image",
                                    size="3",
                                    variant="soft",
                                ),
                                rx.text(
                                    "Drag and drop or click to upload",
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
                            rx.button(
                                rx.cond(
                                    MushroomExpertState.analyzing_image,
                                    rx.spinner(size="2"),
                                    "Analyze Image",
                                ),
                                on_click=lambda: MushroomExpertState.handle_image_upload(
                                    rx.upload_files(upload_id="mushroom_image_upload")
                                ),
                                disabled=MushroomExpertState.analyzing_image,
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
                                f"Image analyzed! Found {MushroomExpertState.get_llm_suggestions_count} attributes",
                                size="3",
                                weight="bold",
                                color="green",
                            ),
                            spacing="2",
                        ),
                        rx.divider(),
                        rx.text(
                            "AI Suggestions:",
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
                                                item[0].replace("_", " ").title(),
                                                size="2",
                                                weight="bold",
                                            ),
                                            rx.text(
                                                f"Value: {item[1]}",
                                                size="2",
                                                color="gray",
                                            ),
                                            align="start",
                                            spacing="1",
                                        ),
                                        rx.spacer(),
                                        rx.button(
                                            "Apply",
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
                                "Apply All Suggestions",
                                size="2",
                                on_click=MushroomExpertState.apply_all_llm_suggestions(),
                                variant="solid",
                            ),
                            rx.button(
                                "Upload Different Image",
                                size="2",
                                variant="outline",
                                on_click=MushroomExpertState.clear_llm_suggestions(),
                            ),
                            spacing="2",
                            width="100%",
                            margin_top="15px",
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
