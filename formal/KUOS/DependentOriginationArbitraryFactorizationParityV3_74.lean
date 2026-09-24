import KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
import Mathlib.Tactic.LinearCombination

namespace KUOS.DependentOriginationArbitraryFactorizationParityV3_74

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterComparisonObstructionV3_68
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Direct arbitrary-factorization octahedral parity reduction v3.74

v3.72 exposes the exact composition equation for an arbitrary
`HigherLocalizationFactorization`, while v3.73 proves that its source-object
dependence is a multiplicative coboundary.

This file combines those two residual freedoms on all eight octahedral faces.
No canonical quotient transport is introduced and no normalization bridge is
assumed.

For arbitrary

```text
H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem
```

choose one source object over each lower vertex `L0` and `L1`.  Summing the
eight v3.72 face equations cancels every lower edge and every direct lower-to-
upper edge twice.  The only uncancelled edge terms are the four pairs of upper
edges evaluated at the two propagated middle-fiber objects.

Because every comparison component of `H` is an equivalence, it is full.  We
therefore choose canonical connector morphisms between the two propagated
objects over `M0` and over `M1`, with comparison image equal to the identity
scalar.  v3.73 then converts each remaining upper-edge pair into its exact
object coboundary.

The resulting truth-test equation is

```text
1
  = four inter-object coboundaries
      + eight arbitrary-lift compositor scalars
```

in `ZMod 2`.

Thus v3.74 removes all comparison-edge cochain terms.  The remaining question
is now completely localized: do pseudofunctor associativity on `H.lift` and
the localization middle switch force this twelve-term residual to vanish, or
can it carry the odd class?

No answer is assumed in this file.
-/

/-- The source fiber of an arbitrary factorization over one raw vertex. -/
abbrev CounterFactorizationFiber
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex) :=
  (restrictHigherLocalizedSystem
    allMorphisms H.lift).obj (.mk X)

/-- Propagate one chosen source object along one raw octahedral edge. -/
noncomputable def counterFactorizationPropagatedObject
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFactorizationFiber H X) :
    CounterFactorizationFiber H Y :=
  (((restrictHigherLocalizedSystem
      allMorphisms H.lift).map f.toLoc).toFunctor.obj A)

/-- Additive form of one comparison-edge scalar. -/
noncomputable def counterFactorizationEdgeAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFactorizationFiber H X) : ZMod 2 :=
  Multiplicative.toAdd (counterFactorizationEdgeScalarAt H f A)

/-- Additive form of one arbitrary localized-lift compositor contribution. -/
noncomputable def counterFactorizationLiftCompAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFactorizationFiber H X) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationLiftCompImageScalarAt H f g A)

/-- Additive form of one inter-object coboundary. -/
noncomputable def counterFactorizationObjectCoboundaryAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u : A ⟶ B) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationObjectCoboundaryAt H f u)

/-- Fullness of every comparison component follows directly from the stored
pointwise equivalence witness. -/
theorem counterFactorizationComparison_full
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex) :
    (H.comparison.app (.mk X)).toFunctor.Full := by
  letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence X
  infer_instance

/-- A connector between any two objects in one source fiber, chosen as the
preimage of the identity morphism in the one-object C2 target fiber. -/
noncomputable def counterFactorizationConnector
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex)
    (A B : CounterFactorizationFiber H X) : A ⟶ B := by
  letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence X
  exact
    (H.comparison.app (.mk X)).toFunctor.preimage
      (eqToHom (Subsingleton.elim
        ((H.comparison.app (.mk X)).toFunctor.obj A)
        ((H.comparison.app (.mk X)).toFunctor.obj B)))

/-- The chosen connector maps to the target identity transport. -/
@[simp] theorem counterFactorizationConnector_map
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex)
    (A B : CounterFactorizationFiber H X) :
    (H.comparison.app (.mk X)).toFunctor.map
        (counterFactorizationConnector H X A B) =
      eqToHom (Subsingleton.elim
        ((H.comparison.app (.mk X)).toFunctor.obj A)
        ((H.comparison.app (.mk X)).toFunctor.obj B)) := by
  letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence X
  simp [counterFactorizationConnector]

/-- Hence the source scalar of the chosen connector is literally one. -/
@[simp] theorem counterFactorizationSourceScalarAt_connector
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex)
    (A B : CounterFactorizationFiber H X) :
    counterFactorizationSourceScalarAt H X
      (counterFactorizationConnector H X A B) = 1 := by
  letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence X
  simp [counterFactorizationSourceScalarAt,
    counterFactorizationConnector]

