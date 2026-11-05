import KUOS.Architecture.QiWuxingGK5CHP77FiniteCutTreeNormalCoherenceV4_68
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.69 — ORIGINAL P77 PATCH PRESENTATION AND NORMALIZATION NATURALITY.

Different original raw patch families may have different index Types and
different raw four-cell representatives. Comparison data retain explicit
index maps in BOTH directions and actual original GK5CG Type-valued
conservative five-cells at every chosen comparison. They do not identify
the raw families or their proof histories. A surjective family refinement
with genuine five-cells supplies such data; coverage is an explicit premise.

The induced block Equiv keeps exactly the same typed source path. Dependent
finite-chain comparisons keep every actual segment boundary and induce
product Equivs of the original witness Types. Conjugation by v4.68's actual
normalization Equivs extends this to arbitrary cut-tree parenthesizations.
Normalization commutes with the comparison on genuine Type-valued witnesses.

Arbitrary finite histories mix original recuts, certified presentation
changes, inverses, composition and left/right contexts. Their ACTUAL induced
Equivs are coherent, preserve original source paths, source-certified P77
partial Homs and exact recovery, and preserve the factorwise obstruction.
Only induced witness maps are identified, never all raw five-cell histories.

Refinement changes a family at existing segment boundaries; no new source
vertex or arbitrary target factorization is inferred. Compatibility remains
necessary and sufficient. No charge substitute, fabricated reverse source
edge, global target fullness, general sheaf claim, pentagonator or Gray.
Original F55/P77/P94A, physical C60 and north C60 CRT remain distinct.

Append-only same-root; strict 空 central, independent Kuu a presentation.
Public root107; protected validation-only #1558 Draft/open/unmerged.
No new axioms, sorry, admit or native_decide. Lean v4.30.0-rc2;
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

/-- Two-sided coverage by CHOSEN genuine five-cell values. Index maps need
not be inverse, and neither raw-family equality nor compatibility is assumed. -/
structure FivefoldP77RawPatchBlockComparison
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchBlock f g h k u v) where
  forwardIndex : target.Index → source.Index
  forwardCell : ∀ j : target.Index,
    NativeGK5CGConservativeFiveCell first last
      (source.raw (forwardIndex j)) (target.raw j)
  backwardIndex : source.Index → target.Index
  backwardCell : ∀ i : source.Index,
    NativeGK5CGConservativeFiveCell first last
      (target.raw (backwardIndex i)) (source.raw i)

/-- Reflexive comparison retains original reflexive five-cell values. -/
def fivefoldP77RawPatchBlockComparisonRefl
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    FivefoldP77RawPatchBlockComparison f g h k block block where
  forwardIndex := id
  forwardCell i := .refl (block.raw i)
  backwardIndex := id
  backwardCell i := .refl (block.raw i)

/-- Reversal swaps the two supplied coverage maps and their actual cells. -/
def fivefoldP77RawPatchBlockComparisonSymm
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchBlock f g h k u v}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k target source where
  forwardIndex := comparison.backwardIndex
  forwardCell := comparison.backwardCell
  backwardIndex := comparison.forwardIndex
  backwardCell := comparison.forwardCell

/-- Compose actual original five-cells, retaining their composite histories. -/
def fivefoldP77RawPatchBlockComparisonTrans
    {u v : FivefoldPathVertex}
    {source middle target : FivefoldP77RawPatchBlock f g h k u v}
    (comparison₁ : FivefoldP77RawPatchBlockComparison f g h k source middle)
    (comparison₂ : FivefoldP77RawPatchBlockComparison f g h k middle target) :
    FivefoldP77RawPatchBlockComparison f g h k source target where
  forwardIndex j := comparison₁.forwardIndex (comparison₂.forwardIndex j)
  forwardCell j := .trans
    (comparison₁.forwardCell (comparison₂.forwardIndex j))
    (comparison₂.forwardCell j)
  backwardIndex i := comparison₂.backwardIndex (comparison₁.backwardIndex i)
  backwardCell i := .trans
    (comparison₂.backwardCell (comparison₁.backwardIndex i))
    (comparison₁.backwardCell i)

