import Mathlib
import KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1

namespace KUOS.GaugeInvariantDependentOriginationGroupoidCechDescentV0_1

open Set Topology
open KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1
open KUOS.GaugeInvariantDependentOriginationOrbitQuotientV0_1
open KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1

universe u v w z t

variable {X : Type u} {Y : Type v} {Gauge : Type w}
variable {Local : ℕ → Type z} {Index : Type t}

/--
A complete-overlap Čech datum valued in the action groupoid `Gauge ⋉ X`.

Each chart index carries one presentation `object i`.  Every ordered pair of
charts carries an actual gauge arrow, and the arrows satisfy identity and exact
non-Abelian cocycle composition.  This is deliberately a complete-overlap
abstraction; it is not yet a theorem about arbitrary sites or open covers.
-/
structure ActionGroupoidCechDatum
    (Gauge : Type w) (X : Type u) (Index : Type t)
    [Group Gauge] [MulAction Gauge X] where
  object : Index → X
  transition : ∀ i j : Index,
    ActionArrow (Gauge := Gauge) (object i) (object j)
  transition_self : ∀ i : Index,
    transition i i = ActionArrow.id (Gauge := Gauge) (object i)
  transition_cocycle : ∀ i j k : Index,
    ActionArrow.comp (transition i j) (transition j k) = transition i k

/-- The identity transition has gauge element `1`. -/
theorem transition_gauge_self
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (i : Index) :
    (datum.transition i i).1 = 1 := by
  have h := congrArg
    (fun a : ActionArrow (Gauge := Gauge) (datum.object i) (datum.object i) => a.1)
    (datum.transition_self i)
  simpa [ActionArrow.id] using h

/--
The underlying gauge elements satisfy the exact non-Abelian Čech cocycle law.
With the arrow convention `i → j`, composition gives `g_jk * g_ij = g_ik`.
-/
theorem transition_gauge_cocycle
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (i j k : Index) :
    (datum.transition j k).1 * (datum.transition i j).1 =
      (datum.transition i k).1 := by
  have h := congrArg
    (fun a : ActionArrow (Gauge := Gauge) (datum.object i) (datum.object k) => a.1)
    (datum.transition_cocycle i j k)
  simpa [ActionArrow.comp] using h

/-- Every two local presentations in a complete-overlap datum have the same
coarse orbit, while the datum still retains the actual transition arrow. -/
theorem cech_objects_same_orbit
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (i j : Index) :
    orbitProjection Gauge X (datum.object i) =
      orbitProjection Gauge X (datum.object j) := by
  apply (orbitProjection_eq_iff_nonempty_actionArrow
    (Gauge := Gauge) (datum.object i) (datum.object j)).2
  exact ⟨datum.transition i j⟩

/-- Semantic values satisfy Čech compatibility when they agree along every
specified transition arrow. -/
def CechSemanticCompatible
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y) : Prop :=
  ∀ i j : Index, semantic (datum.object j) = semantic (datum.object i)

/-- Gauge-invariant semantics are automatically compatible on every
complete-overlap action-groupoid Čech datum. -/
theorem cechSemanticCompatible_of_invariant
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X),
      semantic (g • x) = semantic x) :
    CechSemanticCompatible datum semantic := by
  intro i j
  exact semantic_constant_on_actionArrow semantic hInvariant
    (datum.transition i j)

/-- Constancy on all action-groupoid arrows is already sufficient for Čech
semantic compatibility. -/
theorem cechSemanticCompatible_of_arrow_constancy
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hArrow : ∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
      semantic y = semantic x) :
    CechSemanticCompatible datum semantic := by
  intro i j
  exact hArrow (datum.transition i j)

/-- A compatible family has one anchor-independent semantic value. -/
theorem semantic_value_eq_anchor_of_cechCompatible
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hCompatible : CechSemanticCompatible datum semantic)
    (anchor i : Index) :
    semantic (datum.object i) = semantic (datum.object anchor) := by
  exact hCompatible anchor i

/-- Any nonempty compatible local value family glues to a unique global value
in the discrete semantic codomain.  This is value-level gluing, not existence of
a global `X`-valued section. -/
theorem existsUnique_gluedValue_of_compatible
    [Nonempty Index]
    (localValue : Index → Y)
    (hCompatible : ∀ i j : Index, localValue j = localValue i) :
    ∃! y : Y, ∀ i : Index, localValue i = y := by
  classical
  let i0 : Index := Classical.choice (inferInstance : Nonempty Index)
  refine ⟨localValue i0, ?_, ?_⟩
  · intro i
    exact hCompatible i0 i
  · intro y hy
    exact (hy i0).symm

/-- Action-groupoid arrow constancy yields a unique glued semantic value across
all charts of a nonempty complete-overlap Čech datum. -/
theorem existsUnique_gluedSemantic_of_arrow_constancy
    [Group Gauge] [MulAction Gauge X] [Nonempty Index]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hArrow : ∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
      semantic y = semantic x) :
    ∃! y : Y, ∀ i : Index, semantic (datum.object i) = y := by
  apply existsUnique_gluedValue_of_compatible
    (localValue := fun i => semantic (datum.object i))
  exact cechSemanticCompatible_of_arrow_constancy datum semantic hArrow

/-- Gauge invariance itself therefore gives a unique glued semantic value. -/
theorem existsUnique_gluedSemantic_of_invariant
    [Group Gauge] [MulAction Gauge X] [Nonempty Index]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X),
      semantic (g • x) = semantic x) :
    ∃! y : Y, ∀ i : Index, semantic (datum.object i) = y := by
  apply existsUnique_gluedValue_of_compatible
    (localValue := fun i => semantic (datum.object i))
  exact cechSemanticCompatible_of_invariant datum semantic hInvariant

/--
Dense dependent-origination descent upgrades an arbitrary nonempty
complete-overlap action-groupoid Čech presentation to one unique semantic value,
while simultaneously retaining the unique coarse-orbit semantic factorization
and exact cross-scale readout compatibility.

The existence of the continuous global semantic map is still an explicit input;
this theorem does not manufacture that extension from Čech compatibility.
-/
theorem dense_descent_groupoid_cech_glue_orbit_crossScale_package
    [Group Gauge] [MulAction Gauge X]
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    [Nonempty Index]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (fun x : X => g • x))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      g • realize n u = realize n (localAction n g u))
    (hreadout : ∀ (n : ℕ) (u : Local n),
      semantic (realize n u) = target n u)
    (hTargetInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      target n (localAction n g u) = target n u) :
    (∃! y : Y, ∀ i : Index, semantic (datum.object i) = y) ∧
      (∃! orbitSemantic : GaugeOrbit Gauge X → Y,
        ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x) ∧
      CrossScaleCompatible realize target := by
  have hpack := dense_descent_groupoid_orbit_crossScale_package
    (Gauge := Gauge) realize target localAction semantic hDense
    hActionContinuous hEquivariant hreadout hTargetInvariant
  constructor
  · exact existsUnique_gluedSemantic_of_arrow_constancy datum semantic hpack.1
  · exact hpack.2

end KUOS.GaugeInvariantDependentOriginationGroupoidCechDescentV0_1
