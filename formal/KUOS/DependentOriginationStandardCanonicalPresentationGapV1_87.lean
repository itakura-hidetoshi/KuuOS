import KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86

namespace KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86

universe u

/-!
# The standard/canonical presentation gap v1.87

Version v1.86 promotes the presentation-independent orthogonality fixed-point
space to a complete lattice.  The unresolved comparison between the standard
A/B/C point and the canonical KuuOS point can therefore be represented without
choosing a direction in advance.

Write

```text
S := standardABCPresentation
C := canonicalKuuOSPresentation.
```

Their canonical lower and upper envelopes are

```text
G_min := S ⊓ C,
G_max := S ⊔ C.
```

The interval `[G_min,G_max]` is the intrinsic presentation gap.  It always
contains both distinguished points.  A one-sided comparison orients the gap:

```text
C <= S  ->  G_min = C and G_max = S,
S <= C  ->  G_min = S and G_max = C.
```

Full presentation identification is exactly collapse of the two endpoints.
Combining this with v1.84 identifies gap closure with the two direct generator
inclusions.  Under the v1.79 positive forward residual package, only the
reverse generatorwise A/B/C comparison remains to collapse the interval.
-/

/-! ## Canonical lower and upper envelopes -/

/-- Greatest lower envelope of the standard and canonical presentation points. -/
def standardCanonicalLowerEnvelope :
    GeneratedScaledAnodynePresentation.{u} :=
  standardABCPresentation ⊓ canonicalKuuOSPresentation

/-- Least upper envelope of the standard and canonical presentation points. -/
def standardCanonicalUpperEnvelope :
    GeneratedScaledAnodynePresentation.{u} :=
  standardABCPresentation ⊔ canonicalKuuOSPresentation

/-- The standard/canonical presentation gap as the closed order interval
between the two canonical envelopes. -/
def standardCanonicalPresentationInterval :
    Set GeneratedScaledAnodynePresentation.{u} :=
  Set.Icc standardCanonicalLowerEnvelope standardCanonicalUpperEnvelope

/-- The lower envelope lies below the standard point. -/
theorem lowerEnvelope_le_standardABC :
    standardCanonicalLowerEnvelope.{u} ≤ standardABCPresentation := by
  exact inf_le_left

/-- The lower envelope lies below the canonical point. -/
theorem lowerEnvelope_le_canonicalKuuOS :
    standardCanonicalLowerEnvelope.{u} ≤ canonicalKuuOSPresentation := by
  exact inf_le_right

/-- The standard point lies below the upper envelope. -/
theorem standardABC_le_upperEnvelope :
    standardABCPresentation ≤ standardCanonicalUpperEnvelope.{u} := by
  exact le_sup_left

/-- The canonical point lies below the upper envelope. -/
theorem canonicalKuuOS_le_upperEnvelope :
    canonicalKuuOSPresentation ≤ standardCanonicalUpperEnvelope.{u} := by
  exact le_sup_right

/-- The lower envelope is the greatest presentation lying below both points. -/
@[simp]
theorem le_lowerEnvelope_iff
    (P : GeneratedScaledAnodynePresentation.{u}) :
    P ≤ standardCanonicalLowerEnvelope ↔
      P ≤ standardABCPresentation ∧ P ≤ canonicalKuuOSPresentation := by
  simp [standardCanonicalLowerEnvelope]

/-- The upper envelope is the least presentation lying above both points. -/
@[simp]
theorem upperEnvelope_le_iff
    (P : GeneratedScaledAnodynePresentation.{u}) :
    standardCanonicalUpperEnvelope ≤ P ↔
      standardABCPresentation ≤ P ∧ canonicalKuuOSPresentation ≤ P := by
  simp [standardCanonicalUpperEnvelope]

/-- Membership in the gap interval is exactly the envelope sandwich. -/
@[simp]
theorem mem_standardCanonicalPresentationInterval_iff
    (P : GeneratedScaledAnodynePresentation.{u}) :
    P ∈ standardCanonicalPresentationInterval ↔
      standardCanonicalLowerEnvelope ≤ P ∧
        P ≤ standardCanonicalUpperEnvelope := by
  rfl

/-- The standard A/B/C point belongs to the intrinsic gap interval. -/
theorem standardABCPresentation_mem_interval :
    standardABCPresentation ∈
      standardCanonicalPresentationInterval.{u} := by
  exact ⟨lowerEnvelope_le_standardABC, standardABC_le_upperEnvelope⟩

/-- The canonical KuuOS point belongs to the intrinsic gap interval. -/
theorem canonicalKuuOSPresentation_mem_interval :
    canonicalKuuOSPresentation ∈
      standardCanonicalPresentationInterval.{u} := by
  exact ⟨lowerEnvelope_le_canonicalKuuOS, canonicalKuuOS_le_upperEnvelope⟩

/-! ## One-sided comparison orients the interval -/

