import KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
import KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56
import Mathlib

namespace KUOS.DependentOriginationExactUniversalRealizationRawEquivalenceV4_71

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Coherent raw-equivalence invariance of strict realization v4.71

The v4.55 transport keeps the chosen DO₂ carrier definitionally unchanged.
The v4.56 universal-target theorem supplies a native bicategorical equivalence
to any exact universal target for the transported raw system. The object map
of the v4.70 strict realization is definitionally the chosen carrier.

These are constructor-level identifications, not equalities of entire
pseudofunctors. The proofs below therefore reuse the native equivalence witness
directly, without simplification of its type or expansion of coherence data.

This file concerns equivalence of realized objects under a two-sided coherent
raw equivalence. It does not promote every one-way raw morphism to an
equivalence, identify distinct carriers definitionally, or supply compatible
unit and counit 2-cells in the source bicategory.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A coherent raw equivalence induces a bicategorical equivalence between the
objects selected by the strict DO₂ realization. -/
theorem exactUniversalRealization_equivalent_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty
      (Bicategory.Equivalence
        ((exactUniversalRealization (W := W) A).obj X)
        ((exactUniversalRealization (W := W) A).obj Y)) :=
  transportedUniversalTarget_isCompletion2EquivalentToAnyTarget
    (W := W) A E X.presentation X.universal Y.presentation Y.universal

/-- The same result expressed using the chosen carriers directly. -/
theorem exactUniversalRawObject_carrier_equivalent_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty (Bicategory.Equivalence X.carrier Y.carrier) :=
  transportedUniversalTarget_isCompletion2EquivalentToAnyTarget
    (W := W) A E X.presentation X.universal Y.presentation Y.universal

/-!
## Boundary after v4.71

Object-level raw-equivalence invariance is connected to the strict realization.
The next question is exact liftability of an arbitrary raw morphism between
chosen presentations, or its explicit obstruction. A source bicategorical
equivalence requires further compatible source 2-cell data.
-/

end

end KUOS.DependentOriginationExactUniversalRealizationRawEquivalenceV4_71