/-- For the chosen connector, the object coboundary is entirely the inverse
transported scalar at the target vertex. -/
theorem counterFactorizationObjectCoboundaryAt_connector
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A B : CounterFactorizationFiber H X) :
    counterFactorizationObjectCoboundaryAt H f
        (counterFactorizationConnector H X A B) =
      (counterFactorizationMappedSourceScalarAt H f
        (counterFactorizationConnector H X A B))⁻¹ := by
  simp [counterFactorizationObjectCoboundaryAt]

/-- Additive pair cancellation: the two edge values at connected source
objects differ exactly by the v3.73 object coboundary. -/
theorem counterFactorizationEdgeAdd_pair_eq_coboundary
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u : A ⟶ B) :
    counterFactorizationEdgeAddAt H f A +
        counterFactorizationEdgeAddAt H f B =
      counterFactorizationObjectCoboundaryAddAt H f u := by
  have h :=
    counterFactorizationEdgeScalarAt_change_object H f u
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) h
  have hAdd' :
      counterFactorizationEdgeAddAt H f B =
        counterFactorizationObjectCoboundaryAddAt H f u +
          counterFactorizationEdgeAddAt H f A := by
    simpa only [counterFactorizationEdgeAddAt,
      counterFactorizationObjectCoboundaryAddAt, toAdd_mul] using hAdd
  rw [hAdd']
  calc
    counterFactorizationEdgeAddAt H f A +
          (counterFactorizationObjectCoboundaryAddAt H f u +
            counterFactorizationEdgeAddAt H f A) =
        counterFactorizationObjectCoboundaryAddAt H f u +
          (counterFactorizationEdgeAddAt H f A +
            counterFactorizationEdgeAddAt H f A) := by
              ac_rfl
    _ = counterFactorizationObjectCoboundaryAddAt H f u := by
          rw [CharTwo.add_self_eq_zero, add_zero]

/-- Additive form of the arbitrary-factorization composition equation. -/
theorem counterFactorizationFaceEquationAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFactorizationFiber H X) :
    Multiplicative.toAdd (compScalar X Y Z) +
        counterFactorizationEdgeAddAt H (f ≫ g) A =
      counterFactorizationEdgeAddAt H f A +
        counterFactorizationEdgeAddAt H g
          (counterFactorizationPropagatedObject H f A) +
        counterFactorizationLiftCompAddAt H f g A := by
  have h :=
    counterFactorizationEdgeScalarAt_comp H f g A
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) h
  simp only [toAdd_mul, toAdd_inv,
    CharTwo.neg_eq] at hAdd
  unfold counterFactorizationEdgeAddAt
  unfold counterFactorizationLiftCompAddAt
  unfold counterFactorizationPropagatedObject
  linear_combination hAdd

/-- Face form after replacing the composite by the named direct edge. -/
theorem counterFactorizationTriangleEquationAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {L M U : OctahedralVertex}
    (a : L ⟶ M) (b : M ⟶ U) (c : L ⟶ U)
    (A : CounterFactorizationFiber H L) :
    Multiplicative.toAdd (compScalar L M U) +
        counterFactorizationEdgeAddAt H c A =
      counterFactorizationEdgeAddAt H a A +
        counterFactorizationEdgeAddAt H b
          (counterFactorizationPropagatedObject H a A) +
        counterFactorizationLiftCompAddAt H a b A := by
  have h := counterFactorizationFaceEquationAdd H a b A
  rw [triangle_comp_eq a b c] at h
  exact h

/-- Summing all eight octahedral face equations cancels every lower edge and
every direct lower-to-upper edge.  What remains is four pairs of upper-edge
values at propagated objects, together with the eight arbitrary-lift
compositors. -/
theorem counterFactorization_rawParity_forces_edgePairs_plus_compositors
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    (1 : ZMod 2) =
      (counterFactorizationEdgeAddAt H b00
          (counterFactorizationPropagatedObject H a00 A0) +
        counterFactorizationEdgeAddAt H b00
          (counterFactorizationPropagatedObject H a10 A1)) +
      (counterFactorizationEdgeAddAt H b01
          (counterFactorizationPropagatedObject H a00 A0) +
        counterFactorizationEdgeAddAt H b01
          (counterFactorizationPropagatedObject H a10 A1)) +
      (counterFactorizationEdgeAddAt H b10
          (counterFactorizationPropagatedObject H a01 A0) +
        counterFactorizationEdgeAddAt H b10
          (counterFactorizationPropagatedObject H a11 A1)) +
      (counterFactorizationEdgeAddAt H b11
          (counterFactorizationPropagatedObject H a01 A0) +
        counterFactorizationEdgeAddAt H b11
          (counterFactorizationPropagatedObject H a11 A1)) +
      counterFactorizationLiftCompAddAt H a00 b00 A0 +
      counterFactorizationLiftCompAddAt H a01 b10 A0 +
      counterFactorizationLiftCompAddAt H a00 b01 A0 +
      counterFactorizationLiftCompAddAt H a01 b11 A0 +
      counterFactorizationLiftCompAddAt H a10 b00 A1 +
      counterFactorizationLiftCompAddAt H a11 b10 A1 +
      counterFactorizationLiftCompAddAt H a10 b01 A1 +
      counterFactorizationLiftCompAddAt H a11 b11 A1 := by
  have h000 :=
    counterFactorizationTriangleEquationAdd H a00 b00 c00 A0
  have h010 :=
    counterFactorizationTriangleEquationAdd H a01 b10 c00 A0
  have h001 :=
    counterFactorizationTriangleEquationAdd H a00 b01 c01 A0
  have h011 :=
    counterFactorizationTriangleEquationAdd H a01 b11 c01 A0
  have h100 :=
    counterFactorizationTriangleEquationAdd H a10 b00 c10 A1
  have h110 :=
    counterFactorizationTriangleEquationAdd H a11 b10 c10 A1
  have h101 :=
    counterFactorizationTriangleEquationAdd H a10 b01 c11 A1
  have h111 :=
    counterFactorizationTriangleEquationAdd H a11 b11 c11 A1

  simp [zeta] at h000 h010 h001 h011 h100 h110 h101 h111
  linear_combination
    h000 + h010 + h001 + h011 +
    h100 + h110 + h101 + h111

