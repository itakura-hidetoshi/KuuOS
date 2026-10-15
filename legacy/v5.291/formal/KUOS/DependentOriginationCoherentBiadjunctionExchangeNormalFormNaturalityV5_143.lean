import KUOS.DependentOriginationCoherentBiadjunctionExchangeAxisPairEquivalenceV5_143

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid

set_option autoImplicit false
noncomputable section

/-!
# F46-D / v5.143 — functorial naturality of complete normal forms

F45 proved that extracting the original F19 and F28 complete
Type-valued primitive histories commutes with independently mapping
the F44 quotient under arbitrary genuine functors. F46-C identifies
the generated exchange quotient EXACTLY with the product of these
native histories.

We prove the inverse reconstruction map is natural as an honest
equality of quotient classes. This is stronger than mere equality
of transported endpoint Hom compositions and avoids introducing
any additional strictness or a G-side comparison inverse.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Functorial transport of the canonical F28-first class is the
canonical class of the two independently mapped original Type-valued
axis histories. This is an equality IN THE GENERATED EXCHANGE QUOTIENT
and does not ask any two original same-axis steps to commute. -/
theorem AxisTrace.pairToClass_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (histories : AxisTrace n ma mb × AxisTrace m pa pb) :
    ExchangeClass.mapBoth H K (AxisTrace.pairToClass histories) =
      AxisTrace.pairToClass
        (AxisTrace.mapBlocks H histories.1,
          AxisTrace.mapBlocks K histories.2) := by
  apply (ExchangeClass.axisTraceEquiv
    (ma := KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H ma)
    (mb := KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H mb)
    (pa := KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pa)
    (pb := KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pb)
    (n := n) (m := m)).injective
  calc
    (ExchangeClass.mapBoth H K (AxisTrace.pairToClass histories)).axisTraces =
        (AxisTrace.mapBlocks H (AxisTrace.pairToClass histories).axisTraces.1,
          AxisTrace.mapBlocks K (AxisTrace.pairToClass histories).axisTraces.2) :=
      ExchangeClass.axisTraces_mapBoth H K _
    _ = (AxisTrace.mapBlocks H histories.1, AxisTrace.mapBlocks K histories.2) := by
          rw [AxisTrace.pairToClass_axisTraces]
    _ = (AxisTrace.pairToClass
          (AxisTrace.mapBlocks H histories.1,
            AxisTrace.mapBlocks K histories.2)).axisTraces :=
      (AxisTrace.pairToClass_axisTraces _).symm

/-- Arbitrary original quotient classes normalize naturally through
independent F19/F28 functors; the square is witnessed in the exact
F44 exchange quotient, not merely in the F42 Prop relation. -/
theorem ExchangeClass.comparisonNormal_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    (ExchangeClass.mapBoth H K c).comparisonNormal.toClass =
      ExchangeClass.mapBoth H K c.comparisonNormal.toClass := by
  calc
    (ExchangeClass.mapBoth H K c).comparisonNormal.toClass =
        ExchangeClass.mapBoth H K c :=
      ExchangeClass.comparisonNormal_toClass _
    _ = ExchangeClass.mapBoth H K c.comparisonNormal.toClass :=
      congrArg (ExchangeClass.mapBoth H K)
        (ExchangeClass.comparisonNormal_toClass c).symm

/-- The reversible F46 classification commutes with functors in
both directions: extracting after functor transport is the same as
mapping each original history, and reconstructing after independent
mapping is the same as transporting the reconstructed class. -/
theorem ExchangeClass.axisTraceEquiv_naturality
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    (ExchangeClass.mapBoth H K c).axisTraces =
      (AxisTrace.mapBlocks H c.axisTraces.1,
        AxisTrace.mapBlocks K c.axisTraces.2) :=
  ExchangeClass.axisTraces_mapBoth H K c

#print axioms AxisTrace.pairToClass_mapBoth
#print axioms ExchangeClass.comparisonNormal_mapBoth
#print axioms ExchangeClass.axisTraceEquiv_naturality

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
