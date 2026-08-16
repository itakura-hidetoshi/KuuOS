import Mathlib
import KUOS.GaugeInvariantDependentOriginationOrbitQuotientV0_1

namespace KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1

open Set Topology
open KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1
open KUOS.GaugeInvariantDependentOriginationOrbitQuotientV0_1

universe u v w z

variable {X : Type u} {Y : Type v} {Gauge : Type w}
variable {Local : ℕ → Type z}

/-- A morphism in the action groupoid from `x` to `y` is an actual gauge
transformation carrying `x` to `y`.  Unlike the coarse orbit quotient, this
retains which gauge transformation witnesses the relation. -/
def ActionArrow [Group Gauge] [MulAction Gauge X] (x y : X) : Type w :=
  {g : Gauge // g • x = y}

namespace ActionArrow

/-- Identity arrow at every representative. -/
def id [Group Gauge] [MulAction Gauge X] (x : X) :
    ActionArrow (Gauge := Gauge) x x :=
  ⟨1, by simp⟩

/-- Composition of action-groupoid arrows.  `comp a b` means first `a`, then
`b`, hence the composite gauge element is `b * a`. -/
def comp [Group Gauge] [MulAction Gauge X]
    {x y z : X}
    (a : ActionArrow (Gauge := Gauge) x y)
    (b : ActionArrow (Gauge := Gauge) y z) :
    ActionArrow (Gauge := Gauge) x z :=
  ⟨b.1 * a.1, by
    calc
      (b.1 * a.1) • x = b.1 • (a.1 • x) := by rw [mul_smul]
      _ = b.1 • y := by rw [a.2]
      _ = z := b.2⟩

/-- Every action-groupoid arrow is invertible. -/
def inv [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    ActionArrow (Gauge := Gauge) y x :=
  ⟨a.1⁻¹, by
    rw [← a.2]
    simp [smul_smul]⟩

@[simp] theorem comp_id_source
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    comp (id (Gauge := Gauge) x) a = a := by
  apply Subtype.ext
  simp [comp, id]

@[simp] theorem comp_id_target
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    comp a (id (Gauge := Gauge) y) = a := by
  apply Subtype.ext
  simp [comp, id]

@[simp] theorem comp_assoc
    [Group Gauge] [MulAction Gauge X]
    {w₀ x y z : X}
    (a : ActionArrow (Gauge := Gauge) w₀ x)
    (b : ActionArrow (Gauge := Gauge) x y)
    (c : ActionArrow (Gauge := Gauge) y z) :
    comp (comp a b) c = comp a (comp b c) := by
  apply Subtype.ext
  simp [comp, mul_assoc]

@[simp] theorem comp_inv
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    comp a (inv a) = id (Gauge := Gauge) x := by
  apply Subtype.ext
  simp [comp, inv, id]

@[simp] theorem inv_comp
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    comp (inv a) a = id (Gauge := Gauge) y := by
  apply Subtype.ext
  simp [comp, inv, id]

@[simp] theorem inv_inv
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    inv (inv a) = a := by
  apply Subtype.ext
  simp [inv]

end ActionArrow

/-- Gauge-relatedness is exactly existence of an action-groupoid arrow. -/
theorem gaugeRelated_iff_nonempty_actionArrow
    [Group Gauge] [MulAction Gauge X]
    (x y : X) :
    GaugeRelated (Gauge := Gauge) x y ↔
      Nonempty (ActionArrow (Gauge := Gauge) x y) := by
  constructor
  · rintro ⟨g, hg⟩
    exact ⟨⟨g, hg⟩⟩
  · rintro ⟨a⟩
    exact ⟨a.1, a.2⟩

/-- Equality in the coarse orbit quotient remembers only whether some groupoid
arrow exists, not which arrow it was. -/
theorem orbitProjection_eq_iff_nonempty_actionArrow
    [Group Gauge] [MulAction Gauge X]
    (x y : X) :
    orbitProjection Gauge X x = orbitProjection Gauge X y ↔
      Nonempty (ActionArrow (Gauge := Gauge) x y) := by
  constructor
  · intro h
    have hrel : GaugeRelated (Gauge := Gauge) x y := Quotient.exact h
    exact (gaugeRelated_iff_nonempty_actionArrow (Gauge := Gauge) x y).1 hrel
  · intro h
    apply Quotient.sound
    exact (gaugeRelated_iff_nonempty_actionArrow (Gauge := Gauge) x y).2 h

/-- Isotropy at `x` consists of all action-groupoid loops at `x`. -/
def ActionIsotropy [Group Gauge] [MulAction Gauge X] (x : X) : Type w :=
  ActionArrow (Gauge := Gauge) x x

/-- Stabilizer subgroup at a representative.  This data is invisible in the
coarse orbit set but retained by the action groupoid. -/
def gaugeStabilizer [Group Gauge] [MulAction Gauge X] (x : X) : Subgroup Gauge where
  carrier := {g | g • x = x}
  one_mem' := by simp
  mul_mem' := by
    intro g h hg hh
    calc
      (g * h) • x = g • (h • x) := by rw [mul_smul]
      _ = g • x := by rw [hh]
      _ = x := hg
  inv_mem' := by
    intro g hg
    rw [← hg]
    simp [smul_smul]

/-- Groupoid isotropy and the ordinary stabilizer subgroup contain exactly the
same gauge transformations. -/
def isotropyEquivStabilizer
    [Group Gauge] [MulAction Gauge X]
    (x : X) :
    ActionIsotropy (Gauge := Gauge) x ≃ gaugeStabilizer (Gauge := Gauge) x where
  toFun a := ⟨a.1, a.2⟩
  invFun g := ⟨g.1, g.2⟩
  left_inv := by intro a; rfl
  right_inv := by intro g; rfl

/-- Conjugating a loop by an arrow transports isotropy from the source object to
the target object.  This is the elementary action-groupoid form of isotropy
transport. -/
def transportIsotropy
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y)
    (loop : ActionIsotropy (Gauge := Gauge) x) :
    ActionIsotropy (Gauge := Gauge) y :=
  ActionArrow.comp (ActionArrow.comp (ActionArrow.inv a) loop) a

/-- Isotropy transport is an equivalence; gauge-related representatives have
isomorphic isotropy data rather than having that data erased. -/
def isotropyEquivAlongArrow
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    ActionIsotropy (Gauge := Gauge) x ≃ ActionIsotropy (Gauge := Gauge) y where
  toFun := transportIsotropy a
  invFun := transportIsotropy (ActionArrow.inv a)
  left_inv := by
    intro loop
    apply Subtype.ext
    simp [transportIsotropy, ActionArrow.comp, ActionArrow.inv, mul_assoc]
  right_inv := by
    intro loop
    apply Subtype.ext
    simp [transportIsotropy, ActionArrow.comp, ActionArrow.inv, mul_assoc]

/-- Explicit gauge formula for isotropy transport: `g ↦ a g a⁻¹`. -/
theorem transportIsotropy_gauge
    [Group Gauge] [MulAction Gauge X]
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y)
    (loop : ActionIsotropy (Gauge := Gauge) x) :
    (transportIsotropy a loop).1 = a.1 * loop.1 * a.1⁻¹ := by
  simp [transportIsotropy, ActionArrow.comp, mul_assoc]

