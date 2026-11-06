import KUOS.Architecture.QiWuxingGK5CHP77TypedSevenRewriteHistoryV4_89

/-!
Qi v4.90 — CONSTRUCTIVE SEVENTH-LEVEL REWRITE NORMALIZATION
AND LOCAL COMPLETENESS FOR DISTINCT ORIGINAL FIVE-CELL ENDPOINTS.

The v4.89 NEW Type-valued SevenRewrite has 13 explicitly generated
local rules, not an arbitrary equality-of-degree constructor.
We now PROVE that when the two distinguished ORIGINAL GK5CG
five-cell values are distinct (v4.85), every NEW raw six-cell
word carries an actual, history-preserving seventh-level rewrite
to one of the THREE v4.88 endpoint normal words.

This constructs the missing converse from v4.89:
parallel NEW raw six-cell proof words have explicit seven-cell
comparisons and the chosen degree quotient is complete for
THESE seven-cell histories. The proof recursively uses actual
local congruence, inverse and composition rules, and uniqueness
of endpoint normals. At no point does it identify raw six-cell
syntax, old five-cell values, or add a source GK5CG six/seven-cell.

The long=short winding obstruction of v4.89 is preserved: no
global unconditioned completeness statement is made.
Append-only / tighten-only / same-root, strict 空 center,
independent Kuu is presentation. Lean v4.30.0-rc2;
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
public roots107, protected #1558 stays Draft/open/unmerged.
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

/-- The new seven-cell trace explicitly normalizes inversion of one
of the THREE original raw six-cell normal words. No quotient is used. -/
theorem sevenInverseNormal (l r : W) {w z : W}
    {c : PentagonAdjoinedSixCell W l r w z}
    (hn : EndpointNormal W l r c) :
    ∃ d : PentagonAdjoinedSixCell W l r z w,
      EndpointNormal W l r d ∧
      Nonempty (SevenRewrite W l r (.symm c) d) := by
  cases hn with
  | identity w =>
      exact ⟨.refl w, .identity w, ⟨.inverseId w⟩⟩
  | forward =>
      exact ⟨.symm (.pentagon), .backward, ⟨.refl _⟩⟩
  | backward =>
      exact ⟨.pentagon, .forward, ⟨.doubleInverse (.pentagon)⟩⟩

/-- The only normal-form compositions are unit steps and the two
crossing cancellations. Cases with twice-forward/twice-backward
are impossible when the designated endpoints differ. -/
theorem sevenComposeNormals (l r : W) (hNe : l ≠ r)
    {w x z : W}
    {c : PentagonAdjoinedSixCell W l r w x}
    {d : PentagonAdjoinedSixCell W l r x z}
    (hc : EndpointNormal W l r c)
    (hd : EndpointNormal W l r d) :
    ∃ e : PentagonAdjoinedSixCell W l r w z,
      EndpointNormal W l r e ∧
      Nonempty (SevenRewrite W l r (.trans c d) e) := by
  cases hc with
  | identity w =>
      exact ⟨d, hd, ⟨.leftUnit d⟩⟩
  | forward =>
      cases hd with
      | identity w =>
          exact ⟨.pentagon, .forward, ⟨.rightUnit (.pentagon)⟩⟩
      | forward =>
          exact (hNe rfl).elim
      | backward =>
          exact ⟨.refl l, .identity l, ⟨.inverseRight (.pentagon)⟩⟩
  | backward =>
      cases hd with
      | identity w =>
          exact ⟨.symm (.pentagon), .backward,
            ⟨.rightUnit (.symm (.pentagon))⟩⟩
      | forward =>
          exact ⟨.refl r, .identity r, ⟨.inverseLeft (.pentagon)⟩⟩
      | backward =>
          exact (hNe rfl).elim

