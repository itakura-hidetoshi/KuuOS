import KUOS.DependentOriginationC60KuuOriginalFlagTwoSimplexZigzagDescentV5_284
import KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276

namespace KUOS.DependentOriginationC60KuuPhysicalFlagOriginalSourceBeckChevalleyV5_285

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276
open KUOS.DependentOriginationC60KuuOriginalFlagTwoSimplexZigzagDescentV5_284
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.285 / F112 part 13 — genuine C60 flag-anchored original F47 source Beck–Chevalley

F118 proves actual C60/F69 360 vertex→edge→original-polygon two-simplices,
with raw zigzag two-leg/diagonal non-equality but exact equality
in the ORIGINAL incidence localization and its true kernel quotient.

F112 part 4 had REAL original F42/F54/F55 source Beck–Chevalley NatIso
for independently chosen F42 polygon-cell witnesses on the SAME
original physical edge, with independently typed original source paths.

This stage constructs an explicit ONE-ACTUAL-EDGE physical source
context for ANY of the original 90 C60 edges. The chosen physical
flag vertex gives true original C60 prior/suffix paths, and the
two *distinct actual faces* of that edge carry independently
selected original odd F42 cells. We build:
  * fully source-typed F47 mixed four-boundary frame and comparison;
  * BOTH original-context F58 left and right Beck–Chevalley NatIso;
  * naturality on every F47 three-Hom, separately also on the
    original F43 face and original F54/F55 rotation boundary arrows;
  * the EXACT true F69 two-simplex/ker-localization equality
    simultaneously with full F51 nonzero ZMod2 phase, original
    nine-constructor F55 Delta no-lift and F68 north charge -5.

Authority boundary: the BC is EDGE-LOCAL F47 SOURCE BC ANCHORED
TO a genuine F69 physical flag. It is not a putative F69-wide Cat
diagram (vertices and faces lack generally constructed F47 fibres)
nor a 2-cell/3-cell natural transformation in an absent global original
three-sheaf. The original raw F42/F54 sources, original F69 incidence,
and physical nonflat F68 cochain remain distinct.
-/

/-! ## I. A real source chart on ANY original physical edge -/

/-- The same geometry-based original F108 construction, specialized
to a given actual C60 physical edge, with two genuinely distinct
original incident pentagon/hexagon F42 sites. -/
noncomputable def c60F119OnePhysicalEdgeContext
    (edge : TruncatedIcosahedralEdge) :
    C60F108BothFaceContexts 1 :=
  c60F108BothFaceContextsFromGeometry (fun _ => edge)

theorem c60F119OnePhysicalEdgeContext_edge
    (edge : TruncatedIcosahedralEdge) :
    (c60F119OnePhysicalEdgeContext edge).edge (0 : Fin 1) = edge := rfl

/-- TRUE raw C60 source path FROM the selected physical F69
flag vertex TO the original edge's first endpoint. Neither
the path nor its reverse is asserted to be an old F69 Hom. -/
noncomputable def c60F119FlagPrior
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool) :
    Quiver.Path
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
      (truncatedIcosahedralEdgeEndpoints edge).1 :=
  c60F109EveryDartToDart _ _

/-- TRUE raw physical suffix from the edge's second endpoint to
the flag vertex. This is separately typed from the prior path. -/
noncomputable def c60F119FlagSuffix
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool) :
    Quiver.Path
      (truncatedIcosahedralEdgeEndpoints edge).2
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint) :=
  c60F109EveryDartToDart _ _

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalFlagSourceComparison
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

/-- The original mixed F47 square for two independently typed
odd original F42 face cells at real incident C60 polygon sites. -/
abbrev c60F119PhysicalFlagMixedFrame
    (edge : TruncatedIcosahedralEdge)
    (P : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1)) :=
  c60F112MixedPhysicalFrame t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1) P

/-- An actual F47 SOURCE comparison of two unrelated raw
original face labels on the SAME actual physical edge. -/
def c60F119PhysicalFlagSourceChange
    (edge : TruncatedIcosahedralEdge)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1)) :
    C60F47BoundaryPoint
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀) ⥤
    C60F47BoundaryPoint
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₁) :=
  c60F112MixedPhysicalSourceChange t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge)
    (c60F119OnePhysicalEdgeContext edge)
    (0 : Fin 1) P₀ P₁ rfl

