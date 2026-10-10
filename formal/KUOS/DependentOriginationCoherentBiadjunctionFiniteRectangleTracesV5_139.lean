import KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139

set_option autoImplicit false
noncomputable section

/-!
# F42-B/v5.139 — independently counted two-axis finite refinements

The FIRST axis is a genuine sequence of original F19 chosen
StrongTrans.Modification categorical block refinements; the SECOND
axis is an INDEPENDENT sequence of actual F28 compression-kernel
quotient-category block refinements. Nat depths n and m count ONLY
real primitive split/insert operations on the respective axes.

RectangleTrace n m is a typed original two-axis certificate, and
its existence is EQUIVALENT to F41's original constructive
RectangleRefines. Independent traces genuinely compose with separate
depth addition. This is not an invented strict higher grid of
unrelated 2-cells and requires no G-side comparison inversion.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]

/-- Independent exactly n-step and m-step primitive derivations in
two potentially entirely different actual categories. -/
structure RectangleTrace
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (n m : Nat)
    (modsA modsB : Blocks a b)
    (pqA pqB : Blocks x y) : Prop where
  modifications : Trace n modsA modsB
  comparisons : Trace m pqA pqB

/-- The original F41 rectangular refinement follows as a theorem
from the two independently finite primitive derivations. -/
theorem RectangleTrace.toRefines
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : RectangleTrace n m modsA modsB pqA pqB) :
    RectangleRefines modsA modsB pqA pqB :=
  ⟨Trace.toRefines h.modifications, Trace.toRefines h.comparisons⟩

/-- Both genuine composite Hom equalities follow, without any
independent equality premise, from the finite trace certificates. -/
theorem RectangleTrace.composites
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : RectangleTrace n m modsA modsB pqA pqB) :
    (modsA.composite = modsB.composite) ∧
      (pqA.composite = pqB.composite) :=
  ⟨Trace.composite_eq h.modifications,
    Trace.composite_eq h.comparisons⟩

/-- Empty traces give identity refinements on BOTH independent axes. -/
theorem RectangleTrace.refl
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (mods : Blocks a b) (pq : Blocks x y) :
    RectangleTrace 0 0 mods mods pq pq :=
  ⟨Trace.refl mods, Trace.refl pq⟩

/-- EXACT independent depth bookkeeping for composition of two
genuine two-axis finite refinement derivations. -/
theorem RectangleTrace.trans
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {modsA modsB modsC : Blocks a b}
    {pqA pqB pqC : Blocks x y}
    (hAB : RectangleTrace n₁ m₁ modsA modsB pqA pqB)
    (hBC : RectangleTrace n₂ m₂ modsB modsC pqB pqC) :
    RectangleTrace (n₁ + n₂) (m₁ + m₂) modsA modsC pqA pqC :=
  ⟨Trace.append hAB.modifications hBC.modifications,
    Trace.append hAB.comparisons hBC.comparisons⟩

/-- Any genuinely primitive step on the F19 axis can be paired
with an identity (zero-step) F28 comparison refinement. -/
theorem RectangleTrace.modificationStep
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {modsA modsB : Blocks a b} (h : OneStep modsA modsB)
    (pq : Blocks x y) :
    RectangleTrace 1 0 modsA modsB pq pq :=
  ⟨Trace.snoc (Trace.refl _) h, Trace.refl pq⟩

/-- Independent one-step refinement on the original comparison axis,
with the original F19 modification path held unchanged. -/
theorem RectangleTrace.comparisonStep
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (mods : Blocks a b)
    {pqA pqB : Blocks x y} (h : OneStep pqA pqB) :
    RectangleTrace 0 1 mods mods pqA pqB :=
  ⟨Trace.refl mods, Trace.snoc (Trace.refl _) h⟩

/-- F41 rectangular refinements are FINITE-STEP complete: a proof
always admits independently finite primitive-move lengths on the
two original axes, without a uniform bound on all proofs. -/
theorem RectangleRefines.exists_trace
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : RectangleRefines modsA modsB pqA pqB) :
    ∃ n m : Nat, RectangleTrace n m modsA modsB pqA pqB := by
  rcases Refines.exists_trace h.modifications with ⟨n, hn⟩
  rcases Refines.exists_trace h.comparisons with ⟨m, hm⟩
  exact ⟨n, m, ⟨hn, hm⟩⟩

/-- Precise necessary and sufficient FINITE-depth trace criterion
for the original F41 two-axis constructive refinement. -/
theorem rectangleRefines_iff_finiteTraces
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y} :
    RectangleRefines modsA modsB pqA pqB ↔
      ∃ n m : Nat, RectangleTrace n m modsA modsB pqA pqB := by
  constructor
  · exact RectangleRefines.exists_trace
  · rintro ⟨n, m, h⟩
    exact RectangleTrace.toRefines h

#print axioms RectangleTrace
#print axioms RectangleTrace.toRefines
#print axioms RectangleTrace.composites
#print axioms RectangleTrace.refl
#print axioms RectangleTrace.trans
#print axioms RectangleTrace.modificationStep
#print axioms RectangleTrace.comparisonStep
#print axioms RectangleRefines.exists_trace
#print axioms rectangleRefines_iff_finiteTraces

end Grid

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
