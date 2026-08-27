import KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77

namespace KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77

universe u

/-!
# Post-endpoint canonical comparison v1.78

Version v1.77 proves the standard type-(A) endpoint Leibniz theorem
unconditionally by an explicit A/B cellular decomposition.  Therefore the
master comparison structure of v1.59 no longer has three independent inputs.
Its endpoint field is now theorem-level, and only the genuinely separate
presentation-comparison directions remain.

This file makes that change explicit without identifying the arbitrary-scaling
canonical generator family with the standard A/B/C generator list.

There are two directions.

* `R : StandardABCCanonicalResidualComparison` consists of the two forward
  obligations from v1.48: canonical source-scaling enrichments and all induced
  canonical attachments outside the standard type-(A) subfamily must be
  standard-generated.  Since v1.77 already supplies the type-(A) piece, `R`
  alone implies

      canonicalGenerated <= standardGenerated.

* `V : StandardABCCanonicalReverseComparison` says the literal standard A/B/C
  generators are canonical-generated.  Orthogonal saturation then implies

      standardGenerated <= canonicalGenerated.

The two assumptions are intentionally kept independent.  Supplying both gives
full equality of generated left classes and right lifting classes, with no
remaining endpoint hypothesis.
-/

/-! ## The v1.77 theorem discharges the old endpoint field -/

/-- The factor-level canonical-to-standard comparison now depends only on the
honest v1.59 residual comparison. -/
def standardABCCanonicalAttachmentFactorComparisonConstructed
    (R : StandardABCCanonicalResidualComparison.{u}) :
    CanonicalAttachmentFactorComparison
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) :=
  standardABCCanonicalAttachmentFactorComparison
    standardABCTypeAEndpointLeibnizStability_proved R

/-- Consequently every literal canonical horn-cylinder generator is in the
standard A/B/C generated left class as soon as the two residual factor
obligations are supplied.  The standard type-(A) induced case is no longer a
hypothesis: it is provided by v1.77. -/
theorem canonicalGenerators_le_standardGenerated_of_residual
    (R : StandardABCCanonicalResidualComparison.{u}) :
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))
  exact
    (standardABCCanonicalAttachmentFactorComparisonConstructed R)
      .canonicalGenerators_le_externalGenerated

/-! ## Forward direction: residual comparison implies canonical <= standard -/

/-- The canonical Galois closure is contained in the standard A/B/C Galois
closure under the residual comparison alone.

This is stronger and cleaner than merely recording generator membership: it
uses the universal property of the orthogonally saturated closure, so no
second cellular induction is needed. -/
theorem canonicalGenerated_le_standardGenerated_of_residual
    (R : StandardABCCanonicalResidualComparison.{u}) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  change
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))
  exact
    canonicalGeneratedScaledAnodyne_le_of_saturated
      (canonicalGenerators_le_standardGenerated_of_residual R)
      (externalGeneratedScaledAnodyne_isOrthogonallySaturated
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})))

/-- The forward inclusion reverses on right orthogonals: every standard A/B/C
fibration is canonically attachment-fibrant. -/
theorem standardGeneratedFibration_le_canonicalGeneratedFibration_of_residual
    (R : StandardABCCanonicalResidualComparison.{u}) :
    standardGeneratedScaledFibrationABC ≤
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) := by
  have hrlp := MorphismProperty.antitone_rlp
    (canonicalGenerated_le_standardGenerated_of_residual R)
  change
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp ≤
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u}))
  rw [← canonicalGeneratedScaledAnodyne_rlp_eq_fibration]
  simpa [standardGeneratedScaledAnodyneABC] using hrlp

/-! ## Reverse direction: standard generators <= canonical closes the other side -/

