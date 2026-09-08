import KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
import KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
import Mathlib.CategoryTheory.SmallObject.TransfiniteCompositionLifting

namespace KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open HomotopicalAlgebra
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58

universe u

/-!
# Standard A/B/C Leibniz cellular comparison v1.59

Version v1.58 made the standard scaled-anodyne presentation completely
explicit inside KuuOS:

```text
A = standard inner scaled horns
B = the standard Delta[4] scaling enrichment
C = the collapsed outer-horn family
E_std = A + B + C.
```

It also exposed the orthogonal classes

```text
E_std.rlp.llp
E_std.rlp.
```

Version v1.55 had already identified the type-(A) endpoint attachment with a
genuine categorical scaled Leibniz pushout, using the least scaling generated
by the two pushout legs, and proved that membership of that map descends across
the identity-underlying source enrichment to the induced type-(A) canonical
attachment.

This file joins those two spines without assuming a scaled model structure.
The point is to make the remaining theorem mathematically exact before the
prism filtration is formalized.

We prove four things.

1. The usual cellular closure

   `retracts (transfinite (pushouts (coproducts E_std)))`

   is unconditionally contained in `E_std.rlp.llp`, purely by Mathlib
   orthogonality.  No small-object argument is needed for this direction.

2. For the explicit standard class, the substantive endpoint theorem has
   three equivalent/usefully related forms:

   * stability under the genuine scaled Leibniz construction;
   * containment of every type-(A) scaled Leibniz generator in
     `E_std.rlp.llp`;
   * right lifting of every such map against every map in `E_std.rlp`.

   An explicit A/B/C-cellular decomposition is therefore a sufficient
   certificate for the endpoint theorem.

3. Such a certificate feeds directly through v1.55/v1.54 to give

   `T_induced^(A) <= E_std.rlp.llp`.

4. We then separate the *full* canonical comparison honestly.  The canonical
   KuuOS family allows arbitrary simplex scalings, so the standard type-(A)
   theorem does not cover every induced canonical generator.  We isolate the
   remaining obligations as

   * canonical source-scaling enrichments;
   * induced canonical maps not already in the standard type-(A) subfamily;
   * the reverse inclusion `E_std <= canonicalGenerated`.

   With exactly those residual fields, v1.48 gives equality of the standard
   and canonical generated left/right classes.

Thus no claim `canonical T = standard A/B/C` is made.  The next geometric proof
can concentrate on one precise target: put each type-(A) endpoint prism map in
the A/B/C cellular closure.
-/

/-! ## The standard A/B/C cellular closure -/

/-- The ordinary weakly-cellular closure built from the explicit standard
A/B/C generators: coproducts, pushouts, transfinite compositions, and
retracts.  This definition does not assume a small-object argument. -/
def standardABCCellularClosure :
    MorphismProperty (ScaledSSet.{u}) :=
  (MorphismProperty.transfiniteCompositions.{u}
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts).retracts

/-- Every A/B/C-cellular morphism lies in the orthogonally generated standard
left class.  This is the direction of the cellular/orthogonal comparison that
requires no presentability or small-object hypothesis. -/
theorem standardABCCellularClosure_le_generated :
    (standardABCCellularClosure : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  simpa [standardABCCellularClosure, standardGeneratedScaledAnodyneABC] using
    (MorphismProperty.retracts_transfiniteComposition_pushouts_coproducts_le_llp_rlp.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))

/-- The standard generated class is retract-stable because it is an `llp`
class. -/
instance standardGeneratedScaledAnodyneABC_isStableUnderRetracts :
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{u})).IsStableUnderRetracts := by
  dsimp [standardGeneratedScaledAnodyneABC]
  infer_instance

/-- The standard generated class is stable under cobase change. -/
instance standardGeneratedScaledAnodyneABC_isStableUnderCobaseChange :
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{u})).IsStableUnderCobaseChange := by
  dsimp [standardGeneratedScaledAnodyneABC]
  infer_instance

