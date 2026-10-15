import KUOS.DependentOriginationC60KuuPhysicalFlagOriginalSourceBeckChevalleyV5_285
import KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277

namespace KUOS.DependentOriginationC60KuuCrossEdgeOriginalSourceBeckChevalleyV5_286

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationC60KuuOriginalFlagTwoSimplexZigzagDescentV5_284
open KUOS.DependentOriginationC60KuuPhysicalFlagOriginalSourceBeckChevalleyV5_285
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.286 / F112 stage 14: genuine cross-physical-edge original-source BC

F112 part 13 provided genuine original F42/F54/F55 source LEFT and RIGHT
Beck-Chevalley NatIso for two independently chosen original F42
presentations over ONE physical C60 edge, anchored by actual F69 flags.
F112 part 5 separately provided a real guarded cross-edge F47 source
functor ONLY in the presence of an actual common original F69 cell
site of two DISTINCT physical C60 edges.

This module constructs a new ACTUAL 2-cell in the FUNCTOR CATEGORY
between the two source transport orders:
    (change original F42 pair at edge i) then (cross real overlap)
                        versus
    (cross real overlap) then (change original F42 pair at edge j).
This is a typed Beck-Chevalley natural isomorphism between two
COMPOSITE ORIGINAL F47 SOURCE FUNCTORS, on ALL ORIGINAL F47 3-Homs.
In fact both composite source functors are proved STRICTLY EQUAL
using faithfulness of full Int x Int plus ZMod2 native evaluation,
with required equality-to-Hom boundary transports made explicit.

The physical comparison retains W.common, an actual original F69
vertex or pentagonal/hexagonal face, and does NOT insert a direct
old-F69 edge_i to edge_j Hom. Original physical flag raw routes
are still nonidentical to original incidence diagonals, even
though their localized images agree.

Authority boundary:
* The new NatIso lives in Cat between guarded F47 MIXED SOURCE
  CATEGORIES. It is NOT a new original F55 generator, and does
  NOT erase original F42/F54 raw proof-relevant presentations.
* This does NOT supply F47 fibres on ALL original F69 vertices/faces
  nor prove a global three-stack, arbitrary higher modifications,
  or effective original F42/F54/F55 three-descent.
* Original F55 Delta no-lift, F110 lost F77 phase and F68
  physical north-pentagon curvature charge -5 stay nonzero.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section CrossEdgeOriginalSourceBC
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

/-- Change independently chosen original odd F42 face-pair
presentations on the SAME genuine physical edge. -/
abbrev c60F120SameEdgeSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n)
    (P₀ P₁ : C60F112IndependentOddFacePair C i) :
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀) ⥤
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₁) :=
  c60F112MixedPhysicalSourceChange
    t₁ t₂ left right C C i P₀ P₁ rfl

/-- First change ORIGINAL F42 source presentation at physical
edge i; only THEN cross to a DISTINCT genuine edge j using W. -/
def c60F120LocalThenCross
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀) ⥤
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q₁) :=
  c60F120SameEdgeSourceChange t₁ t₂ left right C i P₀ P₁ ⋙
    c60F112CrossEdgeMixedSourceChange
      t₁ t₂ left right C i j W P₁ Q₁

/-- First cross the genuine F69 intersection to distinct edge j,
then change its original F42 source presentation there. -/
def c60F120CrossThenLocal
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀) ⥤
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q₁) :=
  c60F112CrossEdgeMixedSourceChange
      t₁ t₂ left right C i j W P₀ Q₀ ⋙
    c60F120SameEdgeSourceChange t₁ t₂ left right C j Q₀ Q₁

