import KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96
import KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04
import KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08

open CategoryTheory
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Coherent StrongTrans extension assembly v5.08

v5.07 provides a quotient-independent canonical naturality isomorphism for
every actual morphism of the constructed localization.  The v4.96 reduced
extension package, however, is indexed by one-cells of the locally-discrete
double-opposite source.

This file first bridges those two presentations and then reconnects the
quotient-level canonical family with the already validated v5.01 identity,
v4.99 composition, and v4.97 raw-presentation restriction data.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical v5.07 naturality, reindexed directly by a one-cell of the
locally-discrete source used by the higher localized systems. -/
noncomputable def higherLocalizedCanonicalStrongTransNaturalityOnSource
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) :
    F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f := by
  let g := f.as.unop.unop
  simpa [g] using
    (higherLocalizedCanonicalStrongTransNaturality
      (W := W) gamma g)

set_option backward.isDefEq.respectTransparency false in
/-- On a singleton ordinary localization path, the retained path evaluator is
exactly the v4.97 presentation-arrow naturality. -/
theorem higherLocalizedStrongTransPathNaturality_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context}
    (f : X ⟶ Y) :
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma
        (Localization.Construction.ψ₁ W f.as) =
      higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma f := by
  rfl

/-- Evaluating the quotient arrow `Q(f)` through its canonical singleton
ordinary path representative gives exactly the v4.97 presentation naturality. -/
theorem higherLocalizedStrongTransQuotientRepresentativeNaturality_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context}
    (f : X ⟶ Y) :
    higherLocalizedStrongTransQuotientRepresentativeNaturality
        (W := W) gamma
        (W.Q.map f.as)
        (Localization.Construction.ψ₁ W f.as)
        rfl =
      higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma f := by
  change
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (Iso.refl _)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma
          (Localization.Construction.ψ₁ W f.as)) =
      higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma f
  rw [higherLocalizedStrongTransNaturalityTransport_refl]
  exact
    higherLocalizedStrongTransPathNaturality_presentation
      (W := W) gamma f

/-- The v5.07 canonical quotient family restricts on presentation-image arrows
to the v4.97 canonical presentation naturality. -/
theorem higherLocalizedCanonicalStrongTransNaturality_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context}
    (f : X ⟶ Y) :
    higherLocalizedCanonicalStrongTransNaturality
        (W := W) gamma (W.Q.map f.as) =
      higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma f := by
  have hcanonical :=
    higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_canonical
      (W := W) gamma
      (W.Q.map f.as)
      (Localization.Construction.ψ₁ W f.as)
      rfl
  exact
    hcanonical.symm.trans
      (higherLocalizedStrongTransQuotientRepresentativeNaturality_presentation
        (W := W) gamma f)

/-- Source-indexed form of the preceding presentation bridge. -/
theorem higherLocalizedCanonicalStrongTransNaturalityOnSource_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context}
    (f : X ⟶ Y) :
    higherLocalizedCanonicalStrongTransNaturalityOnSource
        (W := W) gamma
        ((higherPresentationUnitFunctor W).toPseudofunctor.map f) =
      higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma f := by
  simpa [higherLocalizedCanonicalStrongTransNaturalityOnSource,
    higherPresentationUnitFunctor] using
    (higherLocalizedCanonicalStrongTransNaturality_presentation
      (W := W) gamma f)

/-- The source-indexed canonical family satisfies the exact raw
presentation restriction square required by v4.96. -/
theorem higherLocalizedCanonicalStrongTransNaturalityOnSource_restrictionSquare
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context}
    (f : X ⟶ Y) :
    (restrictHigherLocalizedSystem W F).map f ◁
          𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y)) ≫
        (gamma.naturality f).hom =
      (higherLocalizedCanonicalStrongTransNaturalityOnSource
          (W := W) gamma
          ((higherPresentationUnitFunctor W).toPseudofunctor.map f)).hom ≫
        𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ▷
          (restrictHigherLocalizedSystem W G).map f := by
  rw [higherLocalizedCanonicalStrongTransNaturalityOnSource_presentation]
  exact
    higherLocalizedStrongTransPresentationNaturality_restrictionSquare
      (W := W) gamma f

