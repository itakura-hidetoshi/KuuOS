import KUOS.DependentOriginationCoherentBiadjunctionActualLiftConstructiveRefinementV5_138

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138

set_option autoImplicit false
noncomputable section

/-!
# F42-A/v5.139 — finite-depth primitive refinement-derivation certificates

Unlike F41's reflexive-transitive Refines, this file separates
primitive one-step moves from finite Nat-indexed derivations.
OneStep consists ONLY of splitting a native F40 block, inserting
an empty block and transporting such steps under a right-hand block.
It has NO composite-equality or reflexive/transitive constructor.

Trace n p q proves that an ACTUAL finite sequence of EXACTLY n
primitive moves connects p to q. All F41 refinements have SOME such
finite trace by structural induction on F41's original constructors.
Conversely every trace yields the unchanged F41 Refines relation.
This does NOT claim a single uniform depth bound for all refinements.

F19 original modification Hom and actual F28 quotient Hom are not
identified with F26 comparison chains. Original mates remain unchanged.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138.Grid

universe u v uE vE
variable {D : Type u} [Category.{v} D]

/-- One concrete block refinement or its original right context. -/
inductive OneStep : ∀ {x y : D}, Blocks x y → Blocks x y → Prop where
  | split {w x y z : D}
      (p : Blocks w x) (q : Chain.Path x y) (r : Chain.Path y z) :
      OneStep (.snoc p (q.append r)) (.snoc (.snoc p q) r)
  | insertNil {x y : D} (p : Blocks x y) :
      OneStep p (.snoc p (Chain.Path.nil y))
  | whisker {x y z : D} {p q : Blocks x y}
      (h : OneStep p q) (t : Chain.Path y z) :
      OneStep (.snoc p t) (.snoc q t)

/-- Every primitive step is an original F41 constructive refinement. -/
theorem OneStep.toRefines {x y : D} {p q : Blocks x y}
    (h : OneStep p q) : Refines p q := by
  induction h with
  | split p q r =>
      exact Refines.split p q r
  | insertNil p =>
      exact Refines.insertNil p
  | whisker h t ih =>
      exact Refines.whisker ih t

/-- Native composite morphisms are equal after one original step. -/
theorem OneStep.composite_eq {x y : D} {p q : Blocks x y}
    (h : OneStep p q) : p.composite = q.composite :=
  Refines.composite_eq (OneStep.toRefines h)

/-- A finite directed chain of EXACTLY n native primitive moves. -/
inductive Trace : ∀ {x y : D}, Nat → Blocks x y → Blocks x y → Prop where
  | refl {x y : D} (p : Blocks x y) : Trace 0 p p
  | snoc {x y : D} {n : Nat} {p q r : Blocks x y}
      (h : Trace n p q) (step : OneStep q r) :
      Trace (n + 1) p r

/-- Every explicitly finite trace gives a genuine F41 refinement. -/
theorem Trace.toRefines {x y : D} {n : Nat} {p q : Blocks x y}
    (h : Trace n p q) : Refines p q := by
  induction h with
  | refl p =>
      exact Refines.refl p
  | snoc h step ih =>
      exact Refines.trans ih (OneStep.toRefines step)

/-- n-step followed by m-step gives a concrete n+m-step derivation. -/
theorem Trace.append {x y : D} {n m : Nat}
    {p q r : Blocks x y}
    (h : Trace n p q) (k : Trace m q r) :
    Trace (n + m) p r := by
  induction k with
  | refl =>
      simpa only [Nat.add_zero] using h
  | snoc k step ih =>
      simpa only [Nat.add_succ] using
        (Trace.snoc ih step)

/-- Original right-hand whiskering preserves the EXACT step count. -/
theorem Trace.whisker {x y z : D} {n : Nat} {p q : Blocks x y}
    (h : Trace n p q) (t : Chain.Path y z) :
    Trace n (.snoc p t) (.snoc q t) := by
  induction h with
  | refl p =>
      exact Trace.refl _
  | snoc h step ih =>
      exact Trace.snoc ih (OneStep.whisker step t)

/-- Every original F41 reflexive-transitive refinement has an
explicitly FINITE depth and primitive-step derivation. -/
theorem Refines.exists_trace {x y : D} {p q : Blocks x y}
    (h : Refines p q) : ∃ n : Nat, Trace n p q := by
  induction h with
  | refl p =>
      exact ⟨0, Trace.refl p⟩
  | trans h₁ h₂ ih₁ ih₂ =>
      rcases ih₁ with ⟨n, hn⟩
      rcases ih₂ with ⟨m, hm⟩
      exact ⟨n + m, Trace.append hn hm⟩
  | whisker h t ih =>
      rcases ih with ⟨n, hn⟩
      exact ⟨n, Trace.whisker hn t⟩
  | split p q r =>
      exact ⟨1, Trace.snoc (Trace.refl _) (OneStep.split p q r)⟩
  | insertNil p =>
      exact ⟨1, Trace.snoc (Trace.refl _) (OneStep.insertNil p)⟩

/-- An EXACT characterization, rather than only one-way soundness. -/
theorem refines_iff_finiteTrace {x y : D} {p q : Blocks x y} :
    Refines p q ↔ ∃ n : Nat, Trace n p q := by
  constructor
  · exact Refines.exists_trace
  · rintro ⟨n, h⟩
    exact Trace.toRefines h

/-- F42 finite derivations preserve actual category composition. -/
theorem Trace.composite_eq {x y : D} {n : Nat}
    {p q : Blocks x y} (h : Trace n p q) :
    p.composite = q.composite :=
  Refines.composite_eq (Trace.toRefines h)

/-- Preserve finite traces under any genuine functor, including the
original F19 contravariant chosen right-mate presentation functor. -/
theorem Trace.mapBlocks_composite_eq
    {E : Type uE} [Category.{vE} E] (H : D ⥤ E)
    {x y : D} {n : Nat} {p q : Blocks x y} (h : Trace n p q) :
    (mapBlocks H p).composite = (mapBlocks H q).composite :=
  mapBlocks_independent H p q (Trace.composite_eq h)

#print axioms OneStep
#print axioms OneStep.toRefines
#print axioms OneStep.composite_eq
#print axioms Trace
#print axioms Trace.toRefines
#print axioms Trace.append
#print axioms Trace.whisker
#print axioms Refines.exists_trace
#print axioms refines_iff_finiteTrace
#print axioms Trace.composite_eq
#print axioms Trace.mapBlocks_composite_eq

end Grid

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
