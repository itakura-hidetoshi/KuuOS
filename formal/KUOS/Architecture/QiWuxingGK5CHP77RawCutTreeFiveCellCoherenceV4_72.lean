import KUOS.Architecture.QiWuxingGK5CHP77CompositeFiveCellNaturalityV4_71
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.72 — GENUINE ORIGINAL P77 RAW CUT-TREE FIVE-CELL COHERENCE.

The source raw Type now remembers EVERY cut-tree parenthesization, including
all tuple indices and actual original F55/P77 four-cell composites.
A recursively constructed GK5CG conservative five-cell compares this
parenthesized raw value to its flattened right-associated normal form.
Every constructor is an original five-cell vertical congruence, associator
or unit; no new pentagonator, equality of raw proofs or external axiom.

The two-sided comparison between the raw tree family and the canonical
full-index composite family is derived, not postulated. Arbitrary finite
original recuts and full segmentwise presentation comparisons therefore
supply REAL Type-valued five-cells among raw tree composites. These
comparisons preserve genuine source gluing, exact typed Quiver.Path,
source-certified P77 partial Homs and factorwise obstruction where the
original witness hypotheses hold.

The original five-cell history remains a Type value: only its witness
transport / conservative quotient is compared. No claim of history equality,
global target fullness, charge-only recovery, unconditional factor splitting,
new source reverse edge, sheaf descent, new pentagonator or Gray restoration.

Append-only same-root; strict 空 central, independent Kuu is a presentation.
Original F55/P77/P94A, physical C60 and north C60 retain authority.
Public root107; protected PR #1558 validation-only Draft/open/unmerged.
No new axioms, sorry, admit or native_decide. Fixed Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

universe uD vD uE vE
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



/-- Every actual pair of chain indices gives one index of their typed append.
The inverse makes the intermediate source cut explicit. -/
def fivefoldP77RawPatchChainAppendIndexEquiv
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    (FivefoldP77RawPatchChainIndex f g h k left ×
      FivefoldP77RawPatchChainIndex f g h k right) ≃
    FivefoldP77RawPatchChainIndex f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) := by
  induction left with
  | nil vertex =>
      refine {
        toFun := fun w => w.2
        invFun := fun w => (PUnit.unit, w)
        left_inv := ?_
        right_inv := ?_ }
      · rintro ⟨w, rest⟩
        cases w
        rfl
      · intro w
        rfl
  | cons block tail ih =>
      exact (Equiv.prodAssoc _ _ _).trans
        (Equiv.prodCongr (Equiv.refl _) (ih right))

/-- Reassociate the ACTUAL raw P77 four-proof composite using genuine
original GK5CG 5-cells. Empty-left requires a real vertical left-unit cell. -/
def fivefoldP77RawPatchChainAppendRawFiveCell
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    ∀ (i : FivefoldP77RawPatchChainIndex f g h k left)
      (j : FivefoldP77RawPatchChainIndex f g h k right),
      NativeGK5CGConservativeFiveCell first last
        (fivefoldP77RawPatchChainRaw f g h k
          (fivefoldP77RawPatchChainAppend f g h k left right)
          (fivefoldP77RawPatchChainAppendIndexEquiv f g h k left right (i, j)))
        (.trans
          (fivefoldP77RawPatchChainRaw f g h k left i)
          (fivefoldP77RawPatchChainRaw f g h k right j)) := by
  induction left with
  | nil vertex =>
      intro _ j
      change NativeGK5CGConservativeFiveCell first last
        (fivefoldP77RawPatchChainRaw f g h k right j)
        (.trans
          (.refl (fivefoldF55OriginalAt f g h k vertex.phase))
          (fivefoldP77RawPatchChainRaw f g h k right j))
      exact (NativeGK5CGConservativeFiveCell.verticalLeftUnit
        (fivefoldP77RawPatchChainRaw f g h k right j)).symm
  | cons block tail ih =>
      rintro ⟨i, rest⟩ j
      change NativeGK5CGConservativeFiveCell first last
        (.trans (block.raw i)
          (fivefoldP77RawPatchChainRaw f g h k
            (fivefoldP77RawPatchChainAppend f g h k tail right)
            (fivefoldP77RawPatchChainAppendIndexEquiv f g h k tail right (rest, j))))
        (.trans
          (.trans (block.raw i) (fivefoldP77RawPatchChainRaw f g h k tail rest))
          (fivefoldP77RawPatchChainRaw f g h k right j))
      exact .trans
        (.verticalRight (block.raw i) (ih right rest j))
        (.symm (.verticalAssoc
          (block.raw i)
          (fivefoldP77RawPatchChainRaw f g h k tail rest)
          (fivefoldP77RawPatchChainRaw f g h k right j)))

