import KUOS.DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262
import KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163

namespace KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.263 / F108 second stage — original 60-vertex path connectivity

F108 first stage built genuine F42 polygon words with extra, correctly
typed contexts between each chosen edge and its adjacent polygon base.
Here those contexts are CONSTRUCTED FROM THE ORIGINAL 90 PHYSICAL EDGES,
not assumed. Every edge has two ORIGINAL directed quiver arrows, and
the 60 C60 darts are connected using the five around-pentagon slots,
north spokes, aligned cross edges, and one south spoke.

We construct a real reversed original Quiver.Path using actual reverse
physical edge arrows (no equality of nontrivial backtracking paths with
identity). Every pair of original darts is now connected by a finite,
genuinely typed original Quiver.Path. This constructs the F108 context
family for ANY real physical-edge patch selection, including ALL ninety
physical edges by their Fintype.equivFin enumeration.

This removes the PATH-EXISTENCE assumption from v5.262, but does NOT
identify distinct original F42 terms, erase F55 curvature, or turn the
conservative singleton-star identity-word semantics into a nontrivial
full-star source F51 functor.
-/

/-! ## I. Honest reversal of one actual oriented edge and a free path -/

/-- Genuine quiver arrow reversal switches forward/reverse codes for
the SAME physical edge. It is not a categorical inverse equality for
raw free paths and does not identify a length-two backtrack with nil. -/
def c60F109FlipArrow
    {a b : IcosahedralDart} (e : a ⟶ b) : b ⟶ a := by
  rcases e with ⟨e, ⟨ha, hb⟩⟩
  cases e with
  | forward physical =>
      exact ⟨.reverse physical, ⟨hb, ha⟩⟩
  | reverse physical =>
      exact ⟨.forward physical, ⟨hb, ha⟩⟩

/-- Reverse an actual original freely presented C60 path, traversing
each SAME original physical edge in the opposite direction.
The order of the edge word is reversed; this is not a quotient. -/
def c60F109ReversePath :
    {a b : IcosahedralDart} →
      Quiver.Path a b → Quiver.Path b a
  | _, _, .nil => .nil
  | _, _, .cons p e =>
      (c60F109FlipArrow e).toPath.comp (c60F109ReversePath p)

/-! ## II. Original pentagon paths, true north-to-all-darts paths -/

/-- Original one-step clockwise C60 pentagon path at the specified
icosahedral vertex and original physical pentagonal slot. -/
def c60F109AroundStepPath
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    Quiver.Path (icosahedralIncidentDartAt v s)
      (icosahedralIncidentDartAt v (pentagonalSlotNext s)) :=
  (c60F41ForwardArrow (.around ⟨v, s⟩)).toPath

/-- A genuinely typed 0–4 edge ORIGINAL pentagon path from its
slot-zero dart to each of its five actual incident darts. -/
def c60F109AroundPath
    (v : IcosahedralVertex) :
    (s : PentagonalSlot) →
      Quiver.Path (icosahedralIncidentDartAt v .s0)
        (icosahedralIncidentDartAt v s)
  | .s0 => .nil
  | .s1 => c60F109AroundStepPath v .s0
  | .s2 => (c60F109AroundStepPath v .s0).comp
      (c60F109AroundStepPath v .s1)
  | .s3 => ((c60F109AroundStepPath v .s0).comp
      (c60F109AroundStepPath v .s1)).comp
        (c60F109AroundStepPath v .s2)
  | .s4 => (((c60F109AroundStepPath v .s0).comp
      (c60F109AroundStepPath v .s1)).comp
        (c60F109AroundStepPath v .s2)).comp
          (c60F109AroundStepPath v .s3)

/-- Reach a REAL upper-ring base dart by the original north
pentagon and exactly one genuine north-spoke cross edge. -/
def c60F109RootToUpper (i : IcosahedralRingIndex) :
    Quiver.Path (icosahedralIncidentDartAt .north .s0)
      (icosahedralIncidentDartAt (.upper i) .s0) := by
  have p : Quiver.Path (icosahedralIncidentDartAt .north .s0)
      (.first (.northSpoke i)) := by
    simpa only [icosahedralIncidentDartAt, pentagonalSlotIndex_ofIndex]
      using c60F109AroundPath .north (pentagonalSlotOfIndex i)
  exact p.comp ((c60F41ForwardArrow (.cross (.northSpoke i))).toPath)

/-- From north to a lower-ring base: visit actual upper-ring slot
s2, cross the aligned original icosahedral edge, and reverse the
lower pentagon s0→s3 path to return to its true base dart. -/
def c60F109RootToLower (i : IcosahedralRingIndex) :
    Quiver.Path (icosahedralIncidentDartAt .north .s0)
      (icosahedralIncidentDartAt (.lower i) .s0) :=
  (((c60F109RootToUpper i).comp
    (c60F109AroundPath (.upper i) .s2)).comp
      ((c60F41ForwardArrow (.cross (.crossAligned i))).toPath)).comp
        (c60F109ReversePath (c60F109AroundPath (.lower i) .s3))

/-- The ORIGINAL south-pole base is reached from lower ring zero
by traversing the genuine south-spoke in the reverse orientation. -/
def c60F109RootToSouth :
    Quiver.Path (icosahedralIncidentDartAt .north .s0)
      (icosahedralIncidentDartAt .south .s0) :=
  (c60F109RootToLower 0).comp
    ((c60F41ReverseArrow (.cross (.southSpoke 0))).toPath)

