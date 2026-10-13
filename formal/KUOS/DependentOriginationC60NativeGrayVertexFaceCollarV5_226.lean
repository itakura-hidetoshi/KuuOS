import KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
import KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
import Mathlib.CategoryTheory.Functor.Const

namespace KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
open KUOS.DependentOriginationC60ArbitraryAtlasNerveDescentV5_219
open KUOS.DependentOriginationC60FourAtlasCechNerveV5_220
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60PhysicalEdgeGrothendieckV5_224
open KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.226 / F72: actual C60 vertex/edge/face native Gray collar, and a faithful no-go

The F71 incidence Grothendieck construction accepts a conditional diagram.
Here we study its concrete local building blocks at EVERY genuinely incident
vertex, edge and face, while retaining the exact original four-tagged F47
edge source category and the native nontrivial F59 GrayGrade category.

A native GrayGrade vertex-category may map to the original edge F47 source
category via a deliberately nonfaithful constant source-boundary selection.
The original FULL native faithful C60 F47 functor then maps that typed edge
source into a GrayGrade polygon face.  A direct vertex-to-face constant
functor agrees with this two-step transport at all 360 true C60 flags.

There is a MATHEMATICAL OBSTRUCTION to demanding faithfulness on both sides:
the genuine odd/odd Gray braiding gives a nonidentity endomorphism, whereas
every F47 four-tagged object has a unique endomorphism in the actual full
native-kernel quotient (original F61 theorem). Thus NO functor from the
genuine native GrayGrade category to an edge F47 source category can be
faithful, at ANY of the actual 90 physical edges and any 90-bit atlas.

This explicitly identifies the lost vertex-to-edge Gray information.
It does NOT identify raw original F42/F55 with the F47 source quotient,
and does NOT assert a global incidence functor or an (infinity,3)-stack.
The original north-pentagon integer curvature -5 and its genuine
unrepaired global vertex-gauge obstruction remain unchanged.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalNinetyEdgeGrayCollar

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

/-- ORIGINAL physical vertex-to-edge C60 collar in the native Gray
presentation. It selects one actually typed source F47 boundary tag,
and IS NOT claimed faithful or to represent an original F55 source. -/
def c60F72NativeVertexToEdge
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    GrayGrade ⥤ C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge)) :=
  (Functor.const GrayGrade).obj
    (C60F47BoundaryPoint.faceBefore :
      C60F47BoundaryPoint
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge (sigma edge)))

/-- The EXACT original full-native and faithful F47 source-to-F59
target functor becomes an ACTUAL edge-to-face incidence shadow map.
Its codomain is a shared full GrayGrade category, not a phase-only
quotient or a fabricated original F42 face four-cell. -/
def c60F72NativeEdgeToFace
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge)) ⥤ GrayGrade :=
  c60F47MixedGrayFunctor
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge))

/-- The direct Gray vertex-to-physical-face shadow map is the
same genuine neutral-grade constant object underlying the original
F47 edge-to-face Gray evaluation of the selected source boundary. -/
def c60F72NativeVertexToFace : GrayGrade ⥤ GrayGrade :=
  (Functor.const GrayGrade).obj GrayGrade.unit

/-- A STRONGER result than agreeing numeric charges: the
two-step typed Mathlib FUNCTOR through a genuine four-boundary F47
source category equals the direct native Gray vertex-to-face functor. -/
theorem c60F72NativeFlagTransport_functorEq
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    c60F72NativeVertexToEdge
        t₁ t₂ left right sigma edge ⋙
      c60F72NativeEdgeToFace
        t₁ t₂ left right sigma edge =
    c60F72NativeVertexToFace := by
  fapply Functor.ext
  · intro X
    rfl
  · intro X Y f
    change
      (c60F47MixedGrayFunctor
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge (sigma edge))).map
        (𝟙 (C60F47BoundaryPoint.faceBefore :
          C60F47BoundaryPoint
            (c60F48EveryRealEdgeMixedFrame
              t₁ t₂ left right edge (sigma edge)))) =
      𝟙 GrayGrade.unit
    exact Functor.map_id _ _

/-- The physical C60 corner has a genuine vertex-edge-face
2-simplex, AND its native Gray shadow admits a constructed strict
typed comparison. Both apply to each of the 360 ORIGINAL physical
flags: two true endpoints and two true polygon faces per edge. -/
theorem c60F72EveryRealPhysicalFlag_nativeTransportCoherence
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (endpoint side : Bool) :
    (c60F71ActualFlagVertexEdgeHom edge endpoint ≫
        c60F71ActualFlagEdgeFaceHom edge side =
      c60F71ActualFlagVertexFaceHom edge endpoint side) ∧
    (c60F72NativeVertexToEdge
        t₁ t₂ left right sigma edge ⋙
      c60F72NativeEdgeToFace
        t₁ t₂ left right sigma edge =
      c60F72NativeVertexToFace) :=
  ⟨c60F71ActualPhysicalFlagTriangle_coherent edge endpoint side,
    c60F72NativeFlagTransport_functorEq
      t₁ t₂ left right sigma edge⟩

