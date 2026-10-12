import KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
import KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
import Mathlib.CategoryTheory.Quotient

namespace KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60WangBiCoherentHigherAtlasV5_171
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F42 / v5.190 — actual proof-relevant ORIGINAL C60 pentagon/hexagon face 2-cells

F59-F41 built the original 60-object / 180-oriented-arrow free C60
Mathlib path CATEGORY and a genuine functor to the original,
independently phase-sensitive F59 Gray target.

This unit attaches ALL 12 ACTUAL five-edge pentagon faces and
ALL 20 ACTUAL six-edge hexagon faces as PROOF-RELEVANT, genuinely
dependently typed source 2-cell GENERATORS from their exact
nonconstant Quiver.Path boundary loops to the identity loop.
The original raw source 1-paths are NOT quotient-identified;
the 2-cell type retains identities, inverses, vertical
composites and genuine left/right 1-path whiskerings.
Horizontal composition is built in BOTH genuine source orders.

Next prove THE STRONGEST SOURCE-COMPATIBLE TARGET STATEMENT:
the original kernel-checked 27-edge Gray-flat repair descends to
the REAL original C60 vertex potential. Using the actual
F59-F19 tree gauge, ALL original oriented 1-path transports are
provably vertex-potential differences, NOT only all 32 faces
as a separate unrelated array. Consequently every true
original face 2-cell is sent to equality of the two
corresponding source 1-path transport images, and this equality
is preserved through ALL original 2-cell constructors
(including contextual whiskerings and horizontal pasting).

Finally construct the genuine Mathlib QUOTIENT CATEGORY of
original C60 paths by exactly the new face-generator
2-dimensional presentation and its categorical closure.
The existing nontrivial original Gray/phase path functor
FACTORS as a real, kernel-checked Mathlib FUNCTOR through
this quotient, still injective on the original sixty
physical objects and retaining all F55 charge/phase data
on native target homs. The separate full proof-relevant
face 2-cell carrier is NEVER replaced by raw equality.

SCOPE: The quotient category is the ONE-TRUNCATION of the
new C60 2-dimensional computad, NOT itself a full Gray
3-category. The actual old F55 PresentedCell syntax is a
separate original typed 3-morphism presentation. Extending
the source computad to a true nondegenerate Gray 3-category
with its horizontal/vertical 2-cell coherence and
interchange plus F55 3-cell transport remains a separate
constructive obligation, rather than an assumed axiom.
-/

/-! ## I. Vertex-gauge transport for every ORIGINAL C60 1-path -/

/-- Original F59-F19 kernel-proved 60-vertex Gray potential.
Its original 59-edge spanning tree comes from the real C60
cellular chain contraction; no new potential is postulated. -/
def c60F42VertexGauge (v : IcosahedralDart) :
    GradedThreeCell 0 0 :=
  c60F19TreeVertexGauge (Finsupp.single v (1 : ℤ))

/-- Every physical original forward C60 edge grade is literally
the old nontrivial native Gray potential at its target MINUS
the potential at its source. The equation retains BOTH integer
charges and the ZMod2 exchange phase. -/
theorem c60F42PhysicalEdgeGrade_eq_vertexDifference
    (edge : TruncatedIcosahedralEdge) :
    c60WangBiHigherAtlasFlatEdgeLabel edge =
      c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints edge).2 -
      c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints edge).1 := by
  have h := c60WangBiRepairedGrade_exact_treeDescent
  rw [c60WangBiRepairedGrade_realizes_cochain] at h
  change c60WangBiHigherAtlasFlatEdgeCochain =
    c60F19TreeVertexGauge.comp c60IntegralBoundaryOne at h
  have he := LinearMap.congr_fun h (Finsupp.single edge (1 : ℤ))
  change c60WangBiHigherAtlasFlatEdgeLabel edge =
    c60F19TreeVertexGauge
      (c60IntegralBoundaryOne (Finsupp.single edge (1 : ℤ))) at he
  rw [c60IntegralBoundaryOne_singleEdge] at he
  simpa [c60IntegralEdgeBoundaryChain, c60F42VertexGauge] using he

