import KUOS.DependentOriginationOctahedralResidualCancellationV3_99
import Mathlib

namespace KUOS.DependentOriginationAbstractNonfactorizationV4_00

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationOctahedralResidualCancellationV3_99

set_option autoImplicit false

noncomputable section

/-!
# Abstract nonfactorization of the octahedral countermodel v4.00

v3.99 proves that every arbitrary higher-localization factorization H leads to
a contradiction once one source object A0 over L0 and one source object A1
over L1 are chosen.

This file removes those explicit object parameters.

For each raw vertex X, the comparison component

  H.comparison.app (.mk X)

is stored by definition as an equivalence of categories.  Its target is the
nonempty one-object category CounterFiber.  Mathlib's IsEquivalence structure
therefore supplies an EssSurj instance, and objPreimage selects a source object
mapping to the unique target object up to isomorphism.

Choosing such preimages at L0 and L1 supplies the A0,A1 required by v3.99.
Hence the type of higher-localization factorizations of the concrete
octahedral counterSystem is empty.

No canonical quotient normalization, chosen transport, or extra
object-independence assumption is used.
-/

/-- Any purported higher-localization factorization supplies source objects
over L0 and L1 by essential surjectivity of its comparison components, and
those objects trigger the v3.99 contradiction. -/
theorem counterSystem_higherLocalizationFactorization_isEmpty :
    IsEmpty
      (HigherLocalizationFactorization
        (W := allMorphisms) counterSystem) := by
  constructor
  intro H
  letI :
      (H.comparison.app (.mk L0)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence L0
  letI :
      (H.comparison.app (.mk L1)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence L1
  let A0 : CounterFactorizationFiber H L0 :=
    (H.comparison.app (.mk L0)).toFunctor.objPreimage
      (SingleObj.star C2)
  let A1 : CounterFactorizationFiber H L1 :=
    (H.comparison.app (.mk L1)).toFunctor.objPreimage
      (SingleObj.star C2)
  exact counterFactorization_rawParity_contradiction_at_objects
    H A0 A1

/-- Equivalent proposition-level form. -/
theorem no_counterSystem_higherLocalizationFactorization :
    ¬ Nonempty
      (HigherLocalizationFactorization
        (W := allMorphisms) counterSystem) := by
  intro h
  rcases h with ⟨H⟩
  exact counterSystem_higherLocalizationFactorization_isEmpty.false H

/-!
## Boundary after v4.00

The direct arbitrary-factorization truth test is closed.

The concrete octahedral C2 countermodel admits no
HigherLocalizationFactorization at all.  The proof uses only:

* the raw odd octahedral parity class;
* object-coboundary reduction;
* full-localization associator coherence;
* middle-switch naturality and endpoint alignment;
* the explicit raw/full-localization compositor bridge;
* essential surjectivity already contained in the required pointwise
  comparison equivalences.

Thus the earlier canonical five-law counterexample has been strengthened to
direct abstract nonfactorization for this finite carrier.

The truncated-icosahedral program can now be treated as a refinement/carrier
analysis of the already-established obstruction rather than as a substitute
for the missing abstract contradiction.
-/

end

end KUOS.DependentOriginationAbstractNonfactorizationV4_00
