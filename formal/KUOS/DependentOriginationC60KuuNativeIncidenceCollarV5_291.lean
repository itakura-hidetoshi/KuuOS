import KUOS.DependentOriginationC60KuuCurvedIncidenceSourceDescentCriterionV5_290
import KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226

namespace KUOS.DependentOriginationC60KuuNativeIncidenceCollarV5_291

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60PhysicalEdgeGrothendieckV5_224
open KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
open KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226
open KUOS.DependentOriginationC60KuuCurvedIncidenceSourceDescentCriterionV5_290
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.291 / F112 part 19 — the actual 60/90/32 native Gray collar is a functor

F72 already constructed the REAL native Gray vertex-to-source-edge,
original F47 source-edge-to-Gray-face, and direct vertex-to-face
FUNCTORS, and proved the honest two-step triangle relation.

We assemble precisely these previously VERIFIED functors over all of
the ORIGINAL F69 incidence arrows, not a localized witnessed-path base.
The resulting genuine Cat-valued diagram has:
* 60 NONEMPTY native GrayGrade vertex fibres;
* all 90 ACTUAL original four-tagged F42/F54/F55 mixed F47 edge fibres,
  exactly as prescribed by F70/F71, with NO replacement of edge syntax;
* 32 nontrivial FULL NATIVE GrayGrade face fibres, retaining BOTH
  integer charges and independent ZMod2 phase, not F77 shadows;
* natural, strictly coherent maps on ALL 360 physical flag triangles.

This CONSTRUCTS an inhabitant of the WEAK/1-CATEGORICAL F71 Cat-valued
incidence-extension interface and thereby the F124 corrected cochain
interface. It does NOT construct a faithful original F42/F54/F55 raw
three-stack: F72 proves that every GrayGrade vertex -> F47 edge
functor is nonfaithful, and the polygon face fibre is GrayGrade,
NOT a raw F42 face source category. Original F55 Delta nine-generator
nonlift, F77 phase obstruction and F68 original north charge -5 persist.
The nonzero repaired cochain is separate from this strict functor.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalPhysicalIncidenceCollar
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- All sites are ORIGINAL physical C60 sites. The vertex/face
categories are the actually constructed nontrivial native GrayGrade,
not fictitious raw original F42 or F55 source fibres. -/
def c60F125NativeIncidenceFibre
    (sigma : C60F67Atlas) : C60F69PhysicalCellSite → Cat
  | .vertex _ => Cat.of GrayGrade
  | .edge edge => (c60F70PhysicalEdgeF47Diagram
      t₁ t₂ left right sigma).obj
        (⟨edge⟩ : C60F70PhysicalEdgeBase)
  | .face _ => Cat.of GrayGrade

/-- The OLD F69 partial order has exactly these possible
arrows. The edge-to-edge case transports along the equality
forced by the ORIGINAL physical incidence relation. -/
def c60F125NativeIncidenceMap
    (sigma : C60F67Atlas)
    {X Y : C60F69PhysicalCellSite} (h : X ≤ Y) :
    c60F125NativeIncidenceFibre t₁ t₂ left right sigma X ⟶
      c60F125NativeIncidenceFibre t₁ t₂ left right sigma Y := by
  cases X with
  | vertex v =>
    cases Y with
    | vertex w => exact 𝟙 _
    | edge e => exact (c60F72NativeVertexToEdge
        t₁ t₂ left right sigma e).toCatHom
    | face f => exact c60F72NativeVertexToFace.toCatHom
  | edge e =>
    cases Y with
    | vertex v =>
      change False at h
      exact False.elim h
    | edge d =>
      change e = d at h
      subst d
      exact 𝟙 _
    | face f => exact (c60F72NativeEdgeToFace
        t₁ t₂ left right sigma e).toCatHom
  | face f =>
    cases Y with
    | vertex v =>
      change False at h
      exact False.elim h
    | edge e =>
      change False at h
      exact False.elim h
    | face g => exact 𝟙 _

