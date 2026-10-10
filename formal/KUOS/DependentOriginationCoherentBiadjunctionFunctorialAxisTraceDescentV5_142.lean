import KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140

set_option autoImplicit false
noncomputable section

/-!
# F45-B / v5.142 — naturality of extracted independent histories

Two unrelated honest original functors act independently on the real
F19 and F28 axis histories. Projection of the full F44 exchange class
commutes with this functorial transport as an actual equality of
Type-valued independent histories, not merely of the evaluated Hom.

All primitive moves and their exact counts are transported by the
unchanged F43 functorial OneStep map; no strictification of a
pseudofunctor or artificial inverse of G's lax cell is used.
-/


open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140.Grid

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Transport a single ORIGINAL Type-valued axis history while
preserving its exact original number n of primitive operations. -/
def AxisTrace.mapBlocks
    {D' : Type uD'} [Category.{vD'} D']
    (H : D ⥤ D')
    {a b : D} {n : Nat}
    {p q : Blocks a b} (h : AxisTrace n p q) :
    AxisTrace n (mapBlocks H p) (mapBlocks H q) := by
  induction h with
  | refl p =>
      exact AxisTrace.refl (mapBlocks H p)
  | snoc h step ih =>
      exact AxisTrace.snoc ih (oneStep_mapBlocks H step)

/-- Full original F44 ordered transport preserves the F19 axis
history ON THE NOSE, not just its underlying F42 Prop certificate. -/
theorem OrderedInterleaving.modificationTrace_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.mapBoth H K h).modificationTrace =
      AxisTrace.mapBlocks H h.modificationTrace := by
  induction h with
  | refl mods pq =>
      rfl
  | modification h step ih =>
      exact congrArg (fun t => AxisTrace.snoc t (oneStep_mapBlocks H step)) ih
  | comparison h step ih =>
      exact ih

/-- Full original F44 ordered transport preserves the distinct F28
quotient-comparison axis history ON THE NOSE. -/
theorem OrderedInterleaving.comparisonTrace_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.mapBoth H K h).comparisonTrace =
      AxisTrace.mapBlocks K h.comparisonTrace := by
  induction h with
  | refl mods pq =>
      rfl
  | modification h step ih =>
      exact ih
  | comparison h step ih =>
      exact congrArg (fun t => AxisTrace.snoc t (oneStep_mapBlocks K step)) ih

/-- The central commuting square of F45: carrying a full
exchange class through two original functors and then extracting its
proof-relevant axis histories is EXACTLY the same as first extracting
them and then functorially mapping each independent typed axis.

This is a genuinely Type-valued quotient descent with BOTH axes;
the relation identifies no distinct original same-axis histories. -/
theorem ExchangeClass.axisTraces_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    (ExchangeClass.mapBoth H K c).axisTraces =
      (AxisTrace.mapBlocks H c.axisTraces.1,
        AxisTrace.mapBlocks K c.axisTraces.2) := by
  refine Quot.induction_on c ?_
  intro route
  exact Prod.ext
    (OrderedInterleaving.modificationTrace_mapBoth H K route)
    (OrderedInterleaving.comparisonTrace_mapBoth H K route)

/-- Taking F42 original traces after genuine functorial transport
agrees with transporting the F45 Type-level witness separately. -/
theorem AxisTrace.mapBlocks_toTrace
    {D' : Type uD'} [Category.{vD'} D']
    (H : D ⥤ D')
    {a b : D} {n : Nat} {p q : Blocks a b}
    (h : AxisTrace n p q) :
    (AxisTrace.mapBlocks H h).toTrace =
      trace_mapBlocks H h.toTrace := by
  apply Subsingleton.elim

#print axioms AxisTrace.mapBlocks
#print axioms OrderedInterleaving.modificationTrace_mapBoth
#print axioms OrderedInterleaving.comparisonTrace_mapBoth
#print axioms ExchangeClass.axisTraces_mapBoth
#print axioms AxisTrace.mapBlocks_toTrace

end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
