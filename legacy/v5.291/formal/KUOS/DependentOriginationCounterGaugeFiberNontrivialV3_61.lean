import KUOS.DependentOriginationNontrivialSuffixObstructionV3_60

namespace KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14

set_option autoImplicit false

noncomputable section

/-!
# Concrete C2 quotient-gauge fiber nontriviality v3.61

v3.60 isolates one exact remaining local algebraic input for the fixed-gauge
suffix obstruction mechanism:

```text
Nontrivial
  (QuotientGaugeCoordinateFiber W R D (.composition f g)).
```

For the v2.69 octahedral countermodel this can be proved directly, without
inferring anything from generated-holonomy nontriviality.

The target fiber is the one-object groupoid `CounterFiber = SingleObj C2`,
where `C2` is abelian and has the distinguished nonidentity element `zeta`.
Consequently every endofunctor `F : CounterFiber ⥤ CounterFiber` carries a
central scalar natural automorphism with component `zeta`.  The same
construction lifts to an automorphism of the corresponding `Cat.Hom`.

Every composition coordinate in the countermodel is exactly the automorphism
type of a composite endomorphism of `Cat.of CounterFiber`.  Hence every such
dependent gauge fiber is nontrivial.

This is an explicit type-level construction.  It does not use, and does not
follow merely from, the nontrivial generated holonomy proved in v2.69.
-/

/-- Any endofunctor of the one-object abelian `C2` groupoid admits a scalar
natural automorphism. -/
noncomputable def scalarFunctorNatIso
    (F : CounterFiber ⥤ CounterFiber) (z : C2) :
    F ≅ F :=
  NatIso.ofComponents
    (fun X => by
      cases X
      exact asIso (SingleObj.toEnd C2 z))
    (by
      intro X Y f
      cases X
      cases Y
      simp only [SingleObj.comp_as_mul, SingleObj.toEnd_def]
      exact mul_comm z (F.map f))

@[simp]
theorem scalarFunctorNatIso_hom_app_star
    (F : CounterFiber ⥤ CounterFiber) (z : C2) :
    (scalarFunctorNatIso F z).hom.app (SingleObj.star C2) = z := by
  rfl

/-- The scalar automorphism supplied by `zeta` is genuinely nonidentity for
every endofunctor of `CounterFiber`. -/
theorem scalarFunctorNatIso_zeta_ne_refl
    (F : CounterFiber ⥤ CounterFiber) :
    scalarFunctorNatIso F zeta ≠ Iso.refl F := by
  intro h
  have h' := congrArg
    (fun e : F ≅ F => e.hom.app (SingleObj.star C2)) h
  have hz : zeta = 1 := by
    simpa [scalarFunctorNatIso_hom_app_star] using h'
  exact zeta_ne_one hz

/-- Lift the scalar natural automorphism to the hom-category of `Cat`. -/
noncomputable def scalarCatHomIso
    (F : Cat.of CounterFiber ⟶ Cat.of CounterFiber) (z : C2) :
    F ≅ F :=
  Cat.Hom.isoMk (scalarFunctorNatIso F.toFunctor z)

/-- The lifted `zeta` automorphism remains nonidentity. -/
theorem scalarCatHomIso_zeta_ne_refl
    (F : Cat.of CounterFiber ⟶ Cat.of CounterFiber) :
    scalarCatHomIso F zeta ≠ Iso.refl F := by
  intro h
  have h' := congrArg
    (fun e : F ≅ F =>
      e.hom.toNatTrans.app (SingleObj.star C2)) h
  have hz : zeta = 1 := by
    simpa [scalarCatHomIso, scalarFunctorNatIso_hom_app_star] using h'
  exact zeta_ne_one hz

/-- Every composition-coordinate gauge fiber in the concrete v2.69
countermodel is nontrivial.

The witness is the central `zeta` automorphism of the exact composite
quotient-representative `Cat.Hom`; no identification of that representative
with the identity functor is required. -/
theorem counterCompositionGaugeFiber_nontrivial
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    Nontrivial
      (QuotientGaugeCoordinateFiber
        allMorphisms counterSystem D (.composition f g)) := by
  let F : Cat.of CounterFiber ⟶ Cat.of CounterFiber :=
    quotientRepresentativeMap allMorphisms counterSystem D f ≫
      quotientRepresentativeMap allMorphisms counterSystem D g
  change Nontrivial (F ≅ F)
  refine ⟨?_⟩
  exact ⟨scalarCatHomIso F zeta, Iso.refl F,
    scalarCatHomIso_zeta_ne_refl F⟩

/-- Canonical specialization to the pointwise datum `counterD` used by the
v2.69 generated-holonomy truth test. -/
theorem counterCompositionGaugeFiber_nontrivial_counterD
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    Nontrivial
      (QuotientGaugeCoordinateFiber
        allMorphisms counterSystem counterD (.composition f g)) :=
  counterCompositionGaugeFiber_nontrivial counterD f g

/-!
## Boundary after v3.61

The v3.60 local algebraic hypothesis is no longer an unknown in the concrete
v2.69 model:

```text
for every composable localization pair f,g,
QuotientGaugeCoordinateFiber
  allMorphisms counterSystem counterD (.composition f g)
is Nontrivial.
```

This is stronger than extracting one special coordinate from the v2.69
generated-holonomy witness.  It comes instead from the central nontrivial
automorphism carried by every endofunctor of the one-object abelian `C2`
fiber.

The remaining concrete obstruction inputs are now geometric/incidence data:

* an inverse-pair fresh-boundary associator task;
* isolation of its `gComp(f,g)` suffix from the other associator coordinates
  and all unitor-visible coordinates;
* a common unitor-correcting gauge.

No claim is made here that such a concrete task is already present in the
octahedral model.  That is the next truth test.
-/

end

end KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61
