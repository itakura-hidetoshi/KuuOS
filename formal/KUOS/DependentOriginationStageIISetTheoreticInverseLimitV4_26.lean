import KUOS.DependentOriginationStageIICoherentFiniteDepthTowerV4_25
import Mathlib

namespace KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

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
open KUOS.DependentOriginationStageIICoherentFiniteDepthTowerV4_25

set_option autoImplicit false

noncomputable section

/-!
# Set-theoretic inverse limit of the finite-depth Stage-II tower v4.26

v4.25 supplies an explicit Nat-indexed tower of finite-depth central cells with
strict restriction maps.  The previous boundary deliberately stopped before
claiming an infinite limit.

This file now introduces a concrete set-theoretic inverse-limit object.

A section belongs to the limit exactly when

1. at every finite depth it lies in the eight-element canonical support image;
2. for every m <= n, restriction of the n-level section equals its m-level
   section.

The main theorem proves that every such compatible section comes from one
unique octahedral Stage-II source label.  Hence the inverse-limit carrier is
equivalent to the original eight-label source carrier.

This is an actual infinite compatible-section object indexed by Nat, but only
at the set-theoretic/incidence level.  No topology, metric, completeness,
convergence, compactness, Euclidean self-similarity, or fractal dimension is
introduced.

On the scalar side, the finite-depth obstruction section from v4.25 is already
constant.  We therefore define its inverse-limit value at depth zero and prove
that this equals every finite-depth value, equals the certified v4.12
obstruction, equals one in ZMod 2, is nonzero, and is transport-independent.
-/

/-- Predicate saying that a Nat-indexed section stays inside the canonical
eight-face support and is compatible with all inverse-direction restrictions. -/
def StageIIFiniteDepthSupportedCompatibleSection
    (section : Nat → StageIIIncidenceRecursiveDepthCell) : Prop :=
  (∀ depth : Nat,
      ∃ f : OctahedralStageIIParityFace,
        section depth = octahedralStageIIFiniteDepthTower f depth) ∧
    ∀ m n : Nat, m ≤ n →
      stageIIIncidenceRecursiveDepthRestrict m (section n) =
        section m

/-- The set-theoretic inverse limit of the supported finite-depth carrier
tower: compatible sections through all natural-number depths. -/
def StageIIFiniteDepthInverseLimit : Type :=
  {section : Nat → StageIIIncidenceRecursiveDepthCell //
    StageIIFiniteDepthSupportedCompatibleSection section}

/-- Every inverse-limit section lies in the canonical eight-face support at
each finite level. -/
theorem stageIIFiniteDepthInverseLimit_level_supported
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    ∃ f : OctahedralStageIIParityFace,
      x.1 depth = octahedralStageIIFiniteDepthTower f depth := by
  exact x.property.1 depth

/-- Every inverse-limit section satisfies the tower restriction law. -/
theorem stageIIFiniteDepthInverseLimit_restrict
    (x : StageIIFiniteDepthInverseLimit)
    (m n : Nat)
    (h : m ≤ n) :
    stageIIIncidenceRecursiveDepthRestrict m (x.1 n) =
      x.1 m := by
  exact x.property.2 m n h

/-- A source label determines a canonical compatible section through all
finite depths. -/
def octahedralStageIIParityFaceToFiniteDepthInverseLimit
    (f : OctahedralStageIIParityFace) :
    StageIIFiniteDepthInverseLimit :=
  ⟨fun depth => octahedralStageIIFiniteDepthTower f depth, by
    constructor
    · intro depth
      exact ⟨f, rfl⟩
    · intro m n h
      exact octahedralStageIIFiniteDepthTower_restrict_of_le f m n h⟩

@[simp] theorem octahedralStageIIParityFaceToFiniteDepthInverseLimit_apply
    (f : OctahedralStageIIParityFace)
    (depth : Nat) :
    (octahedralStageIIParityFaceToFiniteDepthInverseLimit f).1 depth =
      octahedralStageIIFiniteDepthTower f depth := by
  rfl

