import Mathlib.Data.Quot
import KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141

namespace KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141

set_option autoImplicit false
noncomputable section

/-!
# F44-B / v5.141 — the genuine exchange relation is a path congruence

Two independent original-category refinement paths compose with exact
F19/F28 counts. A primitive adjacent exchange remains an exchange
after placing any genuine path before or after it. The generated
exchange quotient therefore supports a well-defined binary typed
concatenation; no unrelated same-axis steps are identified.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Concatenate ordered Type-level genuine primitive refinements,
maintaining exactly n+n' original modification steps and m+m'
original comparison steps. -/
def OrderedInterleaving.append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb)
    (k : OrderedInterleaving n' m' mb pb mc pc) :
    OrderedInterleaving (n + n') (m + m') ma pa mc pc := by
  induction k with
  | refl =>
      simpa only [Nat.add_zero] using h
  | modification k step ih =>
      simpa only [Nat.add_succ] using
        (OrderedInterleaving.modification (ih h) step)
  | comparison k step ih =>
      simpa only [Nat.add_succ] using
        (OrderedInterleaving.comparison (ih h) step)

/-- A raw adjacent exchange remains one such exchange when an
arbitrary later sequence is appended to both routes. -/
theorem AdjacentSwap.appendSuffix
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {p q : OrderedInterleaving n m ma pa mb pb}
    (h : AdjacentSwap p q)
    (later : OrderedInterleaving n' m' mb pb mc pc) :
    AdjacentSwap (OrderedInterleaving.append p later)
      (OrderedInterleaving.append q later) := by
  induction later with
  | refl =>
      simpa only [OrderedInterleaving.append, Nat.add_zero] using h
  | modification later step ih =>
      simpa only [OrderedInterleaving.append, Nat.add_succ] using
        (AdjacentSwap.afterModification (ih h) step)
  | comparison later step ih =>
      simpa only [OrderedInterleaving.append, Nat.add_succ] using
        (AdjacentSwap.afterComparison (ih h) step)

/-- A raw adjacent exchange remains one such exchange when an
arbitrary earlier sequence is prepended; this checks the core square
and both inductive context constructors. -/
theorem AdjacentSwap.appendPrefix
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OrderedInterleaving n m ma pa mb pb)
    {p q : OrderedInterleaving n' m' mb pb mc pc}
    (h : AdjacentSwap p q) :
    AdjacentSwap (OrderedInterleaving.append earlier p)
      (OrderedInterleaving.append earlier q) := by
  induction h with
  | square prefix hm hp =>
      simpa only [OrderedInterleaving.append, Nat.add_succ] using
        (AdjacentSwap.square (OrderedInterleaving.append earlier prefix) hm hp)
  | afterModification h step ih =>
      simpa only [OrderedInterleaving.append, Nat.add_succ] using
        (AdjacentSwap.afterModification ih step)
  | afterComparison h step ih =>
      simpa only [OrderedInterleaving.append, Nat.add_succ] using
        (AdjacentSwap.afterComparison ih step)

/-- Exact quotient path concatenation: BOTH congruence conditions
are discharged by explicit primitive-interchange computations.
There is no dependence on proof irrelevance of the original Prop. -/
def ExchangeClass.append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc) :
    ExchangeClass (n + n') (m + m') ma mc pa pc :=
  Quot.liftOn₂ h k
    (fun p q => OrderedInterleaving.toClass (OrderedInterleaving.append p q))
    (by
      intro earlier later₁ later₂ hs
      exact Quot.sound (AdjacentSwap.appendPrefix earlier hs))
    (by
      intro earlier₁ earlier₂ later hs
      exact Quot.sound (AdjacentSwap.appendSuffix hs later))

/-- A concatenation of two exchange classes is still certified
by the ACTUAL original F43 two-axis finite refinement relation. -/
theorem ExchangeClass.append_toInterleaving
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
      (n + n') (m + m') ma pa mc pc :=
  (ExchangeClass.append h k).toInterleaving

/-- The original two categorical Hom evaluations agree under
composition in the NONTRIVIAL adjacent-exchange quotient. -/
theorem ExchangeClass.append_composites
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc) :
    ma.composite = mc.composite ∧ pa.composite = pc.composite :=
  (ExchangeClass.append h k).composites

#print axioms OrderedInterleaving.append
#print axioms AdjacentSwap.appendSuffix
#print axioms AdjacentSwap.appendPrefix
#print axioms ExchangeClass.append
#print axioms ExchangeClass.append_toInterleaving
#print axioms ExchangeClass.append_composites

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141
