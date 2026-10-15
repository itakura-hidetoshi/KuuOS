import KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
import Mathlib

namespace KUOS.DependentOriginationStageIICoherentFiniteDepthTowerV4_25

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
open KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
open KUOS.DependentOriginationStageIIOneStepRecursiveTransportV4_23
open KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
open KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90

set_option autoImplicit false

noncomputable section

/-!
# Coherent finite-depth Stage-II obstruction tower v4.25

v4.24 proves that the central-cell pullback transport preserves the Stage-II
carrier at every finite depth.  This file packages those depth-indexed cells
into an explicit restriction tower.

For any target depth m, restriction sends a depth cell to the canonical central
cell at depth m over the same original incidence-selected parent face.  On the
canonical tower this satisfies:

* restriction to the same depth is the identity;
* restriction from n to m lands exactly on the canonical m-cell;
* successive restrictions compose strictly;
* the retained parent face is unchanged.

Thus the eight global support labels form a coherent finite-depth inverse-style
tower over Nat.  The word "tower" here is finite-depth compatibility data; no
categorical or topological inverse limit is asserted.

The integer representative is compatible with every restriction because both
source and target depth cells pull back to the same validated v4.22 parent
representative.  Modulo two, the entire depth-indexed obstruction section is
therefore the constant section omega(T) = 1.

This is the compatibility theorem needed before any separate construction of an
actual infinite limit can be considered.
-/

/-- Restrict any depth cell to the canonical central cell at a chosen target
finite depth, retaining its original incidence-selected parent face. -/
def stageIIIncidenceRecursiveDepthRestrict
    (targetDepth : Nat)
    (c : StageIIIncidenceRecursiveDepthCell) :
    StageIIIncidenceRecursiveDepthCell :=
  stageIIIncidenceRecursiveDepthCell targetDepth c.parent

@[simp] theorem stageIIIncidenceRecursiveDepthRestrict_parent
    (targetDepth : Nat)
    (c : StageIIIncidenceRecursiveDepthCell) :
    (stageIIIncidenceRecursiveDepthRestrict targetDepth c).parent =
      c.parent := by
  rfl

@[simp] theorem stageIIIncidenceRecursiveDepthRestrict_depth
    (targetDepth : Nat)
    (c : StageIIIncidenceRecursiveDepthCell) :
    (stageIIIncidenceRecursiveDepthRestrict targetDepth c).depth =
      targetDepth := by
  rfl

