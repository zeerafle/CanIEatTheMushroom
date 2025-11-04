---
theme: slidev-theme-academic
title: Yiyebilir Mantar Uzman Sistemi
transition: slide-left
fonts:
  serif: Bitter
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
# duration of the presentation
duration: 35min
layout: cover
coverAuthor: Vauwez Sam El Fareez
coverAuthorUrl: https://samfareez.is-a.dev
coverBackgroundSource: unsplash
coverBackgroundUrl: https://images.unsplash.com/photo-1630286057323-905c2a21941f?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1470
coverDate: 7.11.2025
---

# Yiyebilir Mantar Uzman Sistemi

---

# Mantar

- Mantarlar, miselyum adı verilen gizli ipliklerden büyüyen fungi'nin meyve veren kısımlarıdır; şapka, sap ve solungaçlar veya gözenekler gibi kısımlardan sporlar salarak yayılırlar <sup>1</sup>.
- Türleri birbirinden ayırmak için solungaç yapısına, gövdede bir çanak veya halka olup olmadığına, spor izi rengine, kapak ve gövde detaylarına ve nerede büyüdüğüne bakın; bunların olgunlaştıkça değişebileceğini unutmayın <sup>2</sup>.
- Bazı mantarlar gıda veya ilaçtır, bazıları ise zehirlidir; ölümcül benzerleri olduğu için güvenli tanımlama birden fazla eşleştirme özelliği ve uzman bakımı gerektirir <sup>1</sup>.
- Mantarlar yemeklere zengin umami ve topraksı tatlar katar; kurutma işlemi şeflerin derinlik için kullandığı daha güçlü acı ve küf notalarını artırır <sup>3</sup>.
- Mantarlar mutfak dışında da yararlı bileşikler sunar ve artık yetiştirme materyali toprağa ve çevreye yardımcı olmak için biyokömüre dönüştürülebilir <sup>4</sup>.

<Footnotes separator>
  <Footnote :number=1>Britannica Encyclopedia</Footnote>
  <Footnote :number=2>Wikipedia</Footnote>
  <Footnote :number=3>Chun, <i>et al.</i> 10.3390/foods9080980</Footnote>
  <Footnote :number=4>Aiduang, <i>et al.</i> 10.3390/life15020317</Footnote>
</Footnotes>

<!--
- Some mushrooms are food or medicine, others are poisonous; safe identification needs multiple matching features and expert care because deadly look‑alikes exist
- Mushrooms are the fruiting parts of fungi that grow from hidden threads called mycelium; they spread by releasing spores from parts like the cap, stem, and gills or pores <sup>1</sup>.
- To tell species apart, check gill attachment, a cup or ring on the stem, spore print color, cap and stem details, and where it’s growing, noting that these can change as it matures <sup>2</sup>.
- Some mushrooms are food or medicine, others are poisonous; safe identification needs multiple matching features and expert care because deadly look‑alikes exist <sup>1</sup>.
- In cooking, mushrooms add rich umami and earthy flavors; drying boosts stronger bitter and musty notes that chefs use for depth <sup>3</sup>.
- Outside the kitchen, mushrooms offer useful compounds, and leftover growing material can be turned into biochar to help soils and the environment <sup>4</sup>.
 -->

---
layout: fact
---

# The Problem of Identifying Edible Mushroom with AI

Automating the edibility decision is essential because mushroom misidentification can cause __severe illness or death__, and consumer tests show that general __AI/photo ID apps__ still __misclassify dangerous species as edible__ at alarming rates. It is generally not advised to ask a generic AI directly whether a mushroom is edible; instead, __a constrained expert system__ with carefully crafted, auditable rules aligned with mycological best practice can gate decisions and __default to “not edible”__ when required features are missing or uncertain. <sup>5</sup>

<Footnotes separator>
  <Footnote :number=5>Claypool, Public Citizen</Footnote>
</Footnotes>

---

# Kural Tabanı Uzman Sistem

- A rule-based expert system is software that __makes decisions__ by checking __IF‑THEN rules__ written by __domain experts__, like “IF gills are free AND a volva is present THEN flag as high risk.”
- It has two main parts: <span v-mark.red="1">__a knowledge base (the rules and facts)__</span> and an __inference engine__ (the part that picks which rules apply and combines their conclusions).
- It’s __easy to audit and explain__ because every conclusion points back to the exact rules and inputs used, improving transparency and trust.
- Limitations include the effort to capture and maintain many rules, handling edge cases and uncertainty, and possible brittleness if inputs are noisy or incomplete.

---
layout: two-cols
layoutClass: gap-16
---

# Mantar Veri Seti

"This data set includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms in the Agaricus and Lepiota Family (pp. 500-525).  Each species is identified as definitely edible, definitely poisonous, or of unknown edibility and not recommended.  This latter class was combined with the poisonous one." <sup>6</sup>

<Footnotes separator>
  <Footnote :number=6>