/-- Original raw index tuples with the actual binary cut-tree brackets. -/
def FivefoldP77RawPatchTreeIndex
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) : Type :=
  match tree with
  | .leaf chain => FivefoldP77RawPatchChainIndex f g h k chain
  | .node left right =>
      FivefoldP77RawPatchTreeIndex f g h k left ×
        FivefoldP77RawPatchTreeIndex f g h k right

/-- Explicit reversible reindexing of all raw tuple indices under flattening. -/
def fivefoldP77RawPatchTreeIndexNormalizeEquiv
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchTreeIndex f g h k tree ≃
      FivefoldP77RawPatchChainIndex f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree) := by
  induction tree with
  | leaf chain => exact Equiv.refl _
  | node left right ihLeft ihRight =>
      exact (Equiv.prodCongr ihLeft ihRight).trans
        (fivefoldP77RawPatchChainAppendIndexEquiv f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k left)
          (fivefoldP77RawPatchTreeFlatten f g h k right))

/-- Parenthesized composition of genuine ORIGINAL raw P77 four-cell values. -/
def fivefoldP77RawPatchTreeRaw
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchTreeIndex f g h k tree →
      FivefoldP77LocalRaw f g h k u v := by
  induction tree with
  | leaf chain =>
      exact fivefoldP77RawPatchChainRaw f g h k chain
  | node left right ihLeft ihRight =>
      intro indices
      exact .trans (ihLeft indices.1) (ihRight indices.2)

/-- The original source-side five-cell witnesses that EVERY parenthesized
raw value is related to its canonical flattened original raw value. -/
def fivefoldP77RawPatchTreeRawNormalizeFiveCell
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    ∀ indices : FivefoldP77RawPatchTreeIndex f g h k tree,
      NativeGK5CGConservativeFiveCell first last
        (fivefoldP77RawPatchTreeRaw f g h k tree indices)
        (fivefoldP77RawPatchChainRaw f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k tree)
          (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k tree indices)) := by
  induction tree with
  | leaf chain =>
      intro indices
      exact .refl _
  | node left right ihLeft ihRight =>
      rintro ⟨i, j⟩
      change NativeGK5CGConservativeFiveCell first last
        (.trans (fivefoldP77RawPatchTreeRaw f g h k left i)
          (fivefoldP77RawPatchTreeRaw f g h k right j))
        (fivefoldP77RawPatchChainRaw f g h k
          (fivefoldP77RawPatchChainAppend f g h k
            (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right))
          (fivefoldP77RawPatchChainAppendIndexEquiv f g h k
            (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right)
            (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i,
              fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k right j)))
      exact .trans
        (.verticalLeft (ihLeft i) (fivefoldP77RawPatchTreeRaw f g h k right j))
        (.trans
          (.verticalRight
            (fivefoldP77RawPatchChainRaw f g h k
              (fivefoldP77RawPatchTreeFlatten f g h k left)
              (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i))
            (ihRight j))
          ((fivefoldP77RawPatchChainAppendRawFiveCell f g h k
            (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right)
            (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i)
            (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k right j)).symm))

/-- All cut-tree raw tuple indices are inhabited without choosing a factor. -/
theorem fivefoldP77RawPatchTreeIndex_nonempty
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    Nonempty (FivefoldP77RawPatchTreeIndex f g h k tree) := by
  induction tree with
  | leaf chain =>
      exact fivefoldP77RawPatchChainIndex_nonempty f g h k chain
  | node left right ihLeft ihRight =>
      obtain ⟨i⟩ := ihLeft
      obtain ⟨j⟩ := ihRight
      exact ⟨(i, j)⟩

/-- A distinct full-index coarse patch family for each raw parenthesization. -/
def fivefoldP77RawPatchTreeRawBlock
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchBlock f g h k u v where
  Index := FivefoldP77RawPatchTreeIndex f g h k tree
  nonempty := fivefoldP77RawPatchTreeIndex_nonempty f g h k tree
  raw := fivefoldP77RawPatchTreeRaw f g h k tree

