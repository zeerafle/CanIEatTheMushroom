# Mushroom Expert System

## Overview

This is a web-based expert system built with Reflex that determines whether a mushroom is edible or poisonous based on its characteristics. The system asks questions one at a time and stops as soon as a rule matches.

### 🤖 AI Vision Feature

# Set your Gemini API key
export GEMINI_API_KEY="your-key-here"

The AI feature is completely optional - the app works perfectly fine without it!

## How It Works

### 1. Rule Engine (`app/rules_engine.py`)

The `RulesEngine` class:
- Converts CLIPS rules into Python `Rule` objects
- Evaluates rules against user-provided facts
- Determines the next best question to ask based on which attributes appear most frequently in remaining viable rules

### 2. Attribute Definitions (`app/attributes.py`)

Defines all mushroom attributes with:
- Human-readable questions
- Code-to-label mappings (e.g., "a" -> "Almond" for odor)
- All possible values for each attribute

### 3. State Management (`app/state.py`)

The `MushroomExpertState` class manages:
- User answers (dictionary of attribute -> value)
- Current question being asked
- Final prediction and matched rule
- Progress tracking

### 4. UI Components

- `question_form.py`: Displays current question with radio button options
- `result_display.py`: Shows the final result when a rule matches

### 5. Main App (`app/app.py`)

Orchestrates the UI, conditionally showing either the question form or result display.

## Flow

1. User starts with the first question (usually "odor")
2. After each answer:
   - System checks if any rule matches the current facts
   - If a rule matches → show result
   - If no rule matches → ask the next most important question
3. Process continues until a rule fires or no more questions remain

## Key Features

- **Early stopping**: As soon as one rule matches, the system stops asking questions
- **Smart question ordering**: Prioritizes attributes that appear in more remaining rules
- **User-friendly**: Shows progress and allows restarting
- **Bilingual support**: Ready for localization (Turkish title included)

## Installation & Running

### Basic Installation (Manual Mode Only)

```bash
# Install dependencies
uv sync

# Run the app
uv run reflex run
```

### Installation with AI Vision (Optional)

# Configure API key
```bash
cp .env.example .env
# Edit .env and add your Google API key

# Run the app
uv run reflex run
```

Navigate to `http://localhost:3000` to use the expert system.

### Features

- **Manual Mode** (default): Answer questions one by one
- **AI Vision Mode** (optional): Upload mushroom images for automatic attribute detection
  - Requires Google Gemini API key

## Example Rules

**Poisonous**:
- If odor is foul (f) → poisonous
- If gill color is buff (b) → poisonous
- If stalk color below ring is yellow (y) → poisonous

**Edible**:
- If odor is almond (a) → edible
- If habitat is waste (w) → edible
- If cap shape is sunken (s) → edible

## Documentation

- **[Testing Guide](TESTING.md)** - Information about running tests

## Safety Warning

⚠️ **This is an educational expert system only.** Never use this application to determine if real mushrooms are safe to eat. Always consult professional mycologists and field guides for actual mushroom identification.
