import KUOS.DependentOriginationStageIIGeometricOrientationV4_46
import Mathlib

namespace KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47

open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
open KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45
open KUOS.DependentOriginationStageIIGeometricOrientationV4_46

set_option autoImplicit false

noncomputable section

/-!
# Free middle-switch orbit quotient on the Stage-II geometric carrier v4.47

v4.45 proves that the descended middle-switch is a fixed-point-free
self-homeomorphism of the bare geometric Cantor carrier.  v4.46 transports the
finite-depth orientation semantics through that homeomorphism.

The present unit forms the corresponding orbit quotient.

Two geometric points are related exactly when the second is either the first
point itself or its middle-switch mate:

  q ~ p  <->  q = p or q = M p.

Because M is involutive, this is an equivalence relation.  Because M has no
fixed points, every equivalence class has exactly the two distinct
representatives

  {p, M p}.

We then form the Lean Quotient, prove exact equality classification of quotient
classes, and prove the universal factorization property for arbitrary
middle-switch-invariant semantics.

No quotient topology is asserted in this unit.  The result is the exact
set-theoretic orbit carrier of the already-validated free geometric
involution.
-/

/-- Orbit relatedness for the free geometric middle-switch. -/
def StageIIGeometricMiddleSwitchRelated
    (p q : StageIIGeometricCantorCarrier) : Prop :=
  q = p ∨ q = stageIIGeometricCarrierMiddleSwitch p

/-- Reflexivity of geometric middle-switch relatedness. -/
theorem stageIIGeometricMiddleSwitchRelated_refl
    (p : StageIIGeometricCantorCarrier) :
    StageIIGeometricMiddleSwitchRelated p p := by
  exact Or.inl rfl

/-- Symmetry of geometric middle-switch relatedness follows from involutivity. -/
theorem stageIIGeometricMiddleSwitchRelated_symm
    {p q : StageIIGeometricCantorCarrier}
    (hpq : StageIIGeometricMiddleSwitchRelated p q) :
    StageIIGeometricMiddleSwitchRelated q p := by
  rcases hpq with hpq | hpq
  · exact Or.inl hpq.symm
  · refine Or.inr ?_
    calc
      p =
          stageIIGeometricCarrierMiddleSwitch
            (stageIIGeometricCarrierMiddleSwitch p) :=
        (stageIIGeometricCarrierMiddleSwitch_involutive p).symm
      _ =
          stageIIGeometricCarrierMiddleSwitch q := by
        exact
          congrArg stageIIGeometricCarrierMiddleSwitch hpq.symm

/-- Transitivity of geometric middle-switch relatedness uses M^2 = id. -/
theorem stageIIGeometricMiddleSwitchRelated_trans
    {p q r : StageIIGeometricCantorCarrier}
    (hpq : StageIIGeometricMiddleSwitchRelated p q)
    (hqr : StageIIGeometricMiddleSwitchRelated q r) :
    StageIIGeometricMiddleSwitchRelated p r := by
  rcases hpq with hpq | hpq
  · cases hpq
    exact hqr
  · rcases hqr with hqr | hqr
    · exact Or.inr (hqr.trans hpq)
    · refine Or.inl ?_
      calc
        r = stageIIGeometricCarrierMiddleSwitch q := hqr
        _ =
            stageIIGeometricCarrierMiddleSwitch
              (stageIIGeometricCarrierMiddleSwitch p) := by
          exact congrArg stageIIGeometricCarrierMiddleSwitch hpq
        _ = p :=
          stageIIGeometricCarrierMiddleSwitch_involutive p

/-- The free middle-switch orbit equivalence relation. -/
def stageIIGeometricMiddleSwitchSetoid :
    Setoid StageIIGeometricCantorCarrier where
  r := StageIIGeometricMiddleSwitchRelated
  iseqv := by
    constructor
    · exact stageIIGeometricMiddleSwitchRelated_refl
    · intro p q hpq
      exact stageIIGeometricMiddleSwitchRelated_symm hpq
    · intro p q r hpq hqr
      exact stageIIGeometricMiddleSwitchRelated_trans hpq hqr

/-- Set-theoretic orbit carrier of the free Stage-II geometric middle-switch. -/
def StageIIGeometricMiddleSwitchOrbit : Type :=
  Quotient stageIIGeometricMiddleSwitchSetoid

/-- Canonical projection to the middle-switch orbit carrier. -/
def stageIIGeometricMiddleSwitchOrbitProjection
    (p : StageIIGeometricCantorCarrier) :
    StageIIGeometricMiddleSwitchOrbit :=
  Quotient.mk stageIIGeometricMiddleSwitchSetoid p