/-- A covered family refinement gives a two-sided comparison. Surjectivity
prevents dropping an original patch with a missing descent certificate. -/
def fivefoldP77RawPatchBlockComparisonOfRefinement
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchBlock f g h k u v)
    (reindex : target.Index → source.Index)
    (covers : Function.Surjective reindex)
    (cells : ∀ j : target.Index,
      NativeGK5CGConservativeFiveCell first last
        (source.raw (reindex j)) (target.raw j)) :
    FivefoldP77RawPatchBlockComparison f g h k source target := by
  refine {
    forwardIndex := reindex
    forwardCell := cells
    backwardIndex := fun i => Classical.choose (covers i)
    backwardCell := ?_ }
  intro i
  have hi : reindex (Classical.choose (covers i)) = i :=
    Classical.choose_spec (covers i)
  simpa only [hi] using (cells (Classical.choose (covers i))).symm

/-- Both directions copy the EXACT typed source path and transport only its
local quotient certificates along the supplied original Type-valued cells. -/
def fivefoldP77RawPatchBlockComparisonEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchBlock f g h k u v}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k source target) :
    FivefoldP77RawPatchBlockWitness f g h k source ≃
      FivefoldP77RawPatchBlockWitness f g h k target := by
  letI := fivefoldP77ConservativeCategory f g h k
  refine {
    toFun := fun witness => ⟨witness.val, ?_⟩
    invFun := fun witness => ⟨witness.val, ?_⟩
    left_inv := fun witness => Subtype.ext rfl
    right_inv := fun witness => Subtype.ext rfl }
  · intro j
    exact (witness.property (comparison.forwardIndex j)).trans
      ((fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
        ⟨comparison.forwardCell j⟩)
  · intro i
    exact (witness.property (comparison.backwardIndex i)).trans
      ((fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
        ⟨comparison.backwardCell i⟩)

/-- Path preservation is definitional, not just equality of numerical charge. -/
theorem fivefoldP77RawPatchBlockComparisonEquiv_val
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchBlock f g h k u v}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k source target)
    (witness : FivefoldP77RawPatchBlockWitness f g h k source) :
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k comparison witness).val =
      witness.val := rfl

/-- Original overlap AND source-anchor existence transfer in both directions. -/
theorem fivefoldP77RawPatchBlockComparison_compatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchBlock f g h k u v}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k source target) :
    fivefoldP77RawPatchBlockCompatible f g h k source ↔
      fivefoldP77RawPatchBlockCompatible f g h k target := by
  constructor
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchBlock_witness_iff f g h k source).2 hc
    exact (fivefoldP77RawPatchBlock_witness_iff f g h k target).1
      ⟨fivefoldP77RawPatchBlockComparisonEquiv f g h k comparison witness⟩
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchBlock_witness_iff f g h k target).2 hc
    exact (fivefoldP77RawPatchBlock_witness_iff f g h k source).1
      ⟨(fivefoldP77RawPatchBlockComparisonEquiv f g h k comparison).symm witness⟩

/-- Finite dependent comparison retains each actual source segment boundary,
while its two raw families and their index Types may differ at every segment. -/
inductive FivefoldP77RawPatchChainComparison
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      FivefoldP77RawPatchChain f g h k u v →
      FivefoldP77RawPatchChain f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil (u : FivefoldPathVertex) :
      FivefoldP77RawPatchChainComparison f g h k (.nil u) (.nil u)
  | cons {u v w : FivefoldPathVertex}
      {sourceBlock targetBlock : FivefoldP77RawPatchBlock f g h k u v}
      {sourceTail targetTail : FivefoldP77RawPatchChain f g h k v w}
      (block : FivefoldP77RawPatchBlockComparison f g h k sourceBlock targetBlock)
      (tail : FivefoldP77RawPatchChainComparison f g h k sourceTail targetTail) :
      FivefoldP77RawPatchChainComparison f g h k
        (.cons sourceBlock sourceTail) (.cons targetBlock targetTail)

/-- Actual product equivalence of every segment's genuine witness Type. -/
def fivefoldP77RawPatchChainComparisonEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (comparison : FivefoldP77RawPatchChainComparison f g h k source target) :
    FivefoldP77RawPatchChainWitness f g h k source ≃
      FivefoldP77RawPatchChainWitness f g h k target := by
  induction comparison with
  | nil u => exact Equiv.refl _
  | cons block tail ih =>
      exact Equiv.prodCongr
        (fivefoldP77RawPatchBlockComparisonEquiv f g h k block) ih