/-- The comparison preserves FULL native original F47 Hom data,
including BOTH Int charges AND the independent ZMod2 phase. -/
theorem c60F119PhysicalFlagSourceChange_fullNative
    (edge : TruncatedIcosahedralEdge)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {X Y : C60F47BoundaryPoint
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀)}
    (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F119PhysicalFlagSourceChange
        t₁ t₂ left right edge P₀ P₁).map f) =
      c60F47MixedEval f :=
  c60F112MixedPhysicalSourceChange_native t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge)
    (c60F119OnePhysicalEdgeContext edge)
    (0 : Fin 1) P₀ P₁ rfl f

/-- Explicit LEFT original-source Beck–Chevalley NATURAL ISO
anchored at the chosen vertex of a real F69 flag, with
independent physical prior contexts and a genuine F54 later tree. -/
noncomputable def c60F119PhysicalFlagLeftBC
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :=
  c60F112MixedPhysicalLeftBeckChevalley t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge)
    (c60F119OnePhysicalEdgeContext edge)
    (0 : Fin 1) P₀ P₁ rfl
    (c60F119FlagPrior edge endpoint)
    (Quiver.Path.nil)
    later

/-- Explicit RIGHT original-source Beck–Chevalley NATURAL ISO,
using the other genuine old C60 edge endpoint and a separately
typed suffix to the chosen ORIGINAL flag vertex. -/
noncomputable def c60F119PhysicalFlagRightBC
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :=
  c60F112MixedPhysicalRightBeckChevalley t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge)
    (c60F119OnePhysicalEdgeContext edge)
    (0 : Fin 1) P₀ P₁ rfl
    (Quiver.Path.nil)
    (c60F119FlagSuffix edge endpoint)
    earlier

/-- SOURCE BC NATURALITY for EVERY original four-boundary F47 Hom,
not just its phase-forgetting F77 evaluation. -/
def c60F119PhysicalFlagLeftBC_naturality
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc)
    {X Y : C60F47BoundaryPoint
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀)}
    (f : X ⟶ Y) :=
  (c60F119PhysicalFlagLeftBC
    t₁ t₂ left right edge endpoint P₀ P₁ later).hom.naturality f

def c60F119PhysicalFlagRightBC_naturality
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀)
    {X Y : C60F47BoundaryPoint
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀)}
    (f : X ⟶ Y) :=
  (c60F119PhysicalFlagRightBC
    t₁ t₂ left right edge endpoint P₀ P₁ earlier).hom.naturality f

/-- Verify LEFT BC explicitly on the ORIGINAL F43 face-exchange
three-Hom, not only on an abstract arrow of the F47 quotient. -/
def c60F119PhysicalFlagLeftBC_originalFace
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :=
  (c60F119PhysicalFlagLeftBC
    t₁ t₂ left right edge endpoint P₀ P₁ later).hom.naturality
      (c60F47FaceArrow
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀))

/-- Verify RIGHT BC explicitly on the REAL ORIGINAL F54/F55
rotation-square source arrow, with original route type preserved. -/
def c60F119PhysicalFlagRightBC_originalF55
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :=
  (c60F119PhysicalFlagRightBC
    t₁ t₂ left right edge endpoint P₀ P₁ earlier).hom.naturality
      (c60F47OriginalF55Arrow
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀))

/-- The authentic original F47 four-boundary source square
remains commuting after the physical-flag guarded base change. -/
theorem c60F119PhysicalFlagMixedSquare_transport
    (edge : TruncatedIcosahedralEdge)
    (P₀ P₁ : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1)) :
    (c60F119PhysicalFlagSourceChange
      t₁ t₂ left right edge P₀ P₁).map
      (c60F47FaceArrow
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀) ≫
       c60F47CompareAfter
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₀)) =
      c60F47FaceArrow
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₁) ≫
      c60F47CompareAfter
        (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P₁) :=
  c60F112MixedPhysicalSourceChange_square t₁ t₂ left right
    (c60F119OnePhysicalEdgeContext edge)
    (c60F119OnePhysicalEdgeContext edge)
    (0 : Fin 1) P₀ P₁ rfl

