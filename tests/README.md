# Mushroom Expert System Tests

This directory contains comprehensive tests for the mushroom classification expert system.

## Test Structure

### `test_mushroom_rules.py`

Contains two main test suites:

1. **CLIPS Rules Tests** - Direct tests of the CLIPS rules file (`rules.CLP`)
   - Tests individual poisonous mushroom rules
   - Tests individual edible mushroom rules
   - Tests multi-attribute rules (AND conditions)
   - Tests realistic complete mushroom profiles
   - Tests edge cases (no matching rules, multiple matching rules)

2. **CLIPS Engine Integration Tests** - Tests of the `CLIPSRulesEngine` wrapper
   - Engine initialization and reset
   - Single-attribute classifications
   - Multi-attribute classifications
   - Question selection logic
   - Integration with attribute info system
   - Sequential question flow
   - All rule triggers (comprehensive coverage)

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with verbose output:
```bash
pytest -v
```

### Run specific test class:
```bash
pytest tests/test_mushroom_rules.py::TestCLIPSEngineIntegration
```

### Run specific test:
```bash
pytest tests/test_mushroom_rules.py::test_poisonous_odor_f
```

### Run only integration tests:
```bash
pytest -v -k "TestCLIPSEngineIntegration"
```

### Run with output (see print statements):
```bash
pytest -s
```

## Prerequisites

Install test dependencies:
```bash
pip install pytest clipspy
```

## Test Coverage

### CLIPS Rules Coverage

The tests cover all rules in `rules.CLP`:

**Poisonous Rules:**
- `poisonous_odor_f` - Foul odor
- `poisonous_odor_p` - Pungent odor
- `poisonous_odor_c` - Creosote odor
- `poisonous_odor_m` - Musty odor
- `poisonous_gill_color_b` - Buff gill color
- `poisonous_spore_print_color_r` - Green spore print
- `poisonous_stalk_color_below_ring_y` - Yellow stalk below ring
- `poisonous_stalk_color_below_ring_n_stalk_root_MISSING` - Brown stalk + missing root

**Edible Rules:**
- `edible_odor_a` - Almond odor
- `edible_odor_l` - Anise odor
- `edible_odor_n_stalk_shape_t` - No odor + tapering stalk
- `edible_stalk_color_above_ring_g` - Gray stalk above ring
- `edible_stalk_color_above_ring_o` - Orange stalk above ring
- `edible_stalk_color_below_ring_g` - Gray stalk below ring
- `edible_population_a` - Abundant population
- `edible_population_n` - Numerous population
- `edible_habitat_w` - Waste habitat
- `edible_ring_type_f` - Flaring ring
- `edible_cap_shape_s` - Sunken cap
- `edible_ring_number_t_spore_print_color_w` - Two rings + white spore print
- `edible_cap_color_c_odor_n` - Cinnamon cap + no odor
- `edible_odor_n_stalk_root_e` - No odor + equal stalk root
- `edible_gill_spacing_w_cap_color_n` - Crowded gill spacing + brown cap

### Engine Integration Coverage

- ✅ Engine initialization
- ✅ Rule matching (poisonous & edible)
- ✅ Single attribute rules
- ✅ Multi-attribute rules
- ✅ No match scenarios
- ✅ Question selection algorithm
- ✅ Sequential question flow
- ✅ Engine reset functionality
- ✅ Attribute info integration
- ✅ All rule triggers

## Test Fixtures

### `clips_env`
Creates a fresh CLIPS environment with loaded rules for each test.

### `clips_engine`
Creates a `CLIPSRulesEngine` instance for integration tests.

## Writing New Tests

### Testing a New CLIPS Rule

```python
def test_my_new_rule(clips_env):
    """Test description."""
    assert_case(clips_env, case_id, attribute1='value1', attribute2='value2')
    clips_env.run()

    result = get_conclusion(clips_env, case_id)
    assert result is not None
    assert result['target'] == 'poisonous'  # or 'edible'
    assert result['rule'] == 'my_new_rule'
```

### Testing Engine Integration

```python
@pytest.mark.skipif(not ENGINE_AVAILABLE, reason="CLIPS engine not available")
def test_my_integration(clips_engine):
    """Test description."""
    facts = {"attribute": "value"}
    result = clips_engine.check_rules(facts)

    assert result is not None
    target, rule_name, description = result
    assert target == "edible"
```

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install pytest clipspy
    pytest -v
```

## Troubleshooting

### CLIPS not found
```
ImportError: clipspy is not installed
```
**Solution:** `pip install clipspy`

### Rules file not found
```
FileNotFoundError: rules.CLP
```
**Solution:** Run pytest from the project root directory

### Integration tests skipped
```
SKIPPED [1] tests/test_mushroom_rules.py: CLIPS engine not available
```
**Solution:** Ensure `app/clips_engine.py` is properly installed and CLIPS engine is available

## Test Metrics

- **Total Tests:** 30+
- **CLIPS Rule Tests:** 19
- **Integration Tests:** 15+
- **Coverage:** All rules in `rules.CLP`
- **Execution Time:** < 5 seconds (typical)

## Best Practices

1. **Test Isolation:** Each test resets the CLIPS environment
2. **Clear Assertions:** Each test has specific, meaningful assertions
3. **Descriptive Names:** Test names describe what they're testing
4. **Comprehensive Coverage:** All rules and edge cases covered
5. **Skip Unavailable:** Integration tests skip gracefully if CLIPS unavailable
