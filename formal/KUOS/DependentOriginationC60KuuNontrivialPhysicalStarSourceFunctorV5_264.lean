import KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263
import Mathlib.CategoryTheory.Category.Preorder
import Mathlib.Data.Bool.Basic

namespace KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
open KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261
open KUOS.DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.264 / F108 third stage — nonidentity F51 on the REAL WHOLE C60 star

F108 first stage constructed a genuine original F43/F51 interchanger
with charge (0,0), phase 1, between two DIFFERENT original F42 face
pasting orders on the same correct physical endpoint-to-endpoint paths.
F108 second stage constructed all required contexts from the original
C60 60-dart/90-edge graph. The former all-star functor used identity
three-words on every incidence arrow.

This module makes a NONIDENTITY original-source F51 categorical
semantics on ALL morphisms of each real physical incidence star.
The underlying original F69 incidence poset has a REAL monotone
two-stratum classification: original vertices have degree 0,
original physical edges and REAL pentagon/hexagon faces have degree 1.
The walking-arrow category Bool sends false to the ORIGINAL left
horizontal F42 pasting order, true to the ORIGINAL right order,
and false→true to the ACTUAL original F43/F51 interchanger.

Composition is now genuinely functorial across all original F69
incidence Homs. In particular every actual vertex→edge→face triangle
commutes after source F51 evaluation, while the vertex→edge arrow has
native NONZERO phase 1 (and both exact integer charges zero).

Limit: The same CHOSEN incident polygon's original double-face
F42 words label both upper strata at the given physical edge.
This proves the first globally-defined nonidentity star source
action, but does NOT yet independently label both adjacent polygon
faces by their own DIFFERENT original F42 boundaries, nor lift
the whole original F54/F55 source grammar or remove signed curvature.
-/

/-! ## I. The genuine monotone vertex / nonvertex strata -/

/-- Physical C60 incidence RANK of an ORIGINAL site: true is one
of the ACTUAL original 90 edges or 32 real polygonal faces.
This is NOT a newly inserted four-sided surface face. -/
def c60F108OriginalIncidenceStage : C60F69PhysicalCellSite → Bool
  | .vertex _ => false
  | .edge _ => true
  | .face _ => true

/-- Every genuine incidence arrow respects its original
vertex-to-edge-to-polygon order. This is proved from F69's
actual incidence PARTIAL ORDER, not assumed for arbitrary sites. -/
theorem c60F108OriginalIncidenceStage_monotone
    {X Y : C60F69PhysicalCellSite} (h : X ≤ Y) :
    c60F108OriginalIncidenceStage X ≤
      c60F108OriginalIncidenceStage Y := by
  cases X <;> cases Y <;>
    simp_all [c60F108OriginalIncidenceStage, c60F69PhysicalIncidence]

/-- The entire REAL physical singleton-star incidence category
maps to the genuine Boolean walking-arrow preorder category.
No physical incidence arrow is forgotten at source. -/
def c60F108StarToWalkingArrow
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) ⥤ Bool where
  obj X := c60F108OriginalIncidenceStage X.1
  map := fun {X Y} f => by
    apply CategoryTheory.homOfLE
    have h : X.1 ≤ Y.1 := CategoryTheory.leOfHom f
    exact c60F108OriginalIncidenceStage_monotone h
  map_id := by
    intro X
    apply Subsingleton.elim
  map_comp := by
    intro X Y Z f g
    apply Subsingleton.elim

/-! ## II. The ORIGINAL nontrivial F42/F51 walking-arrow target -/

/-- The actual source 2-cell object at each of the two strata.
Both are ORIGINAL F42 proof-relevant pasting words, not grades. -/
def c60F108WalkingSourceObject
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (b : Bool) :
    C60F51OriginalTwo
      ((c60F108DoubleFacePatchFamily C).p i)
      ((c60F108DoubleFacePatchFamily C).q i) :=
  if b then ⟨c60F108DoubleFaceRight C i⟩
  else ⟨c60F108DoubleFaceLeft C i⟩

/-- The unique nontrivial generator of Bool's walking-arrow
category is mapped to the ACTUAL source F43-derived nonidentity
F51 three-arrow; both endomorphism Homs map to identities. -/
def c60F108WalkingSourceMap
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    {b c : Bool} (f : b ⟶ c) :
    c60F108WalkingSourceObject C i b ⟶
      c60F108WalkingSourceObject C i c := by
  cases b <;> cases c
  · exact 𝟙 _
  · exact c60F108PhysicalThreeInterchangerHom C i
  · have hf : (true : Bool) ≤ false := CategoryTheory.leOfHom f
    exact False.elim ((by decide : ¬ ((true : Bool) ≤ false)) hf)
  · exact 𝟙 _

/-- A genuine Mathlib FUNCTOR from the walking arrow into the
ORIGINAL F51 native-kernel 3-Hom category; this is NOT the
phase-forgetting F95 category. -/
def c60F108WalkingToNativeF51
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    Bool ⥤
      C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) where
  obj := c60F108WalkingSourceObject C i
  map := fun {_ _} f => c60F108WalkingSourceMap C i f
  map_id := by
    intro b
    cases b <;> rfl
  map_comp := by
    intro b c d f g
    cases b <;> cases c <;> cases d
    all_goals
      first
      | exact False.elim
          ((by decide : ¬ ((true : Bool) ≤ false))
            (CategoryTheory.leOfHom f))
      | exact False.elim
          ((by decide : ¬ ((true : Bool) ≤ false))
            (CategoryTheory.leOfHom g))
      | simp [c60F108WalkingSourceMap, c60F108WalkingSourceObject]