/-! ## II. The physical site stays curved, with original-source no-lift -/

/-- The proposition asserting that no ORIGINAL nine-constructor
F55 source cell, with the EXACT ORIGINAL F54 square boundaries,
can replace the added mixed-F47 Delta receiver on this edge. -/
def c60F119OriginalF55NoLift
    (edge : TruncatedIcosahedralEdge)
    (P : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1)) : Prop :=
  ¬ ∃ cell :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
    c60F44FaceThreeEval
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P).faceStep +
      c60F55SourceNative cell =
    c60F44OriginalF55Eval
      (c60F119PhysicalFlagMixedFrame t₁ t₂ left right edge P).rotationStep

theorem c60F119OriginalF55NoLift_proved
    (edge : TruncatedIcosahedralEdge)
    (P : C60F112IndependentOddFacePair
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1)) :
    c60F119OriginalF55NoLift t₁ t₂ left right edge P :=
  c60F112IndependentFaceOriginalMixed_noF55Lift
    t₁ t₂ left right (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1) P

/-- ALL actual physical C60 flags support the original source
BC diagram and exact F69 2-simplex geometry simultaneously,
yet their original phase ONE, F55 no-lift and signed north
physical F68 charge -5 remain independent obstructions.

The source BC is edge-local and genuinely typed, NOT an
unconditional F69 vertex/face-wide source 3-descent. -/
theorem c60F119EveryPhysicalFlagSourceAndCurvatureBoundary
    (P : (edge : TruncatedIcosahedralEdge) →
      C60F112IndependentOddFacePair
        (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1))
    (sigma : C60F67Atlas) :
    Fintype.card (TruncatedIcosahedralEdge × (Bool × Bool)) = 360 ∧
    ∀ (edge : TruncatedIcosahedralEdge) (endpoint faceChoice : Bool),
      (c60F118PhysicalFlagRawSpan edge endpoint faceChoice ≠
        c60F118PhysicalFlagRawDiagonal edge endpoint faceChoice) ∧
      (c60F116RawZigzagKernelQ.map
        (c60F118PhysicalFlagRawSpan edge endpoint faceChoice) =
        c60F116RawZigzagKernelQ.map
          (c60F118PhysicalFlagRawDiagonal edge endpoint faceChoice)) ∧
      (c60F51Eval
        (c60F112IndependentPairExchangeHom
          (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1) (P edge))).phase =
        (1 : ZMod 2) ∧
      c60F119OriginalF55NoLift t₁ t₂ left right edge (P edge) ∧
      (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
        (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) := by
  refine ⟨c60F69ActualPhysicalFlagIndex_card, ?_⟩
  intro edge endpoint faceChoice
  exact ⟨c60F118PhysicalFlagRaw_ne_diagonal edge endpoint faceChoice,
    c60F118PhysicalFlag_kernelQuotient edge endpoint faceChoice,
    (c60F112IndependentPairExchange_components
      (c60F119OnePhysicalEdgeContext edge) (0 : Fin 1) (P edge)).2,
    c60F119OriginalF55NoLift_proved t₁ t₂ left right edge (P edge),
    c60F68PhysicalPatchCurvature_northSecondCharge t₁ t₂ left right sigma⟩

#print axioms c60F119OnePhysicalEdgeContext_edge
#print axioms c60F119PhysicalFlagSourceChange_fullNative
#print axioms c60F119PhysicalFlagLeftBC
#print axioms c60F119PhysicalFlagRightBC
#print axioms c60F119PhysicalFlagLeftBC_naturality
#print axioms c60F119PhysicalFlagRightBC_naturality
#print axioms c60F119PhysicalFlagLeftBC_originalFace
#print axioms c60F119PhysicalFlagRightBC_originalF55
#print axioms c60F119PhysicalFlagMixedSquare_transport
#print axioms c60F119OriginalF55NoLift_proved
#print axioms c60F119EveryPhysicalFlagSourceAndCurvatureBoundary

end OriginalFlagSourceComparison
end
end KUOS.DependentOriginationC60KuuPhysicalFlagOriginalSourceBeckChevalleyV5_285