/-- The standard generated class contains identities and is closed under
composition. -/
instance standardGeneratedScaledAnodyneABC_isMultiplicative :
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{u})).IsMultiplicative := by
  dsimp [standardGeneratedScaledAnodyneABC]
  infer_instance

/-- The standard type-(A) horn family is already contained in the standard
generated left class. -/
theorem standardTypeAHorns_le_standardGeneratedABC :
    (standardTypeAScaledHornGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  exact le_trans standardTypeAGenerators_le_ABC
    standardScaledAnodyneGeneratorsABC_le_generated

/-! ## Three exact forms of the endpoint Leibniz theorem -/

/-- The substantive standard endpoint theorem, stated as stability of the
standard generated left class under the genuine v1.55 scaled Leibniz
construction. -/
abbrev StandardABCTypeAEndpointLeibnizStability : Prop :=
  StandardTypeAScaledLeibnizPushoutProductStable
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{u}))

/-- For the standard generated class, Leibniz stability is equivalent to
membership of the entire explicit Leibniz generator family.  The hypothesis
about the input horn is automatic because all type-(A) horns are standard
A/B/C generators. -/
theorem standardABCTypeAEndpointLeibnizStability_iff_generators_le :
    StandardABCTypeAEndpointLeibnizStability.{u} ↔
      (standardTypeAScaledLeibnizPushoutProductGenerators :
        MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC := by
  constructor
  · intro K A B f hf
    dsimp [standardTypeAScaledLeibnizPushoutProductGenerators] at hf
    cases hf with
    | mk g =>
        exact K.pushoutProduct_mem g
          (standardTypeAGenerator_mem_standardGenerated
            (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
  · intro h
    refine { pushoutProduct_mem := ?_ }
    intro g _
    exact h _ (standardTypeAScaledLeibnizPushoutProductGenerator_mem g)

/-- Right-lifting formulation of the same endpoint theorem.  This is useful
when the future proof is organized on the fibration side rather than by an
explicit cellular filtration. -/
def StandardABCTypeAEndpointLeibnizLifting : Prop :=
  ∀ (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : ScaledSSet.{u}} (p : X ⟶ Y),
    standardGeneratedScaledFibrationABC p →
      HasLiftingProperty
        (standardTypeAEndpointScaledLeibnizPushoutProductHom g) p

/-- Stability under the type-(A) endpoint Leibniz construction is exactly the
statement that every such map lifts against every standard A/B/C fibration. -/
theorem standardABCTypeAEndpointLeibnizStability_iff_lifting :
    StandardABCTypeAEndpointLeibnizStability.{u} ↔
      StandardABCTypeAEndpointLeibnizLifting.{u} := by
  constructor
  · intro K g X Y p hp
    have hi :
        standardGeneratedScaledAnodyneABC
          (standardTypeAEndpointScaledLeibnizPushoutProductHom g) :=
      K.pushoutProduct_mem g
        (standardTypeAGenerator_mem_standardGenerated
          (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
    exact hi p hp
  · intro h
    refine { pushoutProduct_mem := ?_ }
    intro g _
    change
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})).rlp.llp
        (standardTypeAEndpointScaledLeibnizPushoutProductHom g)
    intro X Y p hp
    exact h g p hp

/-! ## An explicit cellular certificate is sufficient -/

/-- The exact output expected from a geometric prism filtration: every genuine
scaled type-(A) endpoint Leibniz map is built from standard A/B/C cells by the
ordinary cellular operations. -/
structure StandardABCTypeAEndpointLeibnizCellularCertificate : Prop where
  generators_le_cellular :
    (standardTypeAScaledLeibnizPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardABCCellularClosure

namespace StandardABCTypeAEndpointLeibnizCellularCertificate

/-- A cellular prism filtration automatically proves the orthogonal Leibniz
stability theorem. -/
def toLeibnizStability
    (K : StandardABCTypeAEndpointLeibnizCellularCertificate.{u}) :
    StandardABCTypeAEndpointLeibnizStability.{u} := by
  rw [standardABCTypeAEndpointLeibnizStability_iff_generators_le]
  exact le_trans K.generators_le_cellular
    standardABCCellularClosure_le_generated

/-- Equivalently, a cellular prism filtration proves the right-lifting form of
the endpoint theorem. -/
theorem lifting
    (K : StandardABCTypeAEndpointLeibnizCellularCertificate.{u}) :
    StandardABCTypeAEndpointLeibnizLifting.{u} :=
  standardABCTypeAEndpointLeibnizStability_iff_lifting.mp
    K.toLeibnizStability

end StandardABCTypeAEndpointLeibnizCellularCertificate

/-! ## Feed the endpoint theorem into the v1.55 type-(A) comparison -/

/-- Specialize the v1.55 external comparison structure to the literal standard
A/B/C presentation. -/
def standardABCTypeAExternalScaledLeibnizComparison
    (K : StandardABCTypeAEndpointLeibnizStability.{u}) :
    StandardTypeAExternalScaledLeibnizComparison
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) where
  typeAHorns_le_externalGenerated := by
    change
      (standardTypeAScaledHornGenerators :
        MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC
    exact standardTypeAHorns_le_standardGeneratedABC
  scaledLeibnizPushoutProductStable := by
    change
      StandardTypeAScaledLeibnizPushoutProductStable
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u}))
    exact K

