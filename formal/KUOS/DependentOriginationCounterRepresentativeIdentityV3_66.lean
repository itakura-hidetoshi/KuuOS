import KUOS.DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65

namespace KUOS.DependentOriginationCounterRepresentativeIdentityV3_66

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

set_option autoImplicit false

noncomputable section

/-!
# Countermodel quotient representatives are identity 1-cells v3.66

The v2.69 octahedral C2 model has nontrivial generated 2-cell holonomy, while
v3.64-v3.65 show that quotient-gauge coherence must be analysed independently
of that raw holonomy.

This file isolates the 1-cell side of that distinction.

Every source arrow of the countermodel is the identity functor.  More strongly,
v2.69 already proves that every arbitrary free localization word acts
identically on every C2 morphism.  Since the target is the one-object category
`CounterFiber`, functor extensionality upgrades this pointwise statement to
literal equality with the identity functor.  The Cat wrapper can then be
removed by `Cat.Hom.ext`.

Consequently every selected `Quot.out` quotient representative evaluates to
the identity 1-cell in Cat, even though different generated 2-cell derivations
between such representatives may retain nontrivial holonomy.

This does not yet construct coherent quotient transport.  It removes the
1-cell layer from the remaining truth test, so the next step can work entirely
at the level of the mapId/mapComp 2-isomorphisms and their three coherence
equations.
-/

/-- Any free localization word in the countermodel evaluates to the identity
functor on the one-object C2 fiber.

The proof deliberately uses `Functor.hext`: object equality is supplied by
the subsingleton object type, while the morphism action is the already-proved
v2.69 equality `counterFreePathEvaluator_map_eq`. -/
theorem counterFreePathEvaluator_toFunctor_eq_id
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y) :
    ((freePathEvaluator allMorphisms counterSystem D).map p).toFunctor =
      𝟭 CounterFiber := by
  apply Functor.hext
  · intro A
    exact @Subsingleton.elim Unit inferInstance _ _
  · intro A B x
    exact (counterFreePathEvaluator_map_eq D p x).heq

/-- The same statement at the protected 1-morphism wrapper used by `Cat`. -/
theorem counterFreePathEvaluator_eq_identityCatHom
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y) :
    (freePathEvaluator allMorphisms counterSystem D).map p =
      (𝟭 CounterFiber).toCatHom := by
  apply Cat.Hom.ext
  exact counterFreePathEvaluator_toFunctor_eq_id D p

/-- Therefore every selected quotient representative 1-cell is literally the
identity Cat 1-morphism.  This is stronger than the v3.58 equivalence result
and is independent of generated 2-cell holonomy. -/
theorem counterQuotientRepresentativeMap_eq_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    {X Y : allMorphisms.Localization} (f : X ⟶ Y) :
    quotientRepresentativeMap allMorphisms counterSystem D f =
      (𝟭 CounterFiber).toCatHom := by
  change
    (freePathEvaluator allMorphisms counterSystem D).map (Quot.out f) =
      (𝟭 CounterFiber).toCatHom
  exact counterFreePathEvaluator_eq_identityCatHom D (Quot.out f)

/-- Underlying-functor form of the quotient-representative collapse. -/
theorem counterQuotientRepresentativeMap_toFunctor_eq_id
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    {X Y : allMorphisms.Localization} (f : X ⟶ Y) :
    (quotientRepresentativeMap
      allMorphisms counterSystem D f).toFunctor =
      𝟭 CounterFiber := by
  exact congrArg Cat.Hom.toFunctor
    (counterQuotientRepresentativeMap_eq_identity D f)

/-- In particular, the canonical pointwise datum `counterD` used by the
nontrivial-holonomy witness has identity quotient representatives at every
localization arrow. -/
theorem counterD_quotientRepresentativeMap_eq_identity
    {X Y : allMorphisms.Localization} (f : X ⟶ Y) :
    quotientRepresentativeMap allMorphisms counterSystem counterD f =
      (𝟭 CounterFiber).toCatHom := by
  exact counterQuotientRepresentativeMap_eq_identity counterD f

/-!
## Boundary after v3.66

The concrete model now has the following simultaneously formalized facts:

* generated relation-loop holonomy is nontrivial;
* every localization arrow is invertible;
* every quotient representative evaluation is an equivalence;
* in fact every selected quotient representative 1-cell is literally equal to
  the identity Cat 1-cell.

Thus any remaining obstruction to a fully corrected quotient gauge cannot come
from the 1-cell assignment itself.  It must live in the simultaneous choice of
the identity/composition 2-isomorphisms and their associator/unitor coherence.

The next theorem unit should use this identity-1-cell collapse to attempt an
explicit `CoherentQuotientTransportData` for the countermodel.  Success would
show that v3.65 is genuinely gauge-specific; failure would expose the exact
2-cell equation that remains gauge-independent.
-/

end

end KUOS.DependentOriginationCounterRepresentativeIdentityV3_66