/-- Canonical connector in the M0 source fiber between the two objects
propagated from the lower vertices. -/
noncomputable def counterFactorizationMiddleConnectorM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationPropagatedObject H a00 A0 ⟶
      counterFactorizationPropagatedObject H a10 A1 :=
  counterFactorizationConnector H M0
    (counterFactorizationPropagatedObject H a00 A0)
    (counterFactorizationPropagatedObject H a10 A1)

/-- Canonical connector in the M1 source fiber between the two objects
propagated from the lower vertices. -/
noncomputable def counterFactorizationMiddleConnectorM1
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationPropagatedObject H a01 A0 ⟶
      counterFactorizationPropagatedObject H a11 A1 :=
  counterFactorizationConnector H M1
    (counterFactorizationPropagatedObject H a01 A0)
    (counterFactorizationPropagatedObject H a11 A1)

/-- The direct v3.74 residual equation.

Every comparison-edge cochain contribution has disappeared.  The odd raw
octahedral class can survive an arbitrary factorization only if it is carried
by the sum of four explicit inter-object coboundaries and eight explicit
localized-lift compositor scalars. -/
theorem counterFactorization_rawParity_forces_coboundary_plus_compositor_residual
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    (1 : ZMod 2) =
      counterFactorizationObjectCoboundaryAddAt H b00
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b01
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationLiftCompAddAt H a00 b00 A0 +
      counterFactorizationLiftCompAddAt H a01 b10 A0 +
      counterFactorizationLiftCompAddAt H a00 b01 A0 +
      counterFactorizationLiftCompAddAt H a01 b11 A0 +
      counterFactorizationLiftCompAddAt H a10 b00 A1 +
      counterFactorizationLiftCompAddAt H a11 b10 A1 +
      counterFactorizationLiftCompAddAt H a10 b01 A1 +
      counterFactorizationLiftCompAddAt H a11 b11 A1 := by
  have hRaw :=
    counterFactorization_rawParity_forces_edgePairs_plus_compositors
      H A0 A1
  have h00 :=
    counterFactorizationEdgeAdd_pair_eq_coboundary H b00
      (counterFactorizationMiddleConnectorM0 H A0 A1)
  have h01 :=
    counterFactorizationEdgeAdd_pair_eq_coboundary H b01
      (counterFactorizationMiddleConnectorM0 H A0 A1)
  have h10 :=
    counterFactorizationEdgeAdd_pair_eq_coboundary H b10
      (counterFactorizationMiddleConnectorM1 H A0 A1)
  have h11 :=
    counterFactorizationEdgeAdd_pair_eq_coboundary H b11
      (counterFactorizationMiddleConnectorM1 H A0 A1)

  rw [h00, h01, h10, h11] at hRaw
  exact hRaw

/-!
## Boundary after v3.74

The arbitrary-factorization truth test is now reduced to one exact equation:

```text
raw odd class = object-coboundary residual + lift-compositor residual.
```

All ordinary comparison-edge scalars have cancelled.  The remaining four
coboundaries use only the two canonical middle-fiber connectors selected by
fullness of the pointwise-equivalence comparison.

The next theorem unit should evaluate these twelve residual terms using the
same localization middle switch from v3.69 together with the genuine
`H.lift.map₂_associator` law.

There are still two logically open outcomes:

* the twelve-term residual is forced to zero, yielding direct abstract
  nonfactorization;
* the residual can be odd, identifying an explicit absorption mechanism.

Neither conclusion is imported from the canonical five-law obstruction.
-/

end

end KUOS.DependentOriginationArbitraryFactorizationParityV3_74
