# Tests Quick Start Guide

## TL;DR

```bash
# Run all tests
pytest

# Run with details
pytest -v
```

**Result:** 31 tests, ~0.2s, 100% pass ✅

---

## What Gets Tested

### ✅ CLIPS Rules (17 tests)
- All poisonous mushroom rules
- All edible mushroom rules
- Multi-attribute conditions
- Edge cases

### ✅ Engine Integration (14 tests)
- Classification logic
- Question selection
- Sequential flow
- All rule triggers

---

## Common Commands

```bash
# All tests, verbose
pytest -v

# Show print statements
pytest -s

# Only integration tests
pytest -k "Integration"

# Specific test
pytest tests/test_mushroom_rules.py::test_poisonous_odor_f

# With coverage
pytest --cov=app --cov-report=html

# Parallel (requires pytest-xdist)
pytest -n auto
```

---

## Prerequisites

```bash
pip install pytest clipspy
```

---

## Test Structure

```
tests/
├── test_mushroom_rules.py     # All 31 tests
├── README.md                  # Detailed docs
└── MIGRATION_SUMMARY.md       # What changed
```

---

## Example Test Run

```
$ pytest -v

tests/test_mushroom_rules.py::test_poisonous_odor_f PASSED               [  3%]
tests/test_mushroom_rules.py::test_edible_odor_a PASSED                  [ 25%]
...
tests/test_mushroom_rules.py::TestCLIPSEngineIntegration::test_engine_initialization PASSED [ 58%]
...

============================== 31 passed in 0.19s ==============================
```

---

## Quick Checks

**Check if CLIPS works:**
```bash
python -c "import clips; print('✓ CLIPS OK')"
```

**Check if engine loads:**
```bash
python -c "from app.clips_engine import CLIPSRulesEngine; print('✓ Engine OK')"
```

**Verify rules syntax:**
```bash
python -c "import clips; env = clips.Environment(); env.load('rules.CLP'); print('✓ Rules OK')"
```

---

## Troubleshooting

**Problem:** `ImportError: clipspy`
**Fix:** `pip install clipspy`

**Problem:** `FileNotFoundError: rules.CLP`
**Fix:** Run from project root: `cd CanIEatTheMushroom && pytest`

**Problem:** Tests skipped
**Fix:** Install CLIPS engine and dependencies

---

## CI/CD Ready

```yaml
# GitHub Actions example
- name: Test
  run: |
    pip install pytest clipspy
    pytest -v
```

---

## More Info

- **Detailed guide:** [TESTING.md](../TESTING.md)
- **Test docs:** [README.md](README.md)
- **Migration notes:** [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)

---

## Stats

- **Tests:** 31
- **Time:** 0.19s
- **Coverage:** 100% of rules
- **Pass rate:** 100%

**Ready to ship! 🚀**
