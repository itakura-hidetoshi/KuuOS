import KUOS.DependentOriginationGrayC60F55ParityMonoidalProjectionV5_179
import KUOS.DependentOriginationGrayC60NonneutralDefectDoubleCountV5_178
import KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174

namespace KUOS.DependentOriginationGrayC60BraidedProjectionDescentV5_180

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
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60NonneutralDefectDoubleCountV5_178
open KUOS.DependentOriginationGrayC60F55ParityMonoidalProjectionV5_179
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F32 / v5.180 — parity projection does NOT reflect genuine local C60 descent

F59-F26/27 proved exact signed C60 cochain descent and the 27-edge
canonical flat repair of 90 actual, nontrivial original F55 square
generators. F59-F29/30 attached INDEPENDENT nonneutral native braided
exchange of 2-cell grades a,b, whose phase defect is a*b, and proved
the source geometric 32-face UNSIGNED parity double-count.

F59-F31 constructed a real mathlib STRONG MONOIDAL functor P which
forgets independent braid phase but preserves native F55 integer
charges, tensor, composition, and four genuine C60 source-chart
transport operations. Crucially it is NOT a braided functor.

Here we tie these different notions of descent together without
collapsing the distinction of full native nonneutral 3-cells
(a+b -> b+a) and their neutral endomorphism TARGET COEFFICIENTS.

The honest nonneutral interchanger exchange(a,b) has independently
measured phase a*b and charge zero. We encode ONLY those two measured
invariants as the corresponding neutral-endomorphism coefficient
ε(a,b) = (0,0;a*b), not as a new free source F55 generator. It is
this neutral coefficient that can be added to the actual original
90-edge repaired neutral-valued C60 cochain. The two carriers are
explicitly typed and not identified as the same morphism.

For the resulting edge field:
  B_ab(e) = repaired_original_F55(e) + ε(a,b),
we prove:
1. it has constant extra independent braid phase defect a*b;
2. the genuine native STRONG MONOIDAL parity projection fixes
   exactly the underlying 27-edge repaired F55 field at EVERY
   real physical edge;
3. the parity projection commutes with ACTUAL ORIENTED signed
   5- or 6-edge C60 face 3-cell pasting and its full 32-face surface;
4. the parity image is locally flat on ALL original 32 faces and
   has the specific real 59-edge-tree vertex descent;
5. before projection, B_11 has NONZERO original NORTH pentagon
   curvature (phase 1) despite the projected field being flat;
6. both before/after projection have globally ZERO oriented H²
   surface obstruction (but the braided field has a genuine local
   H¹ descent obstruction). We distinguish this from the
   additional UNSIGNED mod-two 32-face double-count identity;
7. the Wang Bi global Cat natural transformation built from the
   projected field is EXACTLY the original v5.174 corrected
   atlas, with time-dependent 王弼 semantic reading still supplied
   independently, not inferred from braid curvature.

This gives a CONCRETE failure of descent reflection by the native
strong monoidal (but non-braided) parity projection. The full
source-level Gray 3-functor, clinical meaning and old Stage-II
omega remain separate and are NOT asserted.
-/

/-- The phase-only image of the genuine NATIVE nonneutral interchanger
in the NEUTRAL coefficient group used by actual C60 integral cochains.
It records charge/phase but is NOT an equality with a graded
3-morphism (a+b)->(b+a) at nonneutral boundary. -/
def c60F32NeutralBraidCoefficient (a b : ZMod 2) :
    GradedThreeCell 0 0 :=
  ⟨rfl, ((0 : Int), (0 : Int)), a * b⟩

/-- The phase/charge records of the neutral coefficient agree EXACTLY
with the independently typed original native Gray interchanger. -/
theorem c60F32NeutralBraidCoefficient_components (a b : ZMod 2) :
    (c60F32NeutralBraidCoefficient a b).charge =
      (GradedThreeCell.exchange a b).charge ∧
    (c60F32NeutralBraidCoefficient a b).phase =
      (GradedThreeCell.exchange a b).phase := by
  constructor <;> rfl

