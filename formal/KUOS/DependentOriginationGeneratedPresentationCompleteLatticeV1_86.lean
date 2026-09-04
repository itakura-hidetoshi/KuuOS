import KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85
import Mathlib.Order.Closure
import Mathlib.Order.Hom.CompleteLattice

namespace KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85

universe u

/-!
# Generated-presentation complete lattice v1.86

Version v1.85 identifies generated presentations with the fixed points of the
orthogonality operators

```text
L |-> L.rlp.llp,
R |-> R.llp.rlp.
```

The next intrinsic structure is therefore not an ad hoc binary operation on
generator lists.  Each of these operators is a genuine Mathlib
`ClosureOperator` on the complete lattice of morphism properties.  Its closed
elements inherit a complete lattice through the standard
`ClosureOperator.gi` / `GaloisInsertion.liftCompleteLattice` construction.

Transporting the left fixed-point lattice through the v1.85 order isomorphism
gives a complete lattice directly on
`GeneratedScaledAnodynePresentation`.

The resulting arbitrary joins and meets have the expected orthogonality form:

```text
L_(sup_i P_i) = cl_L (sup_i L_(P_i)),
L_(inf_i P_i) = inf_i L_(P_i),

R_(sup_i P_i) = inf_i R_(P_i),
R_(inf_i P_i) = cl_R (sup_i R_(P_i)).
```

Thus presentation-independent theories can be combined by genuine lattice
operations, with no choice of literal generating family.
-/

/-! ## Orthogonality as Mathlib closure operators -/

/-- Left orthogonal saturation as a bundled Mathlib closure operator. -/
def orthogonalAnodyneClosure :
    ClosureOperator (MorphismProperty (ScaledSSet.{u})) where
  toFun := fun L => L.rlp.llp
  monotone' := by
    intro L M hLM
    exact MorphismProperty.antitone_llp
      (MorphismProperty.antitone_rlp hLM)
  le_closure' := fun L => MorphismProperty.le_llp_rlp L
  idempotent' := fun L => MorphismProperty.llp_rlp_llp L.rlp
  IsClosed := IsOrthogonallySaturated
  isClosed_iff := Iff.rfl

@[simp]
theorem orthogonalAnodyneClosure_apply
    (L : MorphismProperty (ScaledSSet.{u})) :
    orthogonalAnodyneClosure L = L.rlp.llp :=
  rfl

@[simp]
theorem orthogonalAnodyneClosure_isClosed_iff
    (L : MorphismProperty (ScaledSSet.{u})) :
    orthogonalAnodyneClosure.IsClosed L ↔ IsOrthogonallySaturated L :=
  Iff.rfl

/-- Right orthogonal saturation is likewise a genuine closure operator. -/
def orthogonalFibrationClosure :
    ClosureOperator (MorphismProperty (ScaledSSet.{u})) where
  toFun := fun R => R.llp.rlp
  monotone' := by
    intro R S hRS
    exact MorphismProperty.antitone_rlp
      (MorphismProperty.antitone_llp hRS)
  le_closure' := by
    intro R A B p hp
    intro X Y i hi
    exact hi p hp
  idempotent' := fun R => MorphismProperty.rlp_llp_rlp R.llp
  IsClosed := IsRightOrthogonallySaturated
  isClosed_iff := Iff.rfl

@[simp]
theorem orthogonalFibrationClosure_apply
    (R : MorphismProperty (ScaledSSet.{u})) :
    orthogonalFibrationClosure R = R.llp.rlp :=
  rfl

@[simp]
theorem orthogonalFibrationClosure_isClosed_iff
    (R : MorphismProperty (ScaledSSet.{u})) :
    orthogonalFibrationClosure.IsClosed R ↔
      IsRightOrthogonallySaturated R :=
  Iff.rfl

/-! ## Complete lattices of fixed points -/

/-- The saturated left fixed points form a complete lattice by the generic
Mathlib fixed-point construction for closure operators. -/
noncomputable instance orthogonallySaturatedScaledAnodyneCompleteLattice :
    CompleteLattice OrthogonallySaturatedScaledAnodyne.{u} :=
  orthogonalAnodyneClosure.gi.liftCompleteLattice

