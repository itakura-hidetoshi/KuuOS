/- R62 research probe. Appended to the certified R61 replay source.
No imports are added here; the parent source fixes the Lean environment.
These predicates model finite observed dependency sets, not mathematical
nonexistence of proofs or authorization to change a policy. -/
namespace KuuOSR62

universe r62u r62v

def Hits {α : Type r62u} (D A : α → Prop) : Prop :=
  ∃ x, D x ∧ A x

def Eligible {α : Type r62u} (D A : α → Prop) : Prop :=
  ∀ x, D x → ¬ A x

def Residual {α : Type r62u} (D R : α → Prop) : α → Prop :=
  fun x => D x ∧ ¬ R x

def Included {α : Type r62u} (A B : α → Prop) : Prop :=
  ∀ x, A x → B x

def ValidRelease {α : Type r62u} (D L R : α → Prop) : Prop :=
  Included R D ∧ ∀ x, R x → ¬ L x

theorem eligible_iff_not_hits {α : Type r62u} (D A : α → Prop) :
    Eligible D A ↔ ¬ Hits D A := by
  constructor
  · intro h hit
    obtain ⟨x, hd, ha⟩ := hit
    exact h x hd ha
  · intro h x hd ha
    exact h ⟨x, hd, ha⟩

theorem residual_eligible_iff {α : Type r62u} (D R A : α → Prop) :
    Eligible (Residual D R) A ↔ ∀ x, D x → A x → R x := by
  classical
  constructor
  · intro h x hd ha
    by_contra hn
    exact h x ⟨hd, hn⟩ ha
  · intro h x hx ha
    exact hx.2 (h x hx.1 ha)

-- Two-route obstruction basis: one shared dependency or one exclusive
-- dependency from each route. No finite enumeration is assumed here.
theorem two_blocked_iff_basis {α : Type r62u} (D A B : α → Prop) :
    (Hits D A ∧ Hits D B) ↔
      (∃ x, D x ∧ A x ∧ B x) ∨
        (∃ x y, D x ∧ A x ∧ ¬ B x ∧ D y ∧ B y ∧ ¬ A y) := by
  classical
  constructor
  · rintro ⟨⟨x, hdx, hax⟩, ⟨y, hdy, hby⟩⟩
    by_cases hbx : B x
    · exact Or.inl ⟨x, hdx, hax, hbx⟩
    · by_cases hay : A y
      · exact Or.inl ⟨y, hdy, hay, hby⟩
      · exact Or.inr ⟨x, y, hdx, hax, hbx, hdy, hby, hay⟩
  · rintro (⟨x, hd, ha, hb⟩ | ⟨x, y, hdx, hax, _, hdy, hby, _⟩)
    · exact ⟨⟨x, hd, ha⟩, ⟨x, hd, hb⟩⟩
    · exact ⟨⟨x, hdx, hax⟩, ⟨y, hdy, hby⟩⟩

theorem two_recovery_iff_break_basis {α : Type r62u} (D R A B : α → Prop) :
    (Eligible (Residual D R) A ∨ Eligible (Residual D R) B) ↔
      (∀ x, D x → A x → B x → R x) ∧
      (∀ x y, D x → A x → ¬ B x → D y → B y → ¬ A y → R x ∨ R y) := by
  classical
  constructor
  · intro h
    rcases h with hA | hB
    · have ha := (residual_eligible_iff D R A).mp hA
      exact ⟨fun x hd hax _ => ha x hd hax,
        fun x _ hdx hax _ _ _ _ => Or.inl (ha x hdx hax)⟩
    · have hb := (residual_eligible_iff D R B).mp hB
      exact ⟨fun x hd _ hbx => hb x hd hbx,
        fun _ y _ _ _ hdy hby _ => Or.inr (hb y hdy hby)⟩
  · intro h
    by_cases ha : Eligible (Residual D R) A
    · exact Or.inl ha
    · right
      by_contra hb
      have h1 : Hits (Residual D R) A := by
        by_contra nh
        exact ha ((eligible_iff_not_hits (Residual D R) A).mpr nh)
      have h2 : Hits (Residual D R) B := by
        by_contra nh
        exact hb ((eligible_iff_not_hits (Residual D R) B).mpr nh)
      rcases (two_blocked_iff_basis (Residual D R) A B).mp ⟨h1, h2⟩ with
        ⟨x, hd, hax, hbx⟩ | ⟨x, y, hdx, hax, hnb, hdy, hby, hna⟩
      · exact hd.2 (h.1 x hd.1 hax hbx)
      · rcases h.2 x y hdx.1 hax hnb hdy.1 hby hna with hr | hr
        · exact hdx.2 hr
        · exact hdy.2 hr

-- Arbitrary indexed family: the supplied completeness certificate is an
-- explicit premise; no claim is made that the repository has been closed.
theorem family_recovery_iff_break_complete_basis
    {α : Type r62u} {ι : Type r62v}
    (deps : ι → α → Prop) (basis : (α → Prop) → Prop) (D R : α → Prop)
    (hBasis : ∀ U : α → Prop,
      (∀ i, Hits U (deps i)) ↔ ∃ C, basis C ∧ Included C U) :
    (∃ i, Eligible (Residual D R) (deps i)) ↔
      ∀ C, basis C → Included C D → Hits R C := by
  classical
  constructor
  · rintro ⟨i, hi⟩ C hc hcd
    by_contra hn
    have hsub : Included C (Residual D R) := by
      intro x hx
      exact ⟨hcd x hx, fun hr => hn ⟨x, hr, hx⟩⟩
    have hall := (hBasis (Residual D R)).mpr ⟨C, hc, hsub⟩
    exact (eligible_iff_not_hits (Residual D R) (deps i)).mp hi (hall i)
  · intro h
    by_contra hn
    have hall : ∀ i, Hits (Residual D R) (deps i) := by
      intro i
      by_contra nh
      exact hn ⟨i, (eligible_iff_not_hits (Residual D R) (deps i)).mpr nh⟩
    obtain ⟨C, hc, hsub⟩ := (hBasis (Residual D R)).mp hall
    have hcd : Included C D := fun x hx => (hsub x hx).1
    obtain ⟨x, hr, hx⟩ := h C hc hcd
    exact (hsub x hx).2 hr