/-- Normalize parenthesized RAW FOUR-CELL FAMILIES by ACTUAL original
GK5CG five-cells, not by source-path uniqueness or numerical charge. -/
def fivefoldP77RawPatchTreeRawNormalizeComparison
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k tree)
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) where
  forwardIndex := (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k tree).symm
  forwardCell := by
    intro j
    have cell := fivefoldP77RawPatchTreeRawNormalizeFiveCell f g h k tree
      ((fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k tree).symm j)
    simpa only [Equiv.apply_symm_apply] using cell
  backwardIndex := fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k tree
  backwardCell := fun i =>
    (fivefoldP77RawPatchTreeRawNormalizeFiveCell f g h k tree i).symm

/-- Genuine raw-tree families of ANY two parenthesizations have original
five-cell comparison once the flattened segment presentations are compared. -/
def fivefoldP77RawPatchTreeRawComparison
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target)) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target) :=
  fivefoldP77RawPatchBlockComparisonTrans f g h k
    (fivefoldP77RawPatchTreeRawNormalizeComparison f g h k source)
    (fivefoldP77RawPatchBlockComparisonTrans f g h k
      (fivefoldP77CompositeBlockComparison f g h k comparison)
      (fivefoldP77RawPatchBlockComparisonSymm f g h k
        (fivefoldP77RawPatchTreeRawNormalizeComparison f g h k target)))

/-- Reflexive actual five-cell data for every original finite raw patch chain. -/
def fivefoldP77RawPatchChainComparisonRefl
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    FivefoldP77RawPatchChainComparison f g h k chain chain := by
  induction chain with
  | nil vertex => exact .nil vertex
  | cons block tail ih =>
      exact .cons (fivefoldP77RawPatchBlockComparisonRefl f g h k block) ih

/-- A genuine exact raw-chain equality gives a typed identity comparison. -/
def fivefoldP77RawPatchChainComparisonOfEq
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target) :
    FivefoldP77RawPatchChainComparison f g h k source target := by
  cases e
  exact fivefoldP77RawPatchChainComparisonRefl f g h k source

/-- Every finite recut therefore constructs actual GK5CG five-cells between
the source and target PARENTHESIZED raw composite families. -/
def fivefoldP77RawPatchCutRouteRawComparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target) :=
  fivefoldP77RawPatchTreeRawComparison f g h k source target
    (fivefoldP77RawPatchChainComparisonOfEq f g h k
      (fivefoldP77RawPatchCutRoute_flatten f g h k route))

/-- The old certified original tree witness glues to EVERY original
parenthesized raw composite using genuine normalization five-cells. -/
def fivefoldP77RawPatchTreeRawGlue
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k tree) :
    FivefoldP77RawPatchBlockWitness f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k tree) :=
  (fivefoldP77RawPatchBlockComparisonEquiv f g h k
    (fivefoldP77RawPatchTreeRawNormalizeComparison f g h k tree)).symm
      (fivefoldP77RawPatchCompositeGlue f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness))

/-- Real gluing retains the original tree-composed typed source path exactly. -/
theorem fivefoldP77RawPatchTreeRawGlue_val
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k tree) :
    (fivefoldP77RawPatchTreeRawGlue f g h k tree witness).val =
      fivefoldP77RawPatchTreePath f g h k tree witness := by
  change fivefoldP77RawPatchChainPath f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree)
      (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness) =
    fivefoldP77RawPatchTreePath f g h k tree witness
  exact (fivefoldP77RawPatchTreePath_normalize f g h k tree witness).symm

/-- The raw tree comparison and actual witness presentation change
commute, even when source/target raw parenthesizations differ. -/
theorem fivefoldP77RawPatchTreeRawGlue_presentation_natural
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target))
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchTreeRawComparison f g h k source target comparison)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness) =
      fivefoldP77RawPatchTreeRawGlue f g h k target
        (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
          comparison witness) := by
  apply Subtype.ext
  calc
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchTreeRawComparison f g h k source target comparison)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness)).val =
      (fivefoldP77RawPatchTreeRawGlue f g h k source witness).val :=
        fivefoldP77RawPatchBlockComparisonEquiv_val f g h k _ _
    _ = fivefoldP77RawPatchTreePath f g h k source witness :=
      fivefoldP77RawPatchTreeRawGlue_val f g h k source witness
    _ = fivefoldP77RawPatchTreePath f g h k target
          (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
            comparison witness) :=
        (fivefoldP77RawPatchTreePresentation_path f g h k
          source target comparison witness).symm
    _ = (fivefoldP77RawPatchTreeRawGlue f g h k target
          (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
            comparison witness)).val :=
        (fivefoldP77RawPatchTreeRawGlue_val f g h k target _).symm

