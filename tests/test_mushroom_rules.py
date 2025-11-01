import pytest
import clips


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
        if fact.template.name == "conclusion" and fact['id'] == case_id:
            return {
                'target': fact['target'],
                'rule': fact['rule']
            }
    return None


def get_all_conclusions(env, case_id):
    """Get all conclusions for a specific case."""
    conclusions = []
    for fact in env.facts():
        if fact.template.name == "conclusion" and fact['id'] == case_id:
            conclusions.append({
                'target': fact['target'],
                'rule': fact['rule']
            })
    return conclusions


def test_poisonous_odor_f(clips_env):
    """Test: Mushroom with foul odor should be poisonous."""
    assert_case(clips_env, 1, odor='f')
    clips_env.run()

    result = get_conclusion(clips_env, 1)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_poisonous_gill_color_b(clips_env):
    """Test: Mushroom with buff gill color should be poisonous."""
    assert_case(clips_env, 2, gill_color='b')
    clips_env.run()

    result = get_conclusion(clips_env, 2)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_poisonous_odor_p(clips_env):
    """Test: Mushroom with pungent odor should be poisonous."""
    assert_case(clips_env, 3, odor='p')
    clips_env.run()

    result = get_conclusion(clips_env, 3)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_poisonous_odor_c(clips_env):
    """Test: Mushroom with creosote odor should be poisonous."""
    assert_case(clips_env, 4, odor='c')
    clips_env.run()

    result = get_conclusion(clips_env, 4)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_poisonous_spore_print_color_r(clips_env):
    """Test: Mushroom with green spore print should be poisonous."""
    assert_case(clips_env, 5, spore_print_color='r')
    clips_env.run()

    result = get_conclusion(clips_env, 5)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_poisonous_and_rule(clips_env):
    """Test: Mushroom with stalk_color_below_ring=n AND stalk_root=MISSING."""
    assert_case(clips_env, 6, stalk_color_below_ring='n', stalk_root='MISSING')
    clips_env.run()

    result = get_conclusion(clips_env, 6)
    assert result is not None
    assert result['target'] == 'poisonous'


def test_edible_stalk_color_above_ring_g(clips_env):
    """Test: Mushroom with gray stalk color above ring should be edible."""
    assert_case(clips_env, 10, stalk_color_above_ring='g')
    clips_env.run()

    result = get_conclusion(clips_env, 10)
    assert result is not None
    assert result['target'] == 'edible'


def test_edible_odor_a(clips_env):
    """Test: Mushroom with almond odor should be edible."""
    assert_case(clips_env, 11, odor='a')
    clips_env.run()

    result = get_conclusion(clips_env, 11)
    assert result is not None
    assert result['target'] == 'edible'


def test_edible_odor_l(clips_env):
    """Test: Mushroom with anise odor should be edible."""
    assert_case(clips_env, 12, odor='l')
    clips_env.run()

    result = get_conclusion(clips_env, 12)
    assert result is not None
    assert result['target'] == 'edible'


def test_edible_population_a(clips_env):
    """Test: Mushroom with abundant population should be edible."""
    assert_case(clips_env, 13, population='a')
    clips_env.run()

    result = get_conclusion(clips_env, 13)
    assert result is not None
    assert result['target'] == 'edible'


def test_edible_and_rule_odor_stalk(clips_env):
    """Test: Mushroom with no odor and tapering stalk should be edible."""
    assert_case(clips_env, 14, odor='n', stalk_shape='t')
    clips_env.run()

    result = get_conclusion(clips_env, 14)
    assert result is not None
    assert result['target'] == 'edible'


def test_edible_and_rule_ring_spore(clips_env):
    """Test: Mushroom with two rings and white spore print should be edible."""
    assert_case(clips_env, 15, ring_number='t', spore_print_color='w')
    clips_env.run()

    result = get_conclusion(clips_env, 15)
    assert result is not None
    assert result['target'] == 'edible'


def test_multiple_edible_rules(clips_env):
    """Test: Mushroom matching multiple edible rules."""
    assert_case(clips_env, 20, odor='n', stalk_shape='t', cap_color='c', ring_number='t', spore_print_color='w')
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 20)

    # Should match multiple edible rules (odor=n+stalk_shape=t, cap_color=c+odor=n, ring_number=t+spore_print_color=w)
    assert len(conclusions) >= 2
    for conclusion in conclusions:
        assert conclusion['target'] == 'edible'


def test_multiple_poisonous_rules(clips_env):
    """Test: Mushroom matching multiple poisonous rules."""
    assert_case(clips_env, 21, odor='f', gill_color='b')
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 21)

    # Should match multiple poisonous rules (odor=f and gill_color=b)
    assert len(conclusions) >= 2
    for conclusion in conclusions:
        assert conclusion['target'] == 'poisonous'


def test_no_matching_rules(clips_env):
    """Test: Mushroom with attributes that don't match any rule."""
    assert_case(clips_env, 30, cap_color='x', gill_spacing='x')
    clips_env.run()

    result = get_conclusion(clips_env, 30)
    assert result is None


def test_realistic_poisonous_mushroom(clips_env):
    """Test: Complete poisonous mushroom profile."""
    assert_case(clips_env, 40, odor='f', cap_color='w', cap_shape='x', gill_color='w',
                gill_spacing='c', habitat='d', population='s', ring_number='o', ring_type='p')
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 40)

    assert len(conclusions) >= 1
    # Check that at least one conclusion is poisonous
    poisonous_conclusions = [c for c in conclusions if c['target'] == 'poisonous']
    assert len(poisonous_conclusions) >= 1


def test_realistic_edible_mushroom(clips_env):
    """Test: Complete edible mushroom profile."""
    assert_case(clips_env, 41, odor='n', stalk_shape='t', cap_color='n', cap_shape='f',
                gill_color='w', gill_spacing='c', habitat='g', population='v')
    clips_env.run()

    conclusions = get_all_conclusions(clips_env, 41)

    assert len(conclusions) >= 1
    # Check that at least one conclusion is edible
    edible_conclusions = [c for c in conclusions if c['target'] == 'edible']
    assert len(edible_conclusions) >= 1