/-- Restricting a canonical n-cell to depth m produces exactly the canonical
m-cell over the same parent. -/
@[simp] theorem stageIIIncidenceRecursiveDepthRestrict_canonical
    (targetDepth sourceDepth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    stageIIIncidenceRecursiveDepthRestrict targetDepth
        (stageIIIncidenceRecursiveDepthCell sourceDepth g) =
      stageIIIncidenceRecursiveDepthCell targetDepth g := by
  rfl

/-- Restriction to the current depth is the identity on canonical tower
objects. -/
@[simp] theorem stageIIIncidenceRecursiveDepthRestrict_self
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    stageIIIncidenceRecursiveDepthRestrict depth
        (stageIIIncidenceRecursiveDepthCell depth g) =
      stageIIIncidenceRecursiveDepthCell depth g := by
  rfl

/-- Restrictions compose strictly: once the original parent is retained,
passing through an intermediate depth does not affect the final restriction. -/
theorem stageIIIncidenceRecursiveDepthRestrict_comp
    (lower middle : Nat)
    (c : StageIIIncidenceRecursiveDepthCell) :
    stageIIIncidenceRecursiveDepthRestrict lower
        (stageIIIncidenceRecursiveDepthRestrict middle c) =
      stageIIIncidenceRecursiveDepthRestrict lower c := by
  rfl

/-- The canonical depth tower attached to one Stage-II source label. -/
def octahedralStageIIFiniteDepthTower
    (f : OctahedralStageIIParityFace)
    (depth : Nat) :
    StageIIIncidenceRecursiveDepthCell :=
  octahedralStageIIFiniteDepthChildPlacement depth f

/-- Every canonical tower level retains the original v4.19/v4.20 seed face. -/
@[simp] theorem octahedralStageIIFiniteDepthTower_parent
    (f : OctahedralStageIIParityFace)
    (depth : Nat) :
    (octahedralStageIIFiniteDepthTower f depth).parent =
      octahedralStageIIIncidenceSeedEquiv f := by
  rfl

/-- Every canonical tower level records its own finite depth. -/
@[simp] theorem octahedralStageIIFiniteDepthTower_depth
    (f : OctahedralStageIIParityFace)
    (depth : Nat) :
    (octahedralStageIIFiniteDepthTower f depth).depth = depth := by
  rfl

/-- Restriction between arbitrary tower levels is exact. -/
@[simp] theorem octahedralStageIIFiniteDepthTower_restrict
    (f : OctahedralStageIIParityFace)
    (targetDepth sourceDepth : Nat) :
    stageIIIncidenceRecursiveDepthRestrict targetDepth
        (octahedralStageIIFiniteDepthTower f sourceDepth) =
      octahedralStageIIFiniteDepthTower f targetDepth := by
  rfl

/-- In particular, every legitimate inverse-direction transition m <= n lands
on the canonical m-level. -/
theorem octahedralStageIIFiniteDepthTower_restrict_of_le
    (f : OctahedralStageIIParityFace)
    (m n : Nat)
    (_h : m ≤ n) :
    stageIIIncidenceRecursiveDepthRestrict m
        (octahedralStageIIFiniteDepthTower f n) =
      octahedralStageIIFiniteDepthTower f m := by
  rfl

/-- Canonical restrictions satisfy the expected two-step compatibility law. -/
theorem octahedralStageIIFiniteDepthTower_restrict_trans
    (f : OctahedralStageIIParityFace)
    (lower middle upper : Nat) :
    stageIIIncidenceRecursiveDepthRestrict lower
        (stageIIIncidenceRecursiveDepthRestrict middle
          (octahedralStageIIFiniteDepthTower f upper)) =
      stageIIIncidenceRecursiveDepthRestrict lower
        (octahedralStageIIFiniteDepthTower f upper) := by
  rfl

/-- At every level the eight source labels remain injectively separated. -/
theorem octahedralStageIIFiniteDepthTower_injective
    (depth : Nat) :
    Function.Injective
      (fun f : OctahedralStageIIParityFace =>
        octahedralStageIIFiniteDepthTower f depth) := by
  exact octahedralStageIIFiniteDepthChildPlacement_injective depth

/-- Although inner-cell adjacency is not newly postulated, every tower level
retains the actual adjacent parent seed faces from v4.19. -/
theorem octahedralStageIIFiniteDepthTower_mates_parent_adjacent
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    truncatedSeedPentagonHexagonAdjacent
      (octahedralStageIIFiniteDepthTower f depth).parent.1
      (octahedralStageIIFiniteDepthTower
        (octahedralStageIIMiddleSwitchMate f) depth).parent.1 := by
  simpa [octahedralStageIIFiniteDepthTower,
    octahedralStageIIFiniteDepthChildPlacement] using
    octahedralStageIIIncidenceSeedEquiv_mates_adjacent f

/-- The recursive inner kinds of middle-switch mates remain opposite at every
tower level. -/
theorem octahedralStageIIFiniteDepthTower_mates_opposite_innerKinds
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    (octahedralStageIIFiniteDepthTower f depth).innerKind ≠
      (octahedralStageIIFiniteDepthTower
        (octahedralStageIIMiddleSwitchMate f) depth).innerKind := by
  exact
    octahedralStageIIFiniteDepthChildPlacement_mates_opposite_innerKinds
      depth f

/-- Middle-switch orientation provenance remains flipped at every tower level. -/
theorem octahedralStageIIFiniteDepthTower_mates_orientation_flip
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceRecursiveDepthCellOrientation
        (octahedralStageIIFiniteDepthTower
          (octahedralStageIIMiddleSwitchMate f) depth) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceRecursiveDepthCellOrientation
          (octahedralStageIIFiniteDepthTower f depth)) := by
  exact
    octahedralStageIIFiniteDepthChildPlacement_mates_orientation_flip
      depth f