/-- The native phase defect of the genuinely independent external
braid records exactly a*b, not the parity of source F55 squares. -/
theorem c60F32NeutralBraidCoefficient_defect (a b : ZMod 2) :
    c60F29PhaseDefect (c60F32NeutralBraidCoefficient a b) = a * b := by
  simp [c60F29PhaseDefect, c60F32NeutralBraidCoefficient]

/-- The native STRONG MONOIDAL parity functor kills the pure
independent braiding coefficient while retaining its external
typed-braiding provenance in the comparison theorem above. -/
theorem c60F32NeutralBraidCoefficient_projected_zero (a b : ZMod 2) :
    c60F31ParityCell (c60F32NeutralBraidCoefficient a b) = 0 := by
  apply GradedThreeCell.ext <;> rfl

/-- The actual canonical 27-edge repaired F55 field plus the
independent measured native a/b braided exchange phase on EACH
of the original ninety physical C60 edges. -/
def c60F32BraidedRepairedEdge (a b : ZMod 2)
    (edge : TruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  c60WangBiRepairedEdgeGrade edge +
    c60F32NeutralBraidCoefficient a b

/-- Even in the full independent target, the original 27-edge repaired
component retains all original F55 charges and phase, while the
new and separately supplied braid defect equals a*b. -/
theorem c60F32BraidedRepaired_defect (a b : ZMod 2)
    (edge : TruncatedIcosahedralEdge) :
    c60F29PhaseDefect (c60F32BraidedRepairedEdge a b edge) = a * b := by
  change c60F29PhaseDefect
    (c60WangBiRepairedEdgeGrade edge +
      c60F32NeutralBraidCoefficient a b) = a * b
  rw [grayNeutral_add_eq_native_comp]
  change c60F29PhaseDefect
    ((c60WangBiRepairedEdgeGrade edge).comp
      (c60F32NeutralBraidCoefficient a b)) = a * b
  rw [c60F29PhaseDefect_comp,
    c60F32NeutralBraidCoefficient_defect]
  have h := c60F55RepairedGrade_mem edge
  change (c60WangBiRepairedEdgeGrade edge).phase =
    ((c60WangBiRepairedEdgeGrade edge).charge.2 : ZMod 2) at h
  simp [c60F29PhaseDefect, h]

/-- The genuine monoidal projection fixes the existing REAL original
F55 repaired label on EVERY one of the ninety original physical
C60 square edges, independently of nonneutral grades a and b. -/
theorem c60F32BraidedRepaired_projected_eq
    (a b : ZMod 2) (edge : TruncatedIcosahedralEdge) :
    c60F31ParityCell (c60F32BraidedRepairedEdge a b edge) =
      c60WangBiRepairedEdgeGrade edge := by
  have hf :
      c60F31ParityCell (c60WangBiRepairedEdgeGrade edge) =
        c60WangBiRepairedEdgeGrade edge := by
    apply (c60F31ParityCell_fixed_iff _).2
    have h := c60F55RepairedGrade_mem edge
    change (c60WangBiRepairedEdgeGrade edge).phase =
      ((c60WangBiRepairedEdgeGrade edge).charge.2 : ZMod 2) at h
    simp [c60F29PhaseDefect, h]
  change c60F31ParityCell
    (c60WangBiRepairedEdgeGrade edge +
      c60F32NeutralBraidCoefficient a b) =
      c60WangBiRepairedEdgeGrade edge
  rw [grayNeutral_add_eq_native_comp]
  change c60F31ParityCell
    ((c60WangBiRepairedEdgeGrade edge).comp
      (c60F32NeutralBraidCoefficient a b)) =
      c60WangBiRepairedEdgeGrade edge
  rw [c60F31ParityCell_comp, hf,
    c60F32NeutralBraidCoefficient_projected_zero]
  exact GradedThreeCell.comp_ident _

/-- The real native Gray target's strong monoidal parity operation
is an honest Z-additive group homomorphism on the neutral 3-cell
endomorphisms used by the actual C60 integral chain complex. -/
def c60F32NeutralParityAddHom :
    GradedThreeCell 0 0 →+ GradedThreeCell 0 0 where
  toFun := c60F31ParityCell
  map_zero' := by
    apply GradedThreeCell.ext <;> rfl
  map_add' := by
    intro p q
    change c60F31ParityCell (p + q) =
      c60F31ParityCell p + c60F31ParityCell q
    apply GradedThreeCell.ext
    · change (p + q).charge =
        (c60F31ParityCell p + c60F31ParityCell q).charge
      rw [grayNeutral_add_charge, grayNeutral_add_charge]
      rfl
    · change ((p + q).charge.2 : ZMod 2) =
        (c60F31ParityCell p + c60F31ParityCell q).phase
      rw [grayNeutral_add_charge, grayNeutral_add_phase]
      change ((p.charge.2 + q.charge.2 : ℤ) : ZMod 2) =
        (p.charge.2 : ZMod 2) + (q.charge.2 : ZMod 2)
      rw [Int.cast_add]

/-- The monoidal parity projection commutes with ALL ORIGINAL
C60 signed 5- or 6-edge face 3-cell holonomies, including the
true original integer orientation coefficients (negative edges). -/
theorem c60F32Parity_signedFace_natural
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : TruncatedIcosahedralSeedFace) :
    c60F31ParityCell (c60WangBiSignedGrayFace grade face) =
      c60WangBiSignedGrayFace (fun e => c60F31ParityCell (grade e)) face := by
  have hlist :
      ∀ l : List (TruncatedIcosahedralEdge × ℤ),
        c60F32NeutralParityAddHom
          ((l.map (fun p => p.2 • grade p.1)).sum) =
        (l.map (fun p =>
          p.2 • c60F32NeutralParityAddHom (grade p.1))).sum := by
    intro l
    induction l with
    | nil => simp
    | cons p ps ih =>
        simp only [List.map_cons, List.sum_cons]
        rw [map_add, map_zsmul, ih]
  exact hlist (c60IntegerOrientedFaceBoundary face)