/-- A compatible supported inverse-limit section has one unique global source
label.  Compatibility at depth zero forces all locally chosen labels to agree. -/
theorem stageIIFiniteDepthInverseLimit_existsUnique_source
    (x : StageIIFiniteDepthInverseLimit) :
    ∃! f : OctahedralStageIIParityFace,
      ∀ depth : Nat,
        x.1 depth = octahedralStageIIFiniteDepthTower f depth := by
  rcases x.property.1 0 with ⟨f0, h0⟩
  have hAll :
      ∀ depth : Nat,
        x.1 depth = octahedralStageIIFiniteDepthTower f0 depth := by
    intro depth
    rcases x.property.1 depth with ⟨f, hf⟩
    have hCompat :=
      x.property.2 0 depth (Nat.zero_le depth)
    rw [hf, h0] at hCompat
    have hAtZero :
        octahedralStageIIFiniteDepthTower f 0 =
          octahedralStageIIFiniteDepthTower f0 0 := by
      simpa using hCompat
    have hSource : f = f0 :=
      octahedralStageIIFiniteDepthTower_injective 0 hAtZero
    simpa [hSource] using hf
  refine ⟨f0, hAll, ?_⟩
  intro g hg
  apply octahedralStageIIFiniteDepthTower_injective 0
  exact (hAll 0).symm.trans (hg 0)

/-- The canonical map from source labels into the inverse limit is injective. -/
theorem octahedralStageIIParityFaceToFiniteDepthInverseLimit_injective :
    Function.Injective
      octahedralStageIIParityFaceToFiniteDepthInverseLimit := by
  intro f g h
  apply octahedralStageIIFiniteDepthTower_injective 0
  have h0 :=
    congrArg
      (fun x : StageIIFiniteDepthInverseLimit => x.1 0) h
  simpa using h0

/-- Every supported compatible inverse-limit section is the canonical tower of
its unique source label. -/
theorem octahedralStageIIParityFaceToFiniteDepthInverseLimit_surjective :
    Function.Surjective
      octahedralStageIIParityFaceToFiniteDepthInverseLimit := by
  intro x
  rcases stageIIFiniteDepthInverseLimit_existsUnique_source x with
    ⟨f, hf, _⟩
  refine ⟨f, ?_⟩
  apply Subtype.ext
  funext depth
  exact (hf depth).symm

/-- Therefore the set-theoretic inverse-limit carrier has exactly the same
information as the original eight Stage-II source labels. -/
noncomputable def octahedralStageIIParityFaceEquivFiniteDepthInverseLimit :
    OctahedralStageIIParityFace ≃ StageIIFiniteDepthInverseLimit :=
  Equiv.ofBijective
    octahedralStageIIParityFaceToFiniteDepthInverseLimit
    ⟨octahedralStageIIParityFaceToFiniteDepthInverseLimit_injective,
      octahedralStageIIParityFaceToFiniteDepthInverseLimit_surjective⟩

/-- At any chosen depth, a canonical inverse-limit point evaluates to the
already-validated finite-depth tower cell of its source label. -/
@[simp] theorem octahedralStageIIParityFaceEquivFiniteDepthInverseLimit_apply
    (f : OctahedralStageIIParityFace)
    (depth : Nat) :
    (octahedralStageIIParityFaceEquivFiniteDepthInverseLimit f).1 depth =
      octahedralStageIIFiniteDepthTower f depth := by
  rfl

/-- The global integer mismatch carried by the inverse tower.  Depth zero is
used only as a representative; v4.25 proves all finite depths agree. -/
def counterStageIIFiniteDepthInverseLimitIntMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ℤ :=
  counterStageIIFiniteDepthRecursiveCarrierIntMismatch T 0

/-- The inverse-limit integer mismatch equals the finite-depth mismatch at
every depth. -/
theorem counterStageIIFiniteDepthInverseLimitIntMismatch_eq_depth
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthInverseLimitIntMismatch T =
      counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth := by
  exact
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_depth_independent
      T 0 depth

