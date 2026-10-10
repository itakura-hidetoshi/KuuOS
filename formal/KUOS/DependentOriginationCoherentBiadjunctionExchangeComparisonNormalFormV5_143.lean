import KUOS.DependentOriginationCoherentBiadjunctionAxisTraceRealizationV5_142

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F46-A / v5.143 — fully proof-relevant F28-first primitive normal form

We keep every F19 and F28 OneStep in its original category and never
commute two steps belonging to the same axis. The canonical F28-first
representative is defined by structural induction on the *F19*
AxisTrace, rather than by forgetting the original order in Prop.

The key bubble lemma moves ONE trailing F28 primitive operation past
ANY finite F19 Type-valued history via the *genuine* F44 adjacent
exchange squares. Every step is witnessed inside the F44 quotient
using the already-proved right-congruence rules, not equality of Hom.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Actual F28-first normal form: apply the independent entire F28
history once with the F19 presentation fixed, then perform the F19
history step by step. No global uniform depth bound is assumed. -/
def AxisTrace.comparisonNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    OrderedInterleaving n m ma pa mb pb := by
  induction hm with
  | refl p =>
      exact AxisTrace.toComparisonInterleaving p hc
  | snoc hm step ih =>
      exact OrderedInterleaving.modification ih step

/-- Projection of a pure original F28 history to the F19 axis is
the exact zero-step identity, even when the F28 depth is arbitrary. -/
theorem AxisTrace.toComparisonInterleaving_modificationTrace
    {a b : D} {x y : E} (mods : Blocks a b)
    {m : Nat} {pa pb : Blocks x y}
    (hc : AxisTrace m pa pb) :
    (AxisTrace.toComparisonInterleaving mods hc).modificationTrace =
      AxisTrace.refl mods := by
  induction hc with
  | refl p =>
      rfl
  | snoc hc step ih =>
      exact ih

/-- Pure F28 execution recovers the original full Type-valued F28
history, including all typed intermediate native quotient blocks. -/
theorem AxisTrace.toComparisonInterleaving_comparisonTrace
    {a b : D} {x y : E} (mods : Blocks a b)
    {m : Nat} {pa pb : Blocks x y}
    (hc : AxisTrace m pa pb) :
    (AxisTrace.toComparisonInterleaving mods hc).comparisonTrace =
      hc := by
  induction hc with
  | refl p =>
      rfl
  | snoc hc step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) ih

/-- Normalization never changes the first (F19) proof-relevant
primitive operation history, not even up to same-axis quotient. -/
theorem AxisTrace.comparisonNormal_modificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonNormal hm hc).modificationTrace = hm := by
  induction hm with
  | refl p =>
      exact AxisTrace.toComparisonInterleaving_modificationTrace p hc
  | snoc hm step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) ih

/-- Normalization also preserves the entire independent original F28
primitive history, not just its length or endpoint composite. -/
theorem AxisTrace.comparisonNormal_comparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonNormal hm hc).comparisonTrace = hc := by
  induction hm with
  | refl p =>
      exact AxisTrace.toComparisonInterleaving_comparisonTrace p hc
  | snoc hm step ih =>
      exact ih

/-- Add one authentic F19 step to the right of a generated exchange
class. The defining quotient lift uses *only* the F44 primitive
context constructor, not any equality of final categorical arrows. -/
def ExchangeClass.afterModification
    {a b : D} {x y : E} {n m : Nat}
    {ma mb mc : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) (hm : OneStep mb mc) :
    ExchangeClass (n + 1) m ma mc pa pb :=
  Quot.liftOn c
    (fun route => (OrderedInterleaving.modification route hm).toClass)
    (by
      intro p q hs
      exact Quot.sound (AdjacentSwap.afterModification hs hm))

/-- Add one authentic F28 step to the right of a generated exchange
class without changing the independently typed F19 presentation. -/
def ExchangeClass.afterComparison
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb pc : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) (hc : OneStep pb pc) :
    ExchangeClass n (m + 1) ma mb pa pc :=
  Quot.liftOn c
    (fun route => (OrderedInterleaving.comparison route hc).toClass)
    (by
      intro p q hs
      exact Quot.sound (AdjacentSwap.afterComparison hs hc))

/-- Bubble a single F28 primitive operation through ANY number of
F19 operations. The inductive case is an explicit F44 primitive
square followed by a genuine quotient congruence, never an assumed
higher-dimensional generic interchange law. -/
theorem AxisTrace.comparisonNormal_bubble
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb pc : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb)
    (step : OneStep pb pc) :
    (OrderedInterleaving.comparison
      (AxisTrace.comparisonNormal hm hc) step).toClass =
    (AxisTrace.comparisonNormal hm (AxisTrace.snoc hc step)).toClass := by
  induction hm with
  | refl p =>
      rfl
  | snoc hm hmstep ih =>
      calc
        (OrderedInterleaving.comparison
          (AxisTrace.comparisonNormal (AxisTrace.snoc hm hmstep) hc)
          step).toClass =
          (OrderedInterleaving.modification
            (OrderedInterleaving.comparison
              (AxisTrace.comparisonNormal hm hc) step) hmstep).toClass :=
            Quot.sound (AdjacentSwap.square
              (AxisTrace.comparisonNormal hm hc) hmstep step)
        _ = (AxisTrace.comparisonNormal
              (AxisTrace.snoc hm hmstep) (AxisTrace.snoc hc step)).toClass := by
                exact congrArg
                  (fun c => ExchangeClass.afterModification c hmstep) ih

#print axioms AxisTrace.comparisonNormal
#print axioms AxisTrace.toComparisonInterleaving_modificationTrace
#print axioms AxisTrace.toComparisonInterleaving_comparisonTrace
#print axioms AxisTrace.comparisonNormal_modificationTrace
#print axioms AxisTrace.comparisonNormal_comparisonTrace
#print axioms ExchangeClass.afterModification
#print axioms ExchangeClass.afterComparison
#print axioms AxisTrace.comparisonNormal_bubble

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