/-- Reverse-original-edge Gray transport is the opposite
vertex difference, with genuine inverse on the old
native 3-cell rather than a phase-forgetting operation. -/
theorem c60F42ReverseEdgeGrade_eq_vertexDifference
    (edge : TruncatedIcosahedralEdge) :
    (c60WangBiHigherAtlasFlatEdgeLabel edge).inv =
      c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints edge).1 -
      c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints edge).2 := by
  have hneg :
      (c60WangBiHigherAtlasFlatEdgeLabel edge).inv =
        -(c60WangBiHigherAtlasFlatEdgeLabel edge) := by
    apply GradedThreeCell.ext <;> rfl
  rw [hneg, c60F42PhysicalEdgeGrade_eq_vertexDifference]
  abel

/-- The genuine old C60 quiver prefunctor transports EVERY actual
typed oriented physical edge by its true source/target difference;
this is not a groupoid quotient of the original source 1-paths. -/
theorem c60F42OriginalQuiverArrow_eq_vertexDifference
    {a b : IcosahedralDart} (arrow : a ⟶ b) :
    (c60F41OriginalEdgePrefunctor.map arrow :
      c60F41TargetVertex a ⟶ c60F41TargetVertex b) =
        c60F42VertexGauge b - c60F42VertexGauge a := by
  rcases arrow with ⟨directed, ⟨hsource, htarget⟩⟩
  cases directed with
  | forward e =>
      change (truncatedIcosahedralEdgeEndpoints e).1 = a at hsource
      change (truncatedIcosahedralEdgeEndpoints e).2 = b at htarget
      subst a
      subst b
      change c60WangBiHigherAtlasFlatEdgeLabel e =
        c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints e).2 -
          c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints e).1
      exact c60F42PhysicalEdgeGrade_eq_vertexDifference e
  | reverse e =>
      change (truncatedIcosahedralEdgeEndpoints e).2 = a at hsource
      change (truncatedIcosahedralEdgeEndpoints e).1 = b at htarget
      subst a
      subst b
      change (c60WangBiHigherAtlasFlatEdgeLabel e).inv =
        c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints e).1 -
          c60F42VertexGauge (truncatedIcosahedralEdgeEndpoints e).2
      exact c60F42ReverseEdgeGrade_eq_vertexDifference e

/-- FULL Mathlib source PATH induction on arbitrary-length,
genuinely typed ORIGINAL C60 1-morphisms: no matter how many
physical original C60 directed edges compose, their complete
Gray image depends precisely on the ORIGINAL source/target
dart gauge values, including independent exchange phase.
This is stronger than separately checking 32 face labels. -/
theorem c60F42EveryOriginalPath_transport_eq_vertexDifference
    {a b : IcosahedralDart} (p : Quiver.Path a b) :
    c60F41OriginalC60GrayPathFunctor.map p =
      c60F42VertexGauge b - c60F42VertexGauge a := by
  induction p with
  | nil =>
      change (0 : GradedThreeCell 0 0) =
        c60F42VertexGauge a - c60F42VertexGauge a
      rw [sub_self]
  | cons p edge ih =>
      change (Paths.lift c60F41OriginalEdgePrefunctor).map
        (p.cons edge) = _
      change (Paths.lift c60F41OriginalEdgePrefunctor).map p =
        c60F42VertexGauge _ - c60F42VertexGauge a at ih
      rw [Paths.lift_cons, ih,
        c60F42OriginalQuiverArrow_eq_vertexDifference edge]
      change (c60F42VertexGauge _ - c60F42VertexGauge a) +
        (c60F42VertexGauge _ - c60F42VertexGauge _) =
          c60F42VertexGauge _ - c60F42VertexGauge a
      abel

