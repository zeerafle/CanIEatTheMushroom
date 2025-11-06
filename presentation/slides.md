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

# Yenilebilir Mantar Uzman Sistemi

---
layout: figure-side
figureUrl: ./images/mushroom_morphology.jpg
figureCaption: Mantar morfolojisi
figureFootnoteNumber: 3
---

# Mantar

- Mantarlar, toprağın altında gizlice yayılan “misel” adlı ince ipliklerden büyür; yer üstünde gördüğümüz şapka ve sap, sporlarını saçıp çoğalmayı sağlayan meyve kısmıdır <sup>1</sup>.
- Bir mantarı tanımak için şunlara bakın: solungaçları/gözenekleri nasıl, volva veya sapta halka var mı, spor izi hangi renk, şapka ve sapın rengi/biçimi nasıl ve nerede büyüyor; bunların olgunlaştıkça değişebileceğini unutmayın <sup>2</sup>.

<Footnotes separator>
  <Footnote :number=1>Britannica Encyclopedia</Footnote>
  <Footnote :number=2>Wikipedia</Footnote>
  <Footnote :number=3>Gupta (2022)</Footnote>
</Footnotes>

<!--
- Mushrooms are the fruiting parts of fungi that grow from hidden threads called mycelium; they spread by releasing spores from parts like the cap, stem, and gills or pores <sup>1</sup>.
  - Toprağın altında yayılıyor
- To tell species apart, check gill attachment, a cup or ring on the stem, spore print color, cap and stem details, and where it’s growing, noting that these can change as it matures <sup>2</sup>.

Here are concise Turkish equivalents for the labeled parts in your diagram.

- cap → şapka
- gills → solungaç
- ring → yüzük
- volva → volva
- scale/scales → pullar
- tubes → tüpler
- pores → gözenekler
- stipe, stalk → sap
-->

---

# Mantar

- Kimi mantarlar yenir ya da ilaç olur, kimileri zehirlidir; ölümcül benzerler olduğu için güvenli tanıma, birden fazla belirtiyi aynı anda doğrulamayı ve uzman görüşünü gerektirir <sup>1</sup>.
- Mantarlar yemeğe güçlü umami ve topraksı tat katar; kurutunca tat daha yoğunlaşır ve bazı acımsı/küflü notalar belirginleşir <sup>3</sup>.
- Mantarlar mutfak dışında da işe yarayan bileşikler içerir; artık yetiştirme malzemesi biyokömüre çevrilerek toprağa ve çevreye fayda sağlayabilir <sup>4</sup>.

<Footnotes separator>
  <Footnote :number=1>Britannica Encyclopedia</Footnote>
  <Footnote :number=3>Chun, <i>et al.</i> (2020)</Footnote>
  <Footnote :number=4>Aiduang, <i>et al.</i> (2025)</Footnote>
</Footnotes>

<!--
- Some mushrooms are food or medicine, others are poisonous; safe identification needs multiple matching features and expert care because deadly look‑alikes exist <sup>1</sup>.
- In cooking, mushrooms add rich umami and earthy flavors; drying boosts stronger bitter and musty notes that chefs use for depth <sup>3</sup>.
- Outside the kitchen, mushrooms offer useful compounds, and leftover growing material can be turned into biochar to help soils and the environment <sup>4</sup>.
-->

---
layout: fact
---

# YZ ile Yenilebilir Mantar Tespiti Problemi

yenilebilirlik kararının otomatikleştirilmesi kritiktir; çünkü mantarın yanlış tanımlanması __şiddetli hastalık veya ölüme__ yol açabilir ve tüketici testleri, genel amaçlı __Yapay Zeka (YZ)/fotoğraflı tanımlama uygulamalarının__ tehlikeli türleri hâlâ __yenilebilir olarak yanlış sınıflandırdığını__ göstermektedir. Genel olarak, bir mantarın yenilebilir olup olmadığını doğrudan genel bir YZ'ye sormak önerilmez; bunun yerine, mikolojik en iyi uygulamalarla uyumlu, dikkatle hazırlanmış ve denetlenebilir kurallara sahip __kısıtlanmış bir uzman sistem__ kararları sınırlandırabilir ve gerekli özellikler eksik veya belirsiz olduğunda __varsayılan olarak “yenilebilir değil”__ sonucunu verebilir. <sup>5</sup>

<Footnotes separator>
  <Footnote :number=5>Claypool (2024)</Footnote>
</Footnotes>

