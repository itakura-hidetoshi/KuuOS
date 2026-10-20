import KuuOSFormal.HistoricalF36F40BridgeP41
import KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

/-!
# F112-P42 — actual original C60 contextual F42 paths and native Kuu face evidence

P41 attached Type-valued genuine independent C60 physical fan/disk
witnesses and exact old ordered boundary words to ALL six original
F42 raw 2-cell constructors. It deliberately did not identify the
original old Quiver.Path source with the native F69 Zigzag source.

The preserved F108/F109 original C60 formalization has ALREADY proved
something stronger than path existence hypotheses: a real original
Quiver.Path between ANY TWO of the actual sixty physical C60 darts.
F108 used these real path contexts to turn a CLOSED old five/six-edge
original F42 physical-face loop into a genuinely typed OPEN endpoint-
to-endpoint F42 source cell over a selected actual edge and face.

P42 now connects those proven existing results to P41's genuinely
independent Kuu annotation, without reinventing the physical path
or assuming missing old/new source 2-category equivalences:

- for any native physical C60 Edge and either of its real face
  choices, construct actual original F108 1-path contexts with F109;
- construct the actual OLD F42 face 2-cell between these genuine
  open endpoint-to-endpoint original Quiver.Paths, of physical face
  degree ONE, not a synthetic identity label;
- annotate that exact original F42 term with a FULL native Type-valued
  physical face fan/disk source and exact ORIGINAL ordered edge word;
- prove physical incidence of the selected actual original edge and
  its chosen real original C60 face (not a generic proxy);
- instantiate those source annotations simultaneously for the
  previously proven ALL NINETY actual original C60 physical edge
  contexts of F109, without any extra path-existence assumptions.

All original source/target path indices remain intact. Original
historic six-edge word reversal remains exact. This does NOT assert
the old Quiver.Path source is equivalent to the independent Kuu
Zigzag category, nor identify original F51/55 raw higher source
with the independent native F42/F54/F55 system or old F68 curvature.
OLD-SIDE-ONLY, no independent KuuOSStrict Gray imports or new axioms.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The selected ACTUAL historical C60 face adjoining the
constructor-wise transported genuine independent Kuu physical edge.
Both independently chosen face sides are kept, not collapsed. -/
def historicalF42EdgeSelectedFace (e : Edge) (side : Bool) :
    TruncatedIcosahedralSeedFace :=
  c60F48AdjacentRealFace (edgeEquiv e) side

/-- The F109 original C60 path construction supplies BOTH
endpoint-to-face-base contexts for ANY actual physical Kuu edge and
EITHER adjacent face. No external free path assumptions are made. -/
def historicalF42EdgeActualContexts (e : Edge) (side : Bool) :
    C60F108FaceContextFamily 1 where
  edge := fun _ => edgeEquiv e
  side := fun _ => side
  prior := fun _ =>
    c60F109EveryDartToDart
      (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).1
      (c60F41PhysicalFaceBoundaryLoop
        (historicalF42EdgeSelectedFace e side)).1
  suffix := fun _ =>
    c60F109EveryDartToDart
      (c60F41PhysicalFaceBoundaryLoop
        (historicalF42EdgeSelectedFace e side)).1
      (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).2

/-- A REAL OPEN-ENDPOINT original F42 face rewrite on the chosen
edge, derived from original F108's contextual five/six-gon
physical-face generator and genuine F109 Quiver.Path contexts. -/
def historicalF42EdgeActualFaceCell (e : Edge) (side : Bool) :=
  c60F108ContextualFaceCell
    (historicalF42EdgeActualContexts e side) (0 : Fin 1)

/-- This exact old open-endpoint source witness has NONZERO F43
physical-face degree. It is not an original identity 2-cell. -/
theorem historicalF42EdgeActualFace_degree_one
    (e : Edge) (side : Bool) :
    c60F43FaceDegree (historicalF42EdgeActualFaceCell e side) =
      (1 : ZMod 2) :=
  c60F108ContextualFace_degree_one
    (historicalF42EdgeActualContexts e side) (0 : Fin 1)