/-- THE ACTUAL C60 pentagonal and hexagonal face closed paths
are sent to genuine identity native Gray 3-cell arrows by
the original nonconstant 60-vertex path functor.
This is source-path based coherence, not merely an oriented
integer cochain whose untyped total vanishes. -/
theorem c60F42All32ActualFaceBoundary_transport_identity
    (face : TruncatedIcosahedralSeedFace) :
    c60F41OriginalC60GrayPathFunctor.map
        (c60F41PhysicalFaceBoundaryLoop face).2 =
      (𝟙 (c60F41OriginalC60GrayPathFunctor.obj
        ((c60F41PhysicalFaceBoundaryLoop face).1 :
          C60F41OriginalPathCategory))) := by
  rw [c60F42EveryOriginalPath_transport_eq_vertexDifference]
  change c60F42VertexGauge (c60F41PhysicalFaceBoundaryLoop face).1 -
      c60F42VertexGauge (c60F41PhysicalFaceBoundaryLoop face).1 =
        (0 : GradedThreeCell 0 0)
  exact sub_self _

/-! ## II. Real proof-relevant source face 2-cell presentation -/

/-- A genuinely TYPE-VALUED 2-dimensional source presentation,
indexed by parallel actual ORIGINAL C60 free paths. Every
physical generator has the EXACT old 5- or 6-edge source
boundary, and all contextual constructors are genuinely
DEPENDENT on the endpoints of the 1-paths. There is no
Prop-level proof erasure of original C60 face witnesses. -/
inductive C60F42PresentedFaceCell :
    {a b : IcosahedralDart} →
      Quiver.Path a b → Quiver.Path a b → Type where
  | ident {a b : IcosahedralDart}
      (p : Quiver.Path a b) :
      C60F42PresentedFaceCell p p
  | physicalFace (face : TruncatedIcosahedralSeedFace) :
      C60F42PresentedFaceCell
        (c60F41PhysicalFaceBoundaryLoop face).2
        Quiver.Path.nil
  | symm {a b : IcosahedralDart} {p q : Quiver.Path a b}
      (cell : C60F42PresentedFaceCell p q) :
      C60F42PresentedFaceCell q p
  | trans {a b : IcosahedralDart}
      {p q r : Quiver.Path a b}
      (left : C60F42PresentedFaceCell p q)
      (right : C60F42PresentedFaceCell q r) :
      C60F42PresentedFaceCell p r
  | whiskerLeft {a b c : IcosahedralDart}
      (prior : Quiver.Path a b)
      {p q : Quiver.Path b c}
      (cell : C60F42PresentedFaceCell p q) :
      C60F42PresentedFaceCell (prior.comp p) (prior.comp q)
  | whiskerRight {a b c : IcosahedralDart}
      {p q : Quiver.Path a b}
      (cell : C60F42PresentedFaceCell p q)
      (suffix : Quiver.Path b c) :
      C60F42PresentedFaceCell (p.comp suffix) (q.comp suffix)

/-- An honest HORIZONTAL source 2-cell composite in the
left-first order: first rewrite the LEFT path in a true
right context, then rewrite the RIGHT path in a true
left context. Endpoints are the original C60 vertices. -/
def C60F42PresentedFaceCell.horizontalLeftFirst
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F42PresentedFaceCell (p.comp r) (q.comp s) :=
  .trans (.whiskerRight α r) (.whiskerLeft q β)

/-- The other genuine source horizontal pasting order.
No equality of these DIFFERENT raw 2-cell terms is
assumed; coherence of their Gray transport images
is proved separately below. -/
def C60F42PresentedFaceCell.horizontalRightFirst
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F42PresentedFaceCell (p.comp r) (q.comp s) :=
  .trans (.whiskerLeft p β) (.whiskerRight α s)