/-- The three raw normal forms are STRICTLY unique for each pair
of endpoints when l≠r; this is a theorem about the NORMAL words,
not an identification of arbitrary raw proof words. -/
theorem sevenEndpointNormal_unique (l r : W) (hNe : l ≠ r)
    {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (hc : EndpointNormal W l r c)
    (hd : EndpointNormal W l r d) :
    c = d := by
  have hdeg : degree c = degree d :=
    allParallel_degreeCoherent l r hNe c d
  cases hc <;> cases hd <;> simp_all [degree]

/-- The core constructive normalization: every free six-cell raw
word comes with a Type-valued chain of SEVEN-cell rewrite steps
to a three-shape endpoint normal form. The witnesses are obtained
by structural induction and are not fabricated from quotient Eq. -/
theorem sevenRaw_existsNormalTrace (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    ∃ d : PentagonAdjoinedSixCell W l r w z,
      EndpointNormal W l r d ∧
      Nonempty (SevenRewrite W l r c d) := by
  induction c with
  | refl w =>
      exact ⟨.refl w, .identity w, ⟨.refl (.refl w)⟩⟩
  | pentagon =>
      exact ⟨.pentagon, .forward, ⟨.refl (.pentagon)⟩⟩
  | symm c ih =>
      rcases ih with ⟨n, hn, ⟨hcn⟩⟩
      rcases sevenInverseNormal l r hn with ⟨n', hn', ⟨hInv⟩⟩
      exact ⟨n', hn', ⟨.trans (.congrInv hcn) hInv⟩⟩
  | trans c d ihc ihd =>
      rcases ihc with ⟨cN, hcN, ⟨hc⟩⟩
      rcases ihd with ⟨dN, hdN, ⟨hd⟩⟩
      rcases sevenComposeNormals l r hNe hcN hdN with
        ⟨n, hn, ⟨hComp⟩⟩
      exact ⟨n, hn, ⟨.trans (.congrComp hc hd) hComp⟩⟩

/-- Normalize to exactly the SELECTED v4.88 three-shape normal
representative, with an explicit seventh-level derivation. -/
theorem sevenRaw_toSelectedNormal (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    Nonempty (SevenRewrite W l r c
      (selectEndpointNormal l r hNe c)) := by
  rcases sevenRaw_existsNormalTrace l r hNe c with ⟨d, hd, ⟨hcd⟩⟩
  have hEq : d = selectEndpointNormal l r hNe c :=
    sevenEndpointNormal_unique l r hNe hd
      (selectEndpointNormal_isNormal l r hNe c)
  rw [← hEq]
  exact ⟨hcd⟩

/-- All parallel raw six-cell words admit ACTUAL TYPE-valued
seven-cell comparison histories, not merely a quotient equality. -/
theorem sevenRaw_allParallel_existsRewrite (l r : W) (hNe : l ≠ r)
    {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Nonempty (SevenRewrite W l r c d) := by
  rcases sevenRaw_existsNormalTrace l r hNe c with
    ⟨cn, hcn, ⟨hcnTrace⟩⟩
  rcases sevenRaw_existsNormalTrace l r hNe d with
    ⟨dn, hdn, ⟨hdnTrace⟩⟩
  have hEq : cn = dn := sevenEndpointNormal_unique l r hNe hcn hdn
  cases hEq
  exact ⟨.trans hcnTrace (.symm hdnTrace)⟩

/-- Local soundness+completeness for signed-degree equivalence,
PROVED using the 13 existing structural rewrite constructors.
Distinctness is essential for this derivation. -/
theorem sevenRewrite_complete_iff_degree (l r : W) (hNe : l ≠ r)
    {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Nonempty (SevenRewrite W l r c d) ↔ degree c = degree d := by
  constructor
  · rintro ⟨e⟩
    exact sevenRewrite_degreeSound e
  · intro _
    exact sevenRaw_allParallel_existsRewrite l r hNe c d

/-- The CHOSEN quotient equality is now equivalent to the existence
of a HISTORY-PRESERVING seventh-level local rewrite, at distinct
endpoints. No strict raw Eq is asserted. -/
theorem sevenRewrite_complete_iff_quotient (l r : W) (hNe : l ≠ r)
    {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Nonempty (SevenRewrite W l r c d) ↔ homMk c = homMk d := by
  rw [sevenRewrite_complete_iff_degree l r hNe c d]
  exact (homDegree_eq_iff l r (homMk c) (homMk d)).symm

/-- Original word equality, seventh-level comparison, and chosen
quotient equality retain their three distinct mathematical types. -/
theorem sevenRaw_equalityHistoryQuotient (l r : W) (hNe : l ≠ r)
    {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    (c = d → Nonempty (SevenRewrite W l r c d)) ∧
    (Nonempty (SevenRewrite W l r c d) → homMk c = homMk d) ∧
    (homMk c = homMk d → Nonempty (SevenRewrite W l r c d)) := by
  constructor
  · intro hcd
    exact ⟨sevenRewrite_ofEq hcd⟩
  constructor
  · rintro ⟨h⟩
    exact sevenRewrite_quotientSound h
  · exact (sevenRewrite_complete_iff_quotient l r hNe c d).2

/-- The converse raw-Eq return remains impossible, even after
full constructive local completeness in the NEW seven-cell grammar. -/
theorem sevenComplete_stillNoStrictReturn (l r : W) (hNe : l ≠ r) :
    (∀ {w z : W} (c d : PentagonAdjoinedSixCell W l r w z),
      Nonempty (SevenRewrite W l r c d)) ∧
    ¬ (∀ (w z : W)
        (c d : PentagonAdjoinedSixCell W l r w z),
        SevenRewrite W l r c d → c = d) := by
  refine ⟨?_, sevenRewrite_noStrictInterpreter l r⟩
  intro w z c d
  exact sevenRaw_allParallel_existsRewrite l r hNe c d

end PentagonAdjoinedSixCell

section ActualOriginalP77SevenRewriteCompleteness
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

/-- For every REAL original P77 terminal raw index, any TWO NEW six-cell
words connecting the SAME ORIGINAL five-cell Type endpoints carry
an actual seventh-level rewrite history. -/
theorem pentagonActualSevenRewrite_allParallelComplete
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z) :
    Nonempty (PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) c d) :=
  PentagonAdjoinedSixCell.sevenRaw_allParallel_existsRewrite
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) c d

/-- Exact equivalence of v4.87/4.88 quotient equality and explicit
v4.89 seventh-level rewrite history, FOR ALL original P77 raw indices. -/
theorem pentagonActualSevenRewrite_completeIffQuotient
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z) :
    Nonempty (PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) c d) ↔
    PentagonAdjoinedSixCell.homMk c =
      PentagonAdjoinedSixCell.homMk d :=
  PentagonAdjoinedSixCell.sevenRewrite_complete_iff_quotient
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) c d

/-- New local completeness + existing old equality-descent no-go:
proving a NEW seven-cell comparison does not identify old GK5CG
five-cell Type values. -/
theorem pentagonActualSevenRewrite_completeWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (∀ {w z : pentagonFinalConservativeLoop f g h k i}
      (c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z),
      Nonempty (PentagonAdjoinedSixCell.SevenRewrite
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) c d)) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨?_, pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩
  intro w z c d
  exact pentagonActualSevenRewrite_allParallelComplete f g h k A B C D₄ i c d

#print axioms PentagonAdjoinedSixCell.sevenInverseNormal
#print axioms PentagonAdjoinedSixCell.sevenComposeNormals
#print axioms PentagonAdjoinedSixCell.sevenEndpointNormal_unique
#print axioms PentagonAdjoinedSixCell.sevenRaw_existsNormalTrace
#print axioms PentagonAdjoinedSixCell.sevenRaw_toSelectedNormal
#print axioms PentagonAdjoinedSixCell.sevenRaw_allParallel_existsRewrite
#print axioms PentagonAdjoinedSixCell.sevenRewrite_complete_iff_degree
#print axioms PentagonAdjoinedSixCell.sevenRewrite_complete_iff_quotient
#print axioms PentagonAdjoinedSixCell.sevenRaw_equalityHistoryQuotient
#print axioms PentagonAdjoinedSixCell.sevenComplete_stillNoStrictReturn
#print axioms pentagonActualSevenRewrite_allParallelComplete
#print axioms pentagonActualSevenRewrite_completeIffQuotient
#print axioms pentagonActualSevenRewrite_completeWithSourceObstruction

end ActualOriginalP77SevenRewriteCompleteness
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