/-- Give the exact original F108/F109 open-endpoint F42 cell its
P41 Type-valued independent full C60 fan/disk annotation, retaining
both original physical source paths as the dependent type index. -/
def historicalF42EdgeActualAnnotated (e : Edge) (side : Bool) :=
  historicalF42Annotate (historicalF42EdgeActualFaceCell e side)

/-- The actual old edge-contextual face source contains exactly ONE
real physical F42 face primitive. The prior/suffix original paths
have not introduced imaginary additional physical faces. -/
theorem historicalF42EdgeOriginalFaceTrace
    (e : Edge) (side : Bool) :
    historicalF42OriginalFaceTrace
      (historicalF42EdgeActualFaceCell e side) =
        [historicalF42EdgeSelectedFace e side] := rfl

/-- That genuine original open-path 2-cell's P41 witness is the
ACTUAL independent Kuu source of the uniquely selected original
C60 physical polygon, with full sector and disk proof terms. -/
theorem historicalF42EdgeActual_single_source
    (e : Edge) (side : Bool) :
    (historicalF42EdgeActualAnnotated e side).supports =
      [⟨historicalF42EdgeSelectedFace e side,
        historicalF42CanonicalFaceSupport
          (historicalF42EdgeSelectedFace e side)⟩] := rfl

/-- The EXACT historical full five/six-edge boundary word remains
available as the SINGLE original face-source word inside a true
endpoint-to-endpoint original F42 face rewrite. For hexagons this
is the P4-verified REVERSED native cyclic word. -/
theorem historicalF42EdgeActual_original_boundary
    (e : Edge) (side : Bool) :
    (historicalF42EdgeActualAnnotated e side).originalWords =
      [kernelC60FullFaceBoundaryEdges
        (historicalF42EdgeSelectedFace e side)] := by
  simpa only [historicalF42EdgeOriginalFaceTrace,
    List.map_cons, List.map_nil] using
      (historicalF42EdgeActualAnnotated e side).originalWords_exact

/-- The ORIGINAL F42 contextual source has correctly typed old
Quiver.Path boundaries, and preserves equality of their full
historical original F41 Gray 1-transport values. This is the
ACTUAL original source 2-cell theorem, not a chosen numerical
Kuu shadow evaluation. -/
theorem historicalF42EdgeActual_original_transport
    (e : Edge) (side : Bool) :
    c60F41OriginalC60GrayPathFunctor.map
        ((c60F108FacePatchFamily
          (historicalF42EdgeActualContexts e side)).p (0 : Fin 1)) =
      c60F41OriginalC60GrayPathFunctor.map
        ((c60F108FacePatchFamily
          (historicalF42EdgeActualContexts e side)).q (0 : Fin 1)) :=
  (historicalF42EdgeActualFaceCell e side).transport_eq

/-- The ORIGINAL selected face is ACTUALLY incident to the
true C60 edge in the ORIGINAL truncated-icosahedral geometry.
No numerical 90-edge index or invented face is involved. -/
theorem historicalF42EdgeActual_original_incidence
    (e : Edge) (side : Bool) :
    truncatedEdgeOnSeedFace (edgeEquiv e)
      (historicalF42EdgeSelectedFace e side) :=
  c60F48AdjacentRealFace_incident (edgeEquiv e) side

/-- The ORIGINAL edge occurs in the selected ORIGINAL ordered
five/six-edge boundary list: stronger than abstract target grade
equality or only a chosen F55 pair of generators. -/
theorem historicalF42EdgeActual_old_word_contains_edge
    (e : Edge) (side : Bool) :
    edgeEquiv e ∈ kernelC60FullFaceBoundaryEdges
      (historicalF42EdgeSelectedFace e side) :=
  (historicalBoundary_mem_iff_incidence
    (edgeEquiv e) (historicalF42EdgeSelectedFace e side)).2
      (historicalF42EdgeActual_original_incidence e side)

