import KUOS.DependentOriginationGrayC60BraidedThreeSectorV5_188
import KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
import Mathlib.CategoryTheory.PathCategory.Basic

namespace KUOS.DependentOriginationGrayC60NativePathFunctorV5_189

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60WangBiCoherentHigherAtlasV5_171
open KUOS.DependentOriginationGrayC60BraidedThreeSectorV5_188

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F41 / v5.189 — ORIGINAL C60 0/1-category, real 32 face loops and Gray transport

F59-F40 constructed the complete 182-site braided monoidal 2/3
cell sector with full phase and integer charges, and proved all
twelve pentagon and twenty hexagon physical faces flat after
the original 27-edge C60 repair.

This theorem unit builds a NONDISCRETE NATIVE 0/1-CATEGORY
rather than silently interpreting a C60 vertex/edge as a
higher Gray 3-cell:
- the objects are ALL 60 actual original truncated darts;
- every one of the 90 original unoriented physical C60 edges
  gives precisely TWO *independently typed* oriented quiver
  arrows, with original source and target;
- the resulting genuine Mathlib Paths free CATEGORY has honest
  path identity, composition and length. The original source
  vertices are NOT collapsed by the category construction;
- ALL 12 pentagon faces and ALL 20 genuine oriented hexagon
  faces are given actual Type-valued CLOSED QUIVER PATHS;
  the preexisting 32 face labels are not invented new edges.

We then build a Mathlib 60-object transport category retaining
the ORIGINAL source dart as an object coordinate and the actual
F59 native GradedThreeCell as its arrow. The unique lifted
path-category FUNCTOR sends every real original oriented edge to
the already theorem-checked nontrivial 27-edge repaired Gray
field, with reverse edges sent to the true inverse. It preserves
identity and arbitrary path composition by the Mathlib free
path-category universal property; the ORIGINAL north-spoke
edge still has nonzero integer square charge and independent
exchange phase. Forward/reverse backtracking evaluates to
the actual native identity, not by quotienting raw paths.

IMPORTANT SCOPE: the resulting functor is a genuine ORIGINAL
C60 0/1-PATH TRANSPORT functor INTO A CATEGORY WHOSE HOMs ARE
native Gray 3-cell values; it is NOT BY ITSELF a dimension-
preserving nondegenerate Gray 3-functor. Completing that requires
a SOURCE bicategory/Gray 3-category whose original 32 signed
face-relators are native 2-cells and whose ORIGINAL F55
PresentedCell typed relations are attached as 3-cells, then
proving the full Gray interchanger and all globular laws.
We explicitly keep this next genuine source-lifting obligation
instead of adding unproved coherence axioms, quotienting F55
sources, or identifying the historic Stage-II obstruction ω.
-/

/-- A true one-to-one CODE for the two original orientations of
each physical C60 edge. No extra physical edge is introduced. -/
def c60F41OrientedEdgeCode :
    OrientedTruncatedIcosahedralEdge ≃
      Bool × TruncatedIcosahedralEdge where
  toFun
    | .forward e => (true, e)
    | .reverse e => (false, e)
  invFun
    | (true, e) => .forward e
    | (false, e) => .reverse e
  left_inv := by
    intro e
    cases e <;> rfl
  right_inv := by
    rintro ⟨b, e⟩
    cases b <;> rfl

/-- Finiteness is transported from the REAL 90 original edges,
not from a separately enumerated abstract graph. -/
noncomputable instance : Fintype OrientedTruncatedIcosahedralEdge :=
  Fintype.ofEquiv (Bool × TruncatedIcosahedralEdge)
    c60F41OrientedEdgeCode.symm

theorem c60F41OriginalDirectedArrowCount :
    Fintype.card OrientedTruncatedIcosahedralEdge = 180 := by
  have h90 : Fintype.card TruncatedIcosahedralEdge = 90 := by decide
  have h := Fintype.card_congr c60F41OrientedEdgeCode
  simpa [Fintype.card_prod, h90] using h