/-- The saturated right fixed points independently form a complete lattice. -/
noncomputable instance orthogonallySaturatedScaledFibrationCompleteLattice :
    CompleteLattice OrthogonallySaturatedScaledFibration.{u} :=
  orthogonalFibrationClosure.gi.liftCompleteLattice

/-- Arbitrary infima of saturated left classes are computed by ambient
intersection: no further closure is needed. -/
@[simp]
theorem saturatedAnodyne_iInf_val
    {ι : Sort*}
    (F : ι → OrthogonallySaturatedScaledAnodyne.{u}) :
    ((⨅ i, F i) : OrthogonallySaturatedScaledAnodyne.{u}).1 =
      ⨅ i, (F i).1 := by
  exact orthogonalAnodyneClosure.gi.gc.u_iInf

/-- Arbitrary suprema of saturated left classes are ambient unions followed by
left orthogonal saturation. -/
@[simp]
theorem saturatedAnodyne_iSup_val
    {ι : Sort*}
    (F : ι → OrthogonallySaturatedScaledAnodyne.{u}) :
    ((⨆ i, F i) : OrthogonallySaturatedScaledAnodyne.{u}).1 =
      orthogonalAnodyneClosure (⨆ i, (F i).1) := by
  have h := orthogonalAnodyneClosure.gi.l_iSup_u F
  exact (congrArg Subtype.val h).symm

/-- Arbitrary infima of saturated right classes are also computed by ambient
intersection. -/
@[simp]
theorem saturatedFibration_iInf_val
    {ι : Sort*}
    (F : ι → OrthogonallySaturatedScaledFibration.{u}) :
    ((⨅ i, F i) : OrthogonallySaturatedScaledFibration.{u}).1 =
      ⨅ i, (F i).1 := by
  exact orthogonalFibrationClosure.gi.gc.u_iInf

/-- Arbitrary suprema of saturated right classes are ambient unions followed by
right orthogonal saturation. -/
@[simp]
theorem saturatedFibration_iSup_val
    {ι : Sort*}
    (F : ι → OrthogonallySaturatedScaledFibration.{u}) :
    ((⨆ i, F i) : OrthogonallySaturatedScaledFibration.{u}).1 =
      orthogonalFibrationClosure (⨆ i, (F i).1) := by
  have h := orthogonalFibrationClosure.gi.l_iSup_u F
  exact (congrArg Subtype.val h).symm

/-! ## Transport the complete lattice to presentation classes -/

/-- Generated presentations inherit the complete lattice of their canonical
saturated-left representatives. -/
noncomputable instance generatedScaledAnodynePresentationCompleteLattice :
    CompleteLattice GeneratedScaledAnodynePresentation.{u} :=
  generatedPresentationSaturatedAnodyneOrderIso.symm.toGaloisInsertion
    .liftCompleteLattice

/-- The left fixed-point coordinate preserves arbitrary joins. -/
@[simp]
theorem presentationToSaturatedAnodyne_iSup
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    presentationToSaturatedAnodyne (⨆ i, P i) =
      ⨆ i, presentationToSaturatedAnodyne (P i) := by
  exact map_iSup generatedPresentationSaturatedAnodyneOrderIso P

/-- The left fixed-point coordinate preserves arbitrary meets. -/
@[simp]
theorem presentationToSaturatedAnodyne_iInf
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    presentationToSaturatedAnodyne (⨅ i, P i) =
      ⨅ i, presentationToSaturatedAnodyne (P i) := by
  exact map_iInf generatedPresentationSaturatedAnodyneOrderIso P

/-- Because the right coordinate is order reversing, a presentation join is a
meet of generated right classes. -/
@[simp]
theorem presentationToSaturatedFibration_iSup
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    presentationToSaturatedFibration (⨆ i, P i) =
      ⨅ i, presentationToSaturatedFibration (P i) := by
  simpa using
    (map_iSup generatedPresentationSaturatedFibrationOrderIso P)

