import KuuOSFormal.HistoricalF36F40BridgeP39

/-!
# F112-P40 — ninety distinct genuine C60 physical supports per original F47 three-source pair

P39 proved that the original historical calibrated F47 frame's
physical supporting edge does NOT descend from its two un-erased,
separately typed F42 face and F55 rotation three-arrow witnesses.
This is because edge is a separate FIELD of the historical frame,
not present in the original calibrated three-arrow equality.

We now formalize the EXACT size of that underdetermination:
for ANY existing original historical C60F47SquareFrame B with
arbitrary properly typed face and rotation original source data,
EVERY one of the 90 original physical C60 edges yields a distinct,
still-calibrated historical frame with precisely the SAME old
Type-valued source face and F55 rotation 3-arrows.

This is proved through a genuine injective map from the
independently constructed Kuu original 90-edge carrier into the
fiber of original F47 frames above the FIXED two-arrow source pair.
A native Kuu edge is recovered exactly from each such frame by
the already proven old/native geometric edge equivalence.
No numerical Fin90 proxy, Gray primitive import into independent
Kuu, or inferred physical face support is involved.

This shows any genuinely source-faithful, geometry-respecting
extension of P38 must carry an additional C60 edge/incidence
support witness: the old three-arrow pair alone has at least
ninety geometrically distinct admissible physical-support choices.
P38's freely adjoined four-boundary presentation functor is
unchanged and is not promoted to a global F42/F55 3-equivalence.

OLD-SIDE-ONLY theorem, no new axioms, native_decide, sorry or admit.
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

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uP40 vP40 uDP40 vDP40
variable {C : Type uP40} [Category.{vP40} C]
variable {D : Type uDP40} [Category.{vDP40} D]
variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- The FULL fiber of original historical F47 frames retaining the
complete UNERASED pair of original F42-face and F55-rotation
Type-valued 3-cell proofs of a fixed genuine frame B.
It is not a fiber of numerical charge-only observations. -/
abbrev HistoricalF47ThreeSourceFiber
    (B : C60F47SquareFrame α β r s) :=
  { B' : C60F47SquareFrame α β r s //
      historicalF47ThreeSourcePair B' =
        historicalF47ThreeSourcePair B }

/-- Every original 90-edge Kuu carrier gives a different actual
historical F47 frame above the SAME complete F42/F55 proof pair,
by the established original/native edge equivalence. -/
def historicalF47AllEdgeFiberMap
    (B : C60F47SquareFrame α β r s) :
    Edge → HistoricalF47ThreeSourceFiber B :=
  fun e => ⟨historicalF47WithEdge B e,
    historicalF47WithEdge_threeSourcePair B e⟩

/-- The edge map preserves the EXACT original F42-face three-arrow.
No Prop erasure or shadow evaluator is substituted. -/
theorem historicalF47AllEdgeFiberMap_face
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47AllEdgeFiberMap B e).1.faceStep = B.faceStep := rfl

/-- The edge map likewise preserves the original F54/F55 rotation
three-arrow at its actual original typed route endpoints. -/
theorem historicalF47AllEdgeFiberMap_rotation
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47AllEdgeFiberMap B e).1.rotationStep =
      B.rotationStep := rfl

/-- Exactly recover the chosen old/native C60 geometric edge from
the REAL original historical F47 frame in the fiber. -/
theorem historicalF47AllEdgeFiberMap_support
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    frameKuuEdge (historicalF47AllEdgeFiberMap B e).1 = e :=
  historicalF47WithEdge_nativeSupport B e

/-- KEY: the ninety physical C60 supports inject into ONE fiber of
the original F42/F55 Type-valued source three-arrow pair.
No two distinct physical edges become equal historical F47 frames. -/
theorem historicalF47AllEdgeFiberMap_injective
    (B : C60F47SquareFrame α β r s) :
    Function.Injective (historicalF47AllEdgeFiberMap B) := by
  intro e f h
  have hh := congrArg
    (fun Q : HistoricalF47ThreeSourceFiber B => frameKuuEdge Q.1) h
  change frameKuuEdge (historicalF47WithEdge B e) =
    frameKuuEdge (historicalF47WithEdge B f) at hh
  simpa only [historicalF47WithEdge_nativeSupport] using hh

/-- The ORIGINAL independently constructed Kuu 90-edge physical
carrier is actually finite with 90 elements, not a constructed
Fin 90 used as a proxy for physical incidence. -/
theorem historicalF47PhysicalSupport_cardinality :
    Fintype.card Edge = 90 :=
  edge_card

/-- Precise mathematical meaning of AT LEAST ninety distinct
geometrically supported original F47 frames over the SAME raw
F42/F55 3-arrow source: an injective map from a 90-element
genuine physical-edge carrier into that source fiber. -/
theorem historicalF47Fiber_atLeastNinety
    (B : C60F47SquareFrame α β r s) :
    Fintype.card Edge = 90 ∧
    Function.Injective (historicalF47AllEdgeFiberMap B) :=
  ⟨historicalF47PhysicalSupport_cardinality,
    historicalF47AllEdgeFiberMap_injective B⟩

/-- Even when every old F47 frame's original source is unchanged,
the corresponding physical two-face native atlas recovers each
chosen genuine old edge WITHOUT identifying distinct C60 faces.
This is the geometric support needed for a future source-faithful
Beck–Chevalley transport. -/
theorem historicalF47AllEdgeFiberMap_twoFace_geometry
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    let P := historicalF47TwoFaceNativeAtlas
      (historicalF47AllEdgeFiberMap B e).1
    P.edge = e ∧
      P.edge ∈ polygonBoundaryEdges P.firstFace ∧
      P.edge ∈ polygonBoundaryEdges P.secondFace ∧
      P.firstFace ≠ P.secondFace := by
  refine ⟨historicalF47WithEdge_atlasSupport B e, ?_⟩
  exact historicalF47WithEdge_twoFace_real B e

/-- There are always TWO ACTUAL distinct members in the same
complete source fiber, at the specific original north-cross and
north-around edges. No unique physical support exists even after
retaining all original F42/F55 raw 3-source evidence. -/
theorem historicalF47SourceFiber_two_distinct_members
    (B : C60F47SquareFrame α β r s) :
    historicalF47AllEdgeFiberMap B (.cross (.northSpoke 0)) ≠
      historicalF47AllEdgeFiberMap B (.around ⟨.north, .s0⟩) :=
  (historicalF47AllEdgeFiberMap_injective B).ne
    northOriginalCross_ne_around

#print axioms HistoricalF47ThreeSourceFiber
#print axioms historicalF47AllEdgeFiberMap
#print axioms historicalF47AllEdgeFiberMap_face
#print axioms historicalF47AllEdgeFiberMap_rotation
#print axioms historicalF47AllEdgeFiberMap_support
#print axioms historicalF47AllEdgeFiberMap_injective
#print axioms historicalF47PhysicalSupport_cardinality
#print axioms historicalF47Fiber_atLeastNinety
#print axioms historicalF47AllEdgeFiberMap_twoFace_geometry
#print axioms historicalF47SourceFiber_two_distinct_members

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