/-- The scalar inverse-limit obstruction is the compatible mod-two section
evaluated at depth zero. -/
def counterStageIIFiniteDepthInverseLimitObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  counterStageIIFiniteDepthObstructionSection T 0

/-- The inverse-limit obstruction equals the obstruction section at every
finite depth. -/
theorem counterStageIIFiniteDepthInverseLimitObstruction_eq_depth
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthInverseLimitObstruction T =
      counterStageIIFiniteDepthObstructionSection T depth := by
  exact
    counterStageIIFiniteDepthObstructionSection_compatible T 0 depth

/-- The inverse-limit obstruction is exactly the certified v4.12 Stage-II
obstruction class. -/
theorem counterStageIIFiniteDepthInverseLimitObstruction_eq_stageII
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthInverseLimitObstruction T =
      counterStageIIObstructionAdd T := by
  change
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T 0 : ℤ) :
        ZMod 2) =
      counterStageIIObstructionAdd T
  exact
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction
      T 0

/-- Therefore the inverse-limit obstruction is the nonzero class one. -/
theorem counterStageIIFiniteDepthInverseLimitObstruction_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthInverseLimitObstruction T = 1 := by
  rw [counterStageIIFiniteDepthInverseLimitObstruction_eq_stageII,
    counterStageIIObstructionAdd_eq_one]

/-- The Stage-II obstruction does not disappear upon passage to the
set-theoretic compatible-section limit. -/
theorem counterStageIIFiniteDepthInverseLimitObstruction_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthInverseLimitObstruction T ≠ 0 := by
  rw [counterStageIIFiniteDepthInverseLimitObstruction_eq_one]
  exact one_ne_zero

/-- The inverse-limit obstruction remains independent of the chosen coherent
quotient transport. -/
theorem counterStageIIFiniteDepthInverseLimitObstruction_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthInverseLimitObstruction T =
      counterStageIIFiniteDepthInverseLimitObstruction U := by
  rw [counterStageIIFiniteDepthInverseLimitObstruction_eq_stageII,
    counterStageIIFiniteDepthInverseLimitObstruction_eq_stageII]
  exact counterStageIIObstructionAdd_transport_independent T U

/-- The integer inverse-limit mismatch reduces exactly to the inverse-limit
mod-two obstruction. -/
theorem counterStageIIFiniteDepthInverseLimitIntMismatch_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ((counterStageIIFiniteDepthInverseLimitIntMismatch T : ℤ) : ZMod 2) =
      counterStageIIFiniteDepthInverseLimitObstruction T := by
  rfl

/-- Hence the integer inverse-limit mismatch is itself nonzero. -/
theorem counterStageIIFiniteDepthInverseLimitIntMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthInverseLimitIntMismatch T ≠ 0 := by
  intro hZero
  apply counterStageIIFiniteDepthInverseLimitObstruction_ne_zero T
  rw [← counterStageIIFiniteDepthInverseLimitIntMismatch_modTwo T, hZero]
  rfl

/-!
## Boundary after v4.26

The finite-depth tower now has an explicit infinite set-theoretic limit object:

  StageIIFiniteDepthInverseLimit.

A point is a Nat-indexed section that lies in the canonical eight-face support
at every level and satisfies every inverse-direction restriction law.

The key result is rigidity:

* every compatible section has one unique global source label;
* the canonical source-to-limit map is bijective;
* therefore the limit carrier is equivalent to the original eight-label
  octahedral Stage-II carrier.

The scalar obstruction also has a well-defined compatible limit value:

* it equals every finite-depth obstruction value;
* it equals the transport-independent v4.12 class;
* it is exactly one in ZMod 2;
* hence it is nonzero;
* the corresponding integer mismatch is nonzero as well.

This is an infinite-depth theorem only in the set-theoretic compatible-section
sense.  It does not provide topology, metric convergence, completeness,
compactness, Euclidean scaling, Hausdorff dimension, or a geometric fractal
limit.  Any such upgrade requires additional independently formalized
structure.
-/

end

end KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