/-- The endpoint Leibniz theorem therefore gives the exact v1.49/v1.55
restricted induced-attachment comparison

`T_induced^(A) <= E_std.rlp.llp`.
-/
theorem standardTypeAInducedAttachments_le_standardGenerated
    (K : StandardABCTypeAEndpointLeibnizStability.{u}) :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  change
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))
  exact
    StandardTypeAExternalScaledLeibnizComparison.inducedTypeAAttachments_le_externalGenerated
      (standardABCTypeAExternalScaledLeibnizComparison K)

/-- The same conclusion in the v1.50 induced endpoint-pushout-product
presentation. -/
theorem standardTypeAEndpointPushoutProducts_le_standardGenerated
    (K : StandardABCTypeAEndpointLeibnizStability.{u}) :
    (standardTypeAEndpointPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  change
    (standardTypeAEndpointPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))
  exact
    StandardTypeAExternalScaledLeibnizComparison.endpointPushoutProducts_le_externalGenerated
      (standardABCTypeAExternalScaledLeibnizComparison K)

/-- A cellular certificate gives the restricted induced comparison directly. -/
theorem StandardABCTypeAEndpointLeibnizCellularCertificate.inducedAttachments_le
    (K : StandardABCTypeAEndpointLeibnizCellularCertificate.{u}) :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC :=
  standardTypeAInducedAttachments_le_standardGenerated
    K.toLeibnizStability

/-! ## Honest residual obligations for the full canonical family -/

/-- After the standard type-(A) subfamily has been handled, the full v1.48
canonical factor comparison still has two independent obligations.

The second field is deliberately stated as a *complement at the morphism
property level*: if an induced canonical morphism is not already one of the
standard type-(A) induced maps, it must separately be shown standard-generated.
This avoids pretending that arbitrary KuuOS simplex scalings are standard
type-(A) scalings. -/
structure StandardABCCanonicalResidualComparison : Prop where
  scalingEnrichments_le_standardGenerated :
    (scaledHornAttachmentScalingEnrichments :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC
  nonTypeAInduced_mem :
    ∀ {A B : ScaledSSet.{u}} (f : A ⟶ B),
      (inducedScaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})) f →
      ¬ (standardTypeAInducedScaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})) f →
      standardGeneratedScaledAnodyneABC f

/-- Type-(A) Leibniz stability plus the explicit non-type-(A) residual field
covers the entire v1.48 induced canonical family. -/
theorem inducedCanonicalAttachments_le_standardGenerated
    (K : StandardABCTypeAEndpointLeibnizStability.{u})
    (R : StandardABCCanonicalResidualComparison.{u}) :
    (inducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  intro A B f hf
  classical
  by_cases hA :
      (standardTypeAInducedScaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})) f
  · exact standardTypeAInducedAttachments_le_standardGenerated K _ hA
  · exact R.nonTypeAInduced_mem f hf hA

