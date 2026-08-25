import KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
import Mathlib.CategoryTheory.MorphismProperty.WeakFactorizationSystem

namespace KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42

universe u

/-!
# Scaled-anodyne weak-factorization universality v1.43

Version 1.42 constructed the canonical generated scaled-anodyne class

`T.rlp.llp`

from the canonical minimally-scaled horn-cylinder attachment generators `T`,
and proved that passing from `T` to this closure does not change the right
class.  The present layer records the stronger universal property of that
closure and isolates the one remaining ingredient needed for a genuine weak
factorization system.

The key points are:

* `T.rlp.llp` is orthogonally saturated and is the least orthogonally
  saturated morphism property containing `T`;
* therefore any compatible presentation from v1.42 that is itself
  orthogonally saturated is literally equal to the canonical closure, not
  merely right-class equivalent to it;
* the canonical generated left class is automatically stable under retracts,
  cobase change, and composition, because it is an `llp` class;
* its right class is automatically stable under retracts, base change, and
  composition, because it is an `rlp` class;
* once factorization through these two classes is supplied, Mathlib's retract
  argument upgrades the pair to a native `IsWeakFactorizationSystem`.

Thus the remaining construction problem is no longer the lifting axioms or
closure laws: it is precisely the factorization theorem, suitable for a future
small-object argument in the category of scaled simplicial sets.
-/

/-! ## Orthogonal saturation and the closure universal property -/

/-- A morphism property is orthogonally saturated when it is fixed by the
left-after-right orthogonal closure. -/
def IsOrthogonallySaturated
    (A : MorphismProperty (ScaledSSet.{u})) : Prop :=
  A.rlp.llp = A

/-- The canonical generated scaled-anodyne class is orthogonally saturated. -/
theorem canonicalGeneratedScaledAnodyne_isOrthogonallySaturated :
    IsOrthogonallySaturated
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) := by
  unfold IsOrthogonallySaturated canonicalGeneratedScaledAnodyne
  rw [MorphismProperty.rlp_llp_rlp]

/-- The canonical generated class is the least orthogonally saturated class
containing all canonical attachment generators. -/
theorem canonicalGeneratedScaledAnodyne_le_of_saturated
    {A : MorphismProperty (ScaledSSet.{u})}
    (hgen :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤ A)
    (hsat : IsOrthogonallySaturated A) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤ A := by
  have hrlp :
      A.rlp ≤
        (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp :=
    MorphismProperty.antitone_rlp hgen
  have hllp :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp ≤
        A.rlp.llp :=
    MorphismProperty.antitone_llp hrlp
  rw [hsat] at hllp
  simpa [canonicalGeneratedScaledAnodyne] using hllp

/-- Orthogonal closure is idempotent on the canonical generated class. -/
theorem canonicalGeneratedScaledAnodyne_closure_idempotent :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).rlp.llp =
      canonicalGeneratedScaledAnodyne :=
  canonicalGeneratedScaledAnodyne_isOrthogonallySaturated

/-- A compatible v1.42 presentation which is itself orthogonally saturated is
not merely fibrancy-equivalent to the canonical presentation: its left class
is literally the canonical generated scaled-anodyne class. -/
theorem ScaledAnodynePresentation.eq_canonical_of_saturated
    (P : ScaledAnodynePresentation.{u})
    (hsat : IsOrthogonallySaturated P.anodyne) :
    P.anodyne =
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) := by
  apply le_antisymm
  · exact P.le_generatedClosure
  · exact canonicalGeneratedScaledAnodyne_le_of_saturated P.generators_le hsat

/-! ## Algebraic closure laws inherited from orthogonality -/

/-- The canonical generated scaled-anodyne class is stable under retracts. -/
instance canonicalGeneratedScaledAnodyne_isStableUnderRetracts :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).IsStableUnderRetracts := by
  dsimp [canonicalGeneratedScaledAnodyne]
  infer_instance

/-- The canonical generated scaled-anodyne class is stable under cobase change. -/
instance canonicalGeneratedScaledAnodyne_isStableUnderCobaseChange :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).IsStableUnderCobaseChange := by
  dsimp [canonicalGeneratedScaledAnodyne]
  infer_instance

/-- The canonical generated scaled-anodyne class is closed under identity and
composition. -/
instance canonicalGeneratedScaledAnodyne_isMultiplicative :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).IsMultiplicative := by
  dsimp [canonicalGeneratedScaledAnodyne]
  infer_instance