/-- Canonical-below-standard is exactly the statement that the lower envelope
is the canonical point. -/
theorem canonicalKuuOS_le_standardABC_iff_lowerEnvelope_eq_canonical :
    canonicalKuuOSPresentation ≤ standardABCPresentation ↔
      standardCanonicalLowerEnvelope = canonicalKuuOSPresentation := by
  constructor
  · intro h
    exact inf_eq_right.mpr h
  · intro h
    rw [← h]
    exact lowerEnvelope_le_standardABC

/-- The same order direction is equivalently detected by the upper envelope. -/
theorem canonicalKuuOS_le_standardABC_iff_upperEnvelope_eq_standard :
    canonicalKuuOSPresentation ≤ standardABCPresentation ↔
      standardCanonicalUpperEnvelope = standardABCPresentation := by
  constructor
  · intro h
    exact sup_eq_left.mpr h
  · intro h
    rw [← h]
    exact canonicalKuuOS_le_upperEnvelope

/-- Thus a canonical-to-standard comparison identifies both gap endpoints. -/
theorem canonicalKuuOS_le_standardABC_iff_envelopes :
    canonicalKuuOSPresentation ≤ standardABCPresentation ↔
      standardCanonicalLowerEnvelope = canonicalKuuOSPresentation ∧
        standardCanonicalUpperEnvelope = standardABCPresentation := by
  constructor
  · intro h
    exact
      ⟨canonicalKuuOS_le_standardABC_iff_lowerEnvelope_eq_canonical.1 h,
        canonicalKuuOS_le_standardABC_iff_upperEnvelope_eq_standard.1 h⟩
  · rintro ⟨h, _⟩
    exact canonicalKuuOS_le_standardABC_iff_lowerEnvelope_eq_canonical.2 h

/-- Standard-below-canonical is exactly the statement that the lower envelope
is the standard point. -/
theorem standardABC_le_canonicalKuuOS_iff_lowerEnvelope_eq_standard :
    standardABCPresentation ≤ canonicalKuuOSPresentation ↔
      standardCanonicalLowerEnvelope = standardABCPresentation := by
  constructor
  · intro h
    exact inf_eq_left.mpr h
  · intro h
    rw [← h]
    exact lowerEnvelope_le_canonicalKuuOS

/-- The reverse order direction is equivalently detected by the upper envelope. -/
theorem standardABC_le_canonicalKuuOS_iff_upperEnvelope_eq_canonical :
    standardABCPresentation ≤ canonicalKuuOSPresentation ↔
      standardCanonicalUpperEnvelope = canonicalKuuOSPresentation := by
  constructor
  · intro h
    exact sup_eq_right.mpr h
  · intro h
    rw [← h]
    exact standardABC_le_upperEnvelope

/-- Thus a standard-to-canonical comparison identifies both gap endpoints. -/
theorem standardABC_le_canonicalKuuOS_iff_envelopes :
    standardABCPresentation ≤ canonicalKuuOSPresentation ↔
      standardCanonicalLowerEnvelope = standardABCPresentation ∧
        standardCanonicalUpperEnvelope = canonicalKuuOSPresentation := by
  constructor
  · intro h
    exact
      ⟨standardABC_le_canonicalKuuOS_iff_lowerEnvelope_eq_standard.1 h,
        standardABC_le_canonicalKuuOS_iff_upperEnvelope_eq_canonical.1 h⟩
  · rintro ⟨h, _⟩
    exact standardABC_le_canonicalKuuOS_iff_lowerEnvelope_eq_standard.2 h

/-- If the canonical point lies below the standard point, the intrinsic gap is
literally the interval from canonical to standard. -/
theorem interval_eq_of_canonicalKuuOS_le_standardABC
    (h : canonicalKuuOSPresentation ≤ standardABCPresentation) :
    standardCanonicalPresentationInterval =
      Set.Icc canonicalKuuOSPresentation standardABCPresentation := by
  unfold standardCanonicalPresentationInterval
  rw [canonicalKuuOS_le_standardABC_iff_lowerEnvelope_eq_canonical.1 h,
    canonicalKuuOS_le_standardABC_iff_upperEnvelope_eq_standard.1 h]

/-- If the standard point lies below the canonical point, the intrinsic gap is
literally the interval from standard to canonical. -/
theorem interval_eq_of_standardABC_le_canonicalKuuOS
    (h : standardABCPresentation ≤ canonicalKuuOSPresentation) :
    standardCanonicalPresentationInterval =
      Set.Icc standardABCPresentation canonicalKuuOSPresentation := by
  unfold standardCanonicalPresentationInterval
  rw [standardABC_le_canonicalKuuOS_iff_lowerEnvelope_eq_standard.1 h,
    standardABC_le_canonicalKuuOS_iff_upperEnvelope_eq_canonical.1 h]

/-! ## Gap closure -/

