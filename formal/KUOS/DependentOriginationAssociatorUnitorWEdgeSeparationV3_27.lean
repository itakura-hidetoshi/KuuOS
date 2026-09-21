import KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26

namespace KUOS.DependentOriginationAssociatorUnitorWEdgeSeparationV3_27

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26

universe u v uH vH

set_option autoImplicit false

/-!
# Associator-unitor W-edge separation v3.27

v3.26 localizes the first genuinely mixed associator/unitor obstruction in the
kernel of double whiskering

  η ↦ F ◁ (η ▷ G).

Because the target bicategory is `Cat`, that kernel disappears whenever the
outer representative functors are equivalences: pre- and post-composition by an
equivalence are faithful on natural transformations.

The generated localization construction gives this situation canonically for
raw presentation arrows that lie in `W`.  The generated presentation comparison
identifies the quotient representative of `W.Q.map f` with the original raw
functor `R.map f`; v2.56 makes the latter an equivalence whenever `W f`.

Thus no additional separation axiom is needed on mixed triangles whose two outer
edges are images of arrows in `W`.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A quotient representative of a raw presentation arrow in `W` is an
equivalence of categories.

This is transported across the canonical generated presentation natural
isomorphism; it is not a new assumption on the quotient representative. -/
theorem quotientRepresentativeMap_Q_map_isEquivalence
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) (hf : W f) :
    (quotientRepresentativeMap W R D (W.Q.map f)).toFunctor.IsEquivalence := by
  have hRaw : (R.map f.toLoc).toFunctor.IsEquivalence := by
    rw [← D.chosen_functor f hf]
    infer_instance
  exact
    (Functor.isEquivalence_iff_of_iso
      (Cat.Hom.toNatIso (generatedPresentationMapIso W R D f))).2 hRaw

/-- In `Cat`, double whiskering is injective when both outer 1-cells are
equivalences.  Mathlib supplies equivalence, hence faithful, instances for the
left- and right-whiskering functors on functor categories. -/
theorem middleIdentityWhiskerSeparating_of_isEquivalence
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
        Functor.whiskerRight θ.toNatTrans G.toFunctor := by
    apply
      ((Functor.whiskeringLeft
        (R.obj (.mk X.as.obj))
        (R.obj (.mk Y.as.obj))
        (R.obj (.mk Z.as.obj))).obj F.toFunctor).map_injective
    simpa using hNat
  apply
    ((Functor.whiskeringRight
      (R.obj (.mk Y.as.obj))
      (R.obj (.mk Y.as.obj))
      (R.obj (.mk Z.as.obj))).obj G.toFunctor).map_injective
  simpa using hRight

/-- The v3.26 separation condition is automatic when the two outer localization
arrows are images of raw `W`-arrows. -/
theorem middleIdentityWhiskerSeparating_of_W_presentation_edges
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : W f) (hg : W g) :
    MiddleIdentityWhiskerSeparating W R D (W.Q.map f) (W.Q.map g) := by
  exact
    middleIdentityWhiskerSeparating_of_isEquivalence
      W R D (W.Q.map f) (W.Q.map g)
      (quotientRepresentativeMap_Q_map_isEquivalence W R D f hf)
      (quotientRepresentativeMap_Q_map_isEquivalence W R D g hg)

/-- Consequently the actual associator/right-unitor/left-unitor overlap-star
triangle closes automatically on `W`-presentation edges. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_W_presentation_edges
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : W f) (hg : W g)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g)))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D
        (.rightUnitor (W.Q.map f)))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D
        (.leftUnitor (W.Q.map g)))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g))
      (.rightUnitor (W.Q.map f)) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g))
      (.leftUnitor (W.Q.map g)) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor (W.Q.map f)) (.leftUnitor (W.Q.map g)) Qt Qu := by
  exact
    associatorAnchor_unitor_overlapStar_triangle_of_separating
      W R D (W.Q.map f) (W.Q.map g) Qs Qt Qu
      hQs hQt hQu hst hsu
      (middleIdentityWhiskerSeparating_of_W_presentation_edges
        W R D f g hf hg)

/-!
## Frontier after v3.27

The v3.26 kernel obstruction is not present on the `W`-generated invertible
part of the localization: generated presentation comparison plus pointwise
W-adjoint equivalence makes both outer representative functors equivalences,
and Mathlib faithfulness of whiskering cancels the residual exactly.

This is a genuine positive closure theorem, but it does not yet cover arbitrary
localized arrows.  A general localization morphism may contain ordinary raw
arrows outside `W`; the current hypotheses do not make their evaluated functors
equivalences.  The next truth-test is therefore narrower:

* determine whether the generated path structure provides enough one-sided
  faithfulness / essential-surjectivity for arbitrary representative paths; or
* exhibit an actual Cat-valued generated path where the double-whiskering kernel
  is nontrivial.

The residual is now absent on the invertible W-spine and confined to genuinely
noninvertible outer presentation data.
-/

end KUOS.DependentOriginationAssociatorUnitorWEdgeSeparationV3_27