/-- Genuine Mathlib QUIVER on the ORIGINAL sixty truncated darts.
An arrow X→Y is precisely one of the original oriented C60
physical edges WITH proofs of its true physical endpoints. -/
instance : Quiver IcosahedralDart where
  Hom X Y := {edge : OrientedTruncatedIcosahedralEdge //
    edge.source = X ∧ edge.target = Y}

/-- The original physical edge with its OWN original orientation.
No synthetic new geometric edge or quotient is introduced. -/
def c60F41ForwardArrow (e : TruncatedIcosahedralEdge) :
    (truncatedIcosahedralEdgeEndpoints e).1 ⟶
      (truncatedIcosahedralEdgeEndpoints e).2 :=
  ⟨.forward e, ⟨rfl, rfl⟩⟩

/-- Reverse the original physical edge, retaining its EXACT
real dart endpoints. Reverse is a quiver arrow, not an
unproved equality of distinct original F54 rotation routes. -/
def c60F41ReverseArrow (e : TruncatedIcosahedralEdge) :
    (truncatedIcosahedralEdgeEndpoints e).2 ⟶
      (truncatedIcosahedralEdgeEndpoints e).1 :=
  ⟨.reverse e, ⟨rfl, rfl⟩⟩

/-- Every actual oriented C60 physical edge becomes a 1-step
path with its exact original source and target. -/
def c60F41OrientedPath
    (e : OrientedTruncatedIcosahedralEdge) :
    Quiver.Path e.source e.target :=
  match e with
  | .forward edge => (c60F41ForwardArrow edge).toPath
  | .reverse edge => (c60F41ReverseArrow edge).toPath

theorem c60F41OrientedPath_length
    (e : OrientedTruncatedIcosahedralEdge) :
    (c60F41OrientedPath e).length = 1 := by
  cases e <;> simp [c60F41OrientedPath]

/-- Original C60 sixty-object native free Mathlib CATEGORY:
arrows are composable original edge paths, not unrelated
codiscrete chart changes or proof-erased relation certificates. -/
abbrev C60F41OriginalPathCategory := Paths IcosahedralDart

theorem c60F41OriginalObjectCount :
    Fintype.card IcosahedralDart = 60 := by
  decide

theorem c60F41OriginalEdgeCount :
    Fintype.card TruncatedIcosahedralEdge = 90 := by
  decide

theorem c60F41OriginalFaceCount :
    Fintype.card TruncatedIcosahedralSeedFace = 32 := by
  decide

/-- An original 12-fold C60 pentagonal face now has an ACTUAL
Type-valued 5-step 1-morphism from its first original dart to
ITSELF; all arrows are the TRUE original around-vertex edges. -/
def c60F41PentagonBoundaryLoop (v : IcosahedralVertex) :
    Quiver.Path (icosahedralIncidentDartAt v .s0)
      (icosahedralIncidentDartAt v .s0) := by
  let p0 : Quiver.Path (icosahedralIncidentDartAt v .s0)
      (icosahedralIncidentDartAt v .s1) :=
    (c60F41ForwardArrow (.around ⟨v, .s0⟩)).toPath
  let p1 : Quiver.Path (icosahedralIncidentDartAt v .s0)
      (icosahedralIncidentDartAt v .s2) :=
    p0.cons (c60F41ForwardArrow (.around ⟨v, .s1⟩))
  let p2 : Quiver.Path (icosahedralIncidentDartAt v .s0)
      (icosahedralIncidentDartAt v .s3) :=
    p1.cons (c60F41ForwardArrow (.around ⟨v, .s2⟩))
  let p3 : Quiver.Path (icosahedralIncidentDartAt v .s0)
      (icosahedralIncidentDartAt v .s4) :=
    p2.cons (c60F41ForwardArrow (.around ⟨v, .s3⟩))
  exact p3.cons (c60F41ForwardArrow (.around ⟨v, .s4⟩))

theorem c60F41PentagonBoundaryLoop_length
    (v : IcosahedralVertex) :
    (c60F41PentagonBoundaryLoop v).length = 5 := by
  rfl

