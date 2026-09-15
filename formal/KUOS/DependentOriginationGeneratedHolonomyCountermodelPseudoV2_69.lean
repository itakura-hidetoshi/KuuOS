import KUOS.DependentOriginationGeneratedHolonomyCountermodelCarrierV2_69
import Mathlib.Tactic.CategoryTheory.BicategoryCoherence

namespace KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56

/-!
# Single-face twisted pseudofunctor v2.69

All six source objects are sent to the same one-object `C2` groupoid and every
source arrow is sent to the identity functor.  The only nontrivial pseudofunctor
compositor is the triangle

```text
L0 -> M0 -> H0,
```

where the compositor is multiplied by `zeta`.  Because the octahedral source
has no nondegenerate four-object chain, the pseudofunctor associativity law has
only identity-degenerate cases.  The twist is therefore a normalized 2-cocycle.

The resulting raw higher contextual system is weakly admissible for the
all-morphisms property because every mapped arrow is literally the identity
functor.
-/

/-- The distinguished triangular face carrying the unique compositor twist. -/
def isTwistedFace (X Y Z : OctahedralVertex) : Prop :=
  X = L0 ∧ Y = M0 ∧ Z = H0

instance (X Y Z : OctahedralVertex) : Decidable (isTwistedFace X Y Z) :=
  inferInstance

/-- The normalized scalar 2-cochain: `zeta` on `L0-M0-H0`, identity elsewhere. -/
def compScalar (X Y Z : OctahedralVertex) : C2 :=
  if isTwistedFace X Y Z then zeta else 1

@[simp] theorem compScalar_L0_M0_H0 : compScalar L0 M0 H0 = zeta := by
  simp [compScalar, isTwistedFace]

@[simp] theorem compScalar_L0_M1_H0 : compScalar L0 M1 H0 = 1 := by
  simp [compScalar, isTwistedFace, L0, M0, M1, H0]

@[simp] theorem compScalar_L0_M0_H1 : compScalar L0 M0 H1 = 1 := by
  simp [compScalar, isTwistedFace, L0, M0, H0, H1]

@[simp] theorem compScalar_L0_M1_H1 : compScalar L0 M1 H1 = 1 := by
  simp [compScalar, isTwistedFace, L0, M0, M1, H0, H1]

@[simp] theorem compScalar_L1_M0_H0 : compScalar L1 M0 H0 = 1 := by
  simp [compScalar, isTwistedFace, L0, L1, M0, H0]

@[simp] theorem compScalar_L1_M0_H1 : compScalar L1 M0 H1 = 1 := by
  simp [compScalar, isTwistedFace, L0, L1, M0, H0, H1]

@[simp] theorem compScalar_L1_M1_H0 : compScalar L1 M1 H0 = 1 := by
  simp [compScalar, isTwistedFace, L0, L1, M0, M1, H0]

@[simp] theorem compScalar_L1_M1_H1 : compScalar L1 M1 H1 = 1 := by
  simp [compScalar, isTwistedFace, L0, L1, M0, M1, H0, H1]

@[simp] theorem compScalar_left_identity (X Z : OctahedralVertex) :
    compScalar X X Z = 1 := by
  simp [compScalar, isTwistedFace, L0, M0]

@[simp] theorem compScalar_right_identity (X Y : OctahedralVertex) :
    compScalar X Y Y = 1 := by
  simp [compScalar, isTwistedFace, M0, H0]

/-- The scalar cochain satisfies the pseudofunctor 2-cocycle equation on every
composable triple.  The proof is exactly the absence of a strict four-chain. -/
theorem compScalar_cocycle
    {X Y Z T : OctahedralVertex}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    compScalar X Z T * compScalar X Y Z =
      compScalar Y Z T * compScalar X Y T := by
  rcases adjacent_eq_of_three_composable f g h with hXY | hYZ | hZT
  · subst Y
    simp
  · subst Z
    simp
  · subst T
    simp