/-- Every generated ORIGINAL 2-cell witnesses a literal equality
of the independent charge/phase-preserving Gray 1-TRANSPORT.
This covers all SIX source constructors by induction, including
real 32-face relations, inverse, vertical paste and BOTH
contextual whiskerings. Source evidence remains Type-valued. -/
theorem C60F42PresentedFaceCell.transport_eq
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (cell : C60F42PresentedFaceCell p q) :
    c60F41OriginalC60GrayPathFunctor.map p =
      c60F41OriginalC60GrayPathFunctor.map q := by
  induction cell with
  | ident _ => rfl
  | physicalFace f =>
      have h := c60F42All32ActualFaceBoundary_transport_identity f
      have hid :
          c60F41OriginalC60GrayPathFunctor.map
            (Quiver.Path.nil :
              Quiver.Path (c60F41PhysicalFaceBoundaryLoop f).1
                (c60F41PhysicalFaceBoundaryLoop f).1) =
            (𝟙 (c60F41OriginalC60GrayPathFunctor.obj
              ((c60F41PhysicalFaceBoundaryLoop f).1 :
                C60F41OriginalPathCategory))) :=
        c60F41OriginalC60GrayPathFunctor.map_id _
      exact h.trans hid.symm
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight =>
      exact ihLeft.trans ihRight
  | whiskerLeft prior cell ih =>
      simp only [c60F41PathFunctor_comp]
      rw [ih]
  | whiskerRight cell suffix ih =>
      simp only [c60F41PathFunctor_comp]
      rw [ih]

/-- All genuinely TYPE-CORRECT original horizontal source
2-cell pasting orders are compatible with the very SAME
native Gray transport, WITHOUT equating different raw
source proof-relevant 2-cells. -/
theorem C60F42PresentedFaceCell.horizontal_both_transport
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F41OriginalC60GrayPathFunctor.map (p.comp r) =
      c60F41OriginalC60GrayPathFunctor.map (q.comp s) :=
  (α.horizontalLeftFirst β).transport_eq

/-- TRUE original five-step C60 pentagon source 1-PATH is
NOT the zero-step source identity, even though there is
now an actual original TYPE-VALUED physicalFace 2-cell
from one to the other and their Gray images agree.
No false equality of original paths is manufactured. -/
theorem c60F42OriginalPentagonBoundary_not_identityPath
    (v : IcosahedralVertex) :
    c60F41PentagonBoundaryLoop v ≠
      (Quiver.Path.nil :
        Quiver.Path (icosahedralIncidentDartAt v .s0)
          (icosahedralIncidentDartAt v .s0)) := by
  intro h
  have hl := congrArg Quiver.Path.length h
  rw [c60F41PentagonBoundaryLoop_length, Quiver.Path.length_nil] at hl
  exact (by decide : (5 : ℕ) ≠ 0) hl

/-! ## III. Native face-presentation HOMOTOPY QUOTIENT and DESCENT -/

/-- The exact original SOURCE face 2-cell presentation as
a relation on the original C60 free PATHS 1-category.
Membership requires a real proof-relevant face witness,
never merely equality of F59 integer/phase values. -/
def c60F42OriginalFaceHomRel :
    HomRel C60F41OriginalPathCategory :=
  fun _ _ p q => Nonempty (C60F42PresentedFaceCell p q)

/-- Its genuine Mathlib QUOTIENT CATEGORY, the honest
**one-truncation** of the original 32-face 2-dimensional
computad, with categorical equivalence/congruence closure.
The ORIGINAL typed 2-cells remain available above. -/
abbrev C60F42FaceRelationPathCategory :=
  CategoryTheory.Quotient c60F42OriginalFaceHomRel

/-- EXACT Mathlib FUNCTOR descending the existing nonconstant
60-vertex/90-edge original Gray/phase 1-path transport
through the source's ACTUAL 32 C60 face 2-cell relations.
All categorical mapId/mapComp fields are kernel-checked by
Mathlib's quotient lifting theorem, not added axioms. -/
def c60F42QuotientFaceGrayFunctor :
    C60F42FaceRelationPathCategory ⥤ C60F41GrayTransportObject :=
  CategoryTheory.Quotient.lift c60F42OriginalFaceHomRel
    c60F41OriginalC60GrayPathFunctor
    (by
      intro a b p q h
      exact Nonempty.elim h
        (fun cell => C60F42PresentedFaceCell.transport_eq cell))

