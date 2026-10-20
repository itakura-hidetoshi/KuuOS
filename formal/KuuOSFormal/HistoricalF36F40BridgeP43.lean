import KuuOSFormal.HistoricalF36F40BridgeP42

/-!
# F112-P43 — honest historical/native C60 adjacent-face permutation and all 360 flags

The P42 original-to-native source packet provides a genuine open,
nonidentity original F42 face 2-cell, plus an un-erased Type-valued
independent C60 fan/disk proof, for EVERY one of the real 90 physical
edges and either original adjacent-face choice.

However the original and independent C60 face-choice Bool indices
are not interchangeable by fiat. We construct the required matching
from the ACTUAL edge-face incidence relation, prove it transports
each historical face label to precisely the corresponding one of the
TWO native adjacent faces, and prove the two original face choices
have DISTINCT native indices. The result permits a possible local
permutation of the old/new face-choice coordinates.

We then attach the genuine independent two-arrow physical incidence
flag triangle to P42's source certificate at EVERY choice of
  * one of the 90 genuine C60 edges,
  * one of the 2 actual endpoint darts,
  * one of the 2 actual original adjacent C60 polygon faces.
This gives a genuinely typed physical F42 source above all 360 real
C60 flags, with exact original boundary word, original F43 degree
one and independent F69 fan/disk soundness; no artificial square
surface face, Gray primitive, or unproved source equivalence.

This is an OLD-SIDE-only comparison. The full old Quiver.Path and
independent Kuu F69 Zigzag source 1-path grammars and F54/F55 full
higher-source categories are not equated. No sorry, admit or
new axioms.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

set_option autoImplicit false
set_option warningAsError true
set_option maxHeartbeats 2000000
noncomputable section

/-- TRUE independent original C60 edge/face incidence determines
membership in the exactly TWO genuine physical polygon faces.
This is a finite fact about the actual 90-edge/32-face geometry,
not a chosen numerical target or an additional axiom. -/
theorem nativeC60IncidentFace_iff_twoChoices :
    ∀ (e : Edge) (p : Polygon),
      edgeOnFace e p ↔
        p = faceAt e false ∨ p = faceAt e true := by
  decide

/-- For any old face choice, its exact independent Kuu polygon
lies on one of the two ACTUAL independently indexed native faces
adjacent to the same real physical edge. No equality of original
and native Bool conventions is presupposed. -/
theorem historicalF42NativeFace_exists
    (e : Edge) (side : Bool) :
    ∃ j : Bool,
      polygonEquiv.symm (historicalF42EdgeSelectedFace e side) =
        faceAt e j := by
  have hi := historicalF42EdgeActual_native_incidence e side
  rcases (nativeC60IncidentFace_iff_twoChoices e
    (polygonEquiv.symm (historicalF42EdgeSelectedFace e side))).mp hi with
    h | h
  · exact ⟨false, h⟩
  · exact ⟨true, h⟩

/-- The native face-side index for an ACTUAL historical edge/face
source is read from its true independent C60 polygon, rather than
asserted to be the same Bool as the old face choice. -/
def historicalF42NativeSide (e : Edge) (side : Bool) : Bool :=
  if polygonEquiv.symm (historicalF42EdgeSelectedFace e side) =
      faceAt e false then false else true

/-- Every old adjacency choice is carried to the EXACT right
native polygon: matching is established from actual incidence. -/
theorem historicalF42NativeSide_spec
    (e : Edge) (side : Bool) :
    polygonEquiv.symm (historicalF42EdgeSelectedFace e side) =
      faceAt e (historicalF42NativeSide e side) := by
  unfold historicalF42NativeSide
  split_ifs with h
  · exact h
  · rcases historicalF42NativeFace_exists e side with ⟨j, hj⟩
    cases j
    · exact False.elim (h hj)
    · exact hj