/-- BOTH genuine, differently routed SOURCE functors preserve
the complete original F47 two-integer charge and ZMod2 phase
on EVERY Hom, never applying F77 phase erasure. -/
theorem c60F120BothTransportOrders_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j)
    {X Y : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀)}
    (f : X ⟶ Y) :
    c60F47MixedEval
        ((c60F120LocalThenCross t₁ t₂ left right
          C i j W P₀ P₁ Q₀ Q₁).map f) =
        c60F47MixedEval f ∧
    c60F47MixedEval
        ((c60F120CrossThenLocal t₁ t₂ left right
          C i j W P₀ P₁ Q₀ Q₁).map f) =
        c60F47MixedEval f := by
  constructor
  · calc
      _ = c60F47MixedEval
          ((c60F120SameEdgeSourceChange
            t₁ t₂ left right C i P₀ P₁).map f) :=
        c60F112CrossEdgeMixedSourceChange_fullNative
          t₁ t₂ left right C i j W P₁ Q₁ _
      _ = c60F47MixedEval f :=
        c60F112MixedPhysicalSourceChange_native
          t₁ t₂ left right C C i P₀ P₁ rfl f
  · calc
      _ = c60F47MixedEval
          ((c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j W P₀ Q₀).map f) :=
        c60F112MixedPhysicalSourceChange_native
          t₁ t₂ left right C C j Q₀ Q₁ rfl _
      _ = c60F47MixedEval f :=
        c60F112CrossEdgeMixedSourceChange_fullNative
          t₁ t₂ left right C i j W P₀ Q₀ f

/-- Original F47 native evaluation of a dependent Hom
conjugated by categorical equality transports remains EXACT.
This avoids treating distinct original F42 or F54 raw types
as definitionally equal. -/
theorem c60F120TargetEqToHom_preservesNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (j : Fin n) (Q : C60F112IndependentOddFacePair C j)
    {A B D E : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q)}
    (hAB : A = B) (hDE : D = E) (f : B ⟶ D) :
    c60F47MixedEval (eqToHom hAB ≫ f ≫ eqToHom hDE) =
      c60F47MixedEval f := by
  cases hAB
  cases hDE
  simp only [eqToHom_refl, Category.id_comp, Category.comp_id]

/-- TRUE CROSS-EDGE ORIGINAL-SOURCE BECK-CHEVALLEY:
the two functors for local source-presentation change
versus guarded transport across TWO DISTINCT actual C60
edges are STRICTLY EQUAL as source F47 Cat functors.
This uses the FULL phase-aware native faithful quotient. -/
theorem c60F120OriginalCrossEdgeSourceBC_strict
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :
    c60F120LocalThenCross t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁ =
    c60F120CrossThenLocal t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁ := by
  fapply CategoryTheory.Functor.ext
  · intro X
    cases X <;> rfl
  · intro X Y f
    apply c60F47MixedGrayFunctor_faithful
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q₁)
    calc
      c60F47MixedEval
        ((c60F120LocalThenCross t₁ t₂ left right
          C i j W P₀ P₁ Q₀ Q₁).map f) =
        c60F47MixedEval f :=
          (c60F120BothTransportOrders_fullNative
            t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁ f).1
      _ = c60F47MixedEval
        ((c60F120CrossThenLocal t₁ t₂ left right
          C i j W P₀ P₁ Q₀ Q₁).map f) :=
          (c60F120BothTransportOrders_fullNative
            t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁ f).2.symm
      _ = c60F47MixedEval
          (eqToHom _ ≫
            (c60F120CrossThenLocal t₁ t₂ left right
              C i j W P₀ P₁ Q₀ Q₁).map f ≫ eqToHom _) := by
          symm
          exact c60F120TargetEqToHom_preservesNative
            t₁ t₂ left right C j Q₁ _ _ _

/-- The actual Cat 2-cell associated with the STRICT
cross-edge source Beck-Chevalley interchange. Its domain
and codomain are two DIFFERENT source-transport orders,
not an invented old F55 3-cell. -/
def c60F120OriginalCrossEdgeSourceBC_NatIso
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :
    c60F120LocalThenCross t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁ ≅
    c60F120CrossThenLocal t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁ :=
  eqToIso
    (c60F120OriginalCrossEdgeSourceBC_strict
      t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁)