/-- On the identity of an actual localized object, the v5.07 quotient-level
canonical family is exactly the v5.01 canonical identity naturality. -/
theorem higherLocalizedCanonicalStrongTransNaturality_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : W.Localization) :
    higherLocalizedCanonicalStrongTransNaturality
        (W := W) gamma (𝟙 X) =
      higherLocalizedStrongTransNaturality_id
        (W := W) gamma (.mk (op (op X))) := by
  have hcanonical :=
    higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_canonical
      (W := W) gamma
      (𝟙 X)
      (𝟙 X.as)
      rfl
  have hrepresentative :
      higherLocalizedStrongTransQuotientRepresentativeNaturality
          (W := W) gamma
          (𝟙 X)
          (𝟙 X.as)
          rfl =
        higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op X))) := by
    change
      higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma (Iso.refl _)
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma (𝟙 X.as)) =
        higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op X)))
    rw [higherLocalizedStrongTransNaturalityTransport_refl]
    change
      higherLocalizedStrongTransPathNaturality
          (W := W) gamma (𝟙 X.as) =
        higherLocalizedStrongTransNaturality_id
          (W := W) gamma (higherLocalizedPathObject W X.as)
    exact
      higherLocalizedStrongTransPathNaturality_id
        (W := W) gamma X.as
  exact hcanonical.symm.trans hrepresentative

/-- Source-indexed form of quotient identity normalization. -/
theorem higherLocalizedCanonicalStrongTransNaturalityOnSource_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    higherLocalizedCanonicalStrongTransNaturalityOnSource
        (W := W) gamma (𝟙 a) =
      higherLocalizedStrongTransNaturality_id
        (W := W) gamma a := by
  let X := a.as.unop.unop
  simpa [higherLocalizedCanonicalStrongTransNaturalityOnSource, X] using
    (higherLocalizedCanonicalStrongTransNaturality_id
      (W := W) gamma X)

/-- The source-indexed canonical quotient family satisfies exactly the v4.96
identity coherence field. -/
theorem higherLocalizedCanonicalStrongTransNaturalityOnSource_id_coherence
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    (higherLocalizedCanonicalStrongTransNaturalityOnSource
        (W := W) gamma (𝟙 a)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapId a).hom =
      (F.mapId a).hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
        (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).hom ≫
        (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).inv := by
  rw [higherLocalizedCanonicalStrongTransNaturalityOnSource_id]
  exact
    higherLocalizedStrongTransNaturality_id_coherence
      (W := W) gamma a