/-- An ORIGINAL oriented C60 hexagon supplies SIX genuine
composable quiver 1-arrows with the SAME original endpoint
proofs as the preexisting F59-C60 incidence construction.
No new edges, fake quadrilateral surface face or quotient. -/
def c60F41HexagonBoundaryLoop (f : IcosahedralFace) :
    Quiver.Path (truncatedIcosahedralHexagonCycle f).e0.source
      (truncatedIcosahedralHexagonCycle f).e0.source := by
  let C := truncatedIcosahedralHexagonCycle f
  let p0 : Quiver.Path C.e0.source C.e0.target :=
    c60F41OrientedPath C.e0
  let p1 : Quiver.Path C.e0.target C.e1.target := by
    rw [C.h01]
    exact c60F41OrientedPath C.e1
  let p2 : Quiver.Path C.e1.target C.e2.target := by
    rw [C.h12]
    exact c60F41OrientedPath C.e2
  let p3 : Quiver.Path C.e2.target C.e3.target := by
    rw [C.h23]
    exact c60F41OrientedPath C.e3
  let p4 : Quiver.Path C.e3.target C.e4.target := by
    rw [C.h34]
    exact c60F41OrientedPath C.e4
  let p5 : Quiver.Path C.e4.target C.e5.target := by
    rw [C.h45]
    exact c60F41OrientedPath C.e5
  let q : Quiver.Path C.e0.source C.e5.target :=
    (((((p0.comp p1).comp p2).comp p3).comp p4).comp p5)
  exact C.h50 ▸ q

/-- Every one of the ORIGINAL 12 pentagons and 20 hexagons
is an ACTUAL BASED CLOSED PATH in the real 60-object C60 free
category. THIS is the genuine nondegenerate 0/1-source
boundary that the next native 2-cell presentation must attach. -/
def c60F41PhysicalFaceBoundaryLoop :
    (f : TruncatedIcosahedralSeedFace) →
      Σ base : IcosahedralDart, Quiver.Path base base
  | .aroundVertex v =>
      ⟨icosahedralIncidentDartAt v .s0, c60F41PentagonBoundaryLoop v⟩
  | .fromTriangle f =>
      ⟨(truncatedIcosahedralHexagonCycle f).e0.source,
        c60F41HexagonBoundaryLoop f⟩

/-- Two strictly genuine C60 polygonal cases, with no
fabrication of a 4-edged face or collapse of face orientation. -/
theorem c60F41PhysicalFaceBoundaryLoop_pentagon_base
    (v : IcosahedralVertex) :
    (c60F41PhysicalFaceBoundaryLoop (.aroundVertex v)).1 =
      icosahedralIncidentDartAt v .s0 := rfl

theorem c60F41PhysicalFaceBoundaryLoop_hexagon_base
    (f : IcosahedralFace) :
    (c60F41PhysicalFaceBoundaryLoop (.fromTriangle f)).1 =
      (truncatedIcosahedralHexagonCycle f).e0.source := rfl

/-! ## A genuine noncollapsed 60-vertex target category carrying
the complete original neutral Gray 3-cell charge and phase. -/

/-- Target 0/1 transport objects retain the ACTUAL original
physical C60 vertex and an independent genuine Gray 2-cell
grade. In particular, the 60 physical vertices are not
identified with a single terminal object. -/
structure C60F41GrayTransportObject where
  vertex : IcosahedralDart
  grade : GrayGrade

/-- An ACTUAL Mathlib category whose homs are the EXISTING
precisely graded, nontrivial F59 3-cell morphisms; source
and target vertex data remain different objects. -/
instance : Category C60F41GrayTransportObject where
  Hom X Y := GradedThreeCell X.grade.degree Y.grade.degree
  id X := GradedThreeCell.ident X.grade.degree
  comp f g := f.comp g
  id_comp := by
    intro X Y f
    exact GradedThreeCell.ident_comp f
  comp_id := by
    intro X Y f
    exact GradedThreeCell.comp_ident f
  assoc := by
    intro W X Y Z f g h
    exact GradedThreeCell.comp_assoc f g h

