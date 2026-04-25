# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "kagglehub==0.3.13",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Generating Rules
    """)
    return


@app.cell
def _():
    import kagglehub

    # Download latest version
    path = kagglehub.dataset_download("uciml/mushroom-classification")

    print("Path to dataset files:", path)
    return (path,)


@app.cell
def _(path):
    import pandas as pd

    df = pd.read_csv(path + '/mushrooms.csv')
    df
    return df, pd


@app.cell
def _(df):
    from sklearn.model_selection import train_test_split

    # split data for rules induction and testing with ratio of 90/10
    train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)
    print("Train set size:", len(train_df))
    print("Test set size:", len(test_df))
    return test_df, train_df


@app.cell
def _():
    # Python (in-memory import from raw GitHub URL)
    import types
    import urllib.request

    url = "https://raw.githubusercontent.com/Brett-Kennedy/PRISM-Rules/refs/heads/main/prism_rules.py"
    source = urllib.request.urlopen(url).read().decode("utf-8")

    mod_name = "prism_rules"  # pick a unique name
    remote = types.ModuleType(mod_name)
    exec(compile(source, url, "exec"), remote.__dict__)

    # use functions/classes from the module
    prism = remote.PrismRules()
    return (prism,)


@app.cell
def _(prism, train_df):
    rules = prism.get_prism_rules(train_df, "class")
    return (rules,)


@app.cell
def _(rules):
    rules
    return


@app.cell
def _():
    import json
    import re


    def parse_condition(condition_str):
        """Parse a condition string like 'odor = f' or 'stalk-root = ?' into attribute and value."""
        parts = condition_str.strip().split(' = ')
        if len(parts) == 2:
            attribute = parts[0].strip().replace('-', '_')
            value = parts[1].strip()
            # Replace ? with MISSING to avoid CLIPS syntax issues
            if value == '?':
                value = 'MISSING'
            return attribute, value
        return None, None


    def extract_rule_info(rule_text):
        """Extract the condition part from the rule text."""
        # The condition is before the first newline
        lines = rule_text.split('\n')
        condition_line = lines[0].strip()
        return condition_line


    def create_rule_name(target, conditions):
        """Create a rule name from target and conditions."""
        # Create a snake_case rule name
        parts = [target.lower()]
        for attr, val in conditions:
            # Replace special characters in rule names
            safe_val = val.replace('?', 'MISSING')
            parts.append(f"{attr}_{safe_val}")
        return '_'.join(parts)


    def generate_clips_template(rules_dict):
        """Generate CLIPS template from the rules."""
        # Collect all unique attributes
        attributes = set()

        for target, rules in rules_dict.items():
            for rule_text in rules:
                condition_line = extract_rule_info(rule_text)
                # Split by AND to handle multiple conditions
                conditions = condition_line.split(' AND ')
                for cond in conditions:
                    attr, _ = parse_condition(cond)
                    if attr:
                        attributes.add(attr)

        # Generate template
        template = "; case template\n"
        template += "(deftemplate case\n"
        template += "  (slot id)\n"
        for attr in sorted(attributes):
            template += f"  (slot {attr})\n"
        template += ")\n\n"

        template += "; conclusion template\n"
        template += "(deftemplate conclusion\n"
        template += "  (slot id)\n"
        template += "  (slot target)\n"
        template += "  (slot rule))\n\n"

        return template


    def generate_clips_rules(rules_dict, target_map=None):
        """Generate CLIPS rules from the parsed rules."""
        if target_map is None:
            target_map = {"0": "poisonous", "1": "edible"}

        clips_rules = ""

        for target_key, rules in rules_dict.items():
            # Convert target_key to string to handle numpy.int64
            target_key_str = str(target_key)
            target_name = target_map.get(target_key_str, target_key_str)

            clips_rules += f"; {'-' * 26}\n"
            clips_rules += f"; {target_name.capitalize()} rules\n"
            clips_rules += f"; {'-' * 26}\n\n"

            for idx, rule_text in enumerate(rules):
                condition_line = extract_rule_info(rule_text)

                # Parse conditions
                condition_parts = condition_line.split(' AND ')
                conditions = []
                for cond in condition_parts:
                    attr, val = parse_condition(cond)
                    if attr and val:
                        conditions.append((attr, val))

                if not conditions:
                    continue

                # Create rule name
                rule_name = create_rule_name(target_name, conditions)

                # Build condition description
                cond_desc = " AND ".join([f"{attr}={val}" for attr, val in conditions])

                # Generate rule
                clips_rules += f'(defrule {rule_name}\n'
                clips_rules += f'  "{target_name.capitalize()}: {cond_desc}"\n'
                clips_rules += f'  (case (id ?case-id)\n'

                for attr, val in conditions:
                    clips_rules += f'        ({attr} {val})\n'

                clips_rules += '  )\n'
                clips_rules += '  =>\n'
                clips_rules += f'  (assert (conclusion (id ?case-id) (target "{target_name}") (rule {rule_name}))))\n\n'

        return clips_rules
    return generate_clips_rules, generate_clips_template, re


@app.cell
def _(generate_clips_rules, generate_clips_template, rules):
    template = generate_clips_template(rules)

    target_map = {"0": "poisonous", "1": "edible"}
    clips_rules = generate_clips_rules(rules, target_map)
    return clips_rules, template


@app.cell
def _(clips_rules, template):
    full_output = template + clips_rules
    print(full_output)
    return (full_output,)


@app.cell
def _(full_output):
    with open('rules.CLP', 'w') as f:
        f.write(full_output)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Evaluating Rules
    """)
    return


