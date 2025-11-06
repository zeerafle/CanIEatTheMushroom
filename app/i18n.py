"""Internationalization (i18n) support for the mushroom expert system."""

import json
from pathlib import Path
from typing import Any, Callable as CallableType

import reflex as rx

# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "tr": "Türkçe",
}

# Translation cache
_translations_cache: dict[str, dict] = {}


def load_translations(locale: str) -> dict:
    """Load translations for a specific locale."""
    if locale in _translations_cache:
        return _translations_cache[locale]

    translations_dir = Path(__file__).parent.parent / "translations"
    translations_file = translations_dir / f"{locale}.json"

    if not translations_file.exists():
        print(f"⚠️ Translation file not found: {translations_file}")
        # Fallback to English
        locale = "en"
        translations_file = translations_dir / "en.json"

    try:
        with open(translations_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
            _translations_cache[locale] = translations
            return translations
    except Exception as e:
        print(f"✗ Error loading translations for {locale}: {e}")
        return {}


def get_nested_value(data: dict, key_path: str, default: str = "") -> str:
    """Get a nested value from a dictionary using dot notation.

    Example: get_nested_value(data, "app.title") -> data["app"]["title"]
    """
    keys = key_path.split(".")
    value = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default

    return str(value) if value is not None else default


class I18nState(rx.State):
    """State for managing internationalization."""

    locale: str = "en"
    _translations: dict = {}

    def on_load_i18n(self):
        """Load translations on app load."""
        self._translations = load_translations(self.locale)

    @rx.event
    def set_locale(self, new_locale: str):
        """Change the current locale."""
        if new_locale in AVAILABLE_LANGUAGES:
            self.locale = new_locale
            self._translations = load_translations(new_locale)
            print(f"✓ Locale changed to: {new_locale}")

    def t(self, key: str, **params: Any) -> str:
        """Translate a key with optional parameters.

        Args:
            key: Translation key in dot notation (e.g., "app.title")
            **params: Parameters to format into the translation string

        Returns:
            Translated string with parameters formatted in

        Example:
            t("question_form.progress", count=5) -> "Questions answered: 5"
        """
        translations = self._translations if self._translations else load_translations(self.locale)
        translated = get_nested_value(translations, key, default=key)

        # Format parameters if provided
        if params:
            try:
                translated = translated.format(**params)
            except (KeyError, ValueError) as e:
                print(f"⚠️ Error formatting translation '{key}': {e}")

        return translated

    @rx.var
    def get_available_languages(self) -> list[tuple[str, str]]:
        """Get list of available languages as (code, name) tuples."""
        return list(AVAILABLE_LANGUAGES.items())


def get_translator(state: rx.State) -> CallableType:
    """Get the translation function for use in components.

    This is a helper to make it easier to use translations in components.
    """
    if hasattr(state, 't'):
        return state.t
    return lambda key, **params: key