/-- Full compositionality of the 60/90/32 original site map.
Only the real vertex-edge-face case is nontrivial: it is exactly
the previously proved F72 original physical source triangle. -/
theorem c60F125NativeIncidenceMap_comp
    (sigma : C60F67Atlas)
    (X Y Z : C60F69PhysicalCellSite)
    (hXY : X ≤ Y) (hYZ : Y ≤ Z) :
    c60F125NativeIncidenceMap t₁ t₂ left right sigma
        (le_trans hXY hYZ) =
      c60F125NativeIncidenceMap t₁ t₂ left right sigma hXY ≫
        c60F125NativeIncidenceMap t₁ t₂ left right sigma hYZ := by
  cases X with
  | vertex v =>
    cases Y with
    | vertex w =>
      change v = w at hXY
      subst w
      cases Z <;>
        simp [c60F125NativeIncidenceMap, Category.id_comp]
    | edge e =>
      cases Z with
      | vertex w =>
        change False at hYZ
        exact False.elim hYZ
      | edge d =>
        change e = d at hYZ
        subst d
        simp [c60F125NativeIncidenceMap, Category.comp_id]
      | face f =>
        change c60F72NativeVertexToFace.toCatHom =
          (c60F72NativeVertexToEdge
            t₁ t₂ left right sigma e).toCatHom ≫
          (c60F72NativeEdgeToFace
            t₁ t₂ left right sigma e).toCatHom
        exact congrArg (fun F : GrayGrade ⥤ GrayGrade => F.toCatHom)
          (c60F72NativeFlagTransport_functorEq
            t₁ t₂ left right sigma e).symm
    | face f =>
      cases Z with
      | vertex w =>
        change False at hYZ
        exact False.elim hYZ
      | edge d =>
        change False at hYZ
        exact False.elim hYZ
      | face g =>
        change f = g at hYZ
        subst g
        simpa only [c60F125NativeIncidenceMap] using
          (Category.comp_id c60F72NativeVertexToFace.toCatHom).symm
  | edge e =>
    cases Y with
    | vertex v =>
      change False at hXY
      exact False.elim hXY
    | edge d =>
      change e = d at hXY
      subst d
      cases Z with
      | vertex v =>
        change False at hYZ
        exact False.elim hYZ
      | edge j =>
        change e = j at hYZ
        subst j
        simp [c60F125NativeIncidenceMap]
      | face f =>
        simp [c60F125NativeIncidenceMap, Category.id_comp]
    | face f =>
      cases Z with
      | vertex v =>
        change False at hYZ
        exact False.elim hYZ
      | edge j =>
        change False at hYZ
        exact False.elim hYZ
      | face g =>
        change f = g at hYZ
        subst g
        simpa only [c60F125NativeIncidenceMap] using
          (Category.comp_id
            (c60F72NativeEdgeToFace
              t₁ t₂ left right sigma e).toCatHom).symm
  | face f =>
    cases Y with
    | vertex v =>
      change False at hXY
      exact False.elim hXY
    | edge d =>
      change False at hXY
      exact False.elim hXY
    | face g =>
      cases Z with
      | vertex v =>
        change False at hYZ
        exact False.elim hYZ
      | edge d =>
        change False at hYZ
        exact False.elim hYZ
      | face j =>
        change (𝟙 (Cat.of GrayGrade)) =
          (𝟙 (Cat.of GrayGrade)) ≫ (𝟙 (Cat.of GrayGrade))
        exact (Category.id_comp
          (𝟙 (Cat.of GrayGrade))).symm

/-- This is a TRUE functor on the WHOLE original nonlocalized
F69 60-vertex/90-edge/32-face incidence category, not merely
a family of 90 disconnected local shadow functors. -/
def c60F125NativeFullIncidenceDiagram
    (sigma : C60F67Atlas) :
    C60F69PhysicalCellSite ⥤ Cat where
  obj := c60F125NativeIncidenceFibre t₁ t₂ left right sigma
  map := fun {_ _} f =>
    c60F125NativeIncidenceMap t₁ t₂ left right sigma (leOfHom f)
  map_id := by
    intro X
    cases X <;> rfl
  map_comp := by
    intro X Y Z f g
    exact c60F125NativeIncidenceMap_comp
      t₁ t₂ left right sigma X Y Z (leOfHom f) (leOfHom g)

