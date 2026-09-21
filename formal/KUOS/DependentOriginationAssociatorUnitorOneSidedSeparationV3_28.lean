import KUOS.DependentOriginationAssociatorUnitorWEdgeSeparationV3_27

namespace KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28

open CategoryTheory
open CategoryTheory.Bicategory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorWEdgeSeparationV3_27

universe u v uH vH u₁ v₁ u₂ v₂ u₃ v₃

set_option autoImplicit false

/-!
# One-sided separation for the associator-unitor residual v3.28

v3.27 kills the v3.26 double-whiskering kernel when both outer representative
functors are equivalences.  That is stronger than the cancellation argument
actually needs.

For a natural transformation `α : H ⟶ K`:

* precomposition `α ↦ F.whiskerLeft α` is injective when `F` is essentially
  surjective: equality on the essential image determines all components by
  naturality across the chosen object-preimage isomorphisms;
* postcomposition `α ↦ Functor.whiskerRight α G` is injective when `G` is
  faithful, by Mathlib's standard faithful-whiskering instance.

Therefore the v3.26 map

  η ↦ F ◁ (η ▷ G)

is injective already from the one-sided conditions

  F.EssSurj  and  G.Faithful.

This is strictly weaker than requiring both outer representative functors to be
equivalences, and it applies directly to arbitrary localization arrows whenever
their chosen representative evaluations satisfy those two properties.
-/

/-- Precomposition by an essentially-surjective functor is injective on natural
transformations.

This is the generic cancellation lemma behind the left half of the v3.28
double-whiskering argument.  It follows the same object-preimage/naturality
pattern used by Mathlib's localization `natTrans_ext`, but requires only
`EssSurj F`, not a localization structure. -/
theorem natTrans_eq_of_whiskerLeft_eq_of_essSurj
    {C : Type u₁} [Category.{v₁} C]
    {D : Type u₂} [Category.{v₂} D]
    {E : Type u₃} [Category.{v₃} E]
    (F : C ⥤ D) [F.EssSurj]
    {H K : D ⥤ E} {α β : H ⟶ K}
    (h : Functor.whiskerLeft F α = Functor.whiskerLeft F β) :
    α = β := by
  ext Y
  rw [← cancel_epi (H.map (F.objObjPreimageIso Y).hom),
    α.naturality, β.naturality]
  have hApp :=
    congr_fun (congrArg NatTrans.app h) (F.objPreimage Y)
  change
    α.app (F.obj (F.objPreimage Y)) =
      β.app (F.obj (F.objPreimage Y)) at hApp
  rw [hApp]

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The exact one-sided criterion sufficient for v3.26 separation in `Cat`:
the left outer representative need only be essentially surjective and the
right outer representative need only be faithful. -/
theorem middleIdentityWhiskerSeparating_of_essSurj_faithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hF :
      (quotientRepresentativeMap W R D f).toFunctor.EssSurj)
    (hG :
      (quotientRepresentativeMap W R D g).toFunctor.Faithful) :
    MiddleIdentityWhiskerSeparating W R D f g := by
  let F := quotientRepresentativeMap W R D f
  let G := quotientRepresentativeMap W R D g
  letI : F.toFunctor.EssSurj := by
    simpa [F] using hF
  letI : G.toFunctor.Faithful := by
    simpa [G] using hG
  intro η θ h
  apply Cat.Hom₂.ext
  have hNat :
      F.toFunctor.whiskerLeft
          (Functor.whiskerRight η.toNatTrans G.toFunctor) =
        F.toFunctor.whiskerLeft
          (Functor.whiskerRight θ.toNatTrans G.toFunctor) := by
    simpa [F, G] using congrArg (fun k => k.toNatTrans) h
  have hRight :
      Functor.whiskerRight η.toNatTrans G.toFunctor =
        Functor.whiskerRight θ.toNatTrans G.toFunctor :=
    natTrans_eq_of_whiskerLeft_eq_of_essSurj F.toFunctor hNat
  exact
    ((Functor.whiskeringRight
      (R.obj (.mk Y.as.obj))
      (R.obj (.mk Y.as.obj))
      (R.obj (.mk Z.as.obj))).obj G.toFunctor).map_injective hRight

/-- The v3.27 equivalence criterion factors through the strictly weaker v3.28
one-sided criterion. -/
theorem middleIdentityWhiskerSeparating_of_isEquivalence_via_oneSided
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hF :
      (quotientRepresentativeMap W R D f).toFunctor.IsEquivalence)
    (hG :
      (quotientRepresentativeMap W R D g).toFunctor.IsEquivalence) :
    MiddleIdentityWhiskerSeparating W R D f g := by
  let F := quotientRepresentativeMap W R D f
  let G := quotientRepresentativeMap W R D g
  letI : F.toFunctor.IsEquivalence := by
    simpa [F] using hF
  letI : G.toFunctor.IsEquivalence := by
    simpa [G] using hG
  exact
    middleIdentityWhiskerSeparating_of_essSurj_faithful
      W R D f g
      (by
        simpa [F] using
          (inferInstance : F.toFunctor.EssSurj))
      (by
        simpa [G] using
          (inferInstance : G.toFunctor.Faithful))

/-- The actual associator/right-unitor/left-unitor overlap-star triangle closes
under the one-sided `EssSurj/Faithful` criterion, without requiring either
outer representative to be an equivalence. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_essSurj_faithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hF :
      (quotientRepresentativeMap W R D f).toFunctor.EssSurj)
    (hG :
      (quotientRepresentativeMap W R D g).toFunctor.Faithful)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator f (𝟙 Y) g))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qt Qu := by
  exact
    associatorAnchor_unitor_overlapStar_triangle_of_separating
      W R D f g Qs Qt Qu hQs hQt hQu hst hsu
      (middleIdentityWhiskerSeparating_of_essSurj_faithful
        W R D f g hF hG)

/-!
## Frontier after v3.28

The residual boundary is now sharper than v3.27.

The mixed triangle does not need invertibility of both outer representative
functors.  It needs only the exact directional cancellation used by the proof:

* the left representative reaches every middle-fiber object up to isomorphism;
* the right representative reflects equality of morphisms.

Hence the obstruction can survive only when at least one of these two
directional properties fails.

For generated localization paths this suggests the next theorem unit should
track `EssSurj` and `Faithful` separately through the free-path evaluator:

1. formal W-inverse steps are equivalences, hence have both properties;
2. ordinary raw arrows outside W need not have either property;
3. composition preserves the relevant property when every factor on that side
   has it.

The next truth-test is therefore path-level propagation: characterize concrete
generated paths whose evaluations are essentially surjective or faithful, and
use that characterization to enlarge the class of mixed triangles closed
without any extra separation axiom.
-/

end KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