/-- Integer representatives are compatible with restriction between arbitrary
finite tower levels. -/
theorem counterTransportFiniteDepthTowerRepresentative_restrict
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (f : OctahedralStageIIParityFace)
    (targetDepth sourceDepth : Nat) :
    counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthRestrict targetDepth
          (octahedralStageIIFiniteDepthTower f sourceDepth)) =
      counterTransportRecursiveDepthCellIntRepresentative T
        (octahedralStageIIFiniteDepthTower f sourceDepth) := by
  rw [octahedralStageIIFiniteDepthTower_restrict]
  change
    counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell targetDepth
          (octahedralStageIIIncidenceSeedEquiv f)) =
      counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell sourceDepth
          (octahedralStageIIIncidenceSeedEquiv f))
  exact
    (counterTransportRecursiveDepthCellIntRepresentative_eq_parent
      T targetDepth (octahedralStageIIIncidenceSeedEquiv f)).trans
      (counterTransportRecursiveDepthCellIntRepresentative_eq_parent
        T sourceDepth (octahedralStageIIIncidenceSeedEquiv f)).symm

/-- The full integer total is compatible with every pair of finite depths. -/
theorem counterTransportFiniteDepthRecursiveCarrierIntTotal_depth_independent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (m n : Nat) :
    counterTransportFiniteDepthRecursiveCarrierIntTotal T m =
      counterTransportFiniteDepthRecursiveCarrierIntTotal T n := by
  exact
    (counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent T m).trans
      (counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent T n).symm

/-- The integral mismatch is likewise compatible with every pair of finite
depths. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_depth_independent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (m n : Nat) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T m =
      counterStageIIFiniteDepthRecursiveCarrierIntMismatch T n := by
  exact
    (counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent T m).trans
      (counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent T n).symm

/-- The mod-two obstruction section carried by the finite-depth tower. -/
def counterStageIIFiniteDepthObstructionSection
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    Nat → ZMod 2 :=
  fun depth =>
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
      ZMod 2)

/-- The entire finite-depth obstruction section is the constant section
omega(T). -/
theorem counterStageIIFiniteDepthObstructionSection_eq_constant
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthObstructionSection T =
      fun _ => counterStageIIObstructionAdd T := by
  funext depth
  exact
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction
      T depth

/-- Since omega(T)=1, the entire finite-depth section is constantly one. -/
theorem counterStageIIFiniteDepthObstructionSection_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthObstructionSection T =
      fun _ => 1 := by
  funext depth
  exact
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_one
      T depth

/-- Restriction compatibility of the scalar obstruction section. -/
theorem counterStageIIFiniteDepthObstructionSection_compatible
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (m n : Nat) :
    counterStageIIFiniteDepthObstructionSection T m =
      counterStageIIFiniteDepthObstructionSection T n := by
  change
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T m : ℤ) :
        ZMod 2) =
      ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T n : ℤ) :
        ZMod 2)
  exact congrArg (fun z : ℤ => (z : ZMod 2))
    (counterStageIIFiniteDepthRecursiveCarrierIntMismatch_depth_independent
      T m n)

/-- Every level of the tower carries a nonzero obstruction class. -/
theorem counterStageIIFiniteDepthObstructionSection_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthObstructionSection T depth ≠ 0 := by
  change
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
        ZMod 2) ≠ 0
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_one]
  exact one_ne_zero

/-- The whole finite-depth obstruction section is transport-independent. -/
theorem counterStageIIFiniteDepthObstructionSection_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthObstructionSection T =
      counterStageIIFiniteDepthObstructionSection U := by
  funext depth
  change
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
        ZMod 2) =
      ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch U depth : ℤ) :
        ZMod 2)
  exact
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_transport_independent
      T U depth

/-!
## Boundary after v4.25

The finite-depth central-cell construction is now not merely a family of
separate preservation theorems.  It is equipped with explicit restriction maps
that preserve the original parent face and satisfy strict composition on the
canonical tower.

Carrier level:
* eight source labels remain injective at every depth;
* restriction sends every canonical n-level to the canonical m-level;
* restrictions compose strictly;
* actual pentagon--hexagon adjacency is retained as parent provenance;
* opposite inner kind and orientation provenance persist at every level.

Scalar level:
* integer representatives are restriction-compatible;
* integer totals and mismatches are independent of finite depth;
* the mod-two obstruction section is the constant section omega(T)=1;
* that section is nonzero and transport-independent.

This supplies a coherent finite-depth tower.  It still does not construct an
infinite inverse limit, a topology on the tower, a metric contraction, or a
fractal limit.  Any next limit theorem must introduce and justify the required
limit object rather than infer it from finite-depth compatibility alone.
-/

end

end KUOS.DependentOriginationStageIICoherentFiniteDepthTowerV4_25