/-- The first all-star NONIDENTITY original-source functor on the
actual C60 finite incidence-star subtype category. Its object
labels are two distinct original proof-relevant F42 words; its
vertex-to-nonvertex maps retain independent native phase 1. -/
def c60F108NontrivialPhysicalStarSourceFunctor
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) ⥤
      C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) :=
  c60F108StarToWalkingArrow C i ⋙
    c60F108WalkingToNativeF51 C i

/-- Genuine Kuu semantics of this NONIDENTITY F51 functor,
obtained by ORIGINAL F95 projection. No phase is brought back
from the quotient projection. -/
def c60F108NontrivialPhysicalStarKuuFunctor
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) ⥤
      C60F95LocalKuuQuotient
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) :=
  c60F108NontrivialPhysicalStarSourceFunctor C i ⋙
    c60F95LocalProjection
      ((c60F108DoubleFacePatchFamily C).p i)
      ((c60F108DoubleFacePatchFamily C).q i)

/-! ## III. Real actual-flag witnesses and NONTRIVIAL source 3-arrow -/

/-- The original actual endpoint dart is a member of the
true physical incidence star at its genuine original edge. -/
def c60F108StarActualVertex
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (endpoint : Bool) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) :=
  ⟨.vertex ((c60F46PhysicalFourFlagSquare (C.edge i)).vertex endpoint), by
    intro j hj
    have hji : j = i := Finset.mem_singleton.mp hj
    subst j
    exact (c60F106AllPhysicalFlags_in_star
      (C.edge i) endpoint (C.side i)).1⟩

/-- The genuine physical edge itself is in its F106 star. -/
def c60F108StarActualEdge
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) :=
  ⟨.edge (C.edge i), by
    intro j hj
    have hji : j = i := Finset.mem_singleton.mp hj
    subst j
    exact Or.inl (le_refl _)⟩

/-- A TRUE original C60 endpoint→physical-edge Hom inside
the FULL physical F106 star, not a synthetic path site. -/
def c60F108StarActualVertexEdge
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (endpoint : Bool) :
    c60F108StarActualVertex C i endpoint ⟶
      c60F108StarActualEdge C i :=
  CategoryTheory.homOfLE
    (c60F69PhysicalVertexEdge
      ((c60F46PhysicalFourFlagSquare (C.edge i)).vertex endpoint)
      (C.edge i) (c60F69ActualFlagEndpoint (C.edge i) endpoint))

/-- On EVERY real edge endpoint, the all-star source functor
is ACTUALLY nonidentity: its native F51 image is the precisely
typed original F43/F51 interchanger, not a synthetic zero word. -/
theorem c60F108StarActualVertexEdge_map
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (endpoint : Bool) :
    (c60F108NontrivialPhysicalStarSourceFunctor C i).map
      (c60F108StarActualVertexEdge C i endpoint) =
        c60F108PhysicalThreeInterchangerHom C i := rfl

/-- Native source phase ONE survives on ALL original
physical endpoint→edge arrows in the nonidentity star functor.
The two genuine Int×Int charges of this source arrow remain zero. -/
theorem c60F108StarActualVertexEdge_nativeComponents
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (endpoint : Bool) :
    (c60F51Eval
      ((c60F108NontrivialPhysicalStarSourceFunctor C i).map
        (c60F108StarActualVertexEdge C i endpoint))).charge =
        ((0 : Int), (0 : Int)) ∧
    (c60F51Eval
      ((c60F108NontrivialPhysicalStarSourceFunctor C i).map
        (c60F108StarActualVertexEdge C i endpoint))).phase =
        (1 : ZMod 2) := by
  rw [c60F108StarActualVertexEdge_map]
  exact c60F108PhysicalThreeInterchanger_components C i

/-! ## IV. Unconditional source semantics on all 90 real edge stars -/

/-- A TRUE original F51 nonidentity all-star functor for EACH of
the ninety actual C60 physical edges, using the original real
C60 free-path context construction of F108 stage two. -/
noncomputable def c60F108AllNinetyNontrivialSource
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    C60F106PhysicalOverlap
      (c60F108DoubleFacePatchFamily c60F109AllNinetyFaceContexts)
      ({i} : Finset (Fin (Fintype.card TruncatedIcosahedralEdge))) ⥤
      C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily c60F109AllNinetyFaceContexts).p i)
        ((c60F108DoubleFacePatchFamily c60F109AllNinetyFaceContexts).q i) :=
  c60F108NontrivialPhysicalStarSourceFunctor
    c60F109AllNinetyFaceContexts i

/-- All ninety original physical edge stars have a source-level
nonidentity vertex→edge arrow, full-native phase one with
zero original integer charges: the real braided source
remains nontrivial BEFORE its deliberate F95 phase quotient. -/
theorem c60F108AllNinetyNontrivial_nativePhase
    (i : Fin (Fintype.card TruncatedIcosahedralEdge))
    (endpoint : Bool) :
    (c60F51Eval
      ((c60F108AllNinetyNontrivialSource i).map
        (c60F108StarActualVertexEdge
          c60F109AllNinetyFaceContexts i endpoint))).phase =
      (1 : ZMod 2) :=
  (c60F108StarActualVertexEdge_nativeComponents
    c60F109AllNinetyFaceContexts i endpoint).2

#print axioms c60F108OriginalIncidenceStage_monotone
#print axioms c60F108StarToWalkingArrow
#print axioms c60F108WalkingSourceMap
#print axioms c60F108WalkingToNativeF51
#print axioms c60F108NontrivialPhysicalStarSourceFunctor
#print axioms c60F108NontrivialPhysicalStarKuuFunctor
#print axioms c60F108StarActualVertexEdge_map
#print axioms c60F108StarActualVertexEdge_nativeComponents
#print axioms c60F108AllNinetyNontrivialSource
#print axioms c60F108AllNinetyNontrivial_nativePhase

end
end KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264
