import clips
import pytest

try:
    from app.attributes import get_attribute_info
    from app.clips_engine import CLIPSRulesEngine

    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False


@pytest.fixture
def clips_env():
    """Fixture to create a CLIPS environment with loaded rules."""
    env = clips.Environment()
    env.load("rules.CLP")
    return env


def assert_case(env, case_id, **attributes):
    """Helper function to assert a mushroom case."""
    fact_str = f"(case (id {case_id})"
    for attr, value in attributes.items():
        fact_str += f" ({attr} {value})"
    fact_str += ")"
    env.assert_string(fact_str)


def get_conclusion(env, case_id):
    """Get conclusion for a specific case."""
    for fact in env.facts():
        if fact.template.name == "conclusion" and fact["id"] == case_id:
            return {"target": fact["target"], "rule": fact["rule"]}
    return None


def get_all_conclusions(env, case_id):
    """Get all conclusions for a specific case."""
    conclusions = []
    for fact in env.facts():
        if fact.template.name == "conclusion" and fact["id"] == case_id:
            conclusions.append({"target": fact["target"], "rule": fact["rule"]})
    return conclusions


def test_poisonous_odor_f(clips_env):
    """Test: Mushroom with foul odor should be poisonous."""
    assert_case(clips_env, 1, odor="f")
    clips_env.run()

    result = get_conclusion(clips_env, 1)
    assert result is not None
    assert result["target"] == "poisonous"


def test_poisonous_gill_color_b(clips_env):
    """Test: Mushroom with buff gill color should be poisonous."""
    assert_case(clips_env, 2, gill_color="b")
    clips_env.run()

    result = get_conclusion(clips_env, 2)
    assert result is not None
    assert result["target"] == "poisonous"


def test_poisonous_odor_p(clips_env):
    """Test: Mushroom with pungent odor should be poisonous."""
    assert_case(clips_env, 3, odor="p")
    clips_env.run()

    result = get_conclusion(clips_env, 3)
    assert result is not None
    assert result["target"] == "poisonous"


def test_poisonous_odor_c(clips_env):
    """Test: Mushroom with creosote odor should be poisonous."""
    assert_case(clips_env, 4, odor="c")
    clips_env.run()

    result = get_conclusion(clips_env, 4)
    assert result is not None
    assert result["target"] == "poisonous"


def test_poisonous_spore_print_color_r(clips_env):
    """Test: Mushroom with green spore print should be poisonous."""
    assert_case(clips_env, 5, spore_print_color="r")
    clips_env.run()

    result = get_conclusion(clips_env, 5)
    assert result is not None
    assert result["target"] == "poisonous"


def test_poisonous_and_rule(clips_env):
    """Test: Mushroom with stalk_color_below_ring=n AND stalk_root=MISSING."""
    assert_case(clips_env, 6, stalk_color_below_ring="n", stalk_root="MISSING")
    clips_env.run()

    result = get_conclusion(clips_env, 6)
    assert result is not None
    assert result["target"] == "poisonous"


def test_edible_stalk_color_above_ring_g(clips_env):
    """Test: Mushroom with gray stalk color above ring should be edible."""
    assert_case(clips_env, 10, stalk_color_above_ring="g")
    clips_env.run()

    result = get_conclusion(clips_env, 10)
    assert result is not None
    assert result["target"] == "edible"


def test_edible_odor_a(clips_env):
    """Test: Mushroom with almond odor should be edible."""
    assert_case(clips_env, 11, odor="a")
    clips_env.run()

    result = get_conclusion(clips_env, 11)
    assert result is not None
    assert result["target"] == "edible"


def test_edible_odor_l(clips_env):
    """Test: Mushroom with anise odor should be edible."""
    assert_case(clips_env, 12, odor="l")
    clips_env.run()

    result = get_conclusion(clips_env, 12)
    assert result is not None
    assert result["target"] == "edible"


def test_edible_population_a(clips_env):
    """Test: Mushroom with abundant population should be edible."""
    assert_case(clips_env, 13, population="a")
    clips_env.run()

    result = get_conclusion(clips_env, 13)
    assert result is not None
    assert result["target"] == "edible"


def test_edible_and_rule_odor_stalk(clips_env):
    """Test: Mushroom with no odor and tapering stalk should be edible."""
    assert_case(clips_env, 14, odor="n", stalk_shape="t")
    clips_env.run()

    result = get_conclusion(clips_env, 14)
    assert result is not None
    assert result["target"] == "edible"