/-- The actual north base reaches the slot-zero dart of ALL twelve
icosahedral pentagons, with no abstract connectedness axiom. -/
def c60F109RootToPentagon :
    (v : IcosahedralVertex) →
    Quiver.Path (icosahedralIncidentDartAt .north .s0)
      (icosahedralIncidentDartAt v .s0)
  | .north => .nil
  | .south => c60F109RootToSouth
  | .upper i => c60F109RootToUpper i
  | .lower i => c60F109RootToLower i

/-- TRUE Quiver.Path connectivity from the real north dart to
each of the original sixty darts. The F163 theorem supplies an
EXHAUSTIVE FINITE enumeration of actual vertex/slot names, not
an unverified graph connectedness hypothesis. -/
noncomputable def c60F109RootToEveryDart (d : IcosahedralDart) :
    Quiver.Path (icosahedralIncidentDartAt .north .s0) d := by
  obtain ⟨v, s, hs⟩ := c60EveryDartHasIncidentSlot d
  exact hs ▸ ((c60F109RootToPentagon v).comp (c60F109AroundPath v s))

/-- A source-level C60 path between ANY two of the sixty original
darts, by reverse original arrows to north and forward original
arrows from north. Nontrivial backtracks are kept as raw paths. -/
noncomputable def c60F109EveryDartToDart
    (a b : IcosahedralDart) : Quiver.Path a b :=
  (c60F109ReversePath (c60F109RootToEveryDart a)).comp
    (c60F109RootToEveryDart b)

/-- Mathematically stronger than a Z-linear edge-chain boundary:
genuine proof-relevant original Quiver.Path inhabited for EVERY
pair of vertices in the connected 60-vertex original C60 graph. -/
theorem c60F109EveryDartToDart_nonempty (a b : IcosahedralDart) :
    Nonempty (Quiver.Path a b) :=
  ⟨c60F109EveryDartToDart a b⟩

/-! ## III. Eliminate the extra path-input obstruction from F108 -/

/-- Canonical path contexts for ANY selected family of REAL C60
physical edges. Each selected adjacent real face is chosen as its
FIRST of the TWO actual C60 polygons; its ORIGINAL face-loop base
is connected to both edge endpoint darts by true original paths. -/
noncomputable def c60F109CanonicalFaceContextFamily
    {n : Nat} (edges : Fin n → TruncatedIcosahedralEdge) :
    C60F108FaceContextFamily n where
  edge := edges
  side := fun _ => false
  prior i :=
    c60F109EveryDartToDart
      (truncatedIcosahedralEdgeEndpoints (edges i)).1
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) false)).1
  suffix i :=
    c60F109EveryDartToDart
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) false)).1
      (truncatedIcosahedralEdgeEndpoints (edges i)).2

/-- F108's missing original C60 prior/suffix contexts EXIST on
every chosen collection of genuine physical edges, including any
singleton, finite overlap, and the entire ninety-edge atlas. -/
theorem c60F109CanonicalContextExists
    {n : Nat} (edges : Fin n → TruncatedIcosahedralEdge) :
    ∃ C : C60F108FaceContextFamily n, C.edge = edges :=
  ⟨c60F109CanonicalFaceContextFamily edges, rfl⟩

/-- Actual original F95 meaning for ANY real physical edge
collection WITHOUT externally supplied path contexts: the
F108 original F42 face generators and their proven charge
coherence now instantiate unconditionally for the chosen edges. -/
noncomputable def c60F109PhysicalEdgeF95Semantics
    {n : Nat} (edges : Fin n → TruncatedIcosahedralEdge) :
    C60F106SingletonF95Semantics
      (c60F108FacePatchFamily
        (c60F109CanonicalFaceContextFamily edges)) :=
  c60F108DerivedPhysicalSemantics
    (c60F109CanonicalFaceContextFamily edges)

/-- FULL finite enumeration of the original ninety REAL edge
types. No synthetic new faces or additional physical edges. -/
noncomputable def c60F109AllNinetyFaceContexts :
    C60F108FaceContextFamily
      (Fintype.card TruncatedIcosahedralEdge) :=
  c60F109CanonicalFaceContextFamily
    (fun i => (Fintype.equivFin TruncatedIcosahedralEdge).symm i)

/-- The original ninety-indexed incidence-star semantics derived
entirely from REAL original physical C60 path constructions.
This is still face-labelled, conservative on incidence arrows. -/
noncomputable def c60F109AllNinetyF95Semantics :
    C60F106SingletonF95Semantics
      (c60F108FacePatchFamily c60F109AllNinetyFaceContexts) :=
  c60F108DerivedPhysicalSemantics c60F109AllNinetyFaceContexts

/-- ALL ninety real edge choices admit the canonical original
nonidentity F51 3-word face-interchanger of F108. The phase
survives transport along truly constructed C60 path contexts. -/
theorem c60F109AllNinetyPhysicalInterchanger_nonzero_phase
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    (c60F108PhysicalThreeInterchanger
      c60F109AllNinetyFaceContexts i).toNative.phase =
      (1 : ZMod 2) :=
  (c60F108PhysicalThreeInterchanger_components
    c60F109AllNinetyFaceContexts i).2

#print axioms c60F109FlipArrow
#print axioms c60F109ReversePath
#print axioms c60F109RootToUpper
#print axioms c60F109RootToLower
#print axioms c60F109RootToSouth
#print axioms c60F109RootToPentagon
#print axioms c60F109RootToEveryDart
#print axioms c60F109EveryDartToDart_nonempty
#print axioms c60F109CanonicalContextExists
#print axioms c60F109PhysicalEdgeF95Semantics
#print axioms c60F109AllNinetyF95Semantics
#print axioms c60F109AllNinetyPhysicalInterchanger_nonzero_phase

end
end KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263