/-- Every segment path is kept, hence the actual ordered source path is kept. -/
theorem fivefoldP77RawPatchChainComparison_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (comparison : FivefoldP77RawPatchChainComparison f g h k source target) :
    ∀ witness : FivefoldP77RawPatchChainWitness f g h k source,
      fivefoldP77RawPatchChainPath f g h k target
          (fivefoldP77RawPatchChainComparisonEquiv f g h k comparison witness) =
        fivefoldP77RawPatchChainPath f g h k source witness := by
  induction comparison with
  | nil u => intro witness; rfl
  | @cons u v w sourceBlock targetBlock sourceTail targetTail block tail ih =>
      rintro ⟨head, rest⟩
      change head.val.comp
          (fivefoldP77RawPatchChainPath f g h k targetTail
            (fivefoldP77RawPatchChainComparisonEquiv f g h k tail rest)) =
        head.val.comp (fivefoldP77RawPatchChainPath f g h k sourceTail rest)
      exact congrArg (fun path : Quiver.Path v w => head.val.comp path) (ih rest)

/-- Transport the actual chain comparison through the two normalization Equivs.
The flattened chains need not be equal as raw dependent chain values. -/
def fivefoldP77RawPatchTreePresentationEquiv
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target)) :
    FivefoldP77RawPatchTreeWitness f g h k source ≃
      FivefoldP77RawPatchTreeWitness f g h k target :=
  ((fivefoldP77RawPatchTreeNormalizeEquiv f g h k source).trans
    (fivefoldP77RawPatchChainComparisonEquiv f g h k comparison)).trans
      (fivefoldP77RawPatchTreeNormalizeEquiv f g h k target).symm

/-- Normalization naturality on genuine Type-valued source witnesses. -/
theorem fivefoldP77RawPatchTreePresentationEquiv_normalize
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target))
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeNormalizeEquiv f g h k target
        (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
          comparison witness) =
      fivefoldP77RawPatchChainComparisonEquiv f g h k comparison
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k source witness) :=
  (fivefoldP77RawPatchTreeNormalizeEquiv f g h k target).apply_symm_apply _

/-- Presentation comparison preserves the exact parenthesized source path. -/
theorem fivefoldP77RawPatchTreePresentation_path
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target))
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreePath f g h k target
        (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
          comparison witness) =
      fivefoldP77RawPatchTreePath f g h k source witness := by
  rw [fivefoldP77RawPatchTreePath_normalize,
    fivefoldP77RawPatchTreePresentationEquiv_normalize,
    fivefoldP77RawPatchChainComparison_path]
  exact (fivefoldP77RawPatchTreePath_normalize f g h k source witness).symm