/-- A point and its middle-switch mate have exactly the same orbit class. -/
@[simp] theorem stageIIGeometricMiddleSwitchOrbitProjection_mate
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricMiddleSwitchOrbitProjection p =
      stageIIGeometricMiddleSwitchOrbitProjection
        (stageIIGeometricCarrierMiddleSwitch p) := by
  apply Quotient.sound
  exact Or.inr rfl

/-- Equality in the orbit quotient is exactly the two-representative relation. -/
theorem stageIIGeometricMiddleSwitchOrbitProjection_eq_iff
    (p q : StageIIGeometricCantorCarrier) :
    stageIIGeometricMiddleSwitchOrbitProjection p =
        stageIIGeometricMiddleSwitchOrbitProjection q ↔
      q = p ∨ q = stageIIGeometricCarrierMiddleSwitch p := by
  constructor
  · intro h
    change StageIIGeometricMiddleSwitchRelated p q
    exact Quotient.exact h
  · intro h
    apply Quotient.sound
    exact h

/-- The concrete set of representatives of the orbit through p. -/
def stageIIGeometricMiddleSwitchOrbitSet
    (p : StageIIGeometricCantorCarrier) :
    Set StageIIGeometricCantorCarrier :=
  {q |
    stageIIGeometricMiddleSwitchOrbitProjection p =
      stageIIGeometricMiddleSwitchOrbitProjection q}

/-- Membership in the concrete orbit set is exactly p-or-mate. -/
theorem mem_stageIIGeometricMiddleSwitchOrbitSet_iff
    (p q : StageIIGeometricCantorCarrier) :
    q ∈ stageIIGeometricMiddleSwitchOrbitSet p ↔
      q = p ∨ q = stageIIGeometricCarrierMiddleSwitch p := by
  exact stageIIGeometricMiddleSwitchOrbitProjection_eq_iff p q

/-- The orbit set is literally the unordered two-point set {p, M p}. -/
theorem stageIIGeometricMiddleSwitchOrbitSet_eq_pair
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricMiddleSwitchOrbitSet p =
      {p, stageIIGeometricCarrierMiddleSwitch p} := by
  ext q
  rw [mem_stageIIGeometricMiddleSwitchOrbitSet_iff]
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff]

/-- The two displayed orbit representatives are genuinely distinct. -/
theorem stageIIGeometricMiddleSwitchOrbit_pair_distinct
    (p : StageIIGeometricCantorCarrier) :
    p ≠ stageIIGeometricCarrierMiddleSwitch p := by
  exact (stageIIGeometricCarrierMiddleSwitch_ne_self p).symm

/-- Explicit exactly-two representative theorem for every free orbit. -/
theorem stageIIGeometricMiddleSwitchOrbit_exactly_two
    (p : StageIIGeometricCantorCarrier) :
    p ∈ stageIIGeometricMiddleSwitchOrbitSet p ∧
      stageIIGeometricCarrierMiddleSwitch p ∈
        stageIIGeometricMiddleSwitchOrbitSet p ∧
      p ≠ stageIIGeometricCarrierMiddleSwitch p ∧
      ∀ q,
        q ∈ stageIIGeometricMiddleSwitchOrbitSet p →
          q = p ∨ q = stageIIGeometricCarrierMiddleSwitch p := by
  constructor
  · exact
      (mem_stageIIGeometricMiddleSwitchOrbitSet_iff p p).2
        (Or.inl rfl)
  constructor
  · exact
      (mem_stageIIGeometricMiddleSwitchOrbitSet_iff
        p (stageIIGeometricCarrierMiddleSwitch p)).2
        (Or.inr rfl)
  constructor
  · exact stageIIGeometricMiddleSwitchOrbit_pair_distinct p
  · intro q hq
    exact
      (mem_stageIIGeometricMiddleSwitchOrbitSet_iff p q).1 hq

/-- Any middle-switch-invariant semantic map descends canonically to the orbit
quotient. -/
def stageIIGeometricMiddleSwitchDescend
    {Y : Type*}
    (semantic : StageIIGeometricCantorCarrier → Y)
    (hInvariant :
      ∀ p,
        semantic (stageIIGeometricCarrierMiddleSwitch p) =
          semantic p) :
    StageIIGeometricMiddleSwitchOrbit → Y :=
  Quotient.lift semantic (by
    intro p q hpq
    rcases hpq with hpq | hpq
    · rw [hpq]
    · rw [hpq, hInvariant p])

/-- The descended semantic map recovers the original semantic on every
representative. -/
@[simp] theorem stageIIGeometricMiddleSwitchDescend_projection
    {Y : Type*}
    (semantic : StageIIGeometricCantorCarrier → Y)
    (hInvariant :
      ∀ p,
        semantic (stageIIGeometricCarrierMiddleSwitch p) =
          semantic p)
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricMiddleSwitchDescend semantic hInvariant
        (stageIIGeometricMiddleSwitchOrbitProjection p) =
      semantic p := by
  rfl

