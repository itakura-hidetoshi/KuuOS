import KUOS.DependentOriginationCoherentBiadjunctionFunctorialAxisTraceDescentV5_142

namespace KUOS.DependentOriginationCoherentBiadjunctionAxisTraceRealizationV5_142

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141
open KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142

set_option autoImplicit false
noncomputable section

/-!
# F45-C / v5.142 — realize independent Type-level histories in either order

The Type-valued native F19 and genuine F28 histories are not
artificial certificates: each is realized by an actual original
F44 ordered primitive route while the other axis stays unchanged.
Any pair therefore generates BOTH concrete standard executions
and both yield actual F44 exchange classes with exactly the
original per-axis depths.

This construction itself DOES NOT claim that arbitrary same-axis
refinements are equal; future completeness/normal-form results must
show any stronger equality by F44's explicit AdjacentSwap rules.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Realize an exact n-step Type-valued ORIGINAL modification trace,
at each step holding the ORIGINAL F28 quotient Blocks fixed. -/
def AxisTrace.toModificationInterleaving
    {a b : D} {x y : E}
    {n : Nat} {ma mb : Blocks a b}
    (h : AxisTrace n ma mb) (pa : Blocks x y) :
    OrderedInterleaving n 0 ma pa mb pa := by
  induction h with
  | refl p =>
      exact OrderedInterleaving.refl p pa
  | snoc h step ih =>
      exact OrderedInterleaving.modification ih step

/-- Realize an exact m-step Type-valued ORIGINAL F28
quotient-category trace while holding the F19 modification
presentation fixed at EVERY intermediate operation. -/
def AxisTrace.toComparisonInterleaving
    {a b : D} {x y : E}
    (ma : Blocks a b)
    {m : Nat} {pa pb : Blocks x y}
    (h : AxisTrace m pa pb) :
    OrderedInterleaving 0 m ma pa ma pb := by
  induction h with
  | refl p =>
      exact OrderedInterleaving.refl ma p
  | snoc h step ih =>
      exact OrderedInterleaving.comparison ih step

/-- Construct a real TWO-AXIS ordered path from both independent
Type-valued histories, ALL original F19 modifications first. -/
def AxisTrace.modificationFirst
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hmod : AxisTrace n ma mb) (hcmp : AxisTrace m pa pb) :
    OrderedInterleaving n m ma pa mb pb := by
  have h₁ : OrderedInterleaving n 0 ma pa mb pa :=
    AxisTrace.toModificationInterleaving hmod pa
  have h₂ : OrderedInterleaving 0 m mb pa mb pb :=
    AxisTrace.toComparisonInterleaving mb hcmp
  simpa only [Nat.add_zero, Nat.zero_add] using
    (OrderedInterleaving.append h₁ h₂)

/-- The same TWO ORIGINAL independent Type-valued histories can be
realized in the exact opposite order, F28 before F19. -/
def AxisTrace.comparisonFirst
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hmod : AxisTrace n ma mb) (hcmp : AxisTrace m pa pb) :
    OrderedInterleaving n m ma pa mb pb := by
  have h₁ : OrderedInterleaving 0 m ma pa ma pb :=
    AxisTrace.toComparisonInterleaving ma hcmp
  have h₂ : OrderedInterleaving n 0 ma pb mb pb :=
    AxisTrace.toModificationInterleaving hmod pb
  simpa only [Nat.add_zero, Nat.zero_add] using
    (OrderedInterleaving.append h₁ h₂)

/-- Every pair of original independently typed histories has a
GENUINE generated-exchange class with the exact original step
counts, constructed by explicit F19-first execution. -/
def AxisTrace.toModificationFirstClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hmod : AxisTrace n ma mb) (hcmp : AxisTrace m pa pb) :
    ExchangeClass n m ma mb pa pb :=
  (AxisTrace.modificationFirst hmod hcmp).toClass

/-- The same pair has an independent, honest F28-first witness
in the exchange quotient, with no inverse of any nonstrict G-cell. -/
def AxisTrace.toComparisonFirstClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hmod : AxisTrace n ma mb) (hcmp : AxisTrace m pa pb) :
    ExchangeClass n m ma mb pa pb :=
  (AxisTrace.comparisonFirst hmod hcmp).toClass

/-- The F19-first original refinement produces an actual F43 Prop,
with the same original independent F42 exact depths. -/
theorem AxisTrace.modificationFirst_toInterleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hmod : AxisTrace n ma mb) (hcmp : AxisTrace m pa pb) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
      n m ma pa mb pb :=
  (AxisTrace.toModificationFirstClass hmod hcmp).toInterleaving

#print axioms AxisTrace.toModificationInterleaving
#print axioms AxisTrace.toComparisonInterleaving
#print axioms AxisTrace.modificationFirst
#print axioms AxisTrace.comparisonFirst
#print axioms AxisTrace.toModificationFirstClass
#print axioms AxisTrace.toComparisonFirstClass
#print axioms AxisTrace.modificationFirst_toInterleaving

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionAxisTraceRealizationV5_142
