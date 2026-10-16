import KUOS.DependentOriginationCoherentBiadjunctionF45TransportedHistoryReconciliationV5_145

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid

set_option autoImplicit false
noncomputable section

/-!
# F49-A / v5.146 — order-labelled ORIGINAL F45 exchange classes

F48 proves that BOTH original F45 path constructors, including their
nondefinitional Nat.zero_add / Eq.mp depth transports, preserve all
genuine intermediate original F19 and F28 primitive refinements.

Here a Type-valued two-constructor choice selects precisely one of
those *original* F45 implementations; no replacement normal form is
used as the route input. Each chosen old path maps to a genuine F44
exchange class and that class agrees, by F48's actual path theorem,
with the F46 typed pair-of-axis-histories canonical class.

The two originally different categories remain independently typed.
No same-axis operation commutation, extra G inverse, or equality of
the two categories' native Hom carriers is asserted.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The TWO concrete original F45 orderings, not arbitrary proof-irrelevant
F43 Prop certificates and not the newly defined F47 normal paths. -/
inductive OriginalF45Order : Type where
  | modificationFirst
  | comparisonFirst

/-- Execute exactly the OLD F45 Type-valued constructors with their
full native Eq.mp index transports. -/
def AxisTrace.originalF45Path
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    OrderedInterleaving n m ma pa mb pb :=
  match order with
  | .modificationFirst => AxisTrace.modificationFirst hm hc
  | .comparisonFirst => AxisTrace.comparisonFirst hm hc

/-- The original F45 route gives an ACTUAL element of the F44
primitive adjacent-swap-generated path quotient. -/
def AxisTrace.originalF45OrderClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeClass n m ma mb pa pb :=
  (AxisTrace.originalF45Path order hm hc).toClass

/-- BOTH *old* F45 paths retain ALL of each original Type-valued
F19/F28 axis history, with no change to the order within an axis. -/
theorem AxisTrace.originalF45Path_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.originalF45Path order hm hc).modificationTrace = hm ∧
      (AxisTrace.originalF45Path order hm hc).comparisonTrace = hc := by
  cases order with
  | modificationFirst =>
      exact ⟨AxisTrace.modificationFirst_originalModificationTrace hm hc,
        AxisTrace.modificationFirst_originalComparisonTrace hm hc⟩
  | comparisonFirst =>
      exact ⟨AxisTrace.comparisonFirst_originalModificationTrace hm hc,
        AxisTrace.comparisonFirst_originalComparisonTrace hm hc⟩

/-- The central F49 bridge: either ACTUAL old F45 execution order
yields precisely the F46 canonical history-pair class, not merely
equal final Hom composites or equivalent F43 Prop witnesses. -/
theorem AxisTrace.originalF45OrderClass_eq_pair
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    AxisTrace.originalF45OrderClass order hm hc =
      AxisTrace.pairToClass (hm, hc) := by
  cases order with
  | modificationFirst =>
      calc
        (AxisTrace.modificationFirst hm hc).toClass =
            (AxisTrace.modificationNormal hm hc).toClass :=
          AxisTrace.originalF45_modificationFirst_eq_normalClass hm hc
        _ = (AxisTrace.comparisonNormal hm hc).toClass :=
          AxisTrace.modificationNormal_class_eq_comparisonNormal hm hc
  | comparisonFirst =>
      exact AxisTrace.originalF45_comparisonFirst_eq_normalClass hm hc

/-- The exact history recovery law is an equation of genuinely
Type-valued original F45 exchange-class invariants. -/
theorem AxisTrace.originalF45OrderClass_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.originalF45OrderClass order hm hc).axisTraces =
      (hm, hc) := by
  rw [AxisTrace.originalF45OrderClass_eq_pair,
    AxisTrace.pairToClass_axisTraces]

/-- Recover an ACTUAL F43 original two-axis interleaving proof from
either historically defined original F45 Type-valued execution. -/
theorem AxisTrace.originalF45Order_toInterleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
      n m ma pa mb pb :=
  (AxisTrace.originalF45OrderClass order hm hc).toInterleaving

/-- Every old F45 order is equivalent to the genuine F46 canonical
path under the EXACT F44 generated adjacent swap relation. -/
theorem AxisTrace.originalF45Order_exchangeEqv_normal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeEqv (AxisTrace.originalF45Path order hm hc)
      (AxisTrace.comparisonNormal hm hc) :=
  (exchangeEqv_iff_class_eq _ _).2
    (AxisTrace.originalF45OrderClass_eq_pair order hm hc)

/-- Transport under TWO independent honest functors commutes with
F49's ORIGINAL path-class realization and F46's complete history
classification, retaining exact independent primitive step counts. -/
theorem AxisTrace.originalF45OrderClass_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (order : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeClass.mapBoth H K
        (AxisTrace.originalF45OrderClass order hm hc) =
      AxisTrace.pairToClass
        (AxisTrace.mapBlocks H hm, AxisTrace.mapBlocks K hc) := by
  calc
    ExchangeClass.mapBoth H K
        (AxisTrace.originalF45OrderClass order hm hc) =
      ExchangeClass.mapBoth H K (AxisTrace.pairToClass (hm, hc)) :=
      congrArg (ExchangeClass.mapBoth H K)
        (AxisTrace.originalF45OrderClass_eq_pair order hm hc)
    _ = AxisTrace.pairToClass
          (AxisTrace.mapBlocks H hm, AxisTrace.mapBlocks K hc) :=
      AxisTrace.pairToClass_mapBoth H K (hm, hc)

/-- ANY two old F45 choices give equal generated exchange classes;
this follows from the full native F19/F28 histories rather than an
assertion that their Type-level syntax trees are definitionally equal. -/
theorem AxisTrace.originalF45OrderClass_independent
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (first second : OriginalF45Order)
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    AxisTrace.originalF45OrderClass first hm hc =
      AxisTrace.originalF45OrderClass second hm hc := by
  calc
    AxisTrace.originalF45OrderClass first hm hc =
        AxisTrace.pairToClass (hm, hc) :=
      AxisTrace.originalF45OrderClass_eq_pair first hm hc
    _ = AxisTrace.originalF45OrderClass second hm hc :=
      (AxisTrace.originalF45OrderClass_eq_pair second hm hc).symm

#print axioms OriginalF45Order
#print axioms AxisTrace.originalF45Path
#print axioms AxisTrace.originalF45OrderClass
#print axioms AxisTrace.originalF45Path_axisTraces
#print axioms AxisTrace.originalF45OrderClass_eq_pair
#print axioms AxisTrace.originalF45OrderClass_axisTraces
#print axioms AxisTrace.originalF45Order_toInterleaving
#print axioms AxisTrace.originalF45Order_exchangeEqv_normal
#print axioms AxisTrace.originalF45OrderClass_mapBoth
#print axioms AxisTrace.originalF45OrderClass_independent

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