<!--
Automating the edibility decision is essential because mushroom misidentification can cause __severe illness or death__, and consumer tests show that general __AI/photo ID apps__ still __misclassify dangerous species as edible__ at alarming rates. It is generally not advised to ask a generic YZ directly whether a mushroom is edible; instead, __a constrained expert system__ with carefully crafted, auditable rules aligned with mycological best practice can gate decisions and __default to “not edible”__ when required features are missing or uncertain. <sup>5</sup>
-->

---

# Kural Tabanı Uzman Sistem

- Kural tabanlı bir uzman sistem, __alan uzmanları__ tarafından yazılmış __IF‑THEN kurallarını__ kontrol ederek __karar veren__ bir yazılımdır; örneğin “IF gills are free AND a volva is present THEN flag as high risk.”
- İki ana bölümden oluşur: <span v-mark.red="1">__bilgi tabanı (kurallar ve gerçekler)__</span> ve __çıkarım motoru__ (hangi kuralların uygulanacağını seçip sonuçları birleştiren kısım).
- Her sonucun kullanılan kurallara ve girdilere geri izlenebilmesi sayesinde __denetlemek ve açıklamak kolaydır__, bu da şeffaflık ve güveni artırır.
- Sınırlamalar arasında çok sayıda kuralı yakalama ve sürdürme çabası, uç durumları ve belirsizliği ele alma ve girdiler gürültülü veya eksik olduğunda olası kırılganlık sayılabilir.

<!--
- A rule-based expert system is software that __makes decisions__ by checking __IF‑THEN rules__ written by __domain experts__, like “IF gills are free AND a volva is present THEN flag as high risk.”
- It has two main parts: <span v-mark.red="1">__a knowledge base (the rules and facts)__</span> and an __inference engine__ (the part that picks which rules apply and combines their conclusions).
- It’s __easy to audit and explain__ because every conclusion points back to the exact rules and inputs used, improving transparency and trust.
- Limitations include the effort to capture and maintain many rules, handling edge cases and uncertainty, and possible brittleness if inputs are noisy or incomplete.
-->

---
layout: two-cols
layoutClass: gap-16
---

# Mantar Veri Seti

"Bu veri kümesi, Agaricus ve Lepiota familyalarındaki 23 solungaçlı mantar türüne karşılık gelen varsayımsal örneklerin açıklamalarını içerir (s. 500–525). Her tür kesinlikle yenilebilir, kesinlikle zehirli veya yenilebilirliği bilinmeyen ve önerilmeyen olarak tanımlanmıştır. Bu son sınıf, zehirli olanla birleştirilmiştir." <sup>6</sup>

<Footnotes separator>
  <Footnote :number=6>"Mushroom," UCI Machine Learning Repository, 1981 </Footnote>
</Footnotes>

::right::

|class|cap-shape|cap-color|bruises|odor| ... |
|-----|---------|---------|-------|----|-----|
|p    |x        |n        |t      |p   | ... |
|e    |x        |y        |t      |a   | ... |
|e    |b        |w        |t      |l   | ... |

<!-- Currently i dont have the rules defined by domain experts.
However, i have the data and i can infer the rules from the data by using
PRISM algorithm

"This data set includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms in the Agaricus and Lepiota Family (pp. 500-525).  Each species is identified as definitely edible, definitely poisonous, or of unknown edibility and not recommended.  This latter class was combined with the poisonous one." <sup>6</sup>
-->

---
layout: image-right
image: ./images/prism_paper.png
backgroundSize: contain
---

# PRISM Algoritması

PRISM, ilk olarak Cendrowska tarafından önerilen bir kural indüksiyon sistemidir <sup>7</sup>.

PRISM, bir tabloda (özellikler arasındaki ilişkiler biçiminde) örüntüleri tanımlamak ve bir öngörücü model olarak kullanılmak üzere kurallar üretmeyi destekler.

Üretilen kurallar ayrık normal formdadır (AND’lerin OR’u); her bir kural bir veya daha fazla terimin AND’i şeklindedir ve her terim Feature = Value biçimindedir; Value, ilgili özelliğin değerlerinden biridir.

<Footnotes separator>
  <Footnote :number=7>Cendrowska (1987)</Footnote>
</Footnotes>

<!--
PRISM is a rules-induction system first proposed by Cendrowska <sup>7</sup>.

PRISM supports generating rules both to describe patterns within a table (in the form of associations between the features) and as a predictive model.

The rules produced are in disjunctive normal form (an OR of ANDs), with each individual rule being the AND of one or more terms, with each term of the form Feature = Value, for some Value within the values for that Feature.
-->

---

# PRISM Örneği

PRISM ile veri kümesinden çıkarılan örnek kurallar aşağıdadır:

