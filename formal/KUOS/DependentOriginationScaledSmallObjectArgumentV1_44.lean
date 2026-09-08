import KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
import Mathlib.CategoryTheory.SmallObject.Basic

namespace KUOS.DependentOriginationScaledSmallObjectArgumentV1_44

open CategoryTheory
open CategoryTheory.Limits
open CategoryTheory.SmallObject
open HomotopicalAlgebra
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43

universe u

/-!
# Scaled small-object argument v1.44

Version 1.43 reduced the canonical scaled-anodyne weak-factorization problem to
one constructive datum:

`HasFactorization (T.rlp.llp) (T.rlp)`,

where `T` is the morphism property of all canonical minimally-scaled
horn-cylinder attachment inclusions.

Pinned Mathlib already contains Quillen's small-object argument.  For an
arbitrary morphism property `I`, the typeclass

`MorphismProperty.HasSmallObjectArgument I`

gives a functorial factorization

`I.rlp.llp` followed by `I.rlp`,

and identifies the left class with retracts of transfinite compositions of
pushouts of coproducts of generators.

This layer connects that theorem directly to the KuuOS canonical scaled
attachment generators and expands the remaining hypothesis into its exact
geometric ingredients.  The generator class itself is small by construction
(`MorphismProperty.ofHoms`), so the remaining work is reduced to:

* local smallness of `ScaledSSet`;
* pushouts;
* small coproducts;
* the transfinite iteration colimits for a suitable regular cardinal;
* preservation of the relative-cell-complex colimits by the source-Hom
  functors.

No cocompleteness or presentability theorem for `ScaledSSet` is silently
assumed here.
-/

/-! ## The canonical generator class is already small -/

/-- The canonical attachment generators form a small morphism property in the
same universe.  This is a direct consequence of their `ofHoms` presentation. -/
instance scaledHornAttachmentGenerators_isSmall :
    MorphismProperty.IsSmall.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) := by
  dsimp [scaledHornAttachmentGenerators]
  infer_instance

/-! ## Exact cardinal data required by Mathlib's small-object theorem -/

/-- The genuinely geometric/categorical data still required at one regular
cardinal `κ` in order to run the small-object argument for the canonical
scaled attachment generators.

The generator-smallness field from Mathlib's
`IsCardinalForSmallObjectArgument` is omitted because it is theorem-level
above. -/
structure CanonicalScaledSmallObjectCardinalData
    (κ : Cardinal.{u}) [Fact κ.IsRegular] [OrderBot κ.ord.ToType] : Prop where
  locallySmall : LocallySmall.{u} (ScaledSSet.{u})
  hasPushouts : HasPushouts (ScaledSSet.{u})
  hasCoproducts : HasCoproducts.{u} (ScaledSSet.{u})
  hasIterationOfShape : HasIterationOfShape κ.ord.ToType (ScaledSSet.{u})
  preservesColimit :
    ∀ {A B X Y : ScaledSSet.{u}}
      (i : A ⟶ B)
      (_ :
        (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) i)
      (f : X ⟶ Y)
      (hf : RelativeCellComplex.{u}
        (fun (_ : κ.ord.ToType) ↦
          (scaledHornAttachmentGenerators : MorphismProperty
            (ScaledSSet.{u})).homFamily) f),
      PreservesColimit hf.F (coyoneda.obj (Opposite.op A))

namespace CanonicalScaledSmallObjectCardinalData

/-- The explicit cardinal data is exactly enough to construct Mathlib's
`IsCardinalForSmallObjectArgument` certificate for the canonical generator
class. -/
@[reducible]
def toIsCardinalForSmallObjectArgument
    {κ : Cardinal.{u}} [Fact κ.IsRegular] [OrderBot κ.ord.ToType]
    (K : CanonicalScaledSmallObjectCardinalData.{u} κ) :
    MorphismProperty.IsCardinalForSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) κ where
  isSmall := by infer_instance
  locallySmall := K.locallySmall
  hasPushouts := K.hasPushouts
  hasCoproducts := K.hasCoproducts
  hasIterationOfShape := K.hasIterationOfShape
  preservesColimit := by
    intro A B X Y i hi f hf
    exact K.preservesColimit i hi f hf

/-- One suitable regular cardinal with the explicit data therefore gives the
full Mathlib small-object-argument typeclass. -/
@[reducible]
def toHasSmallObjectArgument
    {κ : Cardinal.{u}} [Fact κ.IsRegular] [OrderBot κ.ord.ToType]
    (K : CanonicalScaledSmallObjectCardinalData.{u} κ) :
    MorphismProperty.HasSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) :=
  ⟨κ, inferInstance, inferInstance, K.toIsCardinalForSmallObjectArgument⟩

