# Testing Guide for Mushroom Expert System

This document describes the comprehensive test suite for the CLIPS-based mushroom classification expert system.

## Overview

The test suite validates both the CLIPS rules and the Python integration layer, ensuring that:
- All CLIPS rules fire correctly
- The CLIPSRulesEngine wrapper works as expected
- Question selection logic is sound
- The system correctly classifies mushrooms as edible or poisonous

## Test Statistics

- **Total Tests:** 31
- **CLIPS Rule Tests:** 17 (direct CLIPS environment tests)
- **Integration Tests:** 14 (CLIPSRulesEngine wrapper tests)
- **Test Coverage:** 100% of rules in `rules.CLP`
- **Average Execution Time:** < 0.2 seconds

## Running Tests

### Prerequisites

```bash
# Install dependencies
pip install pytest clipspy
```

### Basic Usage

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Show print statements
pytest -s

# Run specific test file
pytest tests/test_mushroom_rules.py

# Run specific test class
pytest tests/test_mushroom_rules.py::TestCLIPSEngineIntegration

# Run specific test
pytest tests/test_mushroom_rules.py::test_poisonous_odor_f

# Run only integration tests
pytest -k "TestCLIPSEngineIntegration"
```

### With Coverage

```bash
# Install coverage
pip install pytest-cov

# Run with coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html
```

## Test Structure

### 1. CLIPS Rules Tests

**Purpose:** Directly test the CLIPS rules file to ensure each rule fires correctly.

**Test Cases:**
- ✅ Poisonous mushroom rules (8 rules)
- ✅ Edible mushroom rules (15 rules)
- ✅ Multi-attribute AND conditions
- ✅ Multiple matching rules
- ✅ No matching rules (edge case)
- ✅ Complete mushroom profiles

**Example:**
```python
def test_poisonous_odor_f(clips_env):
    """Test: Mushroom with foul odor should be poisonous."""
    assert_case(clips_env, 1, odor='f')
    clips_env.run()

    result = get_conclusion(clips_env, 1)
    assert result is not None
    assert result['target'] == 'poisonous'
```

### 2. CLIPS Engine Integration Tests

**Purpose:** Test the `CLIPSRulesEngine` Python wrapper class.

**Test Coverage:**
- ✅ Engine initialization and configuration
- ✅ Single-attribute classification
- ✅ Multi-attribute classification
- ✅ Question selection algorithm
- ✅ Sequential question flow
- ✅ Engine reset functionality
- ✅ Attribute system integration
- ✅ All rule triggers (comprehensive)

**Example:**
```python
def test_poisonous_single_attribute(clips_engine):
    """Test poisonous classification with single attribute."""
    facts = {"odor": "f"}
    result = clips_engine.check_rules(facts)

    assert result is not None
    target, rule_name, description = result
    assert target == "poisonous"
    assert rule_name == "poisonous_odor_f"
```

## Test Fixtures

### `clips_env`
- **Type:** CLIPS Environment
- **Scope:** Function (fresh for each test)
- **Purpose:** Direct CLIPS rule testing
- **Usage:** Load rules and assert facts

```python
@pytest.fixture
def clips_env():
    env = clips.Environment()
    env.load("rules.CLP")
    return env
```

### `clips_engine`
- **Type:** CLIPSRulesEngine instance
- **Scope:** Function (fresh for each test)
- **Purpose:** Integration testing
- **Usage:** Test Python wrapper methods

```python
@pytest.fixture
def clips_engine():
    return CLIPSRulesEngine()
