import KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76
namespace KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76

set_option autoImplicit false

noncomputable section

/-!
# Localized compositor naturality square v3.77

v3.76 rewrites the eight arbitrary-lift octahedral compositor terms as a closed
middle-switch boundary.  The next question is whether the two source-object
evaluations of a middle-switch compositor are independent freedoms.

They are not.  The hom component of a pseudofunctor compositor is a natural
transformation.  For a source-fiber morphism `u : A ⟶ B`, naturality compares

* `F.map (f ≫ g) u`, the direct image of `u`;
* `F.map g (F.map f u)`, the twice-transported image;
* the compositor component at `A`;
* the compositor component at `B`.

After applying the endpoint comparison functor and scalarizing in the concrete
one-object C2 target, this is an exact four-term square in `ZMod 2`.

Specializing to `f = counterMiddleSwitch` and `g = Q(b10), Q(b11)`
identifies the direct side with `Q(b00), Q(b01)` by the v3.69 localization
equalities.  This is the first incidence relation between the v3.76
middle-switch boundary and the v3.74 object-coboundary residual.

No hexagonal or polyhedral closure is assumed in this file.
-/

/-- Image in the raw C2 endpoint of one source-fiber morphism transported by a
single arbitrary localization arrow. -/
noncomputable def counterFactorizationLocalizedMappedSourceScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X : allMorphisms.Localization}
    (k : X ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) : C2 :=
  (H.comparison.app (.mk T)).toFunctor.map
    (((counterFactorizationLocalizationView H).map k.toLoc).toFunctor.map u)

/-- Additive form of the single-arrow transported source scalar. -/
noncomputable def counterFactorizationLocalizedMappedSourceAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X : allMorphisms.Localization}
    (k : X ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationLocalizedMappedSourceScalarAt H T k u)

/-- Image in the raw C2 endpoint of a source-fiber morphism transported first
along `f` and then along `g`. -/
noncomputable def counterFactorizationLocalizedTwiceMappedSourceScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) : C2 :=
  (H.comparison.app (.mk T)).toFunctor.map
    (((counterFactorizationLocalizationView H).map g.toLoc).toFunctor.map
      (((counterFactorizationLocalizationView H).map f.toLoc).toFunctor.map u))

/-- Additive form of the twice-transported source scalar. -/
noncomputable def counterFactorizationLocalizedTwiceMappedSourceAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationLocalizedTwiceMappedSourceScalarAt H T f g u)

