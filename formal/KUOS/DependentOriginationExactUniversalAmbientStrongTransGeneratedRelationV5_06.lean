import KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
import KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06

open CategoryTheory
open CategoryTheory.Functor
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Generated-relation StrongTrans naturality v5.06

v5.04 and v5.05 close the four localization generators for the canonical
StrongTrans naturality data.  This file begins the generated-relation descent
without introducing a new relation language: it reuses the retained
Type-valued syntax from v2.68.

The first step is a canonical evaluator on the free path category
`Paths (Localization.Construction.LocQuiver W)`.  It is built only from the
already validated canonical constructors:

* identity: v5.01;
* ordinary presentation edge: v4.97;
* formal W-inverse edge: v5.05/v4.98;
* nonempty-prefix path composition: v4.99.

Singleton paths are normalized directly to their generator naturality.  This
avoids inserting a spurious leading identity-composition layer and makes the
retained localization generators line up definitionally with v5.04/v5.05.

The next step will prove invariance of this evaluator under
`LocalizationGenerating2Cell`, then extend structurally through
`GeneratedCompClosure2Cell` and `GeneratedLocalization2Cell`.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The ordinary localization quotient functor on the retained v2.68 free-path
category. -/
abbrev higherLocalizedPathQuotientFunctor :
    LocalizationPaths W ⥤ W.Localization :=
  Quotient.functor (Localization.Construction.relations W)

/-- A free-path object, viewed in the locally discrete double-opposite source
used by the localized higher contextual systems. -/
abbrev higherLocalizedPathObject (X : LocalizationPaths W) :
    LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ) :=
  .mk (op (op ((higherLocalizedPathQuotientFunctor W).obj X)))

/-- A free path, mapped to the corresponding source 1-cell of the localized
higher contextual systems. -/
abbrev higherLocalizedPathArrow
    {X Y : LocalizationPaths W}
    (p :
      (Paths.categoryPaths
        (Localization.Construction.LocQuiver W)).Hom X Y) :
    higherLocalizedPathObject W X ⟶ higherLocalizedPathObject W Y :=
  ((higherLocalizedPathQuotientFunctor W).map p).op.op.toLoc

/-- Canonical StrongTrans naturality on a retained free localization path.

No arbitrary witness from v5.00 is used: the definition follows the syntax of
the path and uses only the canonical identity, ordinary-edge, inverse-edge, and
composition constructors. -/
noncomputable def higherLocalizedStrongTransPathNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizationPaths W}
    (p :
      (Paths.categoryPaths
        (Localization.Construction.LocQuiver W)).Hom X Y) :
    F.map (higherLocalizedPathArrow W p) ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (higherLocalizedPathObject W Y) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (higherLocalizedPathObject W X) ≫
        G.map (higherLocalizedPathArrow W p) := by
  exact
    @Quiver.Path.rec
      (Localization.Construction.LocQuiver W) _
      X
      (fun Y path =>
        F.map (higherLocalizedPathArrow W path) ≫
              higherLocalizedStrongTransExtensionApp (W := W) gamma
                (higherLocalizedPathObject W Y) ≅
          higherLocalizedStrongTransExtensionApp (W := W) gamma
                (higherLocalizedPathObject W X) ≫
            G.map (higherLocalizedPathArrow W path))
      (by
        simpa
          [higherLocalizedPathArrow, higherLocalizedPathObject,
            higherLocalizedPathQuotientFunctor] using
          (higherLocalizedStrongTransNaturality_id
            (W := W) gamma
            (higherLocalizedPathObject W X)))
      (fun pfx e hp => by
        have he :
            F.map
                  (higherLocalizedPathArrow W
                    ((Paths.of (Localization.Construction.LocQuiver W)).map e)) ≫
                higherLocalizedStrongTransExtensionApp (W := W) gamma
                  (higherLocalizedPathObject W _) ≅
              higherLocalizedStrongTransExtensionApp (W := W) gamma
                  (higherLocalizedPathObject W _) ≫
                G.map
                  (higherLocalizedPathArrow W
                    ((Paths.of (Localization.Construction.LocQuiver W)).map e)) := by
          rcases e with f | w
          · simpa
              [higherLocalizedPathArrow, higherLocalizedPathObject,
                higherLocalizedPathQuotientFunctor,
                higherPresentationUnitFunctor] using
              (higherLocalizedStrongTransPresentationNaturality
                (W := W) gamma f.toLoc)
          · simpa
              [higherLocalizedPathArrow, higherLocalizedPathObject,
                higherLocalizedPathQuotientFunctor] using
              (higherLocalizedStrongTransWInverseNaturalityV5_05
                (W := W) gamma w.1 w.2)
        cases pfx with
        | nil =>
            simpa using he
        | cons pfx e0 =>
            simpa only
              [higherLocalizedPathArrow, higherLocalizedPathQuotientFunctor,
                Quiver.Path.comp_toPath_eq_cons,
                Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc] using
              (higherLocalizedStrongTransNaturality_comp
                (W := W) gamma
                (higherLocalizedPathArrow W (Quiver.Path.cons pfx e0))
                (higherLocalizedPathArrow W
                  ((Paths.of (Localization.Construction.LocQuiver W)).map e))
                hp he))
      Y p

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransPathNaturality

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06