@app.cell
def _(re, template, test_df):
    # read test data and convert to CLIPS facts
    # Extract valid slots defined in the 'case' template
    # We split to ensure we only look at the 'case' template, not 'conclusion'
    case_template_section = template.split('conclusion template')[0]
    valid_slots = set(re.findall(r'\(slot\s+([a-zA-Z0-9_]+)\)', case_template_section))

    # read test data and convert to CLIPS facts
    facts_list = []
    for idx, row in test_df.iterrows():
        fact_str = f"(case (id {idx})"
        for col in test_df.columns:
            if col != 'class':
                attr = col.replace('-', '_')
                # Only include the attribute if it was defined in the CLIPS template
                if attr in valid_slots:
                    val = str(row[col])
                    if val == '?':
                        val = 'MISSING'
                    fact_str += f" ({attr} {val})"
        fact_str += ")"
        facts_list.append((idx, fact_str, row['class']))

    facts_list
    return (facts_list,)


@app.cell
def _(facts_list):
    import clips
    
    # run inference and get the results from each input data
    env = clips.Environment()
    env.load('rules.CLP')

    results = []
    for _, fact_str_infr, true_class in facts_list:
        env.reset()
        env.assert_string(fact_str_infr)
        env.run()
    
        predicted_class = "unknown"
        fired_rule = "none"
        for fact in env.facts():
            if fact.template.name == 'conclusion':
                predicted_class = fact['target']
                fired_rule = fact['rule']
                break
            
        # The dataset target values are 'e' (edible) and 'p' (poisonous)
        if true_class == 'e':
            true_mapped = 'edible'
        elif true_class == 'p':
            true_mapped = 'poisonous'
        else:
            true_mapped = true_class
        
        results.append({
            'id': _,
            'true_class': true_mapped,
            'predicted_class': predicted_class,
            'rule': fired_rule
        })
    return (results,)


@app.cell
def _(pd, results):
    from sklearn.metrics import confusion_matrix

    # calculate the precision for "edible"
    edible_tp = sum(1 for r in results if r['true_class'] == 'edible' and r['predicted_class'] == 'edible')
    edible_fp = sum(1 for r in results if r['true_class'] == 'poisonous' and r['predicted_class'] == 'edible')
    edible_precision = edible_tp / (edible_tp + edible_fp) if (edible_tp + edible_fp) > 0 else 0.0

    # calculate the recall for "poisonous"
    poisonous_tp = sum(1 for r in results if r['true_class'] == 'poisonous' and r['predicted_class'] == 'poisonous')
    poisonous_fn = sum(1 for r in results if r['true_class'] == 'poisonous' and r['predicted_class'] != 'poisonous')
    poisonous_recall = poisonous_tp / (poisonous_tp + poisonous_fn) if (poisonous_tp + poisonous_fn) > 0 else 0.0

    # calculate how often the system fallback to unknown
    unknown_count = sum(1 for r in results if r['predicted_class'] == 'unknown')
    unknown_rate = unknown_count / len(results) if len(results) > 0 else 0.0

    print(f"Precision for 'edible': {edible_precision:.4f}")
    print(f"Recall for 'poisonous': {poisonous_recall:.4f}")
    print(f"Unknown fallback rate: {unknown_rate:.4f}\n")

    # Generate Confusion Matrix
    y_true = [r['true_class'] for r in results]
    y_pred = [r['predicted_class'] for r in results]

    labels = ['edible', 'poisonous', 'unknown']
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    # Format beautifully with pandas
    cm_df = pd.DataFrame(
        cm, 
        index=[f"True {l}" for l in labels], 
        columns=[f"Pred {l}" for l in labels]
    )

    print("--- Confusion Matrix ---")
    print(cm_df.to_string())
    return


@app.cell
def _(results):
    print("--- First 5 Results Verification ---")
    for r in results[:5]:
        print(f"ID: {r['id']:<4} | True: {r['true_class']:<9} | Predicted: {r['predicted_class']:<9} | Reason (Rule): {r['rule']}")
    return


if __name__ == "__main__":
    app.run()
