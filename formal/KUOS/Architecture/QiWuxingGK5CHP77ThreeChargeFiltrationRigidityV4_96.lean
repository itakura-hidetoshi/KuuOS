import KUOS.Architecture.QiWuxingGK5CHP77InverseCompositeUnitOverlapV4_95

/-!
Qi v4.96 — THREE-CHARGE FILTRATION AND LINEAR RIGIDITY.

Previously proven signed integers on the ACTUAL thirteen-constructor
SevenRewrite syntax:
  T = sevenTriangleCharge          (Qi v4.93)
  J = sevenInvolutionCharge        (Qi v4.94)
  K = sevenInverseCompCharge       (Qi v4.95)

This module DOES NOT change any previous EightCell presentations.
It proves the precise filtration of what descends to which CHOSEN
higher-history quotient:
   v4.91 original EightCell:     (T,J,K) all descend;
   v4.93 TriangleEightCell:     (J,K) descend;
   v4.94 InvolutionEightCell:   K descends;
   v4.95 InverseCompEightCell:  NO NONZERO INTEGER LINEAR
      COMBINATION a*T+b*J+c*K descends.

The final no-go is a constructive integer-algebra theorem: three
explicit old-source-index-preserving critical-pair certificates have
charge jumps (1,0,0), (1,1,0), and (0,0,1). Their triangular
coefficient matrix has determinant 1, so preservation on the entire
v4.95 higher grammar forces a=b=c=0. We PROVE this implication
directly in Lean4 from actual Type-valued comparison constructors.
This does not preclude OTHER invariants or assert all raw seven-cell
histories are comparable.

Each intermediate quotient is separate from the full raw seventh
proof syntax and from the authentic GK5CG five-cell Type source.
We also transport a three-stage strictness witness to every actual
P77 terminal raw index, preserving the original source obstruction.