/-- The standard/canonical presentation gap is closed when its two canonical
endpoints coincide. -/
def StandardCanonicalPresentationGapClosed : Prop :=
  standardCanonicalLowerEnvelope.{u} = standardCanonicalUpperEnvelope

/-- Gap closure is exactly equality of the two distinguished presentation
points. -/
theorem standardCanonicalPresentationGapClosed_iff :
    StandardCanonicalPresentationGapClosed.{u} ↔
      standardABCPresentation = canonicalKuuOSPresentation := by
  constructor
  · intro h
    apply le_antisymm
    · calc
        standardABCPresentation ≤ standardCanonicalUpperEnvelope :=
          standardABC_le_upperEnvelope
        _ = standardCanonicalLowerEnvelope := h.symm
        _ ≤ canonicalKuuOSPresentation := lowerEnvelope_le_canonicalKuuOS
    · calc
        canonicalKuuOSPresentation ≤ standardCanonicalUpperEnvelope :=
          canonicalKuuOS_le_upperEnvelope
        _ = standardCanonicalLowerEnvelope := h.symm
        _ ≤ standardABCPresentation := lowerEnvelope_le_standardABC
  · intro h
    simpa [StandardCanonicalPresentationGapClosed,
      standardCanonicalLowerEnvelope, standardCanonicalUpperEnvelope, h]

/-- Equivalently, gap closure is mutual comparison in the presentation order. -/
theorem standardCanonicalPresentationGapClosed_iff_mutual_le :
    StandardCanonicalPresentationGapClosed.{u} ↔
      standardABCPresentation ≤ canonicalKuuOSPresentation ∧
        canonicalKuuOSPresentation ≤ standardABCPresentation := by
  rw [standardCanonicalPresentationGapClosed_iff,
    standardABC_eq_canonical_iff_mutual_le]

/-- At generator level, gap closure is exactly the two direct one-sided
orthogonal-generation inclusions from v1.84. -/
theorem standardCanonicalPresentationGapClosed_iff_direct_generator_inclusions :
    StandardCanonicalPresentationGapClosed.{u} ↔
      ((standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) ≤
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u}))) ∧
      ((scaledHornAttachmentGenerators :
          MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC) := by
  rw [standardCanonicalPresentationGapClosed_iff,
    standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions]

/-! ## Existing comparison packages in interval language -/

/-- The v1.79 positive forward residual package orients the gap from canonical
to standard. -/
theorem interval_eq_of_positiveResidual
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    standardCanonicalPresentationInterval =
      Set.Icc canonicalKuuOSPresentation standardABCPresentation := by
  exact interval_eq_of_canonicalKuuOS_le_standardABC
    (canonicalKuuOS_le_standardABC_of_positiveResidual K)

/-- The v1.79 generatorwise reverse package orients the gap from standard to
canonical. -/
theorem interval_eq_of_generatorwiseReverse
    (K : StandardABCCanonicalGeneratorwiseReverseComparison.{u}) :
    standardCanonicalPresentationInterval =
      Set.Icc standardABCPresentation canonicalKuuOSPresentation := by
  exact interval_eq_of_standardABC_le_canonicalKuuOS
    (standardABC_le_canonicalKuuOS_iff_generatorwiseReverse.2 K)

/-- Once a positive forward residual comparison has been supplied, closing the
gap is exactly the reverse generatorwise A/B/C obligation. -/
theorem standardCanonicalPresentationGapClosed_iff_generatorwiseReverse_of_positiveResidual
    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :
    StandardCanonicalPresentationGapClosed.{u} ↔
      StandardABCCanonicalGeneratorwiseReverseComparison.{u} := by
  constructor
  · intro hgap
    apply standardABC_le_canonicalKuuOS_iff_generatorwiseReverse.1
    exact le_of_eq (standardCanonicalPresentationGapClosed_iff.1 hgap)
  · intro Kreverse
    apply standardCanonicalPresentationGapClosed_iff.2
    apply le_antisymm
    · exact standardABC_le_canonicalKuuOS_iff_generatorwiseReverse.2 Kreverse
    · exact canonicalKuuOS_le_standardABC_of_positiveResidual K

/-!
The comparison frontier is now represented by a canonical interval in the
presentation-independent complete lattice:

```text
G_min = standard ⊓ canonical
G_max = standard ⊔ canonical

standard, canonical ∈ [G_min,G_max]

canonical <= standard
  -> [G_min,G_max] = [canonical,standard]

standard <= canonical
  -> [G_min,G_max] = [standard,canonical]

G_min = G_max
  <-> standard = canonical
  <-> both direct generator inclusions.
```

This separates three logically different achievements: existence of the
presentation-independent ambient lattice, orientation of the comparison gap,
and collapse of that gap.  The first is unconditional by v1.86.  The latter two
remain precisely the geometric standard/canonical comparison problem.
-/

end KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