/-- Turn a scalar automorphism of the identity functor into a compositor
2-isomorphism in `Cat`. -/
noncomputable def scalarCompIso (z : C2) :
    (𝟭 (Cat.of CounterFiber)) ≅
      (𝟭 (Cat.of CounterFiber) ≫ 𝟭 (Cat.of CounterFiber)) :=
  Cat.Hom.isoMk
    (scalarIdNatIso z ≪≫ eqToIso (by simp))

/-- The raw compositor chosen by the finite model. -/
noncomputable def counterMapComp
    (X Y Z : OctahedralVertex) :
    (𝟭 (Cat.of CounterFiber)) ≅
      (𝟭 (Cat.of CounterFiber) ≫ 𝟭 (Cat.of CounterFiber)) :=
  scalarCompIso (compScalar X Y Z)

/-- Scalar compositors with equal scalars are equal as 2-isomorphisms. -/
theorem counterMapComp_eq_of_compScalar_eq
    {X Y Z X' Y' Z' : OctahedralVertex}
    (h : compScalar X Y Z = compScalar X' Y' Z') :
    counterMapComp X Y Z = counterMapComp X' Y' Z' := by
  simp [counterMapComp, h]

/-- The single-face twisted raw higher contextual system. -/
noncomputable def counterSystem :
    RawHigherContextualSystem
      (Context := OctahedralVertex) (uH := 0) (vH := 0) :=
  LocallyDiscrete.mkPseudofunctor
    (fun _ => Cat.of CounterFiber)
    (fun _ => 𝟙 (Cat.of CounterFiber))
    (fun _ => Iso.refl _)
    (fun {X Y Z} _ _ => counterMapComp X Y Z)
    (by
      intro X Y Z T f g h
      rcases adjacent_eq_of_three_composable f g h with hXY | hYZ | hZT
      · subst Y
        simp [counterMapComp, scalarCompIso]
      · subst Z
        simp [counterMapComp, scalarCompIso]
      · subst T
        simp [counterMapComp, scalarCompIso])
    (by
      intro X Y f
      simp [counterMapComp, scalarCompIso])
    (by
      intro X Y f
      simp [counterMapComp, scalarCompIso])

/-- Every mapped source arrow is definitionally the identity functor. -/
@[simp] theorem counterSystem_map_toFunctor
    {X Y : OctahedralVertex} (f : X ⟶ Y) :
    (counterSystem.map f.toLoc).toFunctor = 𝟭 CounterFiber := by
  rfl

/-- With every source morphism declared invertible, the twisted system still
satisfies weak `W`-admissibility pointwise. -/
theorem counterSystem_admissible :
    IsHigherWAdmissible allMorphisms counterSystem := by
  intro X Y f hf
  rw [counterSystem_map_toFunctor]
  infer_instance

/-- The exact pointwise adjoint-equivalence datum selected from admissibility,
kept as a named object for the generated-loop calculation. -/
noncomputable def counterD :
    PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem :=
  pointwiseWAdjointEquivalenceDataOfAdmissible
    allMorphisms counterSystem_admissible

/-- The distinguished compositor evaluates to the nontrivial scalar. -/
theorem counterSystem_twisted_mapComp :
    counterSystem.mapComp a00.toLoc b00.toLoc =
      counterMapComp L0 M0 H0 := by
  rfl

/-- Each of the other seven nondegenerate triangular compositors is the scalar
identity compositor. -/
theorem counterSystem_untwisted_mapComp_a01_b10 :
    counterSystem.mapComp a01.toLoc b10.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a01_b11 :
    counterSystem.mapComp a01.toLoc b11.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a00_b01 :
    counterSystem.mapComp a00.toLoc b01.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a10_b01 :
    counterSystem.mapComp a10.toLoc b01.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a11_b11 :
    counterSystem.mapComp a11.toLoc b11.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a11_b10 :
    counterSystem.mapComp a11.toLoc b10.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

theorem counterSystem_untwisted_mapComp_a10_b00 :
    counterSystem.mapComp a10.toLoc b00.toLoc = scalarCompIso 1 := by
  simp [counterSystem, counterMapComp]

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