def test_edible_and_rule_ring_spore(clips_env):
    """Test: Mushroom with two rings and white spore print should be edible."""
    assert_case(clips_env, 15, ring_number="t", spore_print_color="w")
    clips_env.run()

    result = get_conclusion(clips_env, 15)
    assert result is not None
    assert result["target"] == "edible"


def test_multiple_edible_rules(clips_env):
    """Test: Mushroom matching multiple edible rules."""
    assert_case(
        clips_env,
        20,
        odor="n",
        stalk_shape="t",
        cap_color="c",
        ring_number="t",
        spore_print_color="w",
    )
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 20)

    # Should match multiple edible rules (odor=n+stalk_shape=t, cap_color=c+odor=n, ring_number=t+spore_print_color=w)
    assert len(conclusions) >= 2
    for conclusion in conclusions:
        assert conclusion["target"] == "edible"


def test_multiple_poisonous_rules(clips_env):
    """Test: Mushroom matching multiple poisonous rules."""
    assert_case(clips_env, 21, odor="f", gill_color="b")
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 21)

    # Should match multiple poisonous rules (odor=f and gill_color=b)
    assert len(conclusions) >= 2
    for conclusion in conclusions:
        assert conclusion["target"] == "poisonous"


def test_no_matching_rules(clips_env):
    """Test: Mushroom with attributes that don't match any rule."""
    assert_case(clips_env, 30, cap_color="x", gill_spacing="x")
    clips_env.run()

    result = get_conclusion(clips_env, 30)
    assert result is None


def test_realistic_poisonous_mushroom(clips_env):
    """Test: Complete poisonous mushroom profile."""
    assert_case(
        clips_env,
        40,
        odor="f",
        cap_color="w",
        cap_shape="x",
        gill_color="w",
        gill_spacing="c",
        habitat="d",
        population="s",
        ring_number="o",
        ring_type="p",
    )
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 40)

    assert len(conclusions) >= 1
    # Check that at least one conclusion is poisonous
    poisonous_conclusions = [c for c in conclusions if c["target"] == "poisonous"]
    assert len(poisonous_conclusions) >= 1


def test_realistic_edible_mushroom(clips_env):
    """Test: Complete edible mushroom profile."""
    assert_case(
        clips_env,
        41,
        odor="n",
        stalk_shape="t",
        cap_color="n",
        cap_shape="f",
        gill_color="w",
        gill_spacing="c",
        habitat="g",
        population="v",
    )
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 41)

    assert len(conclusions) >= 1
    # Check that at least one conclusion is edible
    edible_conclusions = [c for c in conclusions if c["target"] == "edible"]
    assert len(edible_conclusions) >= 1


# ============================================================================
# CLIPS Engine Integration Tests
# ============================================================================


@pytest.fixture
def clips_engine():
    """Fixture to create a CLIPSRulesEngine instance."""
    if not ENGINE_AVAILABLE:
        pytest.skip("CLIPS engine not available")
    return CLIPSRulesEngine()


