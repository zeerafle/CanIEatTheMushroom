# Quick Start: Testing i18n

## Running the App

1. Make sure you're in the project directory:
```bash
cd /home/zeerafle/Projects/CanIEatTheMushroom
```

2. Run the Reflex app:
```bash
reflex run
```

3. Open your browser to `http://localhost:3000`

## Testing Language Switching

1. Look for the language selector in the top-right corner (next to the dark/light mode toggle)

2. Click the dropdown and select "Türkçe" (Turkish)

3. Observe that all text in the UI changes to Turkish:
   - Title: "Bu Mantarı Yiyebilir miyim? 🍄"
   - Subtitle changes to Turkish
   - All button labels change
   - Question and answer options change

4. Switch back to "English" and verify everything returns to English

## What Gets Translated

- ✅ Main app title and subtitle
- ✅ All button labels
- ✅ Form labels and instructions
- ✅ Question text
- ✅ Answer options (Almond → Badem, etc.)
- ✅ Result messages (edible/poisonous)
- ✅ AI/LLM section text
- ✅ Progress indicators

## Current Supported Languages

- **English (en)** - Full support
- **Turkish (tr)** - Full support (example translation)

## Adding Your Own Language

See [I18N_GUIDE.md](./I18N_GUIDE.md) for detailed instructions on adding new languages.

## Troubleshooting

### Language doesn't change
- Make sure the JSON file exists in `translations/` directory
- Check browser console for errors
- Verify JSON syntax is valid

### Missing translations
- Falls back to English automatically
- Check if the key exists in your translation file
- Compare structure with `en.json`

### Text displays translation key instead of value
- Verify the key path is correct in the translation file
- Check for typos in the key name
- Ensure the computed var in `state.py` is using the correct key

## Example Translation Keys

```
app.title                          → "Can I Eat The Mushroom? 🍄"
image_upload.button_upload         → "Choose Image"
question_form.button_submit        → "Submit Answer"
result.edible                      → "This mushroom is likely EDIBLE! ✅"
attributes.odor.question           → "What is the odor of the mushroom?"
attributes.odor.options.a          → "Almond"
```