"Mushroom," UCI Machine Learning Repository, 1981. [Online]. Available: https://doi.org/10.24432/C5959T</Footnote>
</Footnotes>

::right::

|class|cap-shape|cap-color|bruises|odor| ... |
|-----|---------|---------|-------|----|-----|
|p    |x        |n        |t      |p   | ... |
|e    |x        |y        |t      |a   | ... |
|e    |b        |w        |t      |l   | ... |

<!-- Currently i dont have the rules defined by domain experts.
However, i have the data and i can infer the rules from the data by using
PRISM algorithm -->

---
layout: image-right
image: ./images/prism_paper.png
backgroundSize: contain
---

# PRISM Algorithm

PRISM is a rules-induction system first proposed by Cendrowska <sup>7</sup>.

PRISM supports generating rules both to describe patterns within a table (in the form of associations between the features) and as a predictive model.

The rules produced are in disjunctive normal form (an OR of ANDs), with each individual rule being the AND of one or more terms, with each term of the form Feature = Value, for some Value within the values for that Feature.

<Footnotes separator>
  <Footnote :number=7>Cendrowska (1987), 10.1016/S0020-7373(87)80003-2</Footnote>
</Footnotes>

---

# PRISM Example

With PRISM here is the example rules inferred from the dataset:


<<< @/snippets/rules.txt {*}{maxHeight:'300px'}

---

# CLIPS

- CLIPS is an expert system tool originally developed by the Software Technology Branch (STB), NASA/Lyndon B. Johnson Space Center. S
- CLIPS is a rule-based language that uses a simple, fully parenthesized syntax to define data and rules, then matches incoming facts to fire actions.
- There are three ways to represent knowledge in CLIPS:
  - _Rules_, which are primarily intended for heuristic knowledge based on experience.
  - _Deffunctions_ and generic functions, which are primarily intended for procedural knowledge.
  - _Object-oriented programming_, also primarily intended for procedural knowledge.
- Everything is a construct written in parentheses; common constructs include templates for data and rules for logic, and comments start with a semicolon at the line level or as an optional quoted string inside constructs.

---
layout: two-cols
level: 2
---

# CLIPS Syntax


- `deftemplate` defines a data schema (like a record) with named slots; facts then instantiate these templates, e.g., `(case (id 1) (odor f))` matches a template with slots id and odor.
- `defrule` defines production rules with a Left-Hand Side (patterns to match) and a Right-Hand Side after => (actions to perform), and rules are named and may include an optional quoted comment.

::right::

````md magic-move {lines: true}
```Clips {*|1|2,8|19-22|*}
(deftemplate case
  (slot id)
  (slot cap_color)
  (slot cap_shape)
  (slot gill_color)
  (slot gill_spacing)
  (slot habitat)
  (slot odor)
  (slot population)
  (slot ring_number)
  (slot ring_type)
  (slot spore_print_color)
  (slot stalk_color_above_ring)
  (slot stalk_color_below_ring)
  (slot stalk_root)
  (slot stalk_shape)
)

(deftemplate conclusion
  (slot id)
  (slot target)
  (slot rule))
```

```Clips {*|1,3-5|7-11|*}
(defrule poisonous_odor_f
  "Poisonous: odor=f"
  (case (id ?case-id)
        (odor f)
  )
  =>
  (assert (conclusion
    (id ?case-id)
    (target "poisonous")
    (rule poisonous_odor_f)
  )))
```
````

---
layout: two-cols
layoutClass: gap-16
---

# CLIPS Syntax

- The LHS contains pattern-matching expressions against facts; variables start with `?`, e.g., `?case-id` binds a value from a matched fact for reuse on the RHS.
- The RHS executes functions when the LHS matches; common actions include assert to add new facts, retract to remove facts, and printout for output, enabling forward-chaining inference.
- Strings are in double quotes, data types include integers, floats, symbols, strings, and external addresses; parentheses and balanced structure are mandatory for valid code.

::right::

`rules.CLP`

<<< @/../rules.CLP Clips {*}{maxHeight: '400px'}

---

# Building Web Application

- For building web application we use Python
- We can bind the CLIPS inference engine to Python with `clipspy`

```python {*|1-3|4|6-10|12|14-17|*}
import clips

env = clips.Environment()
env.load('rules.CLP')  # (load 'rules.CLP')

fact_string = """
(case (id 1) (odor f))
"""

env.assert_string(fact_string)  # (assert (case (id 1) (odor f)))

env.run()  # (run)

for fact in env.facts():  # (facts)
    if fact.template.name == "conclusion":
        print(fact)  # f-2     (conclusion (id 1) (target "poisonous") (rule poisonous_odor_f))
        print(fact['target'])  # "poisonous"
```

---
level: 2
layout: iframe-right
url: http://localhost:3000/
---

# Building Web Application

- We use Reflex library to build both backend and frontend of the website entirely in python
- We integrated AI to infer the visual attributes automatically. Optional to use.
- [To the website](http://localhost:3000/)

---
layout: center
class: text-center
---

# Thank You
