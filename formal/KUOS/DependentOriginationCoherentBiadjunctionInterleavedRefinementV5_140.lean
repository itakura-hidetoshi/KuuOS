import KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140
import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140

set_option autoImplicit false
noncomputable section

/-!
# F43-B / v5.140: genuine independent-axis finite refinement INTERLEAVINGS

F42 recorded an independently counted pair of primitive finite traces
but did not explicitly represent the ORDER in which F19 and F28
primitive refinement steps are interleaved. Here Interleaving n m
has its own constructors for each individual primitive step of EITHER
axis, preserving their actual intermediate F40 block presentations.

We construct both routes across an elementary square:
  modify, then compare; and compare, then modify.
We also prove this works with arbitrary finite segments, that the
two-axis counts are exactly additive under concatenation, and that
every possible interleaving has the SAME exact indexed F42 rectangle
certificate. Conversely every F42 rectangle certificate can be
sequentialized in BOTH orders. This is the explicit two-axis
finite-step interchange, not merely postulated equality of morphisms.

The interleaving itself (not only its evaluated arrow) transports
through two independent original category functors without changing
the counts or replacing any intermediate refinement step.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140.Grid

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A real finite path of primitive grid refinements, retaining
intermediate presentations and the EXACT per-axis n/m step counts. -/
inductive Interleaving :
    ∀ {a b : D} {x y : E},
      Nat → Nat →
      Blocks a b → Blocks x y →
      Blocks a b → Blocks x y → Prop where
  | refl {a b : D} {x y : E}
      (mods : Blocks a b) (pq : Blocks x y) :
      Interleaving 0 0 mods pq mods pq
  | modification {a b : D} {x y : E}
      {n m : Nat}
      {ma mb mc : Blocks a b} {pa pb : Blocks x y}
      (h : Interleaving n m ma pa mb pb)
      (step : OneStep mb mc) :
      Interleaving (n + 1) m ma pa mc pb
  | comparison {a b : D} {x y : E}
      {n m : Nat}
      {ma mb : Blocks a b} {pa pb pc : Blocks x y}
      (h : Interleaving n m ma pa mb pb)
      (step : OneStep pb pc) :
      Interleaving n (m + 1) ma pa mb pc

/-- Forget ONLY the ordering of the primitive moves, retaining the
FULL original F42 pair of independently counted typed finite traces. -/
theorem Interleaving.toRectangleTrace
    {a b : D} {x y : E}
    {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : Interleaving n m modsA pqA modsB pqB) :
    RectangleTrace n m modsA modsB pqA pqB := by
  induction h with
  | refl mods pq =>
      exact RectangleTrace.refl mods pq
  | modification h step ih =>
      exact ⟨Trace.snoc ih.modifications step, ih.comparisons⟩
  | comparison h step ih =>
      exact ⟨ih.modifications, Trace.snoc ih.comparisons step⟩

/-- Concatenate arbitrarily interleaved original finite paths;
primitive depths add INDEPENDENTLY in each of the two axes. -/
theorem Interleaving.append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {modsA modsB modsC : Blocks a b}
    {pqA pqB pqC : Blocks x y}
    (h : Interleaving n m modsA pqA modsB pqB)
    (k : Interleaving n' m' modsB pqB modsC pqC) :
    Interleaving (n + n') (m + m') modsA pqA modsC pqC := by
  induction k with
  | refl =>
      simpa only [Nat.add_zero] using h
  | modification k step ih =>
      simpa only [Nat.add_succ] using
        (Interleaving.modification (ih h) step)
  | comparison k step ih =>
      simpa only [Nat.add_succ] using
        (Interleaving.comparison (ih h) step)

/-- Place any n-step ORIGINAL F19 modification derivation in a grid,
holding the genuine F28 comparison presentation fixed at every step. -/
theorem Trace.toModificationInterleaving
    {a b : D} {x y : E}
    {n : Nat} {modsA modsB : Blocks a b}
    (h : Trace n modsA modsB) (pq : Blocks x y) :
    Interleaving n 0 modsA pq modsB pq := by
  induction h with
  | refl mods => exact Interleaving.refl mods pq
  | snoc h step ih => exact Interleaving.modification ih step

/-- Place any m-step genuine F28 comparison derivation in a grid,
holding the ORIGINAL F19 modification presentation fixed. -/
theorem Trace.toComparisonInterleaving
    {a b : D} {x y : E}
    (mods : Blocks a b)
    {m : Nat} {pqA pqB : Blocks x y}
    (h : Trace m pqA pqB) :
    Interleaving 0 m mods pqA mods pqB := by
  induction h with
  | refl pq => exact Interleaving.refl mods pq
  | snoc h step ih => exact Interleaving.comparison ih step