/-- Physical C60 0-objects are faithfully embedded in the
target object carrier without making any two darts equal. -/
def c60F41TargetVertex (v : IcosahedralDart) :
    C60F41GrayTransportObject :=
  ⟨v, GrayGrade.unit⟩

/-- Signed edge 3-cell values use the ORIGINAL C60 90-edge
27-repaired F55 target, with reversal as ACTUAL F59 native
3-cell inversion. No parity or charge coordinate is erased. -/
def c60F41OrientedGrayValue
    (e : OrientedTruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  match e with
  | .forward edge => c60WangBiHigherAtlasFlatEdgeLabel edge
  | .reverse edge => (c60WangBiHigherAtlasFlatEdgeLabel edge).inv

/-- One actual graph PREFUNCTOR on the original C60 quiver.
The universal path-category lifting will provide all identity/
composition laws, not assume them for arbitrary formal words. -/
def c60F41OriginalEdgePrefunctor :
    IcosahedralDart ⥤q C60F41GrayTransportObject where
  obj := c60F41TargetVertex
  map := fun {_ _} e => c60F41OrientedGrayValue e.1

/-- The TRUE original 60-object/180-oriented-edge path FUNCTOR,
automatically functorial for all finite ORIGINAL physical paths.
The 27-edge repair is employed as genuine nontrivial
integer/phase transport, not as hypothetical image data. -/
def c60F41OriginalC60GrayPathFunctor :
    C60F41OriginalPathCategory ⥤ C60F41GrayTransportObject :=
  Paths.lift c60F41OriginalEdgePrefunctor

/-- Every REAL source dart remains literally itself in the
target's physical-vertex component. -/
theorem c60F41PathFunctor_vertex
    (v : IcosahedralDart) :
    (c60F41OriginalC60GrayPathFunctor.obj
      (v : C60F41OriginalPathCategory)).vertex = v := rfl

/-- The action on original 0-objects is INJECTIVE; no collapse of
the C60 physical sixty-vertex geometry is permitted. -/
theorem c60F41PathFunctor_injective_vertices
    {u v : IcosahedralDart}
    (h : c60F41OriginalC60GrayPathFunctor.obj
        (u : C60F41OriginalPathCategory) =
      c60F41OriginalC60GrayPathFunctor.obj
        (v : C60F41OriginalPathCategory)) : u = v := by
  exact congrArg C60F41GrayTransportObject.vertex h

/-- Exact map of EACH genuine forward oriented physical edge. -/
theorem c60F41PathFunctor_forward_edge
    (edge : TruncatedIcosahedralEdge) :
    c60F41OriginalC60GrayPathFunctor.map
      (c60F41ForwardArrow edge).toPath =
        c60WangBiHigherAtlasFlatEdgeLabel edge := by
  change (Paths.lift c60F41OriginalEdgePrefunctor).map
    (c60F41ForwardArrow edge).toPath = _
  rw [Paths.lift_toPath]
  rfl

/-- Exact map of EACH reverse original C60 edge: actual native
F59 3-cell inverse, not an informal negative edge arrow. -/
theorem c60F41PathFunctor_reverse_edge
    (edge : TruncatedIcosahedralEdge) :
    c60F41OriginalC60GrayPathFunctor.map
      (c60F41ReverseArrow edge).toPath =
        (c60WangBiHigherAtlasFlatEdgeLabel edge).inv := by
  change (Paths.lift c60F41OriginalEdgePrefunctor).map
    (c60F41ReverseArrow edge).toPath = _
  rw [Paths.lift_toPath]
  rfl

/-- The functor preserves actual ORIGINAL C60 path concatenation
of arbitrary lengths by the FULL Mathlib Category API. -/
theorem c60F41PathFunctor_comp
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    c60F41OriginalC60GrayPathFunctor.map (p.comp q) =
      c60F41OriginalC60GrayPathFunctor.map p ≫
        c60F41OriginalC60GrayPathFunctor.map q :=
  c60F41OriginalC60GrayPathFunctor.map_comp p q

/-- A genuine oriented C60 forward edge followed by its exact
physical reverse maps to native Gray identity. The SOURCE free
quiver path is NOT identified with the source identity path. -/
theorem c60F41PathFunctor_backtracking_nativeIdentity
    (edge : TruncatedIcosahedralEdge) :
    c60F41OriginalC60GrayPathFunctor.map
      ((c60F41ForwardArrow edge).toPath.comp
        (c60F41ReverseArrow edge).toPath) =
      (𝟙 (c60F41OriginalC60GrayPathFunctor.obj
        ((truncatedIcosahedralEdgeEndpoints edge).1 :
          C60F41OriginalPathCategory))) := by
  rw [c60F41PathFunctor_comp,
    c60F41PathFunctor_forward_edge,
    c60F41PathFunctor_reverse_edge]
  exact GradedThreeCell.comp_inv _

/-- Nontrivial physical 1-transport: the ORIGINAL north spoke
still carries an authentic F55 square generator with second
INTEGER charge one, so the path functor is not the constant
identity-on-homs functor. -/
theorem c60F41NorthCrossPathTransport_squareCharge_one :
    (c60F41OriginalC60GrayPathFunctor.map
      (c60F41ForwardArrow (.cross (.northSpoke 0))).toPath).charge.2 =
        (1 : ℤ) := by
  rw [c60F41PathFunctor_forward_edge,
    c60WangBiHigherAtlas_preserves_primal_tree _ (by decide)]
  rfl

/-- Native Gray target phase is preserved on the same ORIGINAL
north-spoke physical edge, independently of integer charge. -/
theorem c60F41NorthCrossPathTransport_phase_one :
    (c60F41OriginalC60GrayPathFunctor.map
      (c60F41ForwardArrow (.cross (.northSpoke 0))).toPath).phase =
        (1 : ZMod 2) := by
  rw [c60F41PathFunctor_forward_edge,
    c60WangBiHigherAtlas_preserves_primal_tree _ (by decide)]
  rfl

/-- ORIGINAL nontrivial 2-edge backtracking path is
NOT the 0-edge identity path in the TRUE free C60 path category,
although its fully phase-sensitive native Gray image is identity.
No unproved source quotient or path equality is introduced. -/
theorem c60F41NorthCrossBacktrackingPath_not_sourceIdentity :
    (c60F41ForwardArrow (.cross (.northSpoke 0))).toPath.comp
        (c60F41ReverseArrow (.cross (.northSpoke 0))).toPath ≠
      (Quiver.Path.nil :
        Quiver.Path (.first (.northSpoke 0) : IcosahedralDart)
          (.first (.northSpoke 0) : IcosahedralDart)) := by
  intro h
  have hc := congrArg Quiver.Path.length h
  simp [Quiver.Path.length_comp] at hc

/-! The original 12 pentagon and 20 hexagon *closed 1-paths*
now constitute correct typed candidate 2-cell boundaries.
A genuine source 2-cell presentation and nondegenerate Gray
3-functor extension are next; we do not manufacture their laws. -/

#print axioms c60F41OrientedEdgeCode
#print axioms c60F41OriginalDirectedArrowCount
#print axioms c60F41ForwardArrow
#print axioms c60F41ReverseArrow
#print axioms c60F41OrientedPath_length
#print axioms c60F41OriginalObjectCount
#print axioms c60F41OriginalEdgeCount
#print axioms c60F41OriginalFaceCount
#print axioms c60F41PentagonBoundaryLoop_length
#print axioms c60F41HexagonBoundaryLoop
#print axioms c60F41PhysicalFaceBoundaryLoop
#print axioms c60F41OriginalC60GrayPathFunctor
#print axioms c60F41PathFunctor_injective_vertices
#print axioms c60F41PathFunctor_forward_edge
#print axioms c60F41PathFunctor_reverse_edge
#print axioms c60F41PathFunctor_comp
#print axioms c60F41PathFunctor_backtracking_nativeIdentity
#print axioms c60F41NorthCrossPathTransport_squareCharge_one
#print axioms c60F41NorthCrossPathTransport_phase_one

end
end KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
