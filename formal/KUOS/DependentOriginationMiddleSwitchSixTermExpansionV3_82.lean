import KUOS.DependentOriginationMiddleSwitchScalarAlignmentV3_81

namespace KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterComparisonObstructionV3_68
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
open KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79
open KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80
open KUOS.DependentOriginationMiddleSwitchScalarAlignmentV3_81

set_option autoImplicit false

noncomputable section

/-!
# Six-term middle-switch expansion v3.82

v3.81 rewrites the remaining M1 residual using a scalar-friendly aligned
connector with five explicit factors:

eqToHom
  ; mapComp(a00, p).hom
  ; F(p)(u_M0)
  ; mapComp(a10, p).inv
  ; eqToHom.

After mapping to an upper endpoint through b : M1 -> T,

* the two equality transports have unit endpoint scalar;
* the first compositor contributes the transported a00/p compositor;
* the middle connector contributes the twice-mapped M0 connector;
* the inverse compositor contributes the inverse transported a10/p compositor.

In additive ZMod 2 scalarization the inverse has the same class.  Thus each
upper mapped aligned connector contributes exactly three terms.  Applying this
to b10 and b11 yields the promised six-term expansion of d10 + d11.

This is still a local coherence statement.  The final comparison with the
v3.76 eight-face compositor boundary and the v3.74 raw residual is left to the
next theorem unit.
-/

/-- Transporting an inverse compositor to the endpoint and then applying the
comparison functor produces the inverse of the corresponding transported hom
scalar. -/
@[simp] theorem counterFactorizationLocalizedTransportedComp_inv_endpointScalar
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (h : Z ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) :
    counterFactorizationLocalizedEndpointScalarAt H T
        (((counterFactorizationLocalizationView H).map h.toLoc).toFunctor.map
          (((counterFactorizationLocalizationView H).mapComp
            f.toLoc g.toLoc).inv.toNatTrans.app A)) =
      (counterFactorizationLocalizedTransportedCompImageScalarAt
        H T f g h A)⁻¹ := by
  let F := counterFactorizationLocalizationView H
  let e := F.mapComp f.toLoc g.toLoc
  let P :=
    (F.map h.toLoc).toFunctor ⋙
      (H.comparison.app (.mk T)).toFunctor
  let invScalar : C2 :=
    counterFactorizationLocalizedEndpointScalarAt H T
      ((F.map h.toLoc).toFunctor.map (e.inv.toNatTrans.app A))
  change invScalar =
    (counterFactorizationLocalizedTransportedCompImageScalarAt
      H T f g h A)⁻¹
  have hCat :=
    Cat.Hom.inv_hom_id_toNatTrans_app e A
  have hMapRaw :=
    congrArg (fun k => P.map k) hCat
  have hMap :
      P.map (e.inv.toNatTrans.app A) ≫
          P.map (e.hom.toNatTrans.app A) =
        𝟙 _ := by
    calc
      P.map (e.inv.toNatTrans.app A) ≫
          P.map (e.hom.toNatTrans.app A) =
        P.map
          (e.inv.toNatTrans.app A ≫
            e.hom.toNatTrans.app A) :=
          (P.map_comp _ _).symm
      _ = P.map (𝟙 _) := hMapRaw
      _ = 𝟙 _ := P.map_id _
  have hScalar :=
    congrArg (fun k => counterSystemHomScalar T k) hMap
  have hMul :
      counterFactorizationLocalizedTransportedCompImageScalarAt
          H T f g h A * invScalar =
        (1 : C2) := by
    simpa only [P, F, e, invScalar,
      Functor.comp_map,
      counterFactorizationLocalizedEndpointScalarAt,
      counterFactorizationLocalizedTransportedCompImageScalarAt,
      counterSystemHomScalar_comp,
      counterSystemHomScalar,
      SingleObj.id_as_one] using hScalar
  exact eq_inv_of_mul_eq_one_right hMul