Append-only / tighten-only / same-root. Strict 空 center and
independent Kuu = presentation. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
public root107. Protected validation PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uSix
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- The full signed three-charge vector on the UNQUOTIENTED original
seventh-level history. The tuple is not a quotient equality. -/
def sevenChargeTriple {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ × ℤ × ℤ :=
  (sevenTriangleCharge s, sevenInvolutionCharge s,
    sevenInverseCompCharge s)

/-- The ORIGINAL v4.91 EightCell comparison preserves every
coordinate of the three-charge vector. -/
theorem originalEightCell_preservesTriple {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenChargeTriple s = sevenChargeTriple t := by
  apply Prod.ext
  · exact eightCell_preservesTriangleCharge q
  · apply Prod.ext
    · exact eightCell_preservesInvolutionCharge q
    · exact eightCell_preservesInverseCompCharge q

/-- Consequently the chosen original higher-history quotient can
never identify two seven-cell histories with different 3-charge
values. This is NECESSITY, not a completeness assertion. -/
theorem originalHistoryClass_eq_preservesTriple {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : eightHistoryClass s = eightHistoryClass t) :
    sevenChargeTriple s = sevenChargeTriple t := by
  rcases (eightHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact originalEightCell_preservesTriple q

/-- At the next stage the previously filled triangle changes the
first coordinate, but both OTHER coordinates still descend to the
v4.93 TriangleEightCell quotient. -/
theorem triangleHistoryClass_eq_preservesTail {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : triangleHistoryClass s = triangleHistoryClass t) :
    sevenInvolutionCharge s = sevenInvolutionCharge t ∧
    sevenInverseCompCharge s = sevenInverseCompCharge t := by
  rcases (triangleHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact ⟨triangleEightCell_preservesInvolutionCharge q,
    triangleEightCell_preservesInverseCompCharge q⟩

/-- After the v4.94 double-inversion completion, the THIRD coordinate
still descends to the chosen higher-history quotient. -/
theorem involutionHistoryClass_eq_preservesLast {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : involutionHistoryClass s = involutionHistoryClass t) :
    sevenInverseCompCharge s = sevenInverseCompCharge t := by
  rcases (involutionHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact involutionEightCell_preservesInverseCompCharge q

/-- The three distinct, actually generated higher critical-pair
shapes certify 3 independent coordinate jumps. The first triangle
generator changes ONLY T. -/
theorem sevenChargeTriple_trianglePivot {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    sevenChargeTriple (sevenLeftTriangleDirect c d) = (0, 0, 0) ∧
    sevenChargeTriple (sevenLeftTriangleViaAssoc c d) = (1, 0, 0) := by
  constructor <;>
    simp [sevenChargeTriple, sevenLeftTriangleDirect,
      sevenLeftTriangleViaAssoc, sevenTriangleCharge,
      sevenInvolutionCharge, sevenInverseCompCharge]

/-- The second-stage double-inversion overlap produces jump
(T,J,K) = (1,1,0), so it is independent of the first pivot after
subtracting that prior jump. -/
theorem sevenChargeTriple_involutionPivot {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenChargeTriple (sevenLeftDoubleInverseDirect c) = (0, 0, 0) ∧
    sevenChargeTriple (sevenLeftDoubleInverseVia c) = (1, 1, 0) := by
  constructor <;>
    simp [sevenChargeTriple, sevenLeftDoubleInverseDirect,
      sevenLeftDoubleInverseVia, sevenTriangleCharge,
      sevenInvolutionCharge, sevenInverseCompCharge]

/-- The third-stage inverseComp/unit peak produces independent jump
(T,J,K) = (0,0,1). -/
theorem sevenChargeTriple_inverseCompPivot {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenChargeTriple (sevenInvCompLeftDirect c) = (0, 0, 0) ∧
    sevenChargeTriple (sevenInvCompLeftVia c) = (0, 0, 1) := by
  constructor <;>
    simp [sevenChargeTriple, sevenInvCompLeftDirect,
      sevenInvCompLeftVia, sevenTriangleCharge,
      sevenInvolutionCharge, sevenInverseCompCharge]

/-- Arbitrary integer linear combination of the three certificates.
A priori this is defined on all raw seventh histories, not a
well-defined function on any chosen eighth-history quotient. -/
def sevenLinearCharge (α β γ : ℤ) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  α * sevenTriangleCharge s +
    β * sevenInvolutionCharge s +
    γ * sevenInverseCompCharge s

/-- A concrete unimodular RIGIDITY certificate. If the linear charge
were preserved by ALL v4.95 InverseCompEightCell comparisons, then
its three integer coefficients would all be zero. The proof uses
three ACTUAL Type-valued generators (triangle, double-inversion,
inverseComp) and full raw seventh-level histories. No general
parallel-history comparison is inserted. -/
theorem sevenLinearCharge_universal_iff_zero
    (l r : W) (α β γ : ℤ) :
    (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d},
      InverseCompEightCell W l r s t →
        sevenLinearCharge α β γ s = sevenLinearCharge α β γ t) ↔
      α = 0 ∧ β = 0 ∧ γ = 0 := by
  constructor
  · intro preserve
    let u : PentagonAdjoinedSixCell W l r l l := .refl l
    have hTriangle :
        sevenLinearCharge α β γ (sevenLeftTriangleDirect u u) =
        sevenLinearCharge α β γ (sevenLeftTriangleViaAssoc u u) :=
      preserve
        (.previous (.previous (.leftTriangle u u)))
    have hα : α = 0 := by
      simpa [sevenLinearCharge, sevenLeftTriangleDirect,
        sevenLeftTriangleViaAssoc, sevenTriangleCharge,
        sevenInvolutionCharge, sevenInverseCompCharge]
        using hTriangle.symm
    have hInvolution :
        sevenLinearCharge α β γ (sevenLeftDoubleInverseDirect u) =
        sevenLinearCharge α β γ (sevenLeftDoubleInverseVia u) :=
      preserve (.previous (.leftOverlap u))
    have hαβ : α + β = 0 := by
      simpa [sevenLinearCharge, sevenLeftDoubleInverseDirect,
        sevenLeftDoubleInverseVia, sevenTriangleCharge,
        sevenInvolutionCharge, sevenInverseCompCharge]
        using hInvolution.symm
    have hβ : β = 0 := by
      simpa [hα] using hαβ
    have hInverseComp :
        sevenLinearCharge α β γ (sevenInvCompLeftDirect u) =
        sevenLinearCharge α β γ (sevenInvCompLeftVia u) :=
      preserve (.leftOverlap u)
    have hγ : γ = 0 := by
      simpa [sevenLinearCharge, sevenInvCompLeftDirect,
        sevenInvCompLeftVia, sevenTriangleCharge,
        sevenInvolutionCharge, sevenInverseCompCharge]
        using hInverseComp.symm
    exact ⟨hα, hβ, hγ⟩
  · rintro ⟨rfl, rfl, rfl⟩
    intro w z c d s t q
    simp [sevenLinearCharge]

/-- The purely integer-algebra core: the three observed charge
differences (1,0,0), (1,1,0), (0,0,1) annihilate no nonzero linear
functional. This is the unimodular obstruction matrix certificate. -/
theorem threeChargePivot_linearIndependent (α β γ : ℤ)
    (hTriangle : α = 0)
    (hInvolution : α + β = 0)
    (hInverseComp : γ = 0) :
    α = 0 ∧ β = 0 ∧ γ = 0 := by
  refine ⟨hTriangle, ?_, hInverseComp⟩
  simpa [hTriangle] using hInvolution

/-- The three successive new eighth-level presentations are
STRICTLY nested on the SAME free seven-cell history grammar.
Each new quotient equates one new critical pair that the prior
chosen quotient distinguishes. -/
def ThreeStageStrict (c : PentagonAdjoinedSixCell W long short long short) : Prop :=
  ((triangleHistoryClass
      (sevenLeftTriangleDirect c (.symm c)) =
    triangleHistoryClass
      (sevenLeftTriangleViaAssoc c (.symm c))) ∧
    eightHistoryClass (sevenLeftTriangleDirect c (.symm c)) ≠
      eightHistoryClass (sevenLeftTriangleViaAssoc c (.symm c))) ∧
  ((involutionHistoryClass (sevenLeftDoubleInverseDirect c) =
    involutionHistoryClass (sevenLeftDoubleInverseVia c)) ∧
    triangleHistoryClass (sevenLeftDoubleInverseDirect c) ≠
      triangleHistoryClass (sevenLeftDoubleInverseVia c)) ∧
  ((inverseCompHistoryClass (sevenInvCompLeftDirect c) =
    inverseCompHistoryClass (sevenInvCompLeftVia c)) ∧
    involutionHistoryClass (sevenInvCompLeftDirect c) ≠
      involutionHistoryClass (sevenInvCompLeftVia c))

/-- Every actual sixth-level forward generator provides a witness
for all three strict higher-history quotient transitions. -/
theorem threeStageStrict_forAny
    (c : PentagonAdjoinedSixCell W long short long short) :
    ThreeStageStrict c :=
  ⟨triangleHistoryClass_strictlyNew c (.symm c),
   involutionHistoryClass_strictlyNew c,
   inverseCompHistoryClass_strictlyNew c⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77ThreeChargeFiltration
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ family₄ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable {s₄ : State f g h k family₄}
variable (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
variable (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
variable (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃)
variable (D₄ : DirectNormalBracketTree f g h k family₃ s₃ family₄ s₄)

/-- For EVERY genuine P77 terminal raw index, the ORIGINAL GK5CG
five-cell Type endpoints supply a concrete adjoined six-cell
generator exhibiting all three successive strict higher quotient
extensions. The old strict source-equality no-go persists alongside
the three new positive higher-history quotient comparisons. -/
theorem pentagonActualThreeStageStrictWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      PentagonAdjoinedSixCell.ThreeStageStrict c ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    PentagonAdjoinedSixCell.threeStageStrict_forAny _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

/-- The full third-stage comparison grammar admits NO universally
conserved nontrivial linear combination of the three charges even
on the ORIGINAL conservative GK5CG five-cell endpoint Type.
This is a claim about new seven/eight-cell PRESENTATIONS only. -/
theorem pentagonActualThreeCharge_linearRigidity
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    (α β γ : ℤ)
    (preserve : ∀ {w z : pentagonFinalConservativeLoop f g h k i}
      {c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z}
      {s t : PentagonAdjoinedSixCell.SevenRewrite
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) c d},
      PentagonAdjoinedSixCell.InverseCompEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) s t →
      PentagonAdjoinedSixCell.sevenLinearCharge α β γ s =
        PentagonAdjoinedSixCell.sevenLinearCharge α β γ t) :
    α = 0 ∧ β = 0 ∧ γ = 0 :=
  (PentagonAdjoinedSixCell.sevenLinearCharge_universal_iff_zero
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    α β γ).1 preserve

#print axioms PentagonAdjoinedSixCell.sevenChargeTriple
#print axioms PentagonAdjoinedSixCell.originalEightCell_preservesTriple
#print axioms PentagonAdjoinedSixCell.originalHistoryClass_eq_preservesTriple
#print axioms PentagonAdjoinedSixCell.triangleHistoryClass_eq_preservesTail
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass_eq_preservesLast
#print axioms PentagonAdjoinedSixCell.sevenChargeTriple_trianglePivot
#print axioms PentagonAdjoinedSixCell.sevenChargeTriple_involutionPivot
#print axioms PentagonAdjoinedSixCell.sevenChargeTriple_inverseCompPivot
#print axioms PentagonAdjoinedSixCell.sevenLinearCharge
#print axioms PentagonAdjoinedSixCell.sevenLinearCharge_universal_iff_zero
#print axioms PentagonAdjoinedSixCell.threeChargePivot_linearIndependent
#print axioms PentagonAdjoinedSixCell.ThreeStageStrict
#print axioms PentagonAdjoinedSixCell.threeStageStrict_forAny
#print axioms pentagonActualThreeStageStrictWithSourceObstruction
#print axioms pentagonActualThreeCharge_linearRigidity

end ActualOriginalP77ThreeChargeFiltration
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
