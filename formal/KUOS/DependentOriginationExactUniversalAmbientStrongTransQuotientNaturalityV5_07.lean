import KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07

open CategoryTheory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Quotient-independent canonical StrongTrans naturality v5.07

The v5.06 retained generated-relation theorem proves that canonical path
naturality is invariant under every explicit
`GeneratedLocalization2Cell`.  Here that invariance is descended to an actual
morphism of Mathlib's constructed localization.

For a quotient morphism `f`, a free-path representative `p` together with
`Q.map p = f` gives a source-arrow comparison from the actual localized arrow
to the path arrow.  Transporting canonical path naturality along that
comparison yields naturality data on `f` itself.

If two representatives map to the same `f`, v2.68 supplies a retained
generated derivation between them; v5.06 invariance, transport composition, and
local discreteness then show that the resulting data are equal.  Thus
`Quot.out` is only computational scaffolding for choosing one representative,
not part of the mathematical content of the resulting family.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Comparison from an actual quotient-localization arrow to the source arrow
obtained from any specified free-path representative of that arrow. -/
noncomputable def higherLocalizedQuotientRepresentativePathArrowIso
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (p : X.as ⟶ Y.as)
    (hp :
      (higherLocalizedPathQuotientFunctor W).map p = f) :
    f.op.op.toLoc ≅ higherLocalizedPathArrow W p :=
  eqToIso
    ((congrArg (fun k => k.op.op.toLoc) hp).symm)

/-- StrongTrans naturality on an actual quotient arrow, evaluated through one
specified free-path representative. -/
noncomputable def higherLocalizedStrongTransQuotientRepresentativeNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (p : X.as ⟶ Y.as)
    (hp :
      (higherLocalizedPathQuotientFunctor W).map p = f) :
    F.map f.op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op Y))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op X))) ≫
        G.map f.op.op.toLoc := by
  exact
    higherLocalizedStrongTransNaturalityTransport
      (W := W) gamma
      (higherLocalizedQuotientRepresentativePathArrowIso
        (W := W) f p hp)
      (higherLocalizedStrongTransPathNaturality
        (W := W) gamma p)

/-- The quotient-arrow naturality obtained from a representative is independent
of the chosen representative and of the equality proof presenting it. -/
theorem higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_of_representatives
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (p q : X.as ⟶ Y.as)
    (hp :
      (higherLocalizedPathQuotientFunctor W).map p = f)
    (hq :
      (higherLocalizedPathQuotientFunctor W).map q = f) :
    higherLocalizedStrongTransQuotientRepresentativeNaturality
        (W := W) gamma f p hp =
      higherLocalizedStrongTransQuotientRepresentativeNaturality
        (W := W) gamma f q hq := by
  have hpq :
      (higherLocalizedPathQuotientFunctor W).map p =
        (higherLocalizedPathQuotientFunctor W).map q :=
    hp.trans hq.symm
  let alpha : GeneratedLocalization2Cell W p q :=
    chosenGeneratedLocalization2CellOfEquality W hpq
  let etaFp :=
    higherLocalizedQuotientRepresentativePathArrowIso
      (W := W) f p hp
  let etaPq :=
    higherLocalizedGeneratedLocalizationPathArrowIso
      (W := W) alpha
  let etaFq :=
    higherLocalizedQuotientRepresentativePathArrowIso
      (W := W) f q hq
  have hPath :=
    higherLocalizedStrongTransPathNaturality_generatedLocalization_invariant
      (W := W) gamma alpha
  change
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma etaFp
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma p) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma etaFq
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q)
  calc
    higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFp
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma p) =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFp
          (higherLocalizedStrongTransNaturalityTransport
            (W := W) gamma etaPq
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma q)) :=
      congrArg
        (fun naturality_p =>
          higherLocalizedStrongTransNaturalityTransport
            (W := W) gamma etaFp naturality_p)
        hPath
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma (etaFp ≪≫ etaPq)
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma q) :=
      higherLocalizedStrongTransNaturalityTransport_trans
        (W := W) gamma etaFp etaPq
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q)
    _ =
        higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma etaFq
          (higherLocalizedStrongTransPathNaturality
            (W := W) gamma q) :=
      higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
        (W := W) gamma
        (etaFp ≪≫ etaPq)
        etaFq
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q)

/-- Data-level canonical StrongTrans naturality on every actual morphism of the
constructed localization.  `Quot.out` merely selects one representative;
the theorem below proves that the value is representative-independent. -/
noncomputable def higherLocalizedCanonicalStrongTransNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : W.Localization}
    (f : X ⟶ Y) :
    F.map f.op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op Y))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op X))) ≫
        G.map f.op.op.toLoc :=
  higherLocalizedStrongTransQuotientRepresentativeNaturality
    (W := W) gamma f (Quot.out f) (Quot.out_eq f)

/-- Any specified representative evaluates to the canonical quotient-level
naturality family. -/
theorem higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_canonical
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (p : X.as ⟶ Y.as)
    (hp :
      (higherLocalizedPathQuotientFunctor W).map p = f) :
    higherLocalizedStrongTransQuotientRepresentativeNaturality
        (W := W) gamma f p hp =
      higherLocalizedCanonicalStrongTransNaturality
        (W := W) gamma f := by
  exact
    higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_of_representatives
      (W := W) gamma f p (Quot.out f) hp (Quot.out_eq f)

/-! ## Regression checks -/

#print axioms higherLocalizedQuotientRepresentativePathArrowIso
#print axioms higherLocalizedStrongTransQuotientRepresentativeNaturality
#print axioms higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_of_representatives
#print axioms higherLocalizedCanonicalStrongTransNaturality
#print axioms higherLocalizedStrongTransQuotientRepresentativeNaturality_eq_canonical

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07