/-- The two genuine, separately typed original face choices on
every C60 edge cannot be mapped to ONE native face-side index.
The old/new Bool permutation is therefore INJECTIVE, rather than
an assumed identity map. -/
theorem historicalF42NativeSide_false_ne_true (e : Edge) :
    historicalF42NativeSide e false ≠
      historicalF42NativeSide e true := by
  intro hh
  have heq :
      polygonEquiv.symm (historicalF42EdgeSelectedFace e false) =
        polygonEquiv.symm (historicalF42EdgeSelectedFace e true) := by
    calc
      polygonEquiv.symm (historicalF42EdgeSelectedFace e false) =
          faceAt e (historicalF42NativeSide e false) :=
        historicalF42NativeSide_spec e false
      _ = faceAt e (historicalF42NativeSide e true) := by rw [hh]
      _ = polygonEquiv.symm
          (historicalF42EdgeSelectedFace e true) :=
        (historicalF42NativeSide_spec e true).symm
  have hf := congrArg polygonEquiv heq
  have hfaces :
      historicalF42EdgeSelectedFace e false =
        historicalF42EdgeSelectedFace e true := by
    simpa only [polygonEquiv.apply_symm_apply] using hf
  exact historicalF42EdgeActual_twoFaces_distinct e hfaces

/-- The ORIGINAL adjacency choices are mapped injectively to
independent native face-choice Bool slots for each genuine edge. -/
theorem historicalF42NativeSide_injective (e : Edge) :
    Function.Injective (historicalF42NativeSide e) := by
  intro i j h
  cases i <;> cases j
  · rfl
  · exact False.elim (historicalF42NativeSide_false_ne_true e h)
  · exact False.elim
      (historicalF42NativeSide_false_ne_true e h.symm)
  · rfl

/-- A source packet above one ACTUAL physical C60 flag.
The native F42 fan/disk and the old F42 source witness live in
separate, proof-relevant source types. Their physical polygon
matches the old genuine face by a PROVED side-choice correspondence. -/
structure HistoricalF42ActualNativeFlag
    (e : Edge) (endpointSide historicalSide : Bool) where
  physical : HistoricalF42PhysicalFaceSupport
    (historicalF42EdgeSelectedFace e historicalSide)
  physicalFace_eq :
    physical.nativeFace = faceAt e
      (historicalF42NativeSide e historicalSide)
  originalF42 : HistoricalF42NativeAnnotated
    (historicalF42EdgeActualFaceCell e historicalSide)
  original_degree :
    c60F43FaceDegree (historicalF42EdgeActualFaceCell e historicalSide) =
      (1 : ZMod 2)
  nativeFlag : ComposableArrows Site 2
  nativeFlag_exact :
    nativeFlag = flagTriangle e endpointSide
      (historicalF42NativeSide e historicalSide)

/-- Construct a real original F42 contextual 2-cell and its full
independent C60 Type-valued proof packet at each actual flag,
including the physical dart-endpoint choice and the correctly
permuted original/native adjacent polygon side. -/
def historicalF42ActualNativeFlag
    (e : Edge) (endpointSide historicalSide : Bool) :
    HistoricalF42ActualNativeFlag e endpointSide historicalSide where
  physical :=
    historicalF42CanonicalFaceSupport
      (historicalF42EdgeSelectedFace e historicalSide)
  physicalFace_eq := historicalF42NativeSide_spec e historicalSide
  originalF42 := historicalF42EdgeActualAnnotated e historicalSide
  original_degree :=
    historicalF42EdgeActualFace_degree_one e historicalSide
  nativeFlag :=
    flagTriangle e endpointSide
      (historicalF42NativeSide e historicalSide)
  nativeFlag_exact := rfl

/-- The native physical polygon in each flag is the SAME as the
original F42 physical source's genuine historical face, not a
generic triangle, square or artificially reassigned index. -/
theorem historicalF42Flag_native_face_matches
    (e : Edge) (endpointSide historicalSide : Bool) :
    (historicalF42ActualNativeFlag e endpointSide historicalSide).physical.nativeFace =
      faceAt e (historicalF42NativeSide e historicalSide) :=
  (historicalF42ActualNativeFlag e endpointSide historicalSide).physicalFace_eq