/-- The square formed by independent certified presentation changes and recuts
commutes as an equality of ACTUAL witness Equivs, not of raw histories. -/
theorem fivefoldP77RawPatchTreePresentation_recut_natural
    {u v : FivefoldPathVertex}
    {source source' target target' : FivefoldP77RawPatchCutTree f g h k u v}
    (sourceRoute : FivefoldP77RawPatchCutRoute f g h k source source')
    (targetRoute : FivefoldP77RawPatchCutRoute f g h k target target')
    (comparison : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source)
      (fivefoldP77RawPatchTreeFlatten f g h k target))
    (comparison' : FivefoldP77RawPatchChainComparison f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k source')
      (fivefoldP77RawPatchTreeFlatten f g h k target')) :
    (fivefoldP77RawPatchCutRouteEquiv f g h k sourceRoute).trans
        (fivefoldP77RawPatchTreePresentationEquiv f g h k source' target'
          comparison') =
      (fivefoldP77RawPatchTreePresentationEquiv f g h k source target
        comparison).trans (fivefoldP77RawPatchCutRouteEquiv f g h k targetRoute) := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchTree_witness_subsingleton f g h k target'
  exact Subsingleton.elim _ _

/-- Finite TYPE-valued histories mix original recuts with genuine family changes.
Raw histories are retained; no equality between these data is imposed. -/
inductive FivefoldP77RawPatchPresentationRoute
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      FivefoldP77RawPatchCutTree f g h k u v →
      FivefoldP77RawPatchCutTree f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | recut {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchCutRoute f g h k source target) :
      FivefoldP77RawPatchPresentationRoute f g h k source target
  | presentation {u v : FivefoldPathVertex}
      (source target : FivefoldP77RawPatchCutTree f g h k u v)
      (comparison : FivefoldP77RawPatchChainComparison f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k source)
        (fivefoldP77RawPatchTreeFlatten f g h k target)) :
      FivefoldP77RawPatchPresentationRoute f g h k source target
  | symm {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
      FivefoldP77RawPatchPresentationRoute f g h k target source
  | trans {u v : FivefoldPathVertex}
      {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
      (firstRoute : FivefoldP77RawPatchPresentationRoute f g h k source middle)
      (secondRoute : FivefoldP77RawPatchPresentationRoute f g h k middle target) :
      FivefoldP77RawPatchPresentationRoute f g h k source target
  | left {u v w : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchPresentationRoute f g h k source target)
      (right : FivefoldP77RawPatchCutTree f g h k v w) :
      FivefoldP77RawPatchPresentationRoute f g h k
        (.node source right) (.node target right)
  | right {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      {source target : FivefoldP77RawPatchCutTree f g h k v w}
      (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
      FivefoldP77RawPatchPresentationRoute f g h k
        (.node left source) (.node left target)

/-- Evaluate the actual operations, including the supplied original five-cell data. -/
def fivefoldP77RawPatchPresentationRouteEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    FivefoldP77RawPatchTreeWitness f g h k source ≃
      FivefoldP77RawPatchTreeWitness f g h k target := by
  induction route with
  | recut route => exact fivefoldP77RawPatchCutRouteEquiv f g h k route
  | presentation source target comparison =>
      exact fivefoldP77RawPatchTreePresentationEquiv f g h k source target comparison
  | symm route ih => exact ih.symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih => exact Equiv.prodCongr ih (Equiv.refl _)
  | right left route ih => exact Equiv.prodCongr (Equiv.refl _) ih

/-- Every finite mixed history preserves the original free source path exactly. -/
theorem fivefoldP77RawPatchPresentationRoute_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k source,
      fivefoldP77RawPatchTreePath f g h k target
          (fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness) =
        fivefoldP77RawPatchTreePath f g h k source witness := by
  induction route with
  | recut route => exact fivefoldP77RawPatchCutRoute_path f g h k route
  | presentation source target comparison =>
      exact fivefoldP77RawPatchTreePresentation_path f g h k source target comparison
  | symm route ih =>
      intro witness
      have hpath := ih
        ((fivefoldP77RawPatchPresentationRouteEquiv f g h k route).symm witness)
      simpa only [Equiv.apply_symm_apply] using hpath.symm
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro witness
      exact (ihSecond (fivefoldP77RawPatchPresentationRouteEquiv
        f g h k firstRoute witness)).trans (ihFirst witness)
  | left route right ih =>
      intro witness
      exact congrArg
        (fun path => path.comp (fivefoldP77RawPatchTreePath f g h k right witness.2))
        (ih witness.1)
  | right left route ih =>
      intro witness
      exact congrArg
        (fun path => (fivefoldP77RawPatchTreePath f g h k left witness.1).comp path)
        (ih witness.2)

/-- History and chosen-comparison independence of induced witness Equivs follows
from proved original source faithfulness. No history-Type subsingleton is claimed. -/
theorem fivefoldP77RawPatchPresentationRouteEquiv_independent
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route₁ route₂ : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    fivefoldP77RawPatchPresentationRouteEquiv f g h k route₁ =
      fivefoldP77RawPatchPresentationRouteEquiv f g h k route₂ := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchTree_witness_subsingleton f g h k target
  exact Subsingleton.elim _ _

/-- Exact source-certified partial Hom equality after every permitted finite change. -/
theorem fivefoldP77RawPatchPresentationRoute_certified
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeCertified f g h k target
        (fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness) =
      fivefoldP77RawPatchTreeCertified f g h k source witness := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  change (fivefoldP77ImageFactor f g h k).map
      (fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k target)
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k target
          (fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness))) =
    (fivefoldP77ImageFactor f g h k).map
      (fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k source)
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k source witness))
  apply congrArg (fun path : Quiver.Path u v =>
    (fivefoldP77ImageFactor f g h k).map path)
  exact (fivefoldP77RawPatchTreePath_normalize f g h k target _).symm.trans
    ((fivefoldP77RawPatchPresentationRoute_path f g h k route witness).trans
      (fivefoldP77RawPatchTreePath_normalize f g h k source witness))

/-- The different raw target presentations have the same original P77 composite
when realized by a genuine source witness; no arbitrary representative is erased. -/
theorem fivefoldP77RawPatchPresentationRoute_target
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k target) =
      fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k source) := by
  exact (fivefoldP77RawPatchTreeCertified_val f g h k target
    (fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness)).symm.trans
      ((congrArg (fun A : FivefoldP77PartialDomain f g h k u v => A.val)
        (fivefoldP77RawPatchPresentationRoute_certified f g h k route witness)).trans
          (fivefoldP77RawPatchTreeCertified_val f g h k source witness))

