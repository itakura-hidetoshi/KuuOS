import KUOS.DependentOriginationCoherentBiadjunctionExchangeComparisonNormalFormV5_143

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid

set_option autoImplicit false
noncomputable section

/-!
# F46-B / v5.143 — every actual ordered two-axis route normalizes

The proof is structural induction on the genuine F44 Type-valued
ordered path. A final F19 step is transported across a quotient
equality by F46-A's primitive context lift. A final F28 step is
pushed left using the explicit finite bubble proof from F46-A.
Thus every possible *interleaving*, with its precise F19/F28 counts,
is equivalent through the original F44 AdjacentSwap relation to the
single F28-first representative computed from its two native
Type-valued F45 histories.

This is path-level normalization, strictly stronger than F43's
original equality of endpoint categorical Hom evaluations.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Every original genuine two-axis ordered path equals its normal
form in the *generated primitive-exchange quotient*. This equality
uses no additional same-axis move identifications. -/
theorem OrderedInterleaving.comparisonNormal_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (route : OrderedInterleaving n m ma pa mb pb) :
    route.toClass =
      (AxisTrace.comparisonNormal
        route.modificationTrace route.comparisonTrace).toClass := by
  induction route with
  | refl mods pq =>
      rfl
  | modification route step ih =>
      change ExchangeClass.afterModification route.toClass step =
        ExchangeClass.afterModification
          (AxisTrace.comparisonNormal
            route.modificationTrace route.comparisonTrace).toClass step
      exact congrArg (fun c => ExchangeClass.afterModification c step) ih
  | comparison route step ih =>
      change ExchangeClass.afterComparison route.toClass step =
        (AxisTrace.comparisonNormal route.modificationTrace
          (AxisTrace.snoc route.comparisonTrace step)).toClass
      calc
        ExchangeClass.afterComparison route.toClass step =
            ExchangeClass.afterComparison
              (AxisTrace.comparisonNormal route.modificationTrace
                route.comparisonTrace).toClass step :=
          congrArg (fun c => ExchangeClass.afterComparison c step) ih
        _ = (AxisTrace.comparisonNormal
              route.modificationTrace
              (AxisTrace.snoc route.comparisonTrace step)).toClass :=
          AxisTrace.comparisonNormal_bubble
            route.modificationTrace route.comparisonTrace step

/-- The normal-form theorem gives an honest certificate in the exact
reflexive, symmetric, transitive closure of F44's original adjacent
independent-axis swaps. No arbitrary composite equality is assumed. -/
theorem OrderedInterleaving.comparisonNormal_exchangeEqv
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (route : OrderedInterleaving n m ma pa mb pb) :
    ExchangeEqv route
      (AxisTrace.comparisonNormal
        route.modificationTrace route.comparisonTrace) :=
  (exchangeEqv_iff_class_eq _ _).2 route.comparisonNormal_eq

/-- Canonical representative of an arbitrary generated exchange
class. It is constructed from the original F45 Type-valued axis
histories, so no operation within one original axis is forgotten. -/
def ExchangeClass.comparisonNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    OrderedInterleaving n m ma pa mb pb :=
  AxisTrace.comparisonNormal c.axisTraces.1 c.axisTraces.2

/-- The F28-first canonical path is a genuine representative of the
same original F44 exchange class. This is the exact path-normalization
equation at the quotient level. -/
theorem ExchangeClass.comparisonNormal_toClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    c.comparisonNormal.toClass = c := by
  refine Quot.induction_on c ?_
  intro route
  exact (OrderedInterleaving.comparisonNormal_eq route).symm

/-- Normalization is genuinely idempotent: extracting the complete
two-axis histories and rebuilding an F28-first path a second time
leaves the original Type-valued F28-first normal form unchanged. -/
theorem AxisTrace.comparisonNormal_idempotent
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    AxisTrace.comparisonNormal
      (AxisTrace.comparisonNormal hm hc).modificationTrace
      (AxisTrace.comparisonNormal hm hc).comparisonTrace =
      AxisTrace.comparisonNormal hm hc := by
  rw [AxisTrace.comparisonNormal_modificationTrace,
    AxisTrace.comparisonNormal_comparisonTrace]

#print axioms OrderedInterleaving.comparisonNormal_eq
#print axioms OrderedInterleaving.comparisonNormal_exchangeEqv
#print axioms ExchangeClass.comparisonNormal
#print axioms ExchangeClass.comparisonNormal_toClass
#print axioms AxisTrace.comparisonNormal_idempotent

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