/-- A genuine two-leg physical incidence flag retains two
DIFFERENT ranks: actual vertex→edge and edge→true face. -/
theorem historicalF42Flag_rank_nontrivial
    (e : Edge) (endpointSide historicalSide : Bool) :
    Site.vertex
        (if endpointSide then (edgeEndpoints e).2 else (edgeEndpoints e).1) ≠
      Site.edge e ∧
    Site.edge e ≠ Site.face
      (polygonEquiv.symm (historicalF42EdgeSelectedFace e historicalSide)) := by
  have h := flagTriangle_distinct e endpointSide
    (historicalF42NativeSide e historicalSide)
  rw [historicalF42NativeSide_spec e historicalSide]
  exact h

/-- Each original contextual F42 physical 2-source represented by
the new 360-flag packet still contains exactly ONE true face,
and the complete original ordered five/six-edge boundary word. -/
theorem historicalF42Flag_original_source_and_word
    (e : Edge) (endpointSide historicalSide : Bool) :
    ((historicalF42ActualNativeFlag e endpointSide historicalSide).originalF42).supports =
        [⟨historicalF42EdgeSelectedFace e historicalSide,
          historicalF42CanonicalFaceSupport
            (historicalF42EdgeSelectedFace e historicalSide)⟩] ∧
    ((historicalF42ActualNativeFlag e endpointSide historicalSide).originalF42).originalWords =
        [kernelC60FullFaceBoundaryEdges
          (historicalF42EdgeSelectedFace e historicalSide)] :=
  ⟨historicalF42EdgeActual_single_source e historicalSide,
    historicalF42EdgeActual_original_boundary e historicalSide⟩

/-- Every such native F42 source has the EXACT independent F69
disk-kernel proof, even after supplying the original historical
Quiver.Path contexts and one of its two actual endpoint vertices. -/
theorem historicalF42Flag_native_disk_kernel
    (e : Edge) (endpointSide historicalSide : Bool) :
    let P := (historicalF42ActualNativeFlag e endpointSide historicalSide).physical
    zigzagKernelQ.map (polygonRawLoop P.nativeFace) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart P.nativeFace 0))) :=
  (historicalF42ActualNativeFlag e endpointSide historicalSide).physical.disk_sound

/-- All 360 physical original C60 vertex-edge-face flag choices
carry independently constructed ORIGINAL endpoint-typed F42
contextual 2-cell evidence AND a full native proof-relevant
physical fan/disk/flag triangle. There is no fabricated Fin 360
carrier: the domain is precisely Edge × Bool × Bool. -/
theorem historicalF42_all360_true_source_flags :
    Fintype.card (Edge × (Bool × Bool)) = 360 ∧
    (∀ t : Edge × (Bool × Bool),
      Nonempty (HistoricalF42ActualNativeFlag t.1 t.2.1 t.2.2)) :=
  ⟨flag_card, fun t =>
    ⟨historicalF42ActualNativeFlag t.1 t.2.1 t.2.2⟩⟩

#print axioms nativeC60IncidentFace_iff_twoChoices
#print axioms historicalF42NativeFace_exists
#print axioms historicalF42NativeSide
#print axioms historicalF42NativeSide_spec
#print axioms historicalF42NativeSide_false_ne_true
#print axioms historicalF42NativeSide_injective
#print axioms HistoricalF42ActualNativeFlag
#print axioms historicalF42ActualNativeFlag
#print axioms historicalF42Flag_native_face_matches
#print axioms historicalF42Flag_rank_nontrivial
#print axioms historicalF42Flag_original_source_and_word
#print axioms historicalF42Flag_native_disk_kernel
#print axioms historicalF42_all360_true_source_flags

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