/-- Dually, a presentation meet is a join in the ordinary inclusion order on
saturated right classes. -/
@[simp]
theorem presentationToSaturatedFibration_iInf
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    presentationToSaturatedFibration (⨅ i, P i) =
      ⨆ i, presentationToSaturatedFibration (P i) := by
  simpa using
    (map_iInf generatedPresentationSaturatedFibrationOrderIso P)

/-! ## Explicit left/right formulas for arbitrary lattice operations -/

/-- The generated left class of an arbitrary presentation join is the
orthogonal closure of the ambient join of the constituent left classes. -/
@[simp]
theorem generatedAnodyneClass_iSup
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    generatedAnodyneClass (⨆ i, P i) =
      orthogonalAnodyneClosure
        (⨆ i, generatedAnodyneClass (P i)) := by
  calc
    generatedAnodyneClass (⨆ i, P i) =
        (presentationToSaturatedAnodyne (⨆ i, P i)).1 := rfl
    _ = (⨆ i, presentationToSaturatedAnodyne (P i)).1 := by
      rw [presentationToSaturatedAnodyne_iSup]
    _ = orthogonalAnodyneClosure
        (⨆ i, generatedAnodyneClass (P i)) := by
      rw [saturatedAnodyne_iSup_val]
      rfl

/-- The generated left class of an arbitrary presentation meet is simply the
ambient meet of the constituent left classes. -/
@[simp]
theorem generatedAnodyneClass_iInf
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    generatedAnodyneClass (⨅ i, P i) =
      ⨅ i, generatedAnodyneClass (P i) := by
  calc
    generatedAnodyneClass (⨅ i, P i) =
        (presentationToSaturatedAnodyne (⨅ i, P i)).1 := rfl
    _ = (⨅ i, presentationToSaturatedAnodyne (P i)).1 := by
      rw [presentationToSaturatedAnodyne_iInf]
    _ = ⨅ i, generatedAnodyneClass (P i) := by
      rw [saturatedAnodyne_iInf_val]
      rfl

/-- The generated right class of an arbitrary presentation join is the ambient
meet of the constituent right classes. -/
@[simp]
theorem generatedFibrationClass_iSup
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    generatedFibrationClass (⨆ i, P i) =
      ⨅ i, generatedFibrationClass (P i) := by
  calc
    generatedFibrationClass (⨆ i, P i) =
        (presentationToSaturatedFibration (⨆ i, P i)).1 := rfl
    _ = (⨅ i, presentationToSaturatedFibration (P i)).1 := by
      rw [presentationToSaturatedFibration_iSup]
    _ = ⨅ i, generatedFibrationClass (P i) := by
      rw [saturatedFibration_iInf_val]
      rfl

/-- The generated right class of an arbitrary presentation meet is the right
orthogonal closure of the ambient join of the constituent right classes. -/
@[simp]
theorem generatedFibrationClass_iInf
    {ι : Sort*}
    (P : ι → GeneratedScaledAnodynePresentation.{u}) :
    generatedFibrationClass (⨅ i, P i) =
      orthogonalFibrationClosure
        (⨆ i, generatedFibrationClass (P i)) := by
  calc
    generatedFibrationClass (⨅ i, P i) =
        (presentationToSaturatedFibration (⨅ i, P i)).1 := rfl
    _ = (⨆ i, presentationToSaturatedFibration (P i)).1 := by
      rw [presentationToSaturatedFibration_iInf]
    _ = orthogonalFibrationClosure
        (⨆ i, generatedFibrationClass (P i)) := by
      rw [saturatedFibration_iSup_val]
      rfl

/-!
The invariant hierarchy is now fully order-theoretic:

```text
literal presentations
  -> preorder by one-sided orthogonal generation
  -> posetal reflection
  -> saturated-left fixed points
  <-> dual saturated-right fixed points
  -> complete lattice.
```

In particular arbitrary families of generated theories have canonical joins and
meets.  On left classes, meets are literal intersections while joins require
orthogonal saturation.  On right classes the same statement is reversed by the
orthogonality duality.  This lattice structure belongs to the generated theory
itself and is independent of the chosen standard or canonical generator list.
-/

end KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86