end CanonicalScaledSmallObjectCardinalData

/-! ## Small-object argument closes the v1.43 factorization frontier -/

/-- A compact name for the exact Mathlib small-object condition on the
canonical scaled horn-cylinder generators. -/
abbrev HasCanonicalScaledSmallObjectArgument : Prop :=
  MorphismProperty.HasSmallObjectArgument.{u}
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u}))

/-- The Mathlib small-object argument supplies exactly the factorization datum
left open in v1.43. -/
@[reducible]
noncomputable def canonicalGeneratedScaledFactorization_of_smallObject
    (h : HasCanonicalScaledSmallObjectArgument.{u}) :
    CanonicalGeneratedScaledFactorization.{u} := by
  letI : MorphismProperty.HasSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) := h
  change MorphismProperty.HasFactorization
    ((scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp)
    ((scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp)
  infer_instance

/-- Consequently the small-object theorem upgrades the canonical orthogonal
pair to a native Mathlib weak factorization system. -/
@[reducible]
noncomputable def canonicalGeneratedScaledWeakFactorizationSystem_of_smallObject
    (h : HasCanonicalScaledSmallObjectArgument.{u}) :
    MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) :=
  canonicalGeneratedScaledWeakFactorizationSystem
    (canonicalGeneratedScaledFactorization_of_smallObject h)

/-- The same conclusion packaged in the v1.43 certificate interface. -/
noncomputable def canonicalGeneratedScaledWFSCertificate_of_smallObject
    (h : HasCanonicalScaledSmallObjectArgument.{u}) :
    CanonicalGeneratedScaledWFSCertificate.{u} where
  factorization := canonicalGeneratedScaledFactorization_of_smallObject h

/-- A single suitable cardinal-data package therefore closes the entire
factorization/WFS frontier. -/
noncomputable def canonicalGeneratedScaledWFSCertificate_of_cardinalData
    {κ : Cardinal.{u}} [Fact κ.IsRegular] [OrderBot κ.ord.ToType]
    (K : CanonicalScaledSmallObjectCardinalData.{u} κ) :
    CanonicalGeneratedScaledWFSCertificate.{u} :=
  canonicalGeneratedScaledWFSCertificate_of_smallObject
    K.toHasSmallObjectArgument

/-! ## Cellular description of the canonical generated left class -/

/-- Under the small-object hypothesis, the canonical scaled-anodyne class is
exactly the retract closure of transfinite compositions of pushouts of
coproducts of canonical attachment generators. -/
theorem canonicalGeneratedScaledAnodyne_eq_cellularClosure
    (h : HasCanonicalScaledSmallObjectArgument.{u}) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) =
      (MorphismProperty.transfiniteCompositions.{u}
        (MorphismProperty.coproducts.{u}
          (scaledHornAttachmentGenerators : MorphismProperty
            (ScaledSSet.{u}))).pushouts).retracts := by
  letI : MorphismProperty.HasSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) := h
  simpa [canonicalGeneratedScaledAnodyne] using
    (MorphismProperty.llp_rlp_of_hasSmallObjectArgument
      (I := (scaledHornAttachmentGenerators : MorphismProperty
        (ScaledSSet.{u}))))

/-- The right class obtained from the small-object theorem is exactly the
canonical generated scaled-fibration class already isolated in v1.43. -/
theorem canonicalGeneratedScaledFibration_eq_generatorRLP :
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) =
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp :=
  rfl

/-!
The v1.44 spine is now:

```text
canonical scaled horn-cylinder generators T
  -> T is small (theorem-level: ofHoms)

regular cardinal κ
  + local smallness of ScaledSSet
  + pushouts
  + small coproducts
  + κ-shaped transfinite iteration colimits
  + Hom(source,-) preservation on relative T-cell complexes
  -> IsCardinalForSmallObjectArgument T κ
  -> HasSmallObjectArgument T

Mathlib small-object theorem
  -> HasFunctorialFactorization (T.rlp.llp) (T.rlp)
  -> HasFactorization (T.rlp.llp) (T.rlp)
  -> native IsWeakFactorizationSystem (T.rlp.llp) (T.rlp)

and
  T.rlp.llp
  = retracts(transfinite compositions(pushouts(coproducts(T)))).
```

Thus the factorization theorem itself is no longer an independent KuuOS
certificate.  The remaining constructive frontier is exactly the
category-theoretic/presentability data needed to instantiate
`CanonicalScaledSmallObjectCardinalData` for `ScaledSSet`.
-/

end KUOS.DependentOriginationScaledSmallObjectArgumentV1_44