import KuuOSFormal.HistoricalF36F40BridgeP44

/-!
# F112-P45 — endpoint-faithful transport along genuine physical flags

The already certified P44 equivalence reindexes all 360 physical
vertex-edge-face flags, retaining their true edge and endpoint.
This module isolates the exact native categorical two-arrow witness
that is transported, and proves its physical source and target ranks.

It does NOT identify arbitrary historical Quiver.Path with native
raw Zigzag; that further source comparison remains open.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The actual physical flag transported from any old-side slot. -/
def historicalF42TransportedPhysicalTriangle
    (e : Edge) (endpointSide historicalSide : Bool) :
    ComposableArrows Site 2 :=
  flagTriangle e endpointSide (historicalF42NativeSide e historicalSide)

/-- The transported triangle is exactly the one carried by
the old contextual F42 proof-relevant packet. -/
theorem historicalF42TransportedPhysicalTriangle_exact
    (e : Edge) (endpointSide historicalSide : Bool) :
    historicalF42TransportedPhysicalTriangle e endpointSide historicalSide =
      (historicalF42ActualNativeFlag e endpointSide historicalSide).nativeFlag :=
  (historicalF42ActualNativeFlag e endpointSide historicalSide).nativeFlag_exact.symm

/-- Inverse native-side indexing recovers the same true physical
two-arrow triangle, without changing the endpoint or edge. -/
theorem historicalF42TransportedPhysicalTriangle_native_inverse
    (e : Edge) (endpointSide nativeSide : Bool) :
    historicalF42TransportedPhysicalTriangle e endpointSide
      ((historicalF42SideEquiv e).symm nativeSide) =
        flagTriangle e endpointSide nativeSide := by
  unfold historicalF42TransportedPhysicalTriangle
  rw [historicalF42SideEquiv_rightInverse]

/-- The transported flag's three actual site ranks are distinct
at the vertex/edge and edge/face boundaries. -/
theorem historicalF42TransportedPhysicalTriangle_distinct
    (e : Edge) (endpointSide historicalSide : Bool) :
    Site.vertex
      (if endpointSide then (edgeEndpoints e).2 else (edgeEndpoints e).1) ≠
        Site.edge e ∧
    Site.edge e ≠
      Site.face (faceAt e (historicalF42NativeSide e historicalSide)) :=
  flagTriangle_distinct e endpointSide
    (historicalF42NativeSide e historicalSide)

/-- The old genuine physical face is precisely the transported
native triangle's polygon. -/
theorem historicalF42TransportedPhysicalTriangle_face
    (e : Edge) (endpointSide historicalSide : Bool) :
    polygonEquiv.symm (historicalF42EdgeSelectedFace e historicalSide) =
      faceAt e (historicalF42NativeSide e historicalSide) :=
  historicalF42NativeSide_spec e historicalSide

#print axioms historicalF42TransportedPhysicalTriangle
#print axioms historicalF42TransportedPhysicalTriangle_exact
#print axioms historicalF42TransportedPhysicalTriangle_native_inverse
#print axioms historicalF42TransportedPhysicalTriangle_distinct
#print axioms historicalF42TransportedPhysicalTriangle_face

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