/-- The constructed quotient functor RETAINS the full existing
original free path Gray transport ON THE NOSE under original
C60 quotient mapping, not merely an informal equivalence. -/
theorem c60F42OriginalGrayTransport_factorsThroughFaces :
    CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙
      c60F42QuotientFaceGrayFunctor =
        c60F41OriginalC60GrayPathFunctor := by
  exact CategoryTheory.Quotient.lift_spec _ _ _

/-- Every ORIGINAL 32-face source presented 2-cell is honored
by the new quotient category as equality of 1-arrow classes.
The strong proof-relevant original face witness is the input,
NOT a fabricated equality of raw source C60 paths. -/
theorem c60F42EveryPhysicalFace_relation_sounds
    (face : TruncatedIcosahedralSeedFace) :
    (CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel).map
      (c60F41PhysicalFaceBoundaryLoop face).2 =
    (CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel).map
      (Quiver.Path.nil :
        Quiver.Path (c60F41PhysicalFaceBoundaryLoop face).1
          (c60F41PhysicalFaceBoundaryLoop face).1) :=
  CategoryTheory.Quotient.sound c60F42OriginalFaceHomRel
    ⟨C60F42PresentedFaceCell.physicalFace face⟩

/-- The nontrivial original physical NORTH-SPOKE edge remains
a genuine unit-square-charge, odd Gray-phase morphism even
after the C60 32-face quotient. No source geometric vertex
or F55 charge is collapsed by the target 1-functor. -/
theorem c60F42NorthCrossQuotientTransport_charge_one :
    ((c60F42QuotientFaceGrayFunctor.map
      ((CategoryTheory.Quotient.functor
        c60F42OriginalFaceHomRel).map
          (c60F41ForwardArrow (.cross (.northSpoke 0))).toPath)).charge.2) =
        (1 : ℤ) := by
  change (c60F41OriginalC60GrayPathFunctor.map
    (c60F41ForwardArrow (.cross (.northSpoke 0))).toPath).charge.2 =
      (1 : ℤ)
  exact c60F41NorthCrossPathTransport_squareCharge_one

/-- Full original C60 vertex distinctions are STILL retained by
the original Gray transport after 32 face gluing. The quotient
source has genuine 60 different original 0-objects, not one
artificial doubly-degenerate source 0-object. -/
theorem c60F42QuotientGrayFunctor_injective_originalVertices
    {u v : IcosahedralDart}
    (h : c60F42QuotientFaceGrayFunctor.obj
        ((CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel).obj
          (u : C60F41OriginalPathCategory)) =
      c60F42QuotientFaceGrayFunctor.obj
        ((CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel).obj
          (v : C60F41OriginalPathCategory))) :
    u = v := by
  exact congrArg C60F41GrayTransportObject.vertex h

#print axioms c60F42VertexGauge
#print axioms c60F42PhysicalEdgeGrade_eq_vertexDifference
#print axioms c60F42ReverseEdgeGrade_eq_vertexDifference
#print axioms c60F42OriginalQuiverArrow_eq_vertexDifference
#print axioms c60F42EveryOriginalPath_transport_eq_vertexDifference
#print axioms c60F42All32ActualFaceBoundary_transport_identity
#print axioms C60F42PresentedFaceCell
#print axioms C60F42PresentedFaceCell.transport_eq
#print axioms C60F42PresentedFaceCell.horizontal_both_transport
#print axioms c60F42OriginalPentagonBoundary_not_identityPath
#print axioms c60F42OriginalFaceHomRel
#print axioms c60F42QuotientFaceGrayFunctor
#print axioms c60F42OriginalGrayTransport_factorsThroughFaces
#print axioms c60F42EveryPhysicalFace_relation_sounds
#print axioms c60F42NorthCrossQuotientTransport_charge_one
#print axioms c60F42QuotientGrayFunctor_injective_originalVertices

end
end KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
