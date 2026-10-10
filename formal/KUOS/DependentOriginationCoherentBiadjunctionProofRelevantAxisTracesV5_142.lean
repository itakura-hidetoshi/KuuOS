import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141

namespace KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141

set_option autoImplicit false
noncomputable section

/-!
# F45-A / v5.142 — recover the TWO original proof-relevant axis histories

F44 introduced an honest Type-valued ordered F19/F28 shuffle and its
quotient ONLY by exchanges of independent consecutive primitive moves.
Here each original axis receives its own Type-valued witness so
two noncommuting same-axis move histories cannot be silently erased.

We project the genuine ordered shuffle to both native axis histories;
every F44 generating adjacent square preserves BOTH histories as
Type-level equalities. Consequently the pair of histories descends to
F44's actual generated exchange quotient, not only to a pair of Prop
existence statements or to equality of evaluated categorical arrows.

No equality of different same-axis refinements is postulated, and
nothing here identifies the original F19 and F28 Hom types.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- One original axis's ordered, exactly n-step primitive derivation.
Unlike F42's Trace (Prop), this remains in Type and retains the
intermediate F40 Blocks at every original step. -/
inductive AxisTrace : ∀ {a b : D},
    Nat → Blocks a b → Blocks a b → Type (max uD vD) where
  | refl {a b : D} (p : Blocks a b) : AxisTrace 0 p p
  | snoc {a b : D} {n : Nat} {p q r : Blocks a b}
      (h : AxisTrace n p q) (step : OneStep q r) :
      AxisTrace (n + 1) p r

/-- Recover the unchanged original F42 finite trace as a Prop. -/
theorem AxisTrace.toTrace
    {a b : D} {n : Nat} {p q : Blocks a b}
    (h : AxisTrace n p q) : Trace n p q := by
  induction h with
  | refl p =>
      exact Trace.refl p
  | snoc h step ih =>
      exact Trace.snoc ih step

/-- Actual source F19 primitive-operation history, with all
same-axis intermediate block presentations, from a genuine F44
ordered shuffle. The comparison operation leaves it unchanged. -/
def OrderedInterleaving.modificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    AxisTrace n ma mb := by
  induction h with
  | refl mods pq =>
      exact AxisTrace.refl mods
  | modification h step ih =>
      exact AxisTrace.snoc ih step
  | comparison h step ih =>
      exact ih

/-- Actual quotient-category F28 primitive-operation history, not
a comparison chain substituted from F26. The F19 operations leave
this witness unchanged. -/
def OrderedInterleaving.comparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    AxisTrace m pa pb := by
  induction h with
  | refl mods pq =>
      exact AxisTrace.refl pq
  | modification h step ih =>
      exact ih
  | comparison h step ih =>
      exact AxisTrace.snoc ih step

/-- Each F44 generating exchange preserves BOTH source and target
Type-level primitive-step histories, as opposed to merely their
total step counts, endpoints, or categorical composite evaluations. -/
theorem AdjacentSwap.axisTraces_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {p q : OrderedInterleaving n m ma pa mb pb}
    (h : AdjacentSwap p q) :
    p.modificationTrace = q.modificationTrace ∧
      p.comparisonTrace = q.comparisonTrace := by
  induction h with
  | square initialPath hm hp =>
      exact ⟨rfl, rfl⟩
  | afterModification h step ih =>
      exact ⟨congrArg (fun t => AxisTrace.snoc t step) ih.1, ih.2⟩
  | afterComparison h step ih =>
      exact ⟨ih.1, congrArg (fun t => AxisTrace.snoc t step) ih.2⟩

/-- The original F19/F28 proof-relevant histories are now actual
data ON THE QUOTIENT, constructed by sound Quot elimination using
the primitive square's equalities, without assuming any extra
same-axis interchange. -/
def ExchangeClass.axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    AxisTrace n ma mb × AxisTrace m pa pb :=
  Quot.liftOn c
    (fun p => (p.modificationTrace, p.comparisonTrace))
    (by
      intro p q hs
      exact Prod.ext (AdjacentSwap.axisTraces_eq hs).1
        (AdjacentSwap.axisTraces_eq hs).2)

/-- Computation at a genuine F44 quotient class: BOTH original
histories are recovered exactly, with no quotienting of same-axis
operation sequences. -/
theorem OrderedInterleaving.axisTraces_toClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.toClass h).axisTraces =
      (h.modificationTrace, h.comparisonTrace) :=
  rfl

/-- Forgetting Type-level history yields the unchanged original
F42 independently typed pair of Prop refinement traces. -/
theorem ExchangeClass.axisTraces_toRectangleTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    RectangleTrace n m ma mb pa pb := by
  exact ⟨c.axisTraces.1.toTrace, c.axisTraces.2.toTrace⟩

/-- Original F19 and F28 refinement composite Hom equalities
follow from the *extracted* Type-level histories. -/
theorem ExchangeClass.axisTraces_composites
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ma.composite = mb.composite ∧ pa.composite = pb.composite :=
  (ExchangeClass.axisTraces_toRectangleTrace c).composites

#print axioms AxisTrace
#print axioms AxisTrace.toTrace
#print axioms OrderedInterleaving.modificationTrace
#print axioms OrderedInterleaving.comparisonTrace
#print axioms AdjacentSwap.axisTraces_eq
#print axioms ExchangeClass.axisTraces
#print axioms OrderedInterleaving.axisTraces_toClass
#print axioms ExchangeClass.axisTraces_toRectangleTrace
#print axioms ExchangeClass.axisTraces_composites

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142