/-- Natural on EVERY original four-boundary F47 source 3-Hom.
This is an actual natural transformation in a Mathlib
functor category; the original boundaries remain dependent. -/
def c60F120OriginalCrossEdgeSourceBC_naturality
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j)
    {X Y : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀)}
    (f : X ⟶ Y) :=
  (c60F120OriginalCrossEdgeSourceBC_NatIso
    t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁).hom.naturality f

/-- Actual original F43 face-exchange 3-Hom satisfies
the cross-edge presentation-change Beck-Chevalley 2-cell. -/
def c60F120OriginalCrossEdgeSourceBC_faceArrow
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :=
  c60F120OriginalCrossEdgeSourceBC_naturality
    t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁
      (c60F47FaceArrow
        (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀))

/-- The ORIGINAL F54/F55 rotation-square source Hom also
obeys the very same cross-edge source BC 2-cell, with no
raw original F54 path equality assumed. -/
def c60F120OriginalCrossEdgeSourceBC_F55Arrow
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :=
  c60F120OriginalCrossEdgeSourceBC_naturality
    t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁
      (c60F47OriginalF55Arrow
        (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀))

/-- The original calibrated mixed F47 boundary square is
preserved under BOTH cross-edge transport orders. This
is not an original nine-constructor F55 replacement. -/
theorem c60F120CrossEdgeSourceBC_mixedSquare
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j) :
    (c60F120LocalThenCross t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁).map
        (c60F47FaceArrow
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀) ≫
         c60F47CompareAfter
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀)) =
    (c60F120CrossThenLocal t₁ t₂ left right
      C i j W P₀ P₁ Q₀ Q₁).map
        (c60F47CompareBefore
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀) ≫
         c60F47OriginalF55Arrow
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀)) := by
  rw [c60F120OriginalCrossEdgeSourceBC_strict]
  exact congrArg
    (fun f => (c60F120CrossThenLocal
      t₁ t₂ left right C i j W P₀ P₁ Q₀ Q₁).map f)
    (c60F47MixedOriginalBoundarySquare
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀))

/-! ## Authentic physical geometry and independent source obstruction -/

/-- On the true original geometric overlap, both independent
original F42 odd exchanges retain phase ONE, AND the signed
F68 north curvature remains nonzero. The old F55 Delta
comparison still cannot be expressed by its nine generators. -/
theorem c60F120CrossEdgeBC_originalObstructions
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P₀ P₁ : C60F112IndependentOddFacePair C i)
    (Q₀ Q₁ : C60F112IndependentOddFacePair C j)
    (sigma : C60F67Atlas) :
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P₀)).phase =
      (1 : ZMod 2) ∧
    (c60F51Eval (c60F112IndependentPairExchangeHom C j Q₀)).phase =
      (1 : ZMod 2) ∧
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
      (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P₀).rotationStep) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j Q₀).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j Q₀).rotationStep) := by
  have hnonlift :=
    c60F112CrossEdgeOriginalF55_nonlift
      t₁ t₂ left right C i j W P₀ Q₀
  exact ⟨(c60F112IndependentPairExchange_components C i P₀).2,
    (c60F112IndependentPairExchange_components C j Q₀).2,
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma,
    c60F68PhysicalPatchCurvature_ne_zero
      t₁ t₂ left right sigma,
    hnonlift.1, hnonlift.2⟩

#print axioms c60F120BothTransportOrders_fullNative
#print axioms c60F120TargetEqToHom_preservesNative
#print axioms c60F120OriginalCrossEdgeSourceBC_strict
#print axioms c60F120OriginalCrossEdgeSourceBC_NatIso
#print axioms c60F120OriginalCrossEdgeSourceBC_naturality
#print axioms c60F120OriginalCrossEdgeSourceBC_faceArrow
#print axioms c60F120OriginalCrossEdgeSourceBC_F55Arrow
#print axioms c60F120CrossEdgeSourceBC_mixedSquare
#print axioms c60F120CrossEdgeBC_originalObstructions

end CrossEdgeOriginalSourceBC
end
end KUOS.DependentOriginationC60KuuCrossEdgeOriginalSourceBeckChevalleyV5_286
