import KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46

namespace KUOS.DependentOriginationExternalScaledDuskinFibrancyV1_47

open CategoryTheory
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46

universe u v w

/-!
# External scaled-Duskin fibrancy v1.47

Version 1.46 proves that an arbitrary external generator family `E` determines
exactly the canonical KuuOS scaled-anodyne/fibration theory as soon as the two
families mutually generate each other's orthogonal closure.

The existing strictification spine v1.37--v1.42 packages a bicategorical model
equivalence in one common universe.  This validation layer therefore keeps the
external generator presentations at that same-universe boundary rather than
claiming a stronger heterogeneous-universe transport theorem.

The resulting theorem chain is

```text
source external presentation E_B
  -> external fibrancy of N_D(B)
  -> canonical attachment fibrancy of N_D(B)

target external presentation E_C
  -> external fibrancy of N_D(C)
  -> canonical attachment fibrancy of N_D(C)

coherent normalized scaled model equivalence B <-> C
  -> existing v1.42 attachment-fibrant carrier
  -> strict global scaled-Duskin fibrancy equivalence.
```

No equality between the source and target external generator lists is needed.
-/

/-- The global Duskin scaled object attached to a bicategory. -/
abbrev globalDuskinScaledObject
    (B : Type u) [Bicategory.{w, v} B] : ScaledSSet.{u} :=
  ScaledSSet.of (duskinNerve B) (duskinScaling B)

/-- An external scaled-anodyne presentation for one global Duskin object.

The generator family is arbitrary; the only mathematical input is the v1.46
mutual closure-generation comparison with the canonical KuuOS attachment
family. -/
structure GlobalDuskinExternalPresentation
    (B : Type u) [Bicategory.{w, v} B] where
  generators : MorphismProperty (ScaledSSet.{u})
  comparison : ScaledAnodyneGeneratorComparison generators

namespace GlobalDuskinExternalPresentation

variable
    {B : Type u} [Bicategory.{w, v} B]
    (P : GlobalDuskinExternalPresentation B)

/-- External fibrancy of the global Duskin scaled object. -/
def IsFibrant : Prop :=
  IsFibrantForExternalGenerators P.generators (globalDuskinScaledObject B)

/-- The external fibrancy predicate is exactly canonical attachment fibrancy. -/
theorem isFibrant_iff_attachmentFibrant :
    P.IsFibrant ↔ IsAttachmentFibrant (globalDuskinScaledObject B) :=
  isFibrantForExternalGenerators_iff_attachmentFibrant
    P.comparison (globalDuskinScaledObject B)

/-- External fibrancy supplies terminal RLP for every chosen global Duskin
scaled horn family. -/
noncomputable def familyTerminalRLP
    (h : P.IsFibrant)
    (H : GlobalDuskinScaledHornFamily B) :
    ScaledHornFamilyTerminalRLP (duskinScaling B) H :=
  familyTerminalRLPOfExternalFibrant P.comparison h H

/-- The external generated left class is literally the canonical generated
scaled-anodyne class. -/
theorem generatedAnodyne_eq_canonical :
    externalGeneratedScaledAnodyne P.generators =
      canonicalGeneratedScaledAnodyne :=
  ScaledAnodyneGeneratorComparison.externalGeneratedScaledAnodyne_eq_canonical
    P.comparison

/-- The external generated right class is literally the canonical generated
scaled-fibration class. -/
theorem generatedFibration_eq_canonical :
    externalGeneratedScaledFibration P.generators =
      canonicalGeneratedScaledFibration :=
  ScaledAnodyneGeneratorComparison.externalGeneratedScaledFibration_eq_canonical
    P.comparison

end GlobalDuskinExternalPresentation

/-! ## External fibrancy for a bicategorical model equivalence -/

/-- A coherent normalized scaled model equivalence equipped with independent
external scaled-anodyne presentations on its source and target global Duskin
objects, within the common universe already required by the strictification
spine.

The source presentation and target presentation remain independent generator
families.  Each is only required to compare with the canonical attachment-
generated closure. -/
structure CoherentNormalizedScaledExternalDuskinModelEquivalence
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (PB : GlobalDuskinExternalPresentation B)
    (PC : GlobalDuskinExternalPresentation C)
    (E : BicategoricalModelEquivalence B C)
    (G : BicategoricalModelEquivalence C B)
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C) where
  homotopyClassModel :
    CoherentNormalizedScaledHomotopyClassModelEquivalence E G HB HC
  sourceExternalFibrant : PB.IsFibrant
  targetExternalFibrant : PC.IsFibrant

namespace CoherentNormalizedScaledExternalDuskinModelEquivalence

variable
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {PB : GlobalDuskinExternalPresentation B}
    {PC : GlobalDuskinExternalPresentation C}
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledExternalDuskinModelEquivalence
      PB PC E G HB HC)

/-- Convert the two independent external fibrancy hypotheses to the canonical
attachment-fibrant model-equivalence carrier of v1.42. -/
noncomputable def toAttachmentFibrantModelEquivalence :
    CoherentNormalizedScaledAttachmentFibrantModelEquivalence E G HB HC where
  homotopyClassModel := K.homotopyClassModel
  sourceAttachmentFibrant :=
    (GlobalDuskinExternalPresentation.isFibrant_iff_attachmentFibrant PB).mp
      K.sourceExternalFibrant
  targetAttachmentFibrant :=
    (GlobalDuskinExternalPresentation.isFibrant_iff_attachmentFibrant PC).mp
      K.targetExternalFibrant

/-- External presentations therefore recover the exact family-specific
terminal-RLP model carrier only when needed. -/
noncomputable def toTerminalRLPModelEquivalence :
    CoherentNormalizedScaledTerminalRLPModelEquivalence E G HB HC :=
  CoherentNormalizedScaledAttachmentFibrantModelEquivalence.toTerminalRLPModelEquivalence
    (toAttachmentFibrantModelEquivalence K)

/-- Strict global scaled-Duskin fibrancy is invariant across the bicategorical
model equivalence when source and target are certified using independent
external scaled-anodyne generator presentations. -/
theorem globalDuskinStrictFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  CoherentNormalizedScaledAttachmentFibrantModelEquivalence.globalDuskinStrictFibrancy_iff
    (toAttachmentFibrantModelEquivalence K)

end CoherentNormalizedScaledExternalDuskinModelEquivalence

/-!
The external comparison route is now closed back into the global bicategorical
spine:

```text
external E_B, E_C
  + mutual closure-generation with canonical attachments
  + external fibrancy of N_D(B), N_D(C)
  + coherent normalized scaled model equivalence
  -> canonical attachment fibrancy of N_D(B), N_D(C)
  -> terminal RLP for the chosen global horn families
  -> presentation-independent strict global scaled-Duskin fibrancy.
```

The only genuinely external mathematical burden that remains for a concrete
standard/Lurie presentation is proving the two v1.46 generator-level closure
inclusions in the common universe of the established strictification spine.
-/

end KUOS.DependentOriginationExternalScaledDuskinFibrancyV1_47