/-- Distinct stabilizer elements remain distinct isotropy arrows even though the
coarse quotient sends their source and target to the same orbit point. -/
theorem distinct_isotropy_arrows_of_distinct_gauge
    [Group Gauge] [MulAction Gauge X]
    {x : X} {g h : Gauge}
    (hg : g • x = x) (hh : h • x = x)
    (hne : g ≠ h) :
    (⟨g, hg⟩ : ActionIsotropy (Gauge := Gauge) x) ≠
      (⟨h, hh⟩ : ActionIsotropy (Gauge := Gauge) x) := by
  intro harrow
  apply hne
  exact congrArg Subtype.val harrow

/-- A coarse orbit point cannot distinguish two distinct isotropy arrows.  The
left conjunct is tautological at the orbit level; the right conjunct records
information retained only by the groupoid presentation. -/
theorem coarse_orbit_forgets_isotropy_arrow_identity
    [Group Gauge] [MulAction Gauge X]
    {x : X} {g h : Gauge}
    (hg : g • x = x) (hh : h • x = x)
    (hne : g ≠ h) :
    orbitProjection Gauge X x = orbitProjection Gauge X x ∧
      (⟨g, hg⟩ : ActionIsotropy (Gauge := Gauge) x) ≠
        (⟨h, hh⟩ : ActionIsotropy (Gauge := Gauge) x) := by
  exact ⟨rfl, distinct_isotropy_arrows_of_distinct_gauge hg hh hne⟩