```

## Helper Functions

### `assert_case(env, case_id, **attributes)`
Asserts a mushroom case fact in the CLIPS environment.

```python
assert_case(clips_env, 1, odor='f', gill_color='b')
# Creates: (case (id 1) (odor f) (gill_color b))
```

### `get_conclusion(env, case_id)`
Retrieves the first conclusion for a case.

```python
result = get_conclusion(clips_env, 1)
# Returns: {'target': 'poisonous', 'rule': 'poisonous_odor_f'}
```

### `get_all_conclusions(env, case_id)`
Retrieves all conclusions for a case (for multi-match scenarios).

```python
conclusions = get_all_conclusions(clips_env, 1)
# Returns: [{'target': '...', 'rule': '...'}, ...]
```

## Test Coverage by Rule

### Poisonous Rules (8 total)

| Rule Name | Test Function | Status |
|-----------|---------------|--------|
| `poisonous_odor_f` | `test_poisonous_odor_f` | ✅ |
| `poisonous_odor_p` | `test_poisonous_odor_p` | ✅ |
| `poisonous_odor_c` | `test_poisonous_odor_c` | ✅ |
| `poisonous_odor_m` | `test_all_poisonous_triggers` | ✅ |
| `poisonous_gill_color_b` | `test_poisonous_gill_color_b` | ✅ |
| `poisonous_spore_print_color_r` | `test_poisonous_spore_print_color_r` | ✅ |
| `poisonous_stalk_color_below_ring_y` | `test_all_poisonous_triggers` | ✅ |
| `poisonous_stalk_color_below_ring_n_stalk_root_MISSING` | `test_poisonous_and_rule` | ✅ |

### Edible Rules (15 total)

| Rule Name | Test Function | Status |
|-----------|---------------|--------|
| `edible_odor_a` | `test_edible_odor_a` | ✅ |
| `edible_odor_l` | `test_edible_odor_l` | ✅ |
| `edible_odor_n_stalk_shape_t` | `test_edible_and_rule_odor_stalk` | ✅ |
| `edible_stalk_color_above_ring_g` | `test_edible_stalk_color_above_ring_g` | ✅ |
| `edible_stalk_color_above_ring_o` | `test_all_edible_triggers` | ✅ |
| `edible_stalk_color_below_ring_g` | `test_all_edible_triggers` | ✅ |
| `edible_population_a` | `test_edible_population_a` | ✅ |
| `edible_population_n` | `test_all_edible_triggers` | ✅ |
| `edible_habitat_w` | `test_all_edible_triggers` | ✅ |
| `edible_ring_type_f` | `test_all_edible_triggers` | ✅ |
| `edible_cap_shape_s` | `test_all_edible_triggers` | ✅ |
| `edible_ring_number_t_spore_print_color_w` | `test_edible_and_rule_ring_spore` | ✅ |
| `edible_cap_color_c_odor_n` | `test_multiple_edible_rules` | ✅ |
| `edible_odor_n_stalk_root_e` | `test_realistic_edible_mushroom` | ✅ |
| `edible_gill_spacing_w_cap_color_n` | `test_realistic_edible_mushroom` | ✅ |

## Edge Cases Tested

1. **No Matching Rules** - Attributes that don't trigger any rule
2. **Multiple Matching Rules** - Cases where multiple rules fire
3. **Incomplete Data** - Partial attribute sets
4. **Complete Profiles** - Realistic full mushroom descriptions
5. **Engine Reset** - Ensuring clean state between checks

## Writing New Tests

### Adding a Test for a New Rule

1. **For CLIPS Rules:**
```python
def test_my_new_rule(clips_env):
    """Test description of what this rule does."""
    # Assert the case with required attributes
    assert_case(clips_env, case_id, attribute1='value1')

    # Run the inference engine
    clips_env.run()

    # Get and verify the conclusion
    result = get_conclusion(clips_env, case_id)
    assert result is not None
    assert result['target'] == 'edible'  # or 'poisonous'
    assert result['rule'] == 'my_new_rule'
```

2. **For Integration:**
```python
def test_my_integration_scenario(clips_engine):
    """Test a specific integration scenario."""
    facts = {"attribute": "value"}
    result = clips_engine.check_rules(facts)

    assert result is not None
    target, rule_name, description = result
    assert target == "expected_target"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest clipspy

      - name: Run tests
        run: pytest -v
```

## Troubleshooting

### Common Issues

**Issue:** `ImportError: clipspy is not installed`
```bash
# Solution
pip install clipspy
```

**Issue:** `FileNotFoundError: rules.CLP`
```bash
# Solution: Run from project root
cd CanIEatTheMushroom
pytest
```

**Issue:** Integration tests skipped
```
SKIPPED: CLIPS engine not available
```
```bash
# Solution: Check CLIPS engine installation
python -c "from app.clips_engine import CLIPSRulesEngine; print('OK')"
```

**Issue:** Tests fail after adding new rule
```bash
# Verify rule syntax in CLIPS
python -c "import clips; env = clips.Environment(); env.load('rules.CLP')"
```

## Performance

- **All 31 tests:** ~0.19 seconds
- **Average per test:** ~6ms
- **Memory usage:** < 10MB
- **Parallelization:** Supported via pytest-xdist

```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto
```

## Best Practices

1. ✅ **Isolation:** Each test uses fresh CLIPS environment
2. ✅ **Clarity:** Descriptive test names and docstrings
3. ✅ **Coverage:** All rules and edge cases covered
4. ✅ **Fast:** Tests run in < 1 second
5. ✅ **Reliable:** No flaky tests, deterministic results
6. ✅ **Maintainable:** Helper functions reduce duplication

## Next Steps

To extend the test suite:

1. **Add property-based tests** using Hypothesis
2. **Add performance benchmarks** for large rule sets
3. **Add UI/integration tests** for Reflex components
4. **Add test data generators** for random mushroom profiles
5. **Add mutation testing** to verify test quality

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [clipspy documentation](https://clipspy.readthedocs.io/)
- [CLIPS documentation](http://www.clipsrules.net/)
- [Test README](tests/README.md)