/-- The descended semantic map is unique among maps agreeing with the original
semantic on all representatives. -/
theorem stageIIGeometricMiddleSwitchDescend_unique
    {Y : Type*}
    (semantic : StageIIGeometricCantorCarrier → Y)
    (hInvariant :
      ∀ p,
        semantic (stageIIGeometricCarrierMiddleSwitch p) =
          semantic p)
    (candidate : StageIIGeometricMiddleSwitchOrbit → Y)
    (hcandidate :
      ∀ p,
        candidate (stageIIGeometricMiddleSwitchOrbitProjection p) =
          semantic p) :
    candidate =
      stageIIGeometricMiddleSwitchDescend semantic hInvariant := by
  funext q
  refine Quotient.inductionOn q ?_
  intro p
  change
    candidate (stageIIGeometricMiddleSwitchOrbitProjection p) =
      stageIIGeometricMiddleSwitchDescend semantic hInvariant
        (stageIIGeometricMiddleSwitchOrbitProjection p)
  rw [hcandidate]
  rfl

/-- Factorization through the orbit quotient is equivalent to middle-switch
invariance. -/
theorem stageIIGeometricMiddleSwitch_factors_through_orbit_iff
    {Y : Type*}
    (semantic : StageIIGeometricCantorCarrier → Y) :
    (∃ orbitSemantic : StageIIGeometricMiddleSwitchOrbit → Y,
        ∀ p,
          orbitSemantic
              (stageIIGeometricMiddleSwitchOrbitProjection p) =
            semantic p) ↔
      (∀ p,
        semantic (stageIIGeometricCarrierMiddleSwitch p) =
          semantic p) := by
  constructor
  · rintro ⟨orbitSemantic, horbit⟩ p
    calc
      semantic (stageIIGeometricCarrierMiddleSwitch p) =
          orbitSemantic
            (stageIIGeometricMiddleSwitchOrbitProjection
              (stageIIGeometricCarrierMiddleSwitch p)) :=
        (horbit (stageIIGeometricCarrierMiddleSwitch p)).symm
      _ =
          orbitSemantic
            (stageIIGeometricMiddleSwitchOrbitProjection p) := by
        rw [← stageIIGeometricMiddleSwitchOrbitProjection_mate p]
      _ = semantic p := horbit p
  · intro hInvariant
    exact
      ⟨stageIIGeometricMiddleSwitchDescend semantic hInvariant,
        by intro p; rfl⟩

/-- Core certificate for the free two-point orbit quotient. -/
structure StageIIGeometricMiddleSwitchOrbitCertificate where
  projectionMate :
    ∀ p,
      stageIIGeometricMiddleSwitchOrbitProjection p =
        stageIIGeometricMiddleSwitchOrbitProjection
          (stageIIGeometricCarrierMiddleSwitch p)
  classExact :
    ∀ p q,
      stageIIGeometricMiddleSwitchOrbitProjection p =
          stageIIGeometricMiddleSwitchOrbitProjection q ↔
        q = p ∨ q = stageIIGeometricCarrierMiddleSwitch p
  mateDistinct :
    ∀ p,
      p ≠ stageIIGeometricCarrierMiddleSwitch p
  orbitSetExact :
    ∀ p,
      stageIIGeometricMiddleSwitchOrbitSet p =
        {p, stageIIGeometricCarrierMiddleSwitch p}

/-- Canonical orbit certificate assembled from the free v4.45 involution. -/
noncomputable def stageIIGeometricMiddleSwitchOrbitCertificate :
    StageIIGeometricMiddleSwitchOrbitCertificate where
  projectionMate :=
    stageIIGeometricMiddleSwitchOrbitProjection_mate
  classExact :=
    stageIIGeometricMiddleSwitchOrbitProjection_eq_iff
  mateDistinct :=
    stageIIGeometricMiddleSwitchOrbit_pair_distinct
  orbitSetExact :=
    stageIIGeometricMiddleSwitchOrbitSet_eq_pair

/-!
## Boundary after v4.47

The free geometric middle-switch now has an exact set-theoretic orbit quotient.

For every bare geometric point p:

  orbit(p) = {p, M p},

and the two displayed representatives are distinct.

Equality of quotient classes has the exact characterization

  [p] = [q]
    <-> q = p or q = M p.

Moreover, a semantic map on the bare geometric carrier factors through the
orbit quotient exactly when it is invariant under the middle-switch, and that
descended map is unique.

Thus the v4.45 free homeomorphism has now acquired its exact quotient-level
universal property without introducing any additional identifications.

No quotient topology is asserted yet.  A subsequent unit may equip this orbit
carrier with the quotient topology and prove the projection is an open
two-sheeted local quotient, or attach the existing transport-independent
Stage-II obstruction to the two-point orbit geometry.
-/

end

end KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47
