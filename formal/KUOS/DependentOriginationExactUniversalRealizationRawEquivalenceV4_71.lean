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
# Raw-equivalence invariance of the exact realization v4.71

v4.56 proves object-level uniqueness and naturality for coherent exact
universal targets.  v4.70 packages the chosen carrier projection as a strict
pseudofunctor on the exact universal mapping source.

This file reconnects those two layers at the source-object boundary.

If two exact universal raw objects have coherently equivalent raw contextual
systems, then their images under the strict DO₂ realization are bicategorically
equivalent.  Thus the realization depends on the raw system only up to the
coherent raw-equivalence notion already proved sufficient for exact universal
target transport.

No choice of presentation is identified definitionally and no equivalence is
asserted for arbitrary one-way raw morphisms.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Coherently equivalent raw systems carried by exact-universal source objects
have equivalent realized objects in DO₂. -/
theorem exactUniversalRealization_equivalent_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty
      (Bicategory.Equivalence
        ((exactUniversalRealization (W := W) A).obj X)
        ((exactUniversalRealization (W := W) A).obj Y)) := by
  simpa only [exactUniversalRealization_obj] using
    (transportedUniversalTarget_isCompletion2EquivalentToAnyTarget
      (W := W) A
      E
      X.presentation X.universal
      Y.presentation Y.universal)

/-- Carrier-level spelling of the same presentation-independent naturality
statement. -/
theorem exactUniversalRawObject_carrier_equivalent_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty (Bicategory.Equivalence X.carrier Y.carrier) := by
  exact
    transportedUniversalTarget_isCompletion2EquivalentToAnyTarget
      (W := W) A
      E
      X.presentation X.universal
      Y.presentation Y.universal

/-!
## Boundary after v4.71

The exact-universal mapping source now has a strict DO₂ realization, and that
realization is invariant up to bicategorical equivalence under coherent
equivalence of the underlying raw contextual systems.

The remaining general mapping-property problem is genuinely about arbitrary
admissible raw morphisms: a one-way morphism does not by itself supply the
two-sided coherent data used here.  Closing that gap requires a theorem that
constructs the appropriate exact-universal mapping 1-cell (or an explicit
obstruction) from the chosen admissibility hypothesis.
-/

end

end KUOS.DependentOriginationExactUniversalRealizationRawEquivalenceV4_71
