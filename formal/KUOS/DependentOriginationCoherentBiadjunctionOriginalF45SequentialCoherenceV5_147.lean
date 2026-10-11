import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedClassV5_146
import KUOS.DependentOriginationCoherentBiadjunctionF45OrderCompatibilityV5_144

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F50-A / v5.147 — sequential composition of the ORIGINAL F45 routes

F49 classified each actual ORIGINAL F45 modificationFirst / comparisonFirst
Type-valued execution, including its genuine Eq.mp/Nat.zero_add index
transport, in the F44 generated adjacent exchange quotient.

This file proves a *new* TWO-STAGE law: concatenating any two actual old
F45 exchange classes, with independently chosen orders on both stages,
equals the actual OLD F45 class built from the TWO independently appended
original F19/F28 Type-valued AxisTrace histories. A third, independently
chosen final order is permitted. The proof uses the F46 classification,
the proven genuine F44 quotient concatenation and complete histories.
No same-axis permutation, unlike Hom identification or inverse G-cell.

We also prove arbitrary independent honest functors preserve BOTH
primitive-history concatenation and F44 exchange-class concatenation,
so their action on a two-stage old F45 execution is exactly natural.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- TWO independent old-F45 stages concatenate to one old-F45 execution
on the exact native pair of concatenated Type-valued original
F19/F28 histories; all THREE choices of original F45 order may differ. -/
theorem AxisTrace.originalF45OrderClass_append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (first second whole : OriginalF45Order)
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc)
    (hc₁ : AxisTrace m pa pb) (hc₂ : AxisTrace m' pb pc) :
    ExchangeClass.append
        (AxisTrace.originalF45OrderClass first hm₁ hc₁)
        (AxisTrace.originalF45OrderClass second hm₂ hc₂) =
      AxisTrace.originalF45OrderClass whole
        (AxisTrace.append hm₁ hm₂)
        (AxisTrace.append hc₁ hc₂) := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    (ExchangeClass.append
        (AxisTrace.originalF45OrderClass first hm₁ hc₁)
        (AxisTrace.originalF45OrderClass second hm₂ hc₂)).axisTraces =
        (AxisTrace.append hm₁ hm₂, AxisTrace.append hc₁ hc₂) := by
      rw [ExchangeClass.axisTraces_append,
        AxisTrace.originalF45OrderClass_axisTraces,
        AxisTrace.originalF45OrderClass_axisTraces]
    _ = (AxisTrace.originalF45OrderClass whole
          (AxisTrace.append hm₁ hm₂)
          (AxisTrace.append hc₁ hc₂)).axisTraces :=
      (AxisTrace.originalF45OrderClass_axisTraces whole _ _).symm

/-- A sequential original-F45 mixed refinement preserves the genuine
original F43 two-axis finite refinement Prop, at exactly n+n' / m+m'
original primitive steps, even when the two real execution orders differ. -/
theorem AxisTrace.originalF45OrderClass_append_toInterleaving
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (first second : OriginalF45Order)
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc)
    (hc₁ : AxisTrace m pa pb) (hc₂ : AxisTrace m' pb pc) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
      (n + n') (m + m') ma pa mc pc :=
  (ExchangeClass.append
    (AxisTrace.originalF45OrderClass first hm₁ hc₁)
    (AxisTrace.originalF45OrderClass second hm₂ hc₂)).toInterleaving

/-- The F19 and genuine F28 original categorical Hom composites remain
equal after actual mixed-order sequential original F45 execution. -/
theorem AxisTrace.originalF45OrderClass_append_composites
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (first second : OriginalF45Order)
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc)
    (hc₁ : AxisTrace m pa pb) (hc₂ : AxisTrace m' pb pc) :
    ma.composite = mc.composite ∧ pa.composite = pc.composite :=
  (ExchangeClass.append
    (AxisTrace.originalF45OrderClass first hm₁ hc₁)
    (AxisTrace.originalF45OrderClass second hm₂ hc₂)).composites

/-- Independent genuine functors transport a *whole* Type-valued
single-axis primitive history concatenation ON THE NOSE; neither
original category is replaced by an auxiliary comparison chain. -/
theorem AxisTrace.mapBlocks_append
    {D' : Type uD'} [Category.{vD'} D']
    (H : D ⥤ D')
    {a b : D} {n n' : Nat}
    {ma mb mc : Blocks a b}
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc) :
    AxisTrace.mapBlocks H (AxisTrace.append hm₁ hm₂) =
      AxisTrace.append
        (AxisTrace.mapBlocks H hm₁)
        (AxisTrace.mapBlocks H hm₂) := by
  induction hm₂ with
  | refl =>
      rfl
  | snoc hm₂ step ih =>
      exact congrArg
        (fun t => AxisTrace.snoc t (oneStep_mapBlocks H step)) (ih hm₁)

/-- ORIGINAL two-axis F44 generated exchange quotient concatenation
is natural for independently chosen genuine functors on F19 and F28,
as an equality of real quotient classes, rather than merely arrows. -/
theorem ExchangeClass.mapBoth_append
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc) :
    ExchangeClass.mapBoth H K (ExchangeClass.append h k) =
      ExchangeClass.append
        (ExchangeClass.mapBoth H K h)
        (ExchangeClass.mapBoth H K k) := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    (ExchangeClass.mapBoth H K (ExchangeClass.append h k)).axisTraces =
      (AxisTrace.mapBlocks H (ExchangeClass.append h k).axisTraces.1,
       AxisTrace.mapBlocks K (ExchangeClass.append h k).axisTraces.2) :=
      ExchangeClass.axisTraces_mapBoth H K _
    _ =
      (AxisTrace.append
          (AxisTrace.mapBlocks H h.axisTraces.1)
          (AxisTrace.mapBlocks H k.axisTraces.1),
       AxisTrace.append
          (AxisTrace.mapBlocks K h.axisTraces.2)
          (AxisTrace.mapBlocks K k.axisTraces.2)) := by
        rw [ExchangeClass.axisTraces_append,
          AxisTrace.mapBlocks_append, AxisTrace.mapBlocks_append]
    _ = (ExchangeClass.append
          (ExchangeClass.mapBoth H K h)
          (ExchangeClass.mapBoth H K k)).axisTraces := by
        rw [ExchangeClass.axisTraces_append,
          ExchangeClass.axisTraces_mapBoth H K h,
          ExchangeClass.axisTraces_mapBoth H K k]

/-- The FULL sequential original-F45 history coherence is NATURAL:
map a genuine two-stage original execution across both independent
functors, then normalize with ANY original final order, or transport
the two original primitive histories first and append them. -/
theorem AxisTrace.originalF45OrderClass_append_mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (first second whole : OriginalF45Order)
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc)
    (hc₁ : AxisTrace m pa pb) (hc₂ : AxisTrace m' pb pc) :
    ExchangeClass.mapBoth H K
      (ExchangeClass.append
        (AxisTrace.originalF45OrderClass first hm₁ hc₁)
        (AxisTrace.originalF45OrderClass second hm₂ hc₂)) =
    AxisTrace.originalF45OrderClass whole
      (AxisTrace.append
        (AxisTrace.mapBlocks H hm₁)
        (AxisTrace.mapBlocks H hm₂))
      (AxisTrace.append
        (AxisTrace.mapBlocks K hc₁)
        (AxisTrace.mapBlocks K hc₂)) := by
  calc
    ExchangeClass.mapBoth H K
        (ExchangeClass.append
          (AxisTrace.originalF45OrderClass first hm₁ hc₁)
          (AxisTrace.originalF45OrderClass second hm₂ hc₂)) =
      ExchangeClass.mapBoth H K
        (AxisTrace.originalF45OrderClass whole
          (AxisTrace.append hm₁ hm₂)
          (AxisTrace.append hc₁ hc₂)) :=
      congrArg (ExchangeClass.mapBoth H K)
        (AxisTrace.originalF45OrderClass_append first second whole hm₁ hm₂ hc₁ hc₂)
    _ = AxisTrace.pairToClass
          (AxisTrace.mapBlocks H (AxisTrace.append hm₁ hm₂),
           AxisTrace.mapBlocks K (AxisTrace.append hc₁ hc₂)) :=
      AxisTrace.originalF45OrderClass_mapBoth H K whole _ _
    _ = AxisTrace.originalF45OrderClass whole
          (AxisTrace.append
            (AxisTrace.mapBlocks H hm₁)
            (AxisTrace.mapBlocks H hm₂))
          (AxisTrace.append
            (AxisTrace.mapBlocks K hc₁)
            (AxisTrace.mapBlocks K hc₂)) := by
      rw [AxisTrace.mapBlocks_append, AxisTrace.mapBlocks_append,
        (AxisTrace.originalF45OrderClass_eq_pair whole _ _).symm]

/-- Changing either of TWO actual ORIGINAL F45 stage execution orders
does not change the genuine concatenated F44 exchange class.
Independently changing the total historical F45 order does not
change its native canonical representation either: all SIX order
choices are used in these TWO actual Type-level quotient equations. -/
theorem AxisTrace.originalF45OrderClass_append_independent
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (first₁ first₂ second₁ second₂ whole₁ whole₂ : OriginalF45Order)
    (hm₁ : AxisTrace n ma mb) (hm₂ : AxisTrace n' mb mc)
    (hc₁ : AxisTrace m pa pb) (hc₂ : AxisTrace m' pb pc) :
    (ExchangeClass.append
        (AxisTrace.originalF45OrderClass first₁ hm₁ hc₁)
        (AxisTrace.originalF45OrderClass second₁ hm₂ hc₂) =
      ExchangeClass.append
        (AxisTrace.originalF45OrderClass first₂ hm₁ hc₁)
        (AxisTrace.originalF45OrderClass second₂ hm₂ hc₂)) ∧
    (AxisTrace.originalF45OrderClass whole₁
        (AxisTrace.append hm₁ hm₂)
        (AxisTrace.append hc₁ hc₂) =
     AxisTrace.originalF45OrderClass whole₂
        (AxisTrace.append hm₁ hm₂)
        (AxisTrace.append hc₁ hc₂)) := by
  constructor
  · calc
      ExchangeClass.append
          (AxisTrace.originalF45OrderClass first₁ hm₁ hc₁)
          (AxisTrace.originalF45OrderClass second₁ hm₂ hc₂) =
        AxisTrace.originalF45OrderClass whole₁
          (AxisTrace.append hm₁ hm₂)
          (AxisTrace.append hc₁ hc₂) :=
        AxisTrace.originalF45OrderClass_append
          first₁ second₁ whole₁ hm₁ hm₂ hc₁ hc₂
      _ = ExchangeClass.append
            (AxisTrace.originalF45OrderClass first₂ hm₁ hc₁)
            (AxisTrace.originalF45OrderClass second₂ hm₂ hc₂) :=
        (AxisTrace.originalF45OrderClass_append
          first₂ second₂ whole₁ hm₁ hm₂ hc₁ hc₂).symm
  · exact AxisTrace.originalF45OrderClass_independent
      whole₁ whole₂ (AxisTrace.append hm₁ hm₂) (AxisTrace.append hc₁ hc₂)

#print axioms AxisTrace.originalF45OrderClass_append
#print axioms AxisTrace.originalF45OrderClass_append_toInterleaving
#print axioms AxisTrace.originalF45OrderClass_append_composites
#print axioms AxisTrace.mapBlocks_append
#print axioms ExchangeClass.mapBoth_append
#print axioms AxisTrace.originalF45OrderClass_append_mapBoth
#print axioms AxisTrace.originalF45OrderClass_append_independent

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