/-- Partial recovery after any mixed history returns the exact ORIGINAL source path. -/
theorem fivefoldP77RawPatchPresentationRoute_recover
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77RawPatchTreeCertified f g h k target
          (fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness)) =
      fivefoldP77RawPatchTreePath f g h k source witness :=
  (fivefoldP77RawPatchTreeCertified_recover f g h k target _).trans
    (fivefoldP77RawPatchPresentationRoute_path f g h k route witness)

/-- Existence remains necessary and sufficient, separately from uniqueness/coherence. -/
theorem fivefoldP77RawPatchPresentationRoute_compatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    fivefoldP77RawPatchTreeCompatible f g h k source ↔
      fivefoldP77RawPatchTreeCompatible f g h k target := by
  constructor
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k source).2 hc
    exact (fivefoldP77RawPatchTree_witness_iff f g h k target).1
      ⟨fivefoldP77RawPatchPresentationRouteEquiv f g h k route witness⟩
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k target).2 hc
    exact (fivefoldP77RawPatchTree_witness_iff f g h k source).1
      ⟨(fivefoldP77RawPatchPresentationRouteEquiv f g h k route).symm witness⟩

/-- Genuine factorwise obstruction is invariant under all covered presentation changes. -/
theorem fivefoldP77RawPatchPresentationRoute_obstructed_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    fivefoldP77RawPatchTreeObstructed f g h k source ↔
      fivefoldP77RawPatchTreeObstructed f g h k target := by
  rw [fivefoldP77RawPatchTree_obstructed_iff,
    fivefoldP77RawPatchTree_obstructed_iff]
  exact not_congr (fivefoldP77RawPatchPresentationRoute_compatible_iff f g h k route)

/-- Replacing presentations or recutting cannot manufacture a missing designated
source certificate. No assertion concerns an unrelated whole-target factorization. -/
theorem fivefoldP77RawPatchPresentationRoute_obstruction
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target)
    (hmissing : fivefoldP77RawPatchTreeObstructed f g h k source) :
    ¬ Nonempty (FivefoldP77RawPatchTreeWitness f g h k target) := by
  intro hw
  have hc := (fivefoldP77RawPatchTree_witness_iff f g h k target).1 hw
  exact ((fivefoldP77RawPatchTree_obstructed_iff f g h k source).1 hmissing)
    ((fivefoldP77RawPatchPresentationRoute_compatible_iff f g h k route).2 hc)

#print axioms FivefoldP77RawPatchBlockComparison
#print axioms fivefoldP77RawPatchBlockComparisonRefl
#print axioms fivefoldP77RawPatchBlockComparisonSymm
#print axioms fivefoldP77RawPatchBlockComparisonTrans
#print axioms fivefoldP77RawPatchBlockComparisonOfRefinement
#print axioms fivefoldP77RawPatchBlockComparisonEquiv
#print axioms fivefoldP77RawPatchBlockComparisonEquiv_val
#print axioms fivefoldP77RawPatchBlockComparison_compatible_iff
#print axioms FivefoldP77RawPatchChainComparison
#print axioms fivefoldP77RawPatchChainComparisonEquiv
#print axioms fivefoldP77RawPatchChainComparison_path
#print axioms fivefoldP77RawPatchTreePresentationEquiv
#print axioms fivefoldP77RawPatchTreePresentationEquiv_normalize
#print axioms fivefoldP77RawPatchTreePresentation_path
#print axioms fivefoldP77RawPatchTreePresentation_recut_natural
#print axioms FivefoldP77RawPatchPresentationRoute
#print axioms fivefoldP77RawPatchPresentationRouteEquiv
#print axioms fivefoldP77RawPatchPresentationRoute_path
#print axioms fivefoldP77RawPatchPresentationRouteEquiv_independent
#print axioms fivefoldP77RawPatchPresentationRoute_certified
#print axioms fivefoldP77RawPatchPresentationRoute_target
#print axioms fivefoldP77RawPatchPresentationRoute_recover
#print axioms fivefoldP77RawPatchPresentationRoute_compatible_iff
#print axioms fivefoldP77RawPatchPresentationRoute_obstructed_iff
#print axioms fivefoldP77RawPatchPresentationRoute_obstruction

end
end KUOS.Architecture.WuxingPentagonUnified