/-- All original recuts transport real tree raw gluing identically on source paths. -/
theorem fivefoldP77RawPatchTreeRawGlue_recut_natural
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchCutRouteRawComparison f g h k route)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness) =
      fivefoldP77RawPatchTreeRawGlue f g h k target
        (fivefoldP77RawPatchCutRouteEquiv f g h k route witness) := by
  apply Subtype.ext
  calc
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchCutRouteRawComparison f g h k route)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness)).val =
      (fivefoldP77RawPatchTreeRawGlue f g h k source witness).val :=
        fivefoldP77RawPatchBlockComparisonEquiv_val f g h k _ _
    _ = fivefoldP77RawPatchTreePath f g h k source witness :=
      fivefoldP77RawPatchTreeRawGlue_val f g h k source witness
    _ = fivefoldP77RawPatchTreePath f g h k target
          (fivefoldP77RawPatchCutRouteEquiv f g h k route witness) :=
        (fivefoldP77RawPatchCutRoute_path f g h k route witness).symm
    _ = (fivefoldP77RawPatchTreeRawGlue f g h k target
          (fivefoldP77RawPatchCutRouteEquiv f g h k route witness)).val :=
        (fivefoldP77RawPatchTreeRawGlue_val f g h k target _).symm

/-- All source history variants induce the same map on original witness Types
when endpoints agree; the actual raw five-cell histories are NOT identified. -/
theorem fivefoldP77RawPatchTreeRawComparison_equiv_independent
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (a b : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target)) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
      (fivefoldP77RawPatchTreeRawComparison f g h k source target a) =
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
      (fivefoldP77RawPatchTreeRawComparison f g h k source target b) := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k
    (fivefoldP77RawPatchTreeRawBlock f g h k target)
  exact Subsingleton.elim _ _

/-- Genuine source-factor obstruction survives every permitted recut,
rather than being repaired by choosing a different raw parenthesization. -/
theorem fivefoldP77RawPatchTreeRaw_obstruction_recut
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (hmissing : fivefoldP77RawPatchTreeObstructed f g h k source) :
    ¬ Nonempty (FivefoldP77RawPatchTreeWitness f g h k target) :=
  fivefoldP77RawPatchCutRoute_obstruction f g h k route hmissing

#print axioms fivefoldP77RawPatchChainAppendIndexEquiv
#print axioms fivefoldP77RawPatchChainAppendRawFiveCell
#print axioms FivefoldP77RawPatchTreeIndex
#print axioms fivefoldP77RawPatchTreeIndexNormalizeEquiv
#print axioms fivefoldP77RawPatchTreeRaw
#print axioms fivefoldP77RawPatchTreeRawNormalizeFiveCell
#print axioms fivefoldP77RawPatchTreeIndex_nonempty
#print axioms fivefoldP77RawPatchTreeRawBlock
#print axioms fivefoldP77RawPatchTreeRawNormalizeComparison
#print axioms fivefoldP77RawPatchTreeRawComparison
#print axioms fivefoldP77RawPatchChainComparisonRefl
#print axioms fivefoldP77RawPatchChainComparisonOfEq
#print axioms fivefoldP77RawPatchCutRouteRawComparison
#print axioms fivefoldP77RawPatchTreeRawGlue
#print axioms fivefoldP77RawPatchTreeRawGlue_val
#print axioms fivefoldP77RawPatchTreeRawGlue_presentation_natural
#print axioms fivefoldP77RawPatchTreeRawGlue_recut_natural
#print axioms fivefoldP77RawPatchTreeRawComparison_equiv_independent
#print axioms fivefoldP77RawPatchTreeRaw_obstruction_recut

end
end KUOS.Architecture.WuxingPentagonUnified