/-- The original proof-relevant F42/F55 F47 source 3-morphisms
retain their COMPLETE two integer charges and distinct ZMod2 phase
when transported into the polygon-face Gray native category. -/
theorem c60F72NativeEdgeToFace_fullNative
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))}
    (f : X ⟶ Y) :
    (c60F72NativeEdgeToFace
      t₁ t₂ left right sigma edge).map f = c60F47MixedEval f := rfl

/-- Complete native Gray evaluation is injective on every original
four-boundary typed mixed F47 source Hom, not merely on the phase
coordinate of its Gray image. -/
theorem c60F72NativeEdgeToFace_faithful
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))}
    {f g : X ⟶ Y}
    (h :
      (c60F72NativeEdgeToFace
        t₁ t₂ left right sigma edge).map f =
      (c60F72NativeEdgeToFace
        t₁ t₂ left right sigma edge).map g) :
    f = g :=
  c60F47MixedGrayFunctor_faithful
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge)) h

/-- AN ACTUAL no-go theorem, not an assumed obstruction:
even with a completely arbitrary candidate functor from the
native GrayGrade category to an old C60 F47 edge source, the
nonidentity odd/odd native Gray braiding must collapse, because
original full-native-kernel F47 endomorphisms are rigid.
Consequently such a candidate can NEVER be faithful. -/
theorem c60F72NoFaithfulNativeGrayVertexToF47
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (F : GrayGrade ⥤ C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))) :
    ¬ F.Faithful := by
  intro hFaithful
  let z : GrayGrade := GrayGrade.tensor GrayGrade.odd GrayGrade.odd
  have hSame :
      F.map (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
      F.map (𝟙 z) :=
    c60F61MixedEndomorphism_unique
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))
      (F.obj z) _ _
  exact GrayGrade.native_braiding_odd_nonidentity
    (hFaithful.map_injective hSame)

/-- The explicitly constructed native vertex-to-edge collar,
even though it is a true Cat functor, is demonstrably NONFAITHFUL;
this information loss cannot be repaired merely by changing
the chosen four-tagged F47 boundary site. -/
theorem c60F72NativeVertexToEdge_notFaithful
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    ¬ (c60F72NativeVertexToEdge
      t₁ t₂ left right sigma edge).Faithful :=
  c60F72NoFaithfulNativeGrayVertexToF47
    t₁ t₂ left right sigma edge _

/-- Arbitrary finite F67 changes of the real physical face choices
preserve the SAME full Gray output on every original proof-relevant
mixed 3-Hom arrow. Thus the native face-level collar retains all
charges/phase even when vertex-to-edge collar is nonfaithful. -/
theorem c60F72NativeEdgeFace_finiteAtlasCompatibility
    (sigma tau : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))}
    (f : X ⟶ Y) :
    (c60F72NativeEdgeToFace
        t₁ t₂ left right tau edge).map
        ((c60F67AtlasRoute
          t₁ t₂ left right sigma tau edge via).map f) =
      (c60F72NativeEdgeToFace
        t₁ t₂ left right sigma edge).map f :=
  c60F67AtlasRoute_fullNative
    t₁ t₂ left right tau edge via sigma f

/-- At all genuinely incident original faces the local transport
data coexist with the surviving north-pentagon obstruction.
Strictly coherent physical flags do NOT imply an effective
UNCORRECTED global 60-vertex Gray potential. -/
theorem c60F72NativeCollar_curvatureObstruction
    (sigma tau : C60F67Atlas) :
    c60F68PhysicalPatchCurvature
        t₁ t₂ left right sigma =
      c60F68PhysicalPatchCurvature
        t₁ t₂ left right tau ∧
    (c60F68PhysicalPatchCurvature
        t₁ t₂ left right sigma
        (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
          (-5 : ℤ) ∧
    (¬ ∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F68AtlasEdgeCochain
        t₁ t₂ left right sigma =
        phi.comp c60IntegralBoundaryOne) ∧
    c60F68CanonicalPhysicalRepair
      t₁ t₂ left right sigma ≠ 0 :=
  c60F69RealFlagNerve_curvature_obstruction_and_repair
    t₁ t₂ left right sigma tau

#print axioms c60F72NativeVertexToEdge
#print axioms c60F72NativeEdgeToFace
#print axioms c60F72NativeVertexToFace
#print axioms c60F72NativeFlagTransport_functorEq
#print axioms c60F72EveryRealPhysicalFlag_nativeTransportCoherence
#print axioms c60F72NativeEdgeToFace_fullNative
#print axioms c60F72NativeEdgeToFace_faithful
#print axioms c60F72NoFaithfulNativeGrayVertexToF47
#print axioms c60F72NativeVertexToEdge_notFaithful
#print axioms c60F72NativeEdgeFace_finiteAtlasCompatibility
#print axioms c60F72NativeCollar_curvatureObstruction

end OriginalNinetyEdgeGrayCollar
end
end KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226