/-- Representative-level quotient naturality is compatible with the canonical
v4.99 composition constructor.  The proof keeps the two source transports
separate, composes them only after applying the generic whisker-transport laws,
and uses locally-discrete presentation independence only at the final source
comparison. -/
theorem higherLocalizedStrongTransQuotientRepresentativeNaturality_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (p : X.as ⟶ Y.as) (q : Y.as ⟶ Z.as)
    (hp :
      (higherLocalizedPathQuotientFunctor W).map p = f)
    (hq :
      (higherLocalizedPathQuotientFunctor W).map q = g) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        f.op.op.toLoc
        g.op.op.toLoc
        (higherLocalizedStrongTransQuotientRepresentativeNaturality
          (W := W) gamma f p hp)
        (higherLocalizedStrongTransQuotientRepresentativeNaturality
          (W := W) gamma g q hq) =
      higherLocalizedStrongTransQuotientRepresentativeNaturality
        (W := W) gamma
        (f ≫ g)
        (p ≫ q)
        (by
          simpa only [Functor.map_comp, hp, hq]) := by
  let etaF :=
    higherLocalizedQuotientRepresentativePathArrowIso
      (W := W) f p hp
  let etaG :=
    higherLocalizedQuotientRepresentativePathArrowIso
      (W := W) g q hq
  have hpq :
      (higherLocalizedPathQuotientFunctor W).map (p ≫ q) = f ≫ g := by
    simpa only [Functor.map_comp, hp, hq]
  let etaFG :=
    higherLocalizedQuotientRepresentativePathArrowIso
      (W := W) (f ≫ g) (p ≫ q) hpq
  let etaFRight :=
    Bicategory.whiskerRightIso etaF g.op.op.toLoc
  let etaGLeft :=
    Bicategory.whiskerLeftIso
      (higherLocalizedPathArrow W p) etaG
  change
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        f.op.op.toLoc
        g.op.op.toLoc
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaF
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma p))
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaG
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma q)) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma etaFG
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma (p ≫ q))
  have hFirst :=
    higherLocalizedStrongTransNaturality_comp_transport_first
      (W := W) gamma
      etaF
      (higherLocalizedStrongTransPathNaturality
        (W := W) gamma p)
      g.op.op.toLoc
      (higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma etaG
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q))
  have hSecond :=
    higherLocalizedStrongTransNaturality_comp_transport_second
      (W := W) gamma
      (higherLocalizedPathArrow W p)
      (higherLocalizedStrongTransPathNaturality
        (W := W) gamma p)
      etaG
      (higherLocalizedStrongTransPathNaturality
        (W := W) gamma q)
  have hSecondOuter :=
    congrArg
      (fun naturality_pg =>
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFRight naturality_pg)
      hSecond
  have hTransport :=
    higherLocalizedStrongTransNaturalityTransport_trans
      (W := W) gamma
      etaFRight etaGLeft
      (higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (higherLocalizedPathArrow W p)
        (higherLocalizedPathArrow W q)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma p)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q))
  have hPath :=
    higherLocalizedStrongTransPathNaturality_comp
      (W := W) gamma p q
  have hPathOuter :=
    congrArg
      (fun naturality_pq =>
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma (etaFRight ≪≫ etaGLeft) naturality_pq)
      hPath
  calc
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFRight
          (higherLocalizedStrongTransNaturality_comp
            (W := W) gamma
            (higherLocalizedPathArrow W p)
            g.op.op.toLoc
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma p)
            (higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma etaG
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma q))) :=
      hFirst
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFRight
          (higherLocalizedStrongTransNaturalityTransport
            (W := W) gamma etaGLeft
            (higherLocalizedStrongTransNaturality_comp
              (W := W) gamma
              (higherLocalizedPathArrow W p)
              (higherLocalizedPathArrow W q)
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma p)
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma q))) :=
      hSecondOuter
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma (etaFRight ≪≫ etaGLeft)
          (higherLocalizedStrongTransNaturality_comp
            (W := W) gamma
            (higherLocalizedPathArrow W p)
            (higherLocalizedPathArrow W q)
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma p)
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma q)) :=
      hTransport
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma (etaFRight ≪≫ etaGLeft)
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma (p ≫ q)) :=
      hPathOuter
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFG
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma (p ≫ q)) :=
      higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
        (W := W) gamma
        (etaFRight ≪≫ etaGLeft)
        etaFG
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma (p ≫ q))

/-! ## Regression checks -/

#print axioms higherLocalizedCanonicalStrongTransNaturalityOnSource
#print axioms higherLocalizedStrongTransPathNaturality_presentation
#print axioms higherLocalizedStrongTransQuotientRepresentativeNaturality_presentation
#print axioms higherLocalizedCanonicalStrongTransNaturality_presentation
#print axioms higherLocalizedCanonicalStrongTransNaturalityOnSource_presentation
#print axioms higherLocalizedCanonicalStrongTransNaturalityOnSource_restrictionSquare
#print axioms higherLocalizedCanonicalStrongTransNaturality_id
#print axioms higherLocalizedCanonicalStrongTransNaturalityOnSource_id
#print axioms higherLocalizedCanonicalStrongTransNaturalityOnSource_id_coherence
#print axioms higherLocalizedStrongTransQuotientRepresentativeNaturality_comp

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08