/-- Gauge-invariant semantics are constant along every action-groupoid arrow. -/
theorem semantic_constant_on_actionArrow
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x)
    {x y : X}
    (a : ActionArrow (Gauge := Gauge) x y) :
    semantic y = semantic x := by
  rw [← a.2]
  exact hInvariant a.1 x

/-- Conversely, constancy along all action-groupoid arrows implies ordinary
gauge invariance. -/
theorem semantic_invariant_of_constant_on_actionArrow
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hArrow : ∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
      semantic y = semantic x) :
    ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x := by
  intro g x
  exact hArrow (⟨g, rfl⟩ : ActionArrow (Gauge := Gauge) x (g • x))

/-- Semantic gauge invariance is exactly functorial collapse of every action
arrow to equality in the discrete semantic codomain. -/
theorem semantic_invariant_iff_constant_on_actionArrows
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y) :
    (∀ (g : Gauge) (x : X), semantic (g • x) = semantic x) ↔
      (∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
        semantic y = semantic x) := by
  constructor
  · intro hInvariant x y a
    exact semantic_constant_on_actionArrow semantic hInvariant a
  · intro hArrow
    exact semantic_invariant_of_constant_on_actionArrow semantic hArrow

/-- Dense dependent-origination descent produces both action-groupoid semantic
constancy and the unique coarse-orbit semantic factorization.  The first retains
arrow/isotropy data; the second is its 0-truncated semantic shadow. -/
theorem dense_descent_groupoid_constancy_and_orbit_factorization
    [Group Gauge] [MulAction Gauge X]
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (fun x : X => g • x))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      g • realize n u = realize n (localAction n g u))
    (hLocalInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      semantic (realize n (localAction n g u)) = semantic (realize n u)) :
    (∀ {x y : X}, ActionArrow (Gauge := Gauge) x y → semantic y = semantic x) ∧
      (∃! orbitSemantic : GaugeOrbit Gauge X → Y,
        ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x) := by
  have hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x :=
    semantic_invariant_of_dense_local_realization
      realize (fun g x => g • x) localAction semantic hDense
      hActionContinuous hEquivariant hLocalInvariant
  constructor
  · intro x y a
    exact semantic_constant_on_actionArrow semantic hInvariant a
  · exact existsUnique_orbitSemantic_of_invariant semantic hInvariant

/-- With exact local readouts, dense descent yields the full three-level package:
action-groupoid semantic constancy, unique orbit-level semantics, and cross-scale
compatibility. -/
theorem dense_descent_groupoid_orbit_crossScale_package
    [Group Gauge] [MulAction Gauge X]
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (fun x : X => g • x))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      g • realize n u = realize n (localAction n g u))
    (hreadout : ∀ (n : ℕ) (u : Local n), semantic (realize n u) = target n u)
    (hTargetInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      target n (localAction n g u) = target n u) :
    (∀ {x y : X}, ActionArrow (Gauge := Gauge) x y → semantic y = semantic x) ∧
      (∃! orbitSemantic : GaugeOrbit Gauge X → Y,
        ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x) ∧
      CrossScaleCompatible realize target := by
  have hpair := dense_descent_orbitSemantic_and_crossScaleCompatibility
    (Gauge := Gauge) realize target localAction semantic hDense hActionContinuous
    hEquivariant hreadout hTargetInvariant
  have hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x :=
    semantic_invariant_of_dense_local_realization
      realize (fun g x => g • x) localAction semantic hDense
      hActionContinuous hEquivariant (by
        intro n g u
        rw [hreadout n, hreadout n]
        exact hTargetInvariant n g u)
  exact ⟨by
      intro x y a
      exact semantic_constant_on_actionArrow semantic hInvariant a,
    hpair.1, hpair.2⟩

end KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1