/-- The v1.59 reverse generator comparison alone implies inclusion of the
entire standard generated closure into the canonical generated closure. -/
theorem standardGenerated_le_canonicalGenerated_of_reverse
    (V : StandardABCCanonicalReverseComparison.{u}) :
    standardGeneratedScaledAnodyneABC ≤
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) := by
  change
    externalGeneratedScaledAnodyne
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u}))
  exact
    externalGeneratedScaledAnodyne_le_of_le_saturated
      V.standardGenerators_le_canonicalGenerated
      canonicalGeneratedScaledAnodyne_isOrthogonallySaturated

/-- The reverse left-class inclusion again reverses on right orthogonals. -/
theorem canonicalGeneratedFibration_le_standardGeneratedFibration_of_reverse
    (V : StandardABCCanonicalReverseComparison.{u}) :
    (canonicalGeneratedScaledFibration :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledFibrationABC := by
  have hrlp := MorphismProperty.antitone_rlp
    (standardGenerated_le_canonicalGenerated_of_reverse V)
  change
    (canonicalGeneratedScaledFibration :
      MorphismProperty (ScaledSSet.{u})) ≤
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})).rlp
  rw [← canonicalGeneratedScaledAnodyne_rlp_eq_fibration] at hrlp
  simpa [standardGeneratedScaledAnodyneABC] using hrlp

/-! ## The post-endpoint master certificate has only the two comparison inputs -/

/-- After v1.77 the full comparison certificate is constructed from exactly
`R` and `V`; the endpoint field is filled by the proved cellular certificate. -/
def standardABCCanonicalComparisonCertificateConstructed
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    StandardABCCanonicalComparisonCertificate.{u} :=
  StandardABCCanonicalComparisonCertificate.ofCellular
    standardABCTypeAEndpointLeibnizCellularCertificateConstructed R V

/-- The two independent comparison directions give literal equality of the
standard and canonical generated left classes. -/
theorem standardGeneratedScaledAnodyneABC_eq_canonical_of_residual_reverse
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    standardGeneratedScaledAnodyneABC =
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) := by
  apply le_antisymm
  · exact standardGenerated_le_canonicalGenerated_of_reverse V
  · exact canonicalGenerated_le_standardGenerated_of_residual R

/-- The corresponding standard and canonical right lifting classes are also
literally equal. -/
theorem standardGeneratedScaledFibrationABC_eq_canonical_of_residual_reverse
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    standardGeneratedScaledFibrationABC =
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) := by
  apply le_antisymm
  · exact
      standardGeneratedFibration_le_canonicalGeneratedFibration_of_residual R
  · exact
      canonicalGeneratedFibration_le_standardGeneratedFibration_of_reverse V

/-- The same equality is available through the v1.59 master-certificate API,
showing that the directional decomposition agrees with the previous abstract
comparison spine. -/
theorem standardGeneratedScaledAnodyneABC_eq_canonical_via_master
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    standardGeneratedScaledAnodyneABC =
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})) :=
  (standardABCCanonicalComparisonCertificateConstructed R V)
    .generatedAnodyne_eq_canonical

/-- And likewise for the right class. -/
theorem standardGeneratedScaledFibrationABC_eq_canonical_via_master
    (R : StandardABCCanonicalResidualComparison.{u})
    (V : StandardABCCanonicalReverseComparison.{u}) :
    standardGeneratedScaledFibrationABC =
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u})) :=
  (standardABCCanonicalComparisonCertificateConstructed R V)
    .generatedFibration_eq_canonical

/-!
The formal frontier is now directionally exact:

```text
v1.77 endpoint theorem
  + residual (I) scaling enrichments
  + residual (II) non-type-A induced canonical maps
      => canonicalGenerated <= standardGenerated

reverse (III) standard ABC <= canonicalGenerated
      => standardGenerated <= canonicalGenerated

both
      => equality of generated anodyne classes
      => equality of generated fibration classes.
```

No field in this file asserts any of (I), (II), or (III).  In particular,
arbitrary simplex scalings in the canonical family remain genuinely visible.
The next geometric work can now attack either direction independently without
reopening the completed endpoint prism proof.
-/

end KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78
