; case template
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

; conclusion template
(deftemplate conclusion
  (slot id)
  (slot target)
  (slot rule))

; --------------------------
; Poisonous rules
; --------------------------

(defrule poisonous_odor_f
  "Poisonous: odor=f"
  (case (id ?case-id)
        (odor f)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_odor_f))))

(defrule poisonous_gill_color_b
  "Poisonous: gill_color=b"
  (case (id ?case-id)
        (gill_color b)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_gill_color_b))))

(defrule poisonous_odor_p
  "Poisonous: odor=p"
  (case (id ?case-id)
        (odor p)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_odor_p))))

(defrule poisonous_odor_c
  "Poisonous: odor=c"
  (case (id ?case-id)
        (odor c)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_odor_c))))

(defrule poisonous_spore_print_color_r
  "Poisonous: spore_print_color=r"
  (case (id ?case-id)
        (spore_print_color r)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_spore_print_color_r))))

(defrule poisonous_odor_m
  "Poisonous: odor=m"
  (case (id ?case-id)
        (odor m)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_odor_m))))

(defrule poisonous_stalk_color_below_ring_y
  "Poisonous: stalk_color_below_ring=y"
  (case (id ?case-id)
        (stalk_color_below_ring y)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_stalk_color_below_ring_y))))

(defrule poisonous_stalk_color_below_ring_n_stalk_root_MISSING
  "Poisonous: stalk_color_below_ring=n AND stalk_root=MISSING"
  (case (id ?case-id)
        (stalk_color_below_ring n)
        (stalk_root MISSING)
  )
  =>
  (assert (conclusion (id ?case-id) (target "poisonous") (rule poisonous_stalk_color_below_ring_n_stalk_root_MISSING))))

; --------------------------
; Edible rules
; --------------------------

(defrule edible_stalk_color_above_ring_g
  "Edible: stalk_color_above_ring=g"
  (case (id ?case-id)
        (stalk_color_above_ring g)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_stalk_color_above_ring_g))))

(defrule edible_odor_a
  "Edible: odor=a"
  (case (id ?case-id)
        (odor a)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_odor_a))))

(defrule edible_odor_l
  "Edible: odor=l"
  (case (id ?case-id)
        (odor l)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_odor_l))))

(defrule edible_stalk_color_below_ring_g
  "Edible: stalk_color_below_ring=g"
  (case (id ?case-id)
        (stalk_color_below_ring g)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_stalk_color_below_ring_g))))

(defrule edible_population_a
  "Edible: population=a"
  (case (id ?case-id)
        (population a)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_population_a))))

(defrule edible_stalk_color_above_ring_o
  "Edible: stalk_color_above_ring=o"
  (case (id ?case-id)
        (stalk_color_above_ring o)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_stalk_color_above_ring_o))))

(defrule edible_habitat_w
  "Edible: habitat=w"
  (case (id ?case-id)
        (habitat w)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_habitat_w))))

(defrule edible_population_n
  "Edible: population=n"
  (case (id ?case-id)
        (population n)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_population_n))))

(defrule edible_ring_type_f
  "Edible: ring_type=f"
  (case (id ?case-id)
        (ring_type f)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_ring_type_f))))

(defrule edible_cap_shape_s
  "Edible: cap_shape=s"
  (case (id ?case-id)
        (cap_shape s)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_cap_shape_s))))

(defrule edible_odor_n_stalk_shape_t
  "Edible: odor=n AND stalk_shape=t"
  (case (id ?case-id)
        (odor n)
        (stalk_shape t)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_odor_n_stalk_shape_t))))

(defrule edible_ring_number_t_spore_print_color_w
  "Edible: ring_number=t AND spore_print_color=w"
  (case (id ?case-id)
        (ring_number t)
        (spore_print_color w)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_ring_number_t_spore_print_color_w))))

(defrule edible_cap_color_c_odor_n
  "Edible: cap_color=c AND odor=n"
  (case (id ?case-id)
        (cap_color c)
        (odor n)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_cap_color_c_odor_n))))

(defrule edible_odor_n_stalk_root_e
  "Edible: odor=n AND stalk_root=e"
  (case (id ?case-id)
        (odor n)
        (stalk_root e)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_odor_n_stalk_root_e))))

(defrule edible_gill_spacing_w_cap_color_n
  "Edible: gill_spacing=w AND cap_color=n"
  (case (id ?case-id)
        (gill_spacing w)
        (cap_color n)
  )
  =>
  (assert (conclusion (id ?case-id) (target "edible") (rule edible_gill_spacing_w_cap_color_n))))