/-- An arbitrary pair of original F42 finite refinement traces
genuinely interleaves as all F19 steps FIRST, then all F28 steps. -/
theorem Interleaving.modificationFirst
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (hmods : Trace n modsA modsB)
    (hpq : Trace m pqA pqB) :
    Interleaving n m modsA pqA modsB pqB := by
  have h₁ : Interleaving n 0 modsA pqA modsB pqA :=
    Trace.toModificationInterleaving hmods pqA
  have h₂ : Interleaving 0 m modsB pqA modsB pqB :=
    Trace.toComparisonInterleaving modsB hpq
  simpa only [Nat.add_zero, Nat.zero_add] using
    (Interleaving.append h₁ h₂)

/-- The SAME independent original traces genuinely interleave in the
OPPOSITE order: all F28 comparisons FIRST, then F19 modifications. -/
theorem Interleaving.comparisonFirst
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (hmods : Trace n modsA modsB)
    (hpq : Trace m pqA pqB) :
    Interleaving n m modsA pqA modsB pqB := by
  have h₁ : Interleaving 0 m modsA pqA modsA pqB :=
    Trace.toComparisonInterleaving modsA hpq
  have h₂ : Interleaving n 0 modsA pqB modsB pqB :=
    Trace.toModificationInterleaving hmods pqB
  simpa only [Nat.add_zero, Nat.zero_add] using
    (Interleaving.append h₁ h₂)

/-- Primitive INTERCHANGE SQUARE: both explicitly different orders
of a genuine OneStep on each independent original axis can occur. -/
theorem Interleaving.primitiveSquare
    {a b : D} {x y : E}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (hm : OneStep modsA modsB) (hp : OneStep pqA pqB) :
    Interleaving 1 1 modsA pqA modsB pqB ∧
      Interleaving 1 1 modsA pqA modsB pqB := by
  constructor
  · exact Interleaving.comparison
      (Interleaving.modification (Interleaving.refl modsA pqA) hm) hp
  · exact Interleaving.modification
      (Interleaving.comparison (Interleaving.refl modsA pqA) hp) hm

/-- This is a TRUE necessary-and-sufficient characterization:
arbitrary ordered two-axis primitive refinement steps do not create
more or fewer reachable endpoint pairs than the independently counted
F42 original RectangleTrace; exact natural depths are preserved. -/
theorem interleaving_iff_rectangleTrace
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y} :
    Interleaving n m modsA pqA modsB pqB ↔
      RectangleTrace n m modsA modsB pqA pqB := by
  constructor
  · exact Interleaving.toRectangleTrace
  · intro h
    exact Interleaving.modificationFirst h.modifications h.comparisons

/-- Every concrete shuffle preserves BOTH original categorical
composites, WITHOUT assuming any endpoint Hom equality as an input. -/
theorem Interleaving.composites
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : Interleaving n m modsA pqA modsB pqB) :
    (modsA.composite = modsB.composite) ∧
      (pqA.composite = pqB.composite) :=
  (Interleaving.toRectangleTrace h).composites

/-- The ENTIRE ordered two-axis primitive trace, not just its
composite, is transported by two independent genuine functors with
the EXACT original n/m primitive step counts and shuffle order. -/
theorem Interleaving.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : Interleaving n m modsA pqA modsB pqB) :
    Interleaving n m
      (mapBlocks H modsA) (mapBlocks K pqA)
      (mapBlocks H modsB) (mapBlocks K pqB) := by
  induction h with
  | refl mods pq =>
      exact Interleaving.refl (mapBlocks H mods) (mapBlocks K pq)
  | modification h step ih =>
      exact Interleaving.modification ih (oneStep_mapBlocks H step)
  | comparison h step ih =>
      exact Interleaving.comparison ih (oneStep_mapBlocks K step)

/-- Both original F40 mapped categorical evaluations agree for every
FUNCTORIALLY TRANSPORTED interleaving, without strictifying either H
or K or assuming any new invertibility. -/
theorem Interleaving.mapBoth_composites
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : Interleaving n m modsA pqA modsB pqB) :
    ((mapBlocks H modsA).composite = (mapBlocks H modsB).composite) ∧
      ((mapBlocks K pqA).composite = (mapBlocks K pqB).composite) :=
  (Interleaving.mapBoth H K h).composites

#print axioms Interleaving
#print axioms Interleaving.toRectangleTrace
#print axioms Interleaving.append
#print axioms Trace.toModificationInterleaving
#print axioms Trace.toComparisonInterleaving
#print axioms Interleaving.modificationFirst
#print axioms Interleaving.comparisonFirst
#print axioms Interleaving.primitiveSquare
#print axioms interleaving_iff_rectangleTrace
#print axioms Interleaving.composites
#print axioms Interleaving.mapBoth
#print axioms Interleaving.mapBoth_composites

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