/-- The corresponding INDEPENDENT Kuu C60 physical edge and face
are genuinely incident, by the already proved constructor-wise
original/new edge and polygon equivalences. -/
theorem historicalF42EdgeActual_native_incidence
    (e : Edge) (side : Bool) :
    edgeOnFace e
      (polygonEquiv.symm (historicalF42EdgeSelectedFace e side)) := by
  apply (edgeOnFace_equiv e
    (polygonEquiv.symm (historicalF42EdgeSelectedFace e side))).2
  simpa only [polygonEquiv.apply_symm_apply] using
    historicalF42EdgeActual_original_incidence e side

/-- Every original C60 face generated by an actual physical edge
has an independently Type-valued disk which CLOSES IN F69, not
a mere original F43 integer-degree proxy. -/
theorem historicalF42EdgeActual_native_disk_sound
    (e : Edge) (side : Bool) :
    zigzagKernelQ.map
      (polygonRawLoop
        (polygonEquiv.symm (historicalF42EdgeSelectedFace e side))) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex
          (cyclicBoundaryDart
            (polygonEquiv.symm (historicalF42EdgeSelectedFace e side)) 0))) :=
  (historicalF42CanonicalFaceSupport
    (historicalF42EdgeSelectedFace e side)).disk_sound

/-- The TWO genuine adjacent original physical C60 polygon
generators on the same edge are DISTINCT. Both nevertheless have
full separately typed original contextual F42 and independent
native physical fan/disk source certificates. -/
theorem historicalF42EdgeActual_twoFaces_distinct
    (e : Edge) :
    historicalF42EdgeSelectedFace e false ≠
      historicalF42EdgeSelectedFace e true :=
  c60F48BothRealFaces_distinct (edgeEquiv e)

/-- General form: ANY existing F108 original physical edge/context
family, with its ACTUAL selected original polygon and endpoint-typed
F42 contextual face, admits the P41 Type-valued native source and
whole ORIGINAL boundary word. This covers arbitrary finite stars. -/
theorem historicalF42EveryContext_native_annotation
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    (historicalF42Annotate
        (c60F108ContextualFaceCell C i)).supports =
      [⟨c60F48AdjacentRealFace (C.edge i) (C.side i),
        historicalF42CanonicalFaceSupport
          (c60F48AdjacentRealFace (C.edge i) (C.side i))⟩] := rfl

/-- IN PARTICULAR the already constructed F109 original NINETY
physical-edge path-context atlas is now annotated with real
independent C60 Type-valued face/disk evidence at EVERY member,
with no new path-existence or F51/55 lift hypotheses. -/
theorem historicalF42AllNinety_original_native_sources
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    (historicalF42Annotate
      (c60F108ContextualFaceCell
        c60F109AllNinetyFaceContexts i)).supports =
      [⟨c60F48AdjacentRealFace
          (c60F109AllNinetyFaceContexts.edge i)
          (c60F109AllNinetyFaceContexts.side i),
        historicalF42CanonicalFaceSupport
          (c60F48AdjacentRealFace
            (c60F109AllNinetyFaceContexts.edge i)
            (c60F109AllNinetyFaceContexts.side i))⟩] :=
  historicalF42EveryContext_native_annotation
    c60F109AllNinetyFaceContexts i

#print axioms historicalF42EdgeSelectedFace
#print axioms historicalF42EdgeActualContexts
#print axioms historicalF42EdgeActualFaceCell
#print axioms historicalF42EdgeActualFace_degree_one
#print axioms historicalF42EdgeActualAnnotated
#print axioms historicalF42EdgeOriginalFaceTrace
#print axioms historicalF42EdgeActual_single_source
#print axioms historicalF42EdgeActual_original_boundary
#print axioms historicalF42EdgeActual_original_transport
#print axioms historicalF42EdgeActual_original_incidence
#print axioms historicalF42EdgeActual_old_word_contains_edge
#print axioms historicalF42EdgeActual_native_incidence
#print axioms historicalF42EdgeActual_native_disk_sound
#print axioms historicalF42EdgeActual_twoFaces_distinct
#print axioms historicalF42EveryContext_native_annotation
#print axioms historicalF42AllNinety_original_native_sources

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