/-- The signed 32-face surface operator also commutes with the
genuine native monoidal parity projection, with no requirement
that arbitrary original edge data were locally flat. -/
theorem c60F32Parity_surface_natural
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60F31ParityCell (c60WangBiSignedGraySurface grade) =
      c60WangBiSignedGraySurface (fun e => c60F31ParityCell (grade e)) := by
  unfold c60WangBiSignedGraySurface
  change c60F32NeutralParityAddHom
      (∑ face : TruncatedIcosahedralSeedFace,
        c60WangBiSignedGrayFace grade face) =
    ∑ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace (fun e => c60F31ParityCell (grade e)) face
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro face _
  exact c60F32Parity_signedFace_natural grade face

/-- Additive local face pasting along original signed C60 edges.
This is a native Gray 3-cell identity, not a false direct
equality between nonparallel raw source 2-cell witnesses. -/
private theorem c60F32SignedList_add
    (grade extra : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (l : List (TruncatedIcosahedralEdge × ℤ)) :
    (l.map (fun p => p.2 • (grade p.1 + extra p.1))).sum =
      (l.map (fun p => p.2 • grade p.1)).sum +
      (l.map (fun p => p.2 • extra p.1)).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons]
      rw [smul_add, ih]
      abel

theorem c60F32SignedGrayFace_add
    (grade extra : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace (fun e => grade e + extra e) face =
      c60WangBiSignedGrayFace grade face +
        c60WangBiSignedGrayFace extra face :=
  c60F32SignedList_add grade extra (c60IntegerOrientedFaceBoundary face)

/-- Signed local face curvature of a CONSTANT genuinely measured
native braid coefficient: its correct integer weight is the
ORIENTED face boundary degree, not simply the face perimeter. -/
theorem c60F32ConstantBraidSignedFace_eq (a b : ZMod 2)
    (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace (fun _ => c60F32NeutralBraidCoefficient a b) face =
      c60F19SignedBoundaryDegree face • c60F32NeutralBraidCoefficient a b :=
  c60F19SignedScalarList_sum
    (c60IntegerOrientedFaceBoundary face) (c60F32NeutralBraidCoefficient a b)

/-- After the original 27-edge canonical repair, adjoining the
nonneutral target Gray braid phase reintroduces local SIGNED
face curvature. Its exact geometric coefficient on all 32 original
faces is their already-verified physical signed boundary degree. -/
theorem c60F32BraidedRepaired_signedFace_complete (a b : ZMod 2)
    (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace (c60F32BraidedRepairedEdge a b) face =
      c60F19ExpectedBoundaryDegree face •
        c60F32NeutralBraidCoefficient a b := by
  change c60WangBiSignedGrayFace
    (fun e => c60WangBiRepairedEdgeGrade e +
      c60F32NeutralBraidCoefficient a b) face = _
  rw [c60F32SignedGrayFace_add,
    c60WangBiRepairedGrade_all32Faces_flat,
    zero_add, c60F32ConstantBraidSignedFace_eq,
    c60F19SignedBoundaryDegree_complete]

/-- The exact signed NORTH pentagon external braid curvature
is a nonzero phase 1 (the geometric degree is -5, not +5).
No original F55 integer charge or Stage-II omega is involved. -/
theorem c60F32OddOddNorthPentagon_phase_one :
    (c60WangBiSignedGrayFace
      (c60F32BraidedRepairedEdge 1 1) (.aroundVertex .north)).phase =
      (1 : ZMod 2) := by
  rw [c60F32BraidedRepaired_signedFace_complete]
  change ((-5 : ℤ) • c60F32NeutralBraidCoefficient 1 1).phase = 1
  calc
    ((-5 : ℤ) • c60F32NeutralBraidCoefficient 1 1).phase =
      (-5 : ℤ) • (c60F32NeutralBraidCoefficient 1 1).phase :=
        grayNeutralPhaseHom.map_zsmul _ _
    _ = (-5 : ZMod 2) := by
      simp [c60F32NeutralBraidCoefficient, zsmul_eq_mul]
    _ = 1 := by decide

/-- Concrete LOCAL DESCENT NO-GO inside the independently braided
neutral-coefficient target, despite the original 27-edge repaired
F55 field having ALL 32 face curvatures zero. -/
theorem c60F32OddOddNorthPentagon_nonflat :
    c60WangBiSignedGrayFace
      (c60F32BraidedRepairedEdge 1 1) (.aroundVertex .north) ≠ 0 := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  rw [c60F32OddOddNorthPentagon_phase_one] at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

/-- The projected higher field is STILL flat on every one of the
real twelve C60 pentagons and twenty hexagons, pointwise.
This is stronger than simply projecting a total degree-two class. -/
theorem c60F32ParityBraidedRepaired_all32_flat
    (a b : ZMod 2) (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace
      (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) face = 0 := by
  have hgrade : (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) =
      c60WangBiRepairedEdgeGrade := by
    funext e
    exact c60F32BraidedRepaired_projected_eq a b e
  rw [hgrade]
  exact c60WangBiRepairedGrade_all32Faces_flat face

/-- The independently braided odd/odd field is NOT the coboundary of
ANY native original C60 vertex potential, because its actual north
pentagon signed curvature is nonzero. This is the precise failure of
H¹ descent; zero global H² is NOT enough. -/
theorem c60F32OddOddBraided_no_vertexDescent :
    ¬ ∃ vertexGauge : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayEdgeCochain (c60F32BraidedRepairedEdge 1 1) =
        vertexGauge.comp c60IntegralBoundaryOne := by
  intro h
  have hall := (c60WangBiGlobalFlatIffVertexDescent
    (c60F32BraidedRepairedEdge 1 1)).2 h
  exact c60F32OddOddNorthPentagon_nonflat (hall (.aroundVertex .north))

/-- But the parity-projected field descends EXACTLY to the
previously CONSTRUCTED original F59-F19 59-edge spanning-tree
vertex gauge. No imaginary repair or unverified existence. -/
theorem c60F32ParityBraidedRepaired_exact_treeDescent
    (a b : ZMod 2) :
    c60F18GrayEdgeCochain
      (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) =
    c60F19TreeVertexGauge.comp c60IntegralBoundaryOne := by
  have hgrade : (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) =
      c60WangBiRepairedEdgeGrade := by
    funext e
    exact c60F32BraidedRepaired_projected_eq a b e
  rw [hgrade]
  exact c60WangBiRepairedGrade_exact_treeDescent

/-- Both the locally nonflat independent-braided ORIGINAL C60
field and its flat parity image have ZERO globally oriented
32-face surface obstruction. This directly separates degree-one
local obstruction from the trivial degree-two global class. -/
theorem c60F32BraidedRepaired_globalH2_zero (a b : ZMod 2) :
    c60WangBiSignedGraySurface (c60F32BraidedRepairedEdge a b) = 0 ∧
    c60WangBiSignedGraySurface
      (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) = 0 := by
  exact ⟨c60WangBiSignedGraySurface_zero _,
    c60WangBiSignedGraySurface_zero _⟩

/-- ACTUAL Mathlib Wang Bi chart natural transformation on the 90
physical original F55 edge squares and all 360 local flags, with
the independently supplied native braid coefficient retained. -/
def c60F32BraidedRepairedWangBiAtlas (a b : ZMod 2)
    (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor :=
  c60WangBiGlobalGradedAtlas side (c60F32BraidedRepairedEdge a b)

/-- Forgetting only independent braiding (not the original integer
charge or F55 phase) recovers IDENTICALLY the previous canonical
27-edge corrected genuine Mathlib Wang Bi natural transformation.
This is a whole-NatTrans equality, not an equality on one Yao code. -/
theorem c60F32ParityWangBiAtlas_eq_repaired
    (a b : ZMod 2) (side : C60DartSideGauge) :
    c60WangBiGlobalGradedAtlas side
      (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) =
      c60WangBiRepairedGlobalAtlas side := by
  have he :
      (fun e => c60F31ParityCell (c60F32BraidedRepairedEdge a b e)) =
      c60WangBiRepairedEdgeGrade := by
    funext e
    exact c60F32BraidedRepaired_projected_eq a b e
  rw [he]
  rfl

/-- The symbolic 王弼 意/time reading is independent of the
braid coefficient: changing chart and transporting an
INDEPENDENTLY supplied temporal interpretation commute at every
physical original C60 flag, not just at the north-pentagon. -/
theorem c60F32WangBiTemporalRead_transport
    {T M : Type*}
    (frame₁ frame₂ : WangBiFrame) (f : frame₁ ⟶ frame₂)
    (reading : WangBiTemporalReading T M)
    (side : C60DartSideGauge)
    (corner : C60ActualSquareCorner) (t : T) :
    c60GaugeTemporalRead frame₂
      (wangBiFrameTransport frame₁ frame₂ f reading) side corner t =
    c60GaugeTemporalRead frame₁ reading side corner t :=
  c60GaugeTemporalRead_natural frame₁ frame₂ f reading side corner t

#print axioms c60F32NeutralBraidCoefficient_components
#print axioms c60F32NeutralBraidCoefficient_defect
#print axioms c60F32NeutralBraidCoefficient_projected_zero
#print axioms c60F32BraidedRepaired_defect
#print axioms c60F32BraidedRepaired_projected_eq
#print axioms c60F32NeutralParityAddHom
#print axioms c60F32Parity_signedFace_natural
#print axioms c60F32Parity_surface_natural
#print axioms c60F32SignedGrayFace_add
#print axioms c60F32ConstantBraidSignedFace_eq
#print axioms c60F32BraidedRepaired_signedFace_complete
#print axioms c60F32OddOddNorthPentagon_phase_one
#print axioms c60F32OddOddNorthPentagon_nonflat
#print axioms c60F32ParityBraidedRepaired_all32_flat
#print axioms c60F32OddOddBraided_no_vertexDescent
#print axioms c60F32ParityBraidedRepaired_exact_treeDescent
#print axioms c60F32BraidedRepaired_globalH2_zero
#print axioms c60F32BraidedRepairedWangBiAtlas
#print axioms c60F32ParityWangBiAtlas_eq_repaired
#print axioms c60F32WangBiTemporalRead_transport

end
end KUOS.DependentOriginationGrayC60BraidedProjectionDescentV5_180