/-- The single-arrow transported source scalar is exactly the endpoint
scalar of the transported source morphism. -/
@[simp] theorem counterFactorizationLocalizedMappedSource_endpointScalar
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X : allMorphisms.Localization}
    (k : X ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedEndpointScalarAt H T
        (((counterFactorizationLocalizationView H).map k.toLoc).toFunctor.map u) =
      counterFactorizationLocalizedMappedSourceScalarAt H T k u := by
  rfl

/-- The twice-transported source scalar is exactly the endpoint scalar after
successive transport along the two localization arrows. -/
@[simp] theorem counterFactorizationLocalizedTwiceMappedSource_endpointScalar
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedEndpointScalarAt H T
        (((counterFactorizationLocalizationView H).map g.toLoc).toFunctor.map
          (((counterFactorizationLocalizationView H).map f.toLoc).toFunctor.map u)) =
      counterFactorizationLocalizedTwiceMappedSourceScalarAt H T f g u := by
  rfl

/-- Exact multiplicative naturality square for one localization-level
pseudofunctor compositor after endpoint comparison. -/
theorem counterFactorizationLocalizedComp_naturality
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedCompImageScalarAt H T f g B *
        counterFactorizationLocalizedMappedSourceScalarAt H T (f ≫ g) u =
      counterFactorizationLocalizedTwiceMappedSourceScalarAt H T f g u *
        counterFactorizationLocalizedCompImageScalarAt H T f g A := by
  have h :=
    ((counterFactorizationLocalizationView H).mapComp
      f.toLoc g.toLoc).hom.toNatTrans.naturality u
  have hScalar :=
    congrArg
      (fun k => counterFactorizationLocalizedEndpointScalarAt H T k)
      h
  set_option backward.isDefEq.respectTransparency false in
    simpa only [
      counterFactorizationLocalizedEndpointScalarAt_comp,
      counterFactorizationLocalizedComp_hom_endpointScalar,
      counterFactorizationLocalizedMappedSource_endpointScalar,
      counterFactorizationLocalizedTwiceMappedSource_endpointScalar,
      Quiver.Hom.comp_toLoc,
      Cat.Hom.comp_toFunctor,
      Functor.comp_map] using hScalar

/-- Additive four-term square.  The variation of a compositor between source
objects is exactly the discrepancy between direct and twice-transported images
of the connecting source morphism. -/
theorem counterFactorizationLocalizedCompAdd_pair_eq_transport_square
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedCompAddAt H T f g A +
        counterFactorizationLocalizedCompAddAt H T f g B =
      counterFactorizationLocalizedMappedSourceAddAt H T (f ≫ g) u +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H T f g u := by
  have h := counterFactorizationLocalizedComp_naturality H T f g u
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) h
  simp only [toAdd_mul] at hAdd
  unfold counterFactorizationLocalizedCompAddAt
  unfold counterFactorizationLocalizedMappedSourceAddAt
  unfold counterFactorizationLocalizedTwiceMappedSourceAddAt
  apply CharTwo.add_eq_zero.mp
  calc
    (Multiplicative.toAdd
          (counterFactorizationLocalizedCompImageScalarAt H T f g A) +
        Multiplicative.toAdd
          (counterFactorizationLocalizedCompImageScalarAt H T f g B)) +
      (Multiplicative.toAdd
          (counterFactorizationLocalizedMappedSourceScalarAt H T (f ≫ g) u) +
        Multiplicative.toAdd
          (counterFactorizationLocalizedTwiceMappedSourceScalarAt H T f g u)) =
        (Multiplicative.toAdd
            (counterFactorizationLocalizedCompImageScalarAt H T f g B) +
          Multiplicative.toAdd
            (counterFactorizationLocalizedMappedSourceScalarAt H T (f ≫ g) u)) +
        (Multiplicative.toAdd
            (counterFactorizationLocalizedTwiceMappedSourceScalarAt H T f g u) +
          Multiplicative.toAdd
            (counterFactorizationLocalizedCompImageScalarAt H T f g A)) := by
              ac_rfl
    _ = 0 := CharTwo.add_eq_zero.mpr hAdd

/-- The M0 connector specialization ending at H0.  The direct route through the
middle switch simplifies exactly to Q(b00). -/
theorem counterFactorization_middleSwitch_comp_pair_b10
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a10 A1) =
    counterFactorizationLocalizedMappedSourceAddAt H H0
        (allMorphisms.Q.map b00)
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  simpa only [counterMiddleSwitch_comp_b10] using
    (counterFactorizationLocalizedCompAdd_pair_eq_transport_square
      H H0 counterMiddleSwitch (allMorphisms.Q.map b10)
      (counterFactorizationMiddleConnectorM0 H A0 A1))

/-- The M0 connector specialization ending at H1.  The direct route through the
middle switch simplifies exactly to Q(b01). -/
theorem counterFactorization_middleSwitch_comp_pair_b11
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a10 A1) =
    counterFactorizationLocalizedMappedSourceAddAt H H1
        (allMorphisms.Q.map b01)
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  simpa only [counterMiddleSwitch_comp_b11] using
    (counterFactorizationLocalizedCompAdd_pair_eq_transport_square
      H H1 counterMiddleSwitch (allMorphisms.Q.map b11)
      (counterFactorizationMiddleConnectorM0 H A0 A1))

/-!
## Boundary after v3.77

Two of the four middle-switch compositor pairs are now resolved by an exact
naturality square.

For the chosen M0 connector:

```text
comp(p,b10,A00) + comp(p,b10,A10)
  = mapped(Q(b00),u_M0) + twiceMapped(p,b10,u_M0)

comp(p,b11,A00) + comp(p,b11,A10)
  = mapped(Q(b01),u_M0) + twiceMapped(p,b11,u_M0).
```

The single-arrow mapped terms are the localization-level forms of the v3.74
b00/b01 object-coboundary contributions because the chosen connector maps to
the identity at M0.  The two twice-mapped terms measure how that connector is
carried through the middle switch before the upper edge.

The next theorem unit must compare those twice-mapped terms with the M1
connector and with the four transported compositor terms from v3.76.  If that
pasting closes in six terms, the hexagonal cell is derived rather than assumed;
only then is a truncated-icosahedral carrier justified.
-/

end

end KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