<<< @/snippets/rules.txt {*}{maxHeight:'300px'}

<!--
With PRISM here is the example rules inferred from the dataset:
-->

---

# CLIPS

- CLIPS, aslen NASA/Lyndon B. Johnson Uzay Merkezi'nin Yazılım Teknolojisi Birimi (STB) tarafından geliştirilen bir uzman sistem aracıdır.
- CLIPS, verileri ve kuralları tanımlamak için basit, tamamen parantezli bir sözdizimi kullanan ve gelen gerçekleri eşleştirip eylemleri tetikleyen kural tabanlı bir dildir.
- CLIPS'te bilgiyi temsil etmenin üç yolu vardır:
  - _Kurallar_, ağırlıklı olarak deneyime dayalı sezgisel bilgi için kullanılır.
  - _Deffunctions_ ve genel (generic) fonksiyonlar, ağırlıklı olarak işlemsel bilgi için kullanılır.
  - _Nesne yönelimli programlama_ da ağırlıklı olarak işlemsel bilgi için kullanılır.
- Her şey parantezler içinde yazılan bir 'construct'tur; yaygın yapılar veri için şablonlar ve mantık için kuralları içerir; satır düzeyinde noktalı virgül ile başlayan veya construct içinde isteğe bağlı tırnaklı dizeler olarak yer alan yorumlar bulunur.

<!--
- CLIPS is an expert system tool originally developed by the Software Technology Branch (STB), NASA/Lyndon B. Johnson Space Center. S
- CLIPS is a rule-based language that uses a simple, fully parenthesized syntax to define data and rules, then matches incoming facts to fire actions.
- There are three ways to represent knowledge in CLIPS:
  - _Rules_, which are primarily intended for heuristic knowledge based on experience.
  - _Deffunctions_ and generic functions, which are primarily intended for procedural knowledge.
  - _Object-oriented programming_, also primarily intended for procedural knowledge.
- Everything is a construct written in parentheses; common constructs include templates for data and rules for logic, and comments start with a semicolon at the line level or as an optional quoted string inside constructs.
-->

---
layout: two-cols
level: 2
---

# CLIPS Söz Dizimi


- `deftemplate`, adlandırılmış slot'lara sahip bir veri şemasını (kayıt gibi) tanımlar; gerçekler bu şablonları örnekler, örneğin `(case (id 1) (odor f))`, id ve odor slot'larına sahip bir şablonu eşleştirir.
- Gerçekler (Facts): çalışma belleğindeki bilgi parçaları. Şablon örnekleri.
- `defrule`, Sol Taraf (LHS: eşleşecek kalıplar) ve `=>` sonrasında Sağ Taraf (RHS: yapılacak eylemler) ile üretim kurallarını tanımlar; kuralların isimleri vardır ve isteğe bağlı tırnaklı bir yorum içerebilirler.

::right::

````md magic-move {lines: true}
```Clips {*|1|2,8|19-24|*}
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

(assert
  (case
    (id 1)
    (odor f)
  )
)
```

```Clips {*|1-4|6-10|12-16|*}
(deftemplate conclusion
  (slot id)
  (slot target)
  (slot rule))

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

<!--
- `deftemplate` defines a data schema (like a record) with named slots; facts then instantiate these templates, e.g., `(case (id 1) (odor f))` matches a template with slots id and odor.
- `defrule` defines production rules with a Left-Hand Side (patterns to match) and a Right-Hand Side after => (actions to perform), and rules are named and may include an optional quoted comment.
-->

---
layout: two-cols
layoutClass: gap-16
---

# CLIPS Söz Dizimi

- LHS (sol taraf) gerçeklere karşı kalıp eşleme ifadelerini içerir; değişkenler `?` ile başlar, örneğin `?case-id` eşleşen bir gerçekden bir değeri bağlar ve RHS'de yeniden kullanılır.
- RHS (sağ taraf), LHS eşleştiğinde fonksiyonları yürütür; yaygın eylemler arasında yeni gerçekler eklemek için `assert`, gerçekleri kaldırmak için `retract` ve çıktı için `printout` bulunur; bu da ileri zincirlemeyi etkinleştirir.
- Dizeler çift tırnak içindedir; veri türleri arasında tamsayılar, kayan sayılar, semboller, dizeler ve dış adresler bulunur; geçerli kod için parantezler ve dengeli yapı zorunludur.

::right::

`rules.CLP`

<<< @/../rules.CLP Clips {*}{maxHeight: '400px'}


<style>
ul {
  font-size: 15px
}
</style>
<!--
- The LHS contains pattern-matching expressions against facts; variables start with `?`, e.g., `?case-id` binds a value from a matched fact for reuse on the RHS.
- The RHS executes functions when the LHS matches; common actions include assert to add new facts, retract to remove facts, and printout for output, enabling forward-chaining inference.
- Strings are in double quotes, data types include integers, floats, symbols, strings, and external addresses; parentheses and balanced structure are mandatory for valid code.
-->

---

# Clips Söz Dizimi

```Clips {1|2|3|5|7-8|10-11|11}
(load "rules.CLP")
(reset)
(assert (case (id 1) (odor f)))

