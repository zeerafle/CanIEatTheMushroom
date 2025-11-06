# Internationalization (i18n) Implementation

This document explains how the i18n system works in the Mushroom Expert System.

## Overview

The application implements JSON-based internationalization without built-in Reflex i18n support. This allows the app to be translated into multiple languages by managing translation files and using a state-based translation system.

## Architecture

### Translation Files (`/translations`)

Translation files are stored in JSON format in the `translations/` directory:
- `en.json` - English translations
- `tr.json` - Turkish translations (example)

Each file contains a structured JSON object with translation keys organized by component:

```json
{
  "app": {
    "title": "Can I Eat The Mushroom? 🍄",
    "subtitle": "Answer questions about the mushroom..."
  },
  "image_upload": {
    "section_title": "🤖 Quick Fill with AI (Optional)",
    ...
  },
  "question_form": {
    ...
  },
  "result": {
    ...
  },
  "attributes": {
    "odor": {
      "question": "What is the odor of the mushroom?",
      "description": "How the mushroom smells...",
      "options": {
        "a": "Almond",
        "l": "Anise",
        ...
      }
    },
    ...
  }
}
```

### I18n Module (`app/i18n.py`)

The i18n module provides:

1. **`I18nState`**: A Reflex state class that manages the current locale and loaded translations
   - `locale`: Current language code (e.g., "en", "tr")
   - `set_locale(new_locale)`: Event handler to change language
   - `t(key, **params)`: Translation function that looks up keys and formats parameters

2. **`load_translations(locale)`**: Loads and caches translation JSON files

3. **`AVAILABLE_LANGUAGES`**: Dictionary mapping language codes to display names

### Updated State (`app/state.py`)

The main `MushroomExpertState` now inherits from `I18nState` and provides:

- **Computed vars for all UI text** (prefixed with `ui_`):
  - `ui_app_title`, `ui_app_subtitle`
  - `ui_button_upload`, `ui_button_submit`, `ui_button_start_over`
  - `ui_result_edible`, `ui_result_poisonous`, etc.

- **Translated attribute info** via `get_attribute_info_i18n()`:
  - Questions, descriptions, and options are all translated based on current locale

### Updated Attributes (`app/attributes.py`)

Added `get_attribute_info_i18n(attr_name, t_func)` which:
- Takes a translation function as input
- Returns translated question, description, and options for any attribute
- Keeps the original `get_attribute_info()` for backward compatibility

## Usage

### Adding a New Language

1. Create a new JSON file in `translations/` directory (e.g., `fr.json`)

2. Copy the structure from `en.json` and translate all values:
```json
{
  "app": {
    "title": "Puis-je Manger Ce Champignon? 🍄",
    ...
  },
  ...
}
```

3. Add the language to `AVAILABLE_LANGUAGES` in `app/i18n.py`:
```python
AVAILABLE_LANGUAGES = {
    "en": "English",
    "tr": "Türkçe",
    "fr": "Français",  # New language
}
```

### Adding New Translatable Text

1. **Add to translation JSON files** - Add the key-value pair in all language files:
```json
{
  "my_component": {
    "new_text": "Hello World"
  }
}
```

2. **Add computed var to state** - In `app/state.py`, add a computed var:
```python
@rx.var
def ui_my_new_text(self) -> str:
    return self.t("my_component.new_text")
```

3. **Use in components**:
```python
rx.text(MushroomExpertState.ui_my_new_text)
```

### Using Parameters in Translations

For dynamic text with variables:

1. **In JSON file**:
```json
{
  "result": {
    "matched_rule": "Matched rule: {rule}"
  }
}
```

2. **In state**:
```python
@rx.var
def ui_result_matched_rule(self) -> str:
    return self.t("result.matched_rule", rule=self.matched_rule)
```

## Language Selector

The app includes a language selector dropdown in the top-right corner (next to the color mode button) that allows users to switch languages on-the-fly. When changed, all text in the UI updates immediately.

## Best Practices

1. **Keep keys organized** - Group related translations together (by component or feature)

2. **Use descriptive keys** - `question_form.button_submit` is better than `btn1`

3. **Maintain consistency** - Use the same structure across all language files

4. **Test all languages** - Always verify translations render correctly in the UI

5. **Fallback handling** - The system falls back to English if a translation file is missing

## Technical Notes

- **Translation caching**: Translations are cached in memory after first load for performance
- **Dot notation**: Keys use dot notation (e.g., `"app.title"`) for nested access
- **State-based**: Uses Reflex's state system, so language changes trigger UI updates automatically
- **Type safety**: Computed vars provide type hints and IDE autocomplete support

## Example: Complete Workflow

To add Spanish support:

1. Create `translations/es.json`:
```json
{
  "app": {
    "title": "¿Puedo Comer Este Hongo? 🍄",
    "subtitle": "Responda preguntas sobre el hongo para determinar si es comestible o venenoso."
  },
  ...
}
```

2. Update `app/i18n.py`:
```python
AVAILABLE_LANGUAGES = {
    "en": "English",
    "tr": "Türkçe",
    "es": "Español",
}
```

3. Test by selecting "Español" from the language dropdown

That's it! The system handles the rest automatically.