/-- The preceding data is exactly a v1.48 canonical factor comparison with the
external family specialized to standard A/B/C. -/
def standardABCCanonicalAttachmentFactorComparison
    (K : StandardABCTypeAEndpointLeibnizStability.{u})
    (R : StandardABCCanonicalResidualComparison.{u}) :
    CanonicalAttachmentFactorComparison
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) where
  scalingEnrichments_le_externalGenerated := by
    change
      (scaledHornAttachmentScalingEnrichments :
        MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC
    exact R.scalingEnrichments_le_standardGenerated
  inducedAttachments_le_externalGenerated := by
    change
      (inducedScaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC
    exact inducedCanonicalAttachments_le_standardGenerated K R

/-- The remaining reverse direction needed for equality of the two generated
presentations.  It is kept separate from the endpoint theorem because it is a
different mathematical statement. -/
structure StandardABCCanonicalReverseComparison : Prop where
  standardGenerators_le_canonicalGenerated :
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u}))

/-- A master certificate collecting exactly the still-independent obligations
for full equality between the explicit standard A/B/C presentation and the
stronger canonical KuuOS presentation. -/
structure StandardABCCanonicalComparisonCertificate : Prop where
  endpointLeibniz : StandardABCTypeAEndpointLeibnizStability.{u}
  residual : StandardABCCanonicalResidualComparison.{u}
  reverse : StandardABCCanonicalReverseComparison.{u}

namespace StandardABCCanonicalComparisonCertificate

/-- The master certificate produces the exact factorized v1.48 comparison. -/
def toFactorizedComparison
    (K : StandardABCCanonicalComparisonCertificate.{u}) :
    FactorizedScaledAnodyneGeneratorComparison
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) where
  factors :=
    standardABCCanonicalAttachmentFactorComparison
      K.endpointLeibniz K.residual
  externalGenerators_le_canonicalGenerated :=
    K.reverse.standardGenerators_le_canonicalGenerated

/-- Consequently the standard A/B/C generated left class equals the canonical
KuuOS generated left class. -/
theorem generatedAnodyne_eq_canonical
    (K : StandardABCCanonicalComparisonCertificate.{u}) :
    standardGeneratedScaledAnodyneABC =
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) := by
  change
    externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) =
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u}))
  exact K.toFactorizedComparison.externalGeneratedScaledAnodyne_eq_canonical

/-- Their right lifting classes agree as well. -/
theorem generatedFibration_eq_canonical
    (K : StandardABCCanonicalComparisonCertificate.{u}) :
    standardGeneratedScaledFibrationABC =
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) := by
  change
    externalGeneratedScaledFibration
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) =
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u}))
  exact K.toFactorizedComparison.externalGeneratedScaledFibration_eq_canonical

end StandardABCCanonicalComparisonCertificate

/-- A cellular type-(A) prism theorem can be inserted directly into the master
comparison certificate. -/
def StandardABCCanonicalComparisonCertificate.ofCellular
    (C : StandardABCTypeAEndpointLeibnizCellularCertificate.{u})
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    StandardABCCanonicalComparisonCertificate.{u} where
  endpointLeibniz := C.toLeibnizStability
  residual := R
  reverse := V

/-!
The comparison frontier is now precise and non-overlapping:

```text
explicit A/B/C prism filtration
  -> standardTypeA scaled Leibniz maps are ABC-cellular
  -> standard type-A induced attachments are in ABC.rlp.llp

full canonical comparison additionally needs
  (I)  canonical scaling enrichments in ABC.rlp.llp
  (II) induced canonical maps outside the standard type-A subfamily in ABC.rlp.llp
  (III) ABC <= canonicalGenerated

(I)+(II)+type-A + (III)
  -> v1.48 FactorizedScaledAnodyneGeneratorComparison
  -> standard generated left class = canonical generated left class
  -> standard right class = canonical right class.
```

In particular, the next geometric unit does not need to solve all of v1.48 at
once.  It has a single exact target:

`standardTypeAScaledLeibnizPushoutProductGenerators <= standardABCCellularClosure`.
-/

end KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
