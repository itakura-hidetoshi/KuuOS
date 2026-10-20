import KuuOSFormal.HistoricalF36F40BridgeP38

/-!
# F112-P39 — original F47 physical-edge support is independent source data

Unlike a genuine type-indexed physical F42 support certificate, the
F59-F47 original C60F47SquareFrame retains its actual historical C60
edge in a FIELD separate from the old F42 physical face 3-arrow and
original F55 rotation 3-arrow. The calibration equality only
constrains their original chosen full-gray evaluations; it does NOT
reference the physical edge.

We prove this as an actual SOURCE-LEVEL NO-GO, rather than guessing a
historical/native F42 3-source equivalence:
  * changing the genuine original 90-edge C60 support does not change
    the two original proof-relevant F47 source 3-arrows, or the proven
    mixed-square calibration;
  * two physically DIFFERENT original C60 edges give two distinct
    native edges and corresponding authentic two-face fan/disk atlases;
  * NO function of the original F42 face 3-arrow and F55 rotation
    3-arrow alone can reconstruct the historical frame's physical
    C60 supporting edge, even with a FIXED original frame as witness;
  * hence even a function of their un-erased Type-valued pair cannot
    reconstruct the frame-indexed physical two-face atlas support.

The correct next genuinely type-faithful historical F47 F42/F55
comparison must supply an additional source-support/incidence
witness or restrict to a supported frame, not reconstruct this
missing relation from full signed charge, phase or the old raw 3-arrows.

OLD-SIDE-only validation. No Gray import in independent KuuOSStrict,
no alteration to preserved original KUOS.*, no sorry/admit/new axioms.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uP39 vP39 uDP39 vDP39
variable {C : Type uP39} [Category.{vP39} C]
variable {D : Type uDP39} [Category.{vDP39} D]
variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Preserve the ACTUAL original F42 and original F55 proof-relevant
3-arrows and their PROVED mixed square, but change only the physically
stored C60 edge using the previously certified constructor-level
old/native Edge equivalence. This is a fully valid original frame
because the original calibration does not constrain its edge field. -/
def historicalF47WithEdge
    (B : C60F47SquareFrame α β r s)
    (e : Edge) : C60F47SquareFrame α β r s :=
  { B with edge := edgeEquiv e }

/-- Replacing the physical edge does not alter the original F42
face 3-cell witness, even as a Type-valued source proof. -/
theorem historicalF47WithEdge_faceStep
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47WithEdge B e).faceStep = B.faceStep := rfl

/-- Nor is the original F55 rotation 3-cell replaced by an
evaluated charge or an independently invented 3-proof. -/
theorem historicalF47WithEdge_rotationStep
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47WithEdge B e).rotationStep = B.rotationStep := rfl

/-- Every changed-edge historical frame is STILL calibrated using
the original actual F42/F55 higher-source target values. -/
theorem historicalF47WithEdge_calibrated
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    c60F44FaceThreeEval (historicalF47WithEdge B e).faceStep +
        c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55Eval
        (historicalF47WithEdge B e).rotationStep :=
  (historicalF47WithEdge B e).calibrated

/-- The resulting old F47 physical edge, reconstructed through the
already proved original/native C60 equivalence, is EXACTLY e. -/
theorem historicalF47WithEdge_nativeSupport
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    frameKuuEdge (historicalF47WithEdge B e) = e := by
  change edgeEquiv.symm (edgeEquiv e) = e
  exact edgeEquiv.symm_apply_apply e

/-- P36's actual native two-face atlas still carries the exact
chosen original edge, and two complete real F42 polygon sources
on its two genuinely adjacent physical faces. -/
theorem historicalF47WithEdge_atlasSupport
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47TwoFaceNativeAtlas
      (historicalF47WithEdge B e)).edge = e :=
  historicalF47WithEdge_nativeSupport B e

/-- Both independent original adjacent C60 faces actually have the
selected edge on their boundary, and these faces are distinct. -/
theorem historicalF47WithEdge_twoFace_real
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    let P := historicalF47TwoFaceNativeAtlas
      (historicalF47WithEdge B e)
    P.edge ∈ polygonBoundaryEdges P.firstFace ∧
      P.edge ∈ polygonBoundaryEdges P.secondFace ∧
      P.firstFace ≠ P.secondFace := by
  exact ⟨(historicalF47TwoFaceNativeAtlas
      (historicalF47WithEdge B e)).firstEdge_onBoundary,
    (historicalF47TwoFaceNativeAtlas
      (historicalF47WithEdge B e)).secondEdge_onBoundary,
    (historicalF47TwoFaceNativeAtlas
      (historicalF47WithEdge B e)).faces_ne⟩

