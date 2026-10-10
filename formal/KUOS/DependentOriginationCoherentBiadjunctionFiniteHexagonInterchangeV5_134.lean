import KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
import KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonInterchangeV5_134

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133

set_option autoImplicit false
noncomputable section

/-!
# F37/v5.134: independent two-dimensional finite vertical/horizontal pasting

The F36 finite paths consist of ACTUAL composable F28 quotient-category
arrows (NOT F26 comparison chains). The independent F35 hexagon is the
ACTUAL four-stage F31/F34 associator/exchange NatIso. We prove the
interchange of these two constructions with an additional arbitrary
natural transformation, WITHOUT requiring it to be invertible.

This is ordinary quotient-category natural-transformation higher
coherence; it is not an ambient bicategory biequivalence or a claim
of arbitrary tricategorical modification interchange.
-/

namespace Higher
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133.Chain

universe u v uE vE
variable {D : Type u} [Category.{v} D]

/-- Two independent natural transformations can be vertically pasted
across EVERY finite categorical path. The proof uses BOTH F36 inductive
naturality equations, retaining the intermediate functor M. -/
theorem Path.verticalPasting {E : Type uE} [Category.{vE} E]
    {L M R : D ⥤ E} (α : L ⟶ M) (β : M ⟶ R)
    {x y : D} (p : Path x y) :
    (L.map p.composite ≫ α.app y) ≫ β.app y =
      α.app x ≫ (β.app x ≫ R.map p.composite) := by
  calc
    (L.map p.composite ≫ α.app y) ≫ β.app y =
        (α.app x ≫ M.map p.composite) ≫ β.app y := by
          rw [Path.naturality α p]
    _ = α.app x ≫ (M.map p.composite ≫ β.app y) :=
      Category.assoc _ _ _
    _ = α.app x ≫ (β.app x ≫ R.map p.composite) := by
      rw [Path.naturality β p]

/-- Finite vertical pasting remains exact under a split into any TWO
finite paths, not just the F35 two individual arrows. -/
theorem Path.verticalPasting_append {E : Type uE} [Category.{vE} E]
    {L M R : D ⥤ E} (α : L ⟶ M) (β : M ⟶ R)
    {x y z : D} (p : Path x y) (q : Path y z) :
    ((L.map p.composite ≫ L.map q.composite) ≫ α.app z) ≫ β.app z =
      α.app x ≫ (β.app x ≫
        (R.map p.composite ≫ R.map q.composite)) := by
  simpa only [Path.composite_append, Functor.map_comp] using
    (Path.verticalPasting α β (p.append q))

/-- Higher vertical pasting is independent of which BINARY
parenthesization evaluates a fixed ordered finite categorical path. -/
theorem Bracketing.verticalPasting {E : Type uE} [Category.{vE} E]
    {L M R : D ⥤ E} (α : L ⟶ M) (β : M ⟶ R)
    {x y : D} (p : Bracketing x y) :
    (L.map p.evaluated ≫ α.app y) ≫ β.app y =
      α.app x ≫ (β.app x ≫ R.map p.evaluated) := by
  simpa only [Bracketing.evaluated_eq_flattened] using
    (Path.verticalPasting α β p.flattened)

end Higher

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- The original F35 four-stage NATIVE F28 quotient hexagon exchanges
with the vertical composition of an arbitrary finite F36 arrow path.
The very same finite square is equal, on BOTH sides, to the original
direct F34 exchange, by the F35 NatIso-level hexagon theorem. -/
theorem kernelStagewiseHexagonFiniteInterchange
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF cF aG cG
        (vF ≫ uF) (vG ≫ uG)
    let stagewise := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let direct := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG (vF ≫ uF) (vG ≫ uG) wF wG
    (L.map p.composite ≫ stagewise.hom.app y =
      stagewise.hom.app x ≫ R.map p.composite) ∧
    (L.map p.composite ≫ stagewise.hom.app y =
      L.map p.composite ≫ direct.hom.app y) ∧
    (stagewise.hom.app x ≫ R.map p.composite =
      direct.hom.app x ≫ R.map p.composite) := by
  dsimp only
  let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
    (vF ≫ uF) (vG ≫ uG) ⋙
    rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG
  let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
    leftKernelQuotientWhiskerFunctor aF cF aG cG
      (vF ≫ uF) (vG ≫ uG)
  let stagewise := kernelMixedHexagonStagewiseLongNatIso
    aF bF aG bG uF uG vF vG wF wG
  let direct := kernelQuotientHorizontalExchangeNatIso
    aF bF aG bG (vF ≫ uF) (vG ≫ uG) wF wG
  change (L.map p.composite ≫ stagewise.hom.app y =
    stagewise.hom.app x ≫ R.map p.composite) ∧
    (L.map p.composite ≫ stagewise.hom.app y =
      L.map p.composite ≫ direct.hom.app y) ∧
    (stagewise.hom.app x ≫ R.map p.composite =
      direct.hom.app x ≫ R.map p.composite)
  have h : stagewise = direct :=
    kernelMixedHexagonStagewiseNatIso_coherence aF bF aG bG
      uF uG vF vG wF wG
  constructor
  · exact Chain.Path.naturality stagewise.hom p
  constructor <;> rw [h]

/-- After the original FOUR horizontal hexagon stages, a SECOND
arbitrary (possibly noninvertible) quotient-category NatTrans may be
vertically pasted: an actual two-dimensional naturality interchanger
for any finite comparison path. -/
theorem kernelStagewiseHexagonFiniteVerticalPasting
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory dF cF dG cG)
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF cF aG cG
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG
    let stagewise := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    (L.map p.composite ≫ stagewise.hom.app y) ≫ β.app y =
      stagewise.hom.app x ≫ (β.app x ≫ T.map p.composite) := by
  dsimp only
  exact Higher.Path.verticalPasting
    (kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom β p

/-- All ways to split an arbitrary finite F28 quotient path retain
the same two-dimensional hexagon/second-transformation pasting. -/
theorem kernelStagewiseHexagonFiniteVerticalAppend
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory dF cF dG cG)
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF cF aG cG
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y z : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y) (q : Chain.Path y z) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG
    let stagewise := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    ((L.map p.composite ≫ L.map q.composite) ≫
      stagewise.hom.app z) ≫ β.app z =
    stagewise.hom.app x ≫ (β.app x ≫
      (T.map p.composite ≫ T.map q.composite)) := by
  dsimp only
  exact Higher.Path.verticalPasting_append
    (kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom β p q

/-- Arbitrary binary bracketing of the same ordered path is compatible
with both the FOUR-stage structural hexagon and a second NatTrans. -/
theorem kernelStagewiseHexagonBracketedVerticalPasting
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory dF cF dG cG)
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF cF aG cG
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Bracketing x y) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG
    let stagewise := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    (L.map p.evaluated ≫ stagewise.hom.app y) ≫ β.app y =
      stagewise.hom.app x ≫ (β.app x ≫ T.map p.evaluated) := by
  dsimp only
  exact Higher.Bracketing.verticalPasting
    (kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom β p

#print axioms Higher.Path.verticalPasting
#print axioms Higher.Path.verticalPasting_append
#print axioms Higher.Bracketing.verticalPasting
#print axioms kernelStagewiseHexagonFiniteInterchange
#print axioms kernelStagewiseHexagonFiniteVerticalPasting
#print axioms kernelStagewiseHexagonFiniteVerticalAppend
#print axioms kernelStagewiseHexagonBracketedVerticalPasting

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonInterchangeV5_134