/-- The canonical right class generated by the horn-cylinder attachments. -/
def canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u}) :=
  (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp

/-- The right class is stable under retracts. -/
instance canonicalGeneratedScaledFibration_isStableUnderRetracts :
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})).IsStableUnderRetracts := by
  dsimp [canonicalGeneratedScaledFibration]
  infer_instance

/-- The right class is stable under base change. -/
instance canonicalGeneratedScaledFibration_isStableUnderBaseChange :
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})).IsStableUnderBaseChange := by
  dsimp [canonicalGeneratedScaledFibration]
  infer_instance

/-- The right class is closed under identity and composition. -/
instance canonicalGeneratedScaledFibration_isMultiplicative :
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})).IsMultiplicative := by
  dsimp [canonicalGeneratedScaledFibration]
  infer_instance

/-- The canonical generated left class is exactly the left orthogonal of the
canonical generated right class. -/
theorem canonicalGeneratedScaledFibration_llp :
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})).llp =
      canonicalGeneratedScaledAnodyne := by
  rfl

/-- The canonical generated right class is exactly the right orthogonal of the
canonical generated left class. -/
theorem canonicalGeneratedScaledAnodyne_rlp_eq_fibration :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).rlp =
      canonicalGeneratedScaledFibration := by
  simpa [canonicalGeneratedScaledFibration] using
    (canonicalGeneratedScaledAnodyne_rlp (u := u))

/-- Every left-class morphism lifts against every right-class morphism. -/
theorem canonicalGenerated_hasLiftingProperty
    {A B X Y : ScaledSSet.{u}}
    (i : A ⟶ B)
    (p : X ⟶ Y)
    (hi : (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) i)
    (hp : (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) p) :
    HasLiftingProperty i p := by
  exact hi p hp

/-! ## Conditional native weak factorization system -/

/-- The only extra datum still needed to obtain a native weak factorization
system is factorization of every scaled map through the generated left and
right classes. -/
abbrev CanonicalGeneratedScaledFactorization : Prop :=
  MorphismProperty.HasFactorization
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
    (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u}))

/-- Once the factorization theorem is supplied, Mathlib's retract argument
upgrades the canonical orthogonal pair to a genuine weak factorization system. -/
def canonicalGeneratedScaledWeakFactorizationSystem
    (hfac : CanonicalGeneratedScaledFactorization.{u}) :
    MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) := by
  letI : MorphismProperty.HasFactorization
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) := hfac
  apply MorphismProperty.IsWeakFactorizationSystem.mk'
  intro A B X Y i p hi hp
  exact canonicalGenerated_hasLiftingProperty i p hi hp

/-- A compact certificate recording the remaining factorization theorem.  All
orthogonality and closure laws are theorem-level consequences. -/
structure CanonicalGeneratedScaledWFSCertificate : Prop where
  factorization : CanonicalGeneratedScaledFactorization.{u}

namespace CanonicalGeneratedScaledWFSCertificate

/-- The certificate canonically yields Mathlib's native weak factorization
system. -/
def toWeakFactorizationSystem
    (K : CanonicalGeneratedScaledWFSCertificate.{u}) :
    MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) :=
  canonicalGeneratedScaledWeakFactorizationSystem K.factorization

/-- Under the certificate, every generated anodyne/fibration square has a
lift, phrased through Mathlib's native weak-factorization API. -/
theorem hasLiftingProperty
    (K : CanonicalGeneratedScaledWFSCertificate.{u})
    {A B X Y : ScaledSSet.{u}}
    (i : A ⟶ B)
    (p : X ⟶ Y)
    (hi : (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) i)
    (hp : (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) p) :
    HasLiftingProperty i p := by
  letI : MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) :=
    K.toWeakFactorizationSystem
  exact MorphismProperty.hasLiftingProperty_of_wfs i p hi hp

end CanonicalGeneratedScaledWFSCertificate

/-!
The v1.43 spine is therefore:

```text
canonical attachment generators T
  -> right class T.rlp
  -> canonical left class T.rlp.llp

universal property:
  T.rlp.llp is the least orthogonally saturated class containing T

closure laws, automatically from Mathlib orthogonality:
  left  : retracts + cobase change + composition
  right : retracts + base change + composition

one remaining input:
  HasFactorization (T.rlp.llp) (T.rlp)

then Mathlib retract argument:
  IsWeakFactorizationSystem (T.rlp.llp) (T.rlp)
```

This separates the future small-object/factorization construction from every
other aspect of the scaled-anodyne lifting theory.  No external scaled-anodyne
model structure is claimed here.
-/

end KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