/-- Two genuinely distinct physical edges of the original
truncated icosahedron, not two proxy tags in a Finite set. -/
theorem northOriginalCross_ne_around :
    (Edge.cross (.northSpoke 0)) ≠
      Edge.around ⟨.north, .s0⟩ := by
  intro h
  cases h

/-- Keep the actual un-erased old proof-relevant F42 face and F55
rotation 3-arrow witnesses as one source data item; the old edge
is intentionally NOT stored in this two-proof observation. -/
def historicalF47ThreeSourcePair
    (B : C60F47SquareFrame α β r s) :
    (α ⟶ β) × (r ⟶ s) :=
  (B.faceStep, B.rotationStep)

/-- Both physically DIFFERENT F47 frames have the EXACT SAME pair
of original source three-arrows and the original mixed calibration. -/
theorem historicalF47WithEdge_threeSourcePair
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    historicalF47ThreeSourcePair (historicalF47WithEdge B e) =
      historicalF47ThreeSourcePair B := rfl

/-- CORE NO-GO: for ANY existing original calibrated F47 frame B,
there is NO universal decoder that can reconstruct the physically
stored native C60 90-edge from the old proof-relevant F42 face
three-arrow and original F55 rotation three-arrow ALONE.

Proof: replace B's original real physical edge by an actual
north cross edge and by a different original north around edge.
Both old 3-source witnesses remain identical, and both original
calibration equations remain true, but the native edges differ. -/
theorem historicalF47PhysicalSupport_not_determined_by_threeSources
    (B : C60F47SquareFrame α β r s) :
    ¬ ∃ decode :
        (α ⟶ β) → (r ⟶ s) → Edge,
      ∀ B' : C60F47SquareFrame α β r s,
        decode B'.faceStep B'.rotationStep = frameKuuEdge B' := by
  rintro ⟨decode, hdecode⟩
  have hcross := hdecode
    (historicalF47WithEdge B (.cross (.northSpoke 0)))
  have haround := hdecode
    (historicalF47WithEdge B (.around ⟨.north, .s0⟩))
  have hc : decode B.faceStep B.rotationStep =
      (Edge.cross (.northSpoke 0)) := by
    simpa only [historicalF47WithEdge_faceStep,
      historicalF47WithEdge_rotationStep,
      historicalF47WithEdge_nativeSupport] using hcross
  have ha : decode B.faceStep B.rotationStep =
      (Edge.around ⟨.north, .s0⟩) := by
    simpa only [historicalF47WithEdge_faceStep,
      historicalF47WithEdge_rotationStep,
      historicalF47WithEdge_nativeSupport] using haround
  exact northOriginalCross_ne_around (hc.symm.trans ha)

/-- Stronger geometric consequence: even the complete native
first/second face atlas SUPPORT (edge plus both actual polygons)
cannot be reconstructed from the two un-erased ORIGINAL F42/F55
three-arrow witnesses without an additional physical support
datum. This is not a no-go on the already stored full F47 frame. -/
theorem historicalF47AtlasSupport_no_sourcePairDecoder
    (B : C60F47SquareFrame α β r s) :
    ¬ ∃ decode : ((α ⟶ β) × (r ⟶ s)) → Edge,
      ∀ B' : C60F47SquareFrame α β r s,
        decode (historicalF47ThreeSourcePair B') =
          (historicalF47TwoFaceNativeAtlas B').edge := by
  rintro ⟨decode, hdecode⟩
  apply historicalF47PhysicalSupport_not_determined_by_threeSources B
  refine ⟨fun face rotation => decode (face, rotation), ?_⟩
  intro B'
  exact hdecode B'

#print axioms historicalF47WithEdge
#print axioms historicalF47WithEdge_faceStep
#print axioms historicalF47WithEdge_rotationStep
#print axioms historicalF47WithEdge_calibrated
#print axioms historicalF47WithEdge_nativeSupport
#print axioms historicalF47WithEdge_atlasSupport
#print axioms historicalF47WithEdge_twoFace_real
#print axioms northOriginalCross_ne_around
#print axioms historicalF47ThreeSourcePair
#print axioms historicalF47WithEdge_threeSourcePair
#print axioms historicalF47PhysicalSupport_not_determined_by_threeSources
#print axioms historicalF47AtlasSupport_no_sourcePairDecoder

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