theorem locked_common_dependency_blocks_recovery
    {α : Type r62u} {ι : Type r62v}
    (deps : ι → α → Prop) (D L R : α → Prop) (x : α)
    (hd : D x) (hl : L x) (hall : ∀ i, deps i x)
    (hv : ValidRelease D L R) :
    ¬ ∃ i, Eligible (Residual D R) (deps i) := by
  intro h
  obtain ⟨i, hi⟩ := h
  exact hi x ⟨hd, fun hr => hv.2 x hr hl⟩ (hall i)

-- An inclusion-minimal, valid recovery release must equal the denied
-- dependencies of at least one restored route, pointwise.
theorem minimal_release_is_route_intersection
    {α : Type r62u} {ι : Type r62v}
    (deps : ι → α → Prop) (D L R : α → Prop)
    (hv : ValidRelease D L R)
    (hrec : ∃ i, Eligible (Residual D R) (deps i))
    (hmin : ∀ S : α → Prop, ValidRelease D L S → Included S R →
      (∃ i, Eligible (Residual D S) (deps i)) → Included R S) :
    ∃ i, ∀ x, R x ↔ D x ∧ deps i x := by
  obtain ⟨i, hi⟩ := hrec
  have hs : Included (fun x => D x ∧ deps i x) R :=
    fun x hx => (residual_eligible_iff D R (deps i)).mp hi x hx.1 hx.2
  have hsv : ValidRelease D L (fun x => D x ∧ deps i x) :=
    ⟨fun _ hx => hx.1, fun x hx => hv.2 x (hs x hx)⟩
  have hsr : ∃ j, Eligible (Residual D (fun x => D x ∧ deps i x)) (deps j) :=
    ⟨i, (residual_eligible_iff D (fun x => D x ∧ deps i x) (deps i)).mpr
      (fun _ hd ha => ⟨hd, ha⟩)⟩
  have hrs := hmin (fun x => D x ∧ deps i x) hsv hs hsr
  exact ⟨i, fun x => ⟨hrs x, hs x⟩⟩

-- Existence of a valid hypothetical release is exactly existence of a
-- route whose denied dependencies do not intersect the locked set.
theorem exists_valid_release_iff_unlocked_route
    {α : Type r62u} {ι : Type r62v}
    (deps : ι → α → Prop) (D L : α → Prop) :
    (∃ R : α → Prop, ValidRelease D L R ∧
      ∃ i, Eligible (Residual D R) (deps i)) ↔
    ∃ i, ∀ x, D x → deps i x → ¬ L x := by
  constructor
  · rintro ⟨R, hv, i, hi⟩
    exact ⟨i, fun x hd ha =>
      hv.2 x ((residual_eligible_iff D R (deps i)).mp hi x hd ha)⟩
  · rintro ⟨i, hi⟩
    refine ⟨fun x => D x ∧ deps i x, ?_, i, ?_⟩
    · exact ⟨fun _ hx => hx.1, fun x hx => hi x hx.1 hx.2⟩
    · exact (residual_eligible_iff D (fun x => D x ∧ deps i x) (deps i)).mpr
        (fun _ hd ha => ⟨hd, ha⟩)

-- Converse minimality: a route intersection minimal among all unlocked
-- route intersections is inclusion-minimal among valid recovery releases.
theorem minimal_route_intersection_is_minimal_release
    {α : Type r62u} {ι : Type r62v}
    (deps : ι → α → Prop) (D L : α → Prop) (i : ι)
    (hu : ∀ x, D x → deps i x → ¬ L x)
    (hm : ∀ j, (∀ x, D x → deps j x → ¬ L x) →
      Included (fun x => D x ∧ deps j x) (fun x => D x ∧ deps i x) →
      Included (fun x => D x ∧ deps i x) (fun x => D x ∧ deps j x)) :
    ValidRelease D L (fun x => D x ∧ deps i x) ∧
      (∃ j, Eligible (Residual D (fun x => D x ∧ deps i x)) (deps j)) ∧
      (∀ S : α → Prop, ValidRelease D L S →
        Included S (fun x => D x ∧ deps i x) →
        (∃ j, Eligible (Residual D S) (deps j)) →
        Included (fun x => D x ∧ deps i x) S) := by
  refine ⟨⟨fun _ hx => hx.1, fun x hx => hu x hx.1 hx.2⟩, ?_, ?_⟩
  · exact ⟨i, (residual_eligible_iff D (fun x => D x ∧ deps i x) (deps i)).mpr
      (fun _ hd ha => ⟨hd, ha⟩)⟩
  · intro S hsv hsi hrec
    obtain ⟨j, hj⟩ := hrec
    have hjs : Included (fun x => D x ∧ deps j x) S :=
      fun x hx => (residual_eligible_iff D S (deps j)).mp hj x hx.1 hx.2
    have hju : ∀ x, D x → deps j x → ¬ L x :=
      fun x hd ha => hsv.2 x (hjs x ⟨hd, ha⟩)
    have hji : Included (fun x => D x ∧ deps j x) (fun x => D x ∧ deps i x) :=
      fun x hx => hsi x (hjs x hx)
    have hij := hm j hju hji
    exact fun x hx => hjs x (hij x hx)

end KuuOSR62