/-- Equality transport remains scalar-trivial after arbitrary localization
transport to a raw endpoint. -/
@[simp] theorem counterFactorizationLocalizedMappedEqToHom_endpointScalar
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X : allMorphisms.Localization}
    (k : X ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (q : A = B) :
    counterFactorizationLocalizedEndpointScalarAt H T
        (((counterFactorizationLocalizationView H).map k.toLoc).toFunctor.map
          (eqToHom q)) =
      1 := by
  rw [CategoryTheory.eqToHom_map]
  exact counterFactorizationLocalizedEndpointScalarAt_eqToHom H T _

/-- Multiplicative expansion of the scalar-friendly aligned M0 connector after
mapping along one arbitrary M1-to-upper raw edge. -/
theorem counterFactorization_scalarAligned_mappedSourceScalar
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {T : OctahedralVertex} (b : M1 ⟶ T)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedMappedSourceScalarAt H T
        (allMorphisms.Q.map b)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) =
      (counterFactorizationLocalizedTransportedCompImageScalarAt H T
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b) A1)⁻¹ *
        counterFactorizationLocalizedTwiceMappedSourceScalarAt H T
          counterMiddleSwitch (allMorphisms.Q.map b)
          (counterFactorizationMiddleConnectorM0 H A0 A1) *
        counterFactorizationLocalizedTransportedCompImageScalarAt H T
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b) A0 := by
  rw [← counterFactorizationLocalizedMappedSource_endpointScalar
    H T (allMorphisms.Q.map b)
    (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1)]
  unfold counterFactorizationMiddleConnectorM0_scalarAlignedAtM1
  let P :=
    ((counterFactorizationLocalizationView H).map
      (allMorphisms.Q.map b).toLoc).toFunctor
  have hMap :
      P.map
        (eqToHom (counterFactorizationMiddleSwitch_sourceEndpoint_eq H A0) ≫
          ((counterFactorizationLocalizationView H).mapComp
            (allMorphisms.Q.map a00).toLoc
            counterMiddleSwitch.toLoc).hom.toNatTrans.app A0 ≫
          ((counterFactorizationLocalizationView H).map
            counterMiddleSwitch.toLoc).toFunctor.map
              (counterFactorizationMiddleConnectorM0 H A0 A1) ≫
          ((counterFactorizationLocalizationView H).mapComp
            (allMorphisms.Q.map a10).toLoc
            counterMiddleSwitch.toLoc).inv.toNatTrans.app A1 ≫
          eqToHom (counterFactorizationMiddleSwitch_targetEndpoint_eq H A1)) =
        P.map (eqToHom
            (counterFactorizationMiddleSwitch_sourceEndpoint_eq H A0)) ≫
          P.map
            (((counterFactorizationLocalizationView H).mapComp
              (allMorphisms.Q.map a00).toLoc
              counterMiddleSwitch.toLoc).hom.toNatTrans.app A0) ≫
          P.map
            (((counterFactorizationLocalizationView H).map
              counterMiddleSwitch.toLoc).toFunctor.map
                (counterFactorizationMiddleConnectorM0 H A0 A1)) ≫
          P.map
            (((counterFactorizationLocalizationView H).mapComp
              (allMorphisms.Q.map a10).toLoc
              counterMiddleSwitch.toLoc).inv.toNatTrans.app A1) ≫
          P.map (eqToHom
            (counterFactorizationMiddleSwitch_targetEndpoint_eq H A1)) := by
    simp only [P, Functor.map_comp]
  change
    counterFactorizationLocalizedEndpointScalarAt H T
      (P.map
        (eqToHom (counterFactorizationMiddleSwitch_sourceEndpoint_eq H A0) ≫
          ((counterFactorizationLocalizationView H).mapComp
            (allMorphisms.Q.map a00).toLoc
            counterMiddleSwitch.toLoc).hom.toNatTrans.app A0 ≫
          ((counterFactorizationLocalizationView H).map
            counterMiddleSwitch.toLoc).toFunctor.map
              (counterFactorizationMiddleConnectorM0 H A0 A1) ≫
          ((counterFactorizationLocalizationView H).mapComp
            (allMorphisms.Q.map a10).toLoc
            counterMiddleSwitch.toLoc).inv.toNatTrans.app A1 ≫
          eqToHom (counterFactorizationMiddleSwitch_targetEndpoint_eq H A1))) =
      _
  rw [hMap]
  dsimp [P]
  simp only [
    counterFactorizationLocalizedEndpointScalarAt_comp,
    counterFactorizationLocalizedMappedEqToHom_endpointScalar,
    counterFactorizationLocalizedTransportedComp_endpointScalar,
    counterFactorizationLocalizedTwiceMappedSource_endpointScalar,
    counterFactorizationLocalizedTransportedComp_inv_endpointScalar]
  simp only [one_mul, mul_one, mul_assoc]

/-- Additive three-term expansion for one M1-to-upper edge. -/
theorem counterFactorization_scalarAligned_mappedSourceAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {T : OctahedralVertex} (b : M1 ⟶ T)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedMappedSourceAddAt H T
        (allMorphisms.Q.map b)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) =
      counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b) A0 +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H T
          counterMiddleSwitch (allMorphisms.Q.map b)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b) A1 := by
  have h :=
    counterFactorization_scalarAligned_mappedSourceScalar H b A0 A1
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) h
  simp only [toAdd_mul, toAdd_inv, CharTwo.neg_eq] at hAdd
  change
    counterFactorizationLocalizedMappedSourceAddAt H T
        (allMorphisms.Q.map b)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) =
      counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b) A1 +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H T
          counterMiddleSwitch (allMorphisms.Q.map b)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b) A0 at hAdd
  calc
    counterFactorizationLocalizedMappedSourceAddAt H T
        (allMorphisms.Q.map b)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) =
      counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b) A1 +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H T
          counterMiddleSwitch (allMorphisms.Q.map b)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b) A0 := hAdd
    _ =
      counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b) A0 +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H T
          counterMiddleSwitch (allMorphisms.Q.map b)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTransportedCompAddAt H T
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b) A1 := by
            ac_rfl

/-- The remaining M1 coboundary pair is exactly the candidate six-term
middle-switch expression. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_sixTerm
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
    counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b10) A0 +
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b11) A0 +
      counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b10) A1 +
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b11) A1 +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  rw [counterFactorizationMiddleConnectorM1_pair_coboundary_eq_scalarAlignedMapped
    H A0 A1]
  rw [
    counterFactorization_scalarAligned_mappedSourceAdd H b10 A0 A1,
    counterFactorization_scalarAligned_mappedSourceAdd H b11 A0 A1]
  ac_rfl

/-!
## Boundary after v3.82

The M1 side is now fully scalarized:

d10 + d11
  = four transported compositor terms
      + twiceMapped_b10(u_M0)
      + twiceMapped_b11(u_M0).

This is the six-term closure candidate anticipated after v3.73.

Together with v3.78,

middle-switch M0 compositor pairs
  = d00 + d01
      + twiceMapped_b10(u_M0)
      + twiceMapped_b11(u_M0),

the two twice-mapped terms are poised to cancel when the v3.76 middle-switch
boundary is combined with the four coboundaries.

The next theorem unit should first prove that the eight full-localization
compositor scalars on Q-images are exactly the eight raw restricted-lift
compositor scalars from v3.74.  Only after that bridge is explicit should the
global octahedral parity contradiction be assembled.
-/

end

end KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82