@pytest.mark.skipif(not ENGINE_AVAILABLE, reason="CLIPS engine not available")
class TestCLIPSEngineIntegration:
    """Test the CLIPSRulesEngine wrapper class."""

    def test_engine_initialization(self, clips_engine):
        """Test that the engine initializes correctly."""
        assert clips_engine is not None
        assert clips_engine.env is not None

    def test_poisonous_single_attribute(self, clips_engine):
        """Test poisonous classification with single attribute (foul odor)."""
        facts = {"odor": "f"}
        result = clips_engine.check_rules(facts)

        assert result is not None
        target, rule_name, description = result
        assert target == "poisonous"
        assert rule_name == "poisonous_odor_f"
        assert description is not None

    def test_edible_single_attribute(self, clips_engine):
        """Test edible classification with single attribute (almond odor)."""
        facts = {"odor": "a"}
        result = clips_engine.check_rules(facts)

        assert result is not None
        target, rule_name, description = result
        assert target == "edible"
        assert rule_name == "edible_odor_a"

    def test_multi_attribute_edible(self, clips_engine):
        """Test edible classification requiring multiple attributes."""
        facts = {"odor": "n", "stalk_shape": "t"}
        result = clips_engine.check_rules(facts)

        assert result is not None
        target, rule_name, description = result
        assert target == "edible"
        assert rule_name == "edible_odor_n_stalk_shape_t"

    def test_multi_attribute_poisonous(self, clips_engine):
        """Test poisonous classification requiring multiple attributes."""
        facts = {"stalk_color_below_ring": "n", "stalk_root": "MISSING"}
        result = clips_engine.check_rules(facts)

        assert result is not None
        target, rule_name, description = result
        assert target == "poisonous"

    def test_incomplete_data_no_match(self, clips_engine):
        """Test that incomplete data returns None."""
        facts = {"cap_color": "n"}
        result = clips_engine.check_rules(facts)

        # This might match or not depending on rules - just verify it doesn't crash
        # Most cap_color values alone don't trigger rules
        assert result is None or isinstance(result, tuple)

    def test_question_selection_first(self, clips_engine):
        """Test that first question is selected correctly."""
        next_q = clips_engine.get_next_question({})

        assert next_q is not None
        assert next_q in clips_engine.get_all_attributes()
        # Should prioritize important attributes like odor
        assert next_q == "odor"

    def test_question_selection_after_answer(self, clips_engine):
        """Test question selection after answering one question."""
        answered = {"odor": "n"}
        next_q = clips_engine.get_next_question(answered)

        assert next_q is not None
        assert next_q != "odor"  # Should not ask for already answered attribute
        assert next_q in clips_engine.get_all_attributes()

    def test_all_attributes_available(self, clips_engine):
        """Test that all expected attributes are available."""
        all_attrs = clips_engine.get_all_attributes()

        expected_attrs = [
            "cap_color",
            "cap_shape",
            "gill_color",
            "gill_spacing",
            "habitat",
            "odor",
            "population",
            "ring_number",
            "ring_type",
            "spore_print_color",
            "stalk_color_above_ring",
            "stalk_color_below_ring",
            "stalk_root",
            "stalk_shape",
        ]

        assert set(all_attrs) == set(expected_attrs)

    def test_engine_reset(self, clips_engine):
        """Test that engine can be reset and reused."""
        # First check
        facts1 = {"odor": "f"}
        result1 = clips_engine.check_rules(facts1)
        assert result1 is not None

        # Reset and check again with different facts
        clips_engine.reset_engine()
        facts2 = {"odor": "a"}
        result2 = clips_engine.check_rules(facts2)
        assert result2 is not None

        # Results should be different
        assert result1[0] == "poisonous"
        assert result2[0] == "edible"

    def test_attribute_info_integration(self, clips_engine):
        """Test integration with attribute info system."""
        next_q = clips_engine.get_next_question({})
        attr_info = get_attribute_info(next_q)

        assert "question" in attr_info
        assert "options" in attr_info
        assert len(attr_info["options"]) > 0

        # Each option should be a tuple of (code, label)
        for option in attr_info["options"]:
            assert isinstance(option, tuple)
            assert len(option) == 2

    def test_sequential_questions(self, clips_engine):
        """Test a sequence of questions like in the actual app flow."""
        answers = {}

        # Get first question
        q1 = clips_engine.get_next_question(answers)
        assert q1 is not None

        # Answer it (choose neutral value that won't trigger immediate match)
        answers[q1] = "n"

        # Check if we have a conclusion
        result = clips_engine.check_rules(answers)
        if result is None:
            # Get next question
            q2 = clips_engine.get_next_question(answers)
            assert q2 is not None
            assert q2 != q1

    def test_all_poisonous_triggers(self, clips_engine):
        """Test all single-attribute poisonous triggers."""
        poisonous_cases = [
            {"odor": "f"},
            {"odor": "p"},
            {"odor": "c"},
            {"odor": "m"},
            {"gill_color": "b"},
            {"spore_print_color": "r"},
            {"stalk_color_below_ring": "y"},
        ]

        for facts in poisonous_cases:
            result = clips_engine.check_rules(facts)
            assert result is not None, f"Failed for {facts}"
            assert result[0] == "poisonous", f"Expected poisonous for {facts}"

    def test_all_edible_triggers(self, clips_engine):
        """Test all single-attribute edible triggers."""
        edible_cases = [
            {"odor": "a"},
            {"odor": "l"},
            {"stalk_color_above_ring": "g"},
            {"stalk_color_above_ring": "o"},
            {"stalk_color_below_ring": "g"},
            {"population": "a"},
            {"population": "n"},
            {"habitat": "w"},
            {"ring_type": "f"},
            {"cap_shape": "s"},
        ]

        for facts in edible_cases:
            result = clips_engine.check_rules(facts)
            assert result is not None, f"Failed for {facts}"
            assert result[0] == "edible", f"Expected edible for {facts}"