; <Fact-1>

(run)
(facts)

; f-1 (case (id 1) (cap_color nil) (cap_shape nil) (gill_color nil) (gill_spacing nil) (habitat nil) (odor f) (population nil) (ring_number nil) (ring_type nil) (spore_print_color nil) (stalk_color_above_ring nil) (stalk_color_below_ring nil) (stalk_root nil) (stalk_shape nil))
; f-2 (conclusion (id 1) (target "poisonous") (rule poisonous_odor_f)) Toplam 2 bilgi için.
```

---

# Web Uygulaması Geliştirme

- Web uygulamasını geliştirmek için Python kullanıyoruz.
- CLIPS çıkarım motorunu Python’a `clipspy` ile bağlayabiliriz.

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

<!--
- For building web application we use Python
- We can bind the CLIPS inference engine to Python with `clipspy`
-->

---
level: 2
layout: iframe-right
url: http://localhost:3000/
---

# Web Uygulaması Geliştirme

- Siteyi tamamen Python ile —hem backend hem de frontend— Reflex kütüphanesiyle geliştiriyoruz.
- Görsel öznitelikleri otomatik olarak çıkarmak için YZ entegre ettik. Kullanımı isteğe bağlıdır.
- [Web sitesine git](http://localhost:3000/)

<!--
- We use Reflex library to build both backend and frontend of the website entirely in python
- We integrated YZ to infer the visual attributes automatically. Optional to use.
- [To the website](http://localhost:3000/)
-->

---
layout: index
indexEntries:
  - { title: "The Editors of Encyclopaedia Britannica. (2025, Kasım 3). Mushroom | Definition, Characteristics, Species, & Facts. https://www.britannica.com/science/mushroom", uri: "https://www.britannica.com/science/mushroom" }
  - { title: "Mushroom. (2025). Içinde En.wikipedia.org/. https://en.wikipedia.org/w/index.php?title=Mushroom&oldid=1319179626", uri: "https://en.wikipedia.org/w/index.php?title=Mushroom&oldid=1319179626" }
  - { title: "Gupta, A. (2022). Classification Of Mushroom Using Artificial Neural Network. https://doi.org/10.1101/2022.08.31.505980", uri: "https://doi.org/10.1101/2022.08.31.505980"}
  - { title: "Chun, S., Chambers, E., & Han, I. (2020). Development of a Sensory Flavor Lexicon for Mushrooms and Subsequent Characterization of Fresh and Dried Mushrooms. Foods, 9(8), 980. https://doi.org/10.3390/foods9080980", uri: "https://www.mdpi.com/2304-8158/9/8/980" }
  - { title: "Aiduang, W., Jatuwong, K., Kiatsiriroat, T., Kamopas, W., Tiyayon, P., Jawana, R., Xayyavong, O., & Lumyong, S. (2025). Spent Mushroom Substrate-Derived Biochar and Its Applications in Modern Agricultural Systems: An Extensive Overview. Life, 15(2), 317. https://doi.org/10.3390/life15020317", uri: "https://www.mdpi.com/2075-1729/15/2/317" }
  - { title: "Claypool, R. (2024, Mart 18). A.I. Foraging Tools Generate Mushroom Misinformation. Public Citizen. https://www.citizen.org/article/mushroom-risk-ai-app-misinformation/", uri: "https://www.citizen.org/article/mushroom-risk-ai-app-misinformation/" }
  - { title: "Mushroom. (1981). [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5959T", uri: "https://archive.ics.uci.edu/dataset/73"}
  - { title: "Cendrowska, J. (1987). PRISM: An algorithm for inducing modular rules. International Journal of Man-Machine Studies, 27(4), 349-370. https://doi.org/10.1016/S0020-7373(87)80003-2", uri: "https://linkinghub.elsevier.com/retrieve/pii/S0020737387800032"}
indexRedirectType: external
---

# Referans

<style>
ol {
  font-size: 10px
}
</style>

---
layout: center
class: text-center
---

# Dinlediğiniz İçin Teşekkür Ederim