/-- The previously conditional F71 1-CATEGORICAL incidence
interface is INHABITED by the native F72 collar. Exact F70
source fibre equality is definitional on ALL original edges. -/
def c60F125NativeFullIncidenceExtension
    (sigma : C60F67Atlas) :
    C60F71IncidenceExtension t₁ t₂ left right sigma where
  diagram := c60F125NativeFullIncidenceDiagram t₁ t₂ left right sigma
  edge_agrees := by
    intro edge
    rfl

/-- The original F69 incidence geometry and all F47 edge source
fibres coexist with the canonical NONZERO 90-edge F68 repair. -/
def c60F125NativeCorrectedIncidenceDescent
    (sigma : C60F67Atlas) :
    C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma :=
  c60F124CanonicalCorrectedIncidenceOfExtension
    t₁ t₂ left right sigma
    (c60F125NativeFullIncidenceExtension t₁ t₂ left right sigma)

/-- The strict native collar gives an explicit element of the
WEAK original F71 interface; raw higher source effectivity is
NOT a consequence of this type inhabitation. -/
theorem c60F125F71NativeIncidence_nonempty (sigma : C60F67Atlas) :
    Nonempty (C60F71IncidenceExtension t₁ t₂ left right sigma) :=
  ⟨c60F125NativeFullIncidenceExtension t₁ t₂ left right sigma⟩

/-- The corrected Gray-cochain *interface* becomes inhabited by
an ACTUAL original F69 incidence Cat functor, with no zero-curvature
assumption on the unmodified physical field. -/
theorem c60F125NativeCorrectedIncidence_nonempty (sigma : C60F67Atlas) :
    Nonempty (C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma) :=
  ⟨c60F125NativeCorrectedIncidenceDescent t₁ t₂ left right sigma⟩

/-- The genuine all-360 physical incidence flags are coherent,
and every admissible correction remains nonzero, with charge +5
on the NORTH original pentagon rather than erasing its -5 field. -/
theorem c60F125NativeCorrected_allFlags_curved
    (sigma : C60F67Atlas) :
    (∀ (edge : TruncatedIcosahedralEdge) (endpoint side : Bool),
        (c60F125NativeFullIncidenceDiagram t₁ t₂ left right sigma).map
            (c60F71ActualFlagVertexEdgeHom edge endpoint) ≫
        (c60F125NativeFullIncidenceDiagram t₁ t₂ left right sigma).map
            (c60F71ActualFlagEdgeFaceHom edge side) =
        (c60F125NativeFullIncidenceDiagram t₁ t₂ left right sigma).map
            (c60F71ActualFlagVertexFaceHom edge endpoint side)) ∧
    (c60F125NativeCorrectedIncidenceDescent
        t₁ t₂ left right sigma).correction ≠ 0 ∧
    (((c60F125NativeCorrectedIncidenceDescent
        t₁ t₂ left right sigma).correction.comp
          c60IntegralBoundaryTwo)
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 = (5 : ℤ) :=
  c60F124AllOriginalFlags_conditionalAndCurved
    t₁ t₂ left right sigma
    (c60F125NativeCorrectedIncidenceDescent t₁ t₂ left right sigma)

/-- F72's proved obstruction remains: at every genuine edge,
ANY chosen native GrayGrade vertex-to-ORIGINAL F47 functor
necessarily loses information. The new global functor does
not claim faithful raw-original-source 3-stack descent. -/
theorem c60F125NoFaithfulFullSourceVertexCollar
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    ¬ (c60F72NativeVertexToEdge
      t₁ t₂ left right sigma edge).Faithful :=
  c60F72NativeVertexToEdge_notFaithful
    t₁ t₂ left right sigma edge

#print axioms c60F125NativeIncidenceFibre
#print axioms c60F125NativeIncidenceMap
#print axioms c60F125NativeIncidenceMap_comp
#print axioms c60F125NativeFullIncidenceDiagram
#print axioms c60F125NativeFullIncidenceExtension
#print axioms c60F125NativeCorrectedIncidenceDescent
#print axioms c60F125F71NativeIncidence_nonempty
#print axioms c60F125NativeCorrectedIncidence_nonempty
#print axioms c60F125NativeCorrected_allFlags_curved
#print axioms c60F125NoFaithfulFullSourceVertexCollar

end OriginalPhysicalIncidenceCollar
end
end KUOS.DependentOriginationC60KuuNativeIncidenceCollarV5_291
