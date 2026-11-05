import KUOS.Architecture.QiWuxingGK5CHP77PatchPresentationNaturalityV4_69
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.70 — CERTIFIED ORIGINAL P77 SEGMENT SUBDIVISION AND GLUING.

A finite dependent chain defines an actual original raw composite block.
Its index Type contains EVERY tuple of segment indices; no local patch is
dropped. Genuine factorwise source witnesses glue into this block. Explicit
two-sided original Type-valued five-cell data compare it with a coarse block.

Fine witnesses are equivalent to the TOTAL Type of coarse witnesses equipped
with their genuine fine factorization and exact source-path equality. For a
fixed coarse witness, the factorization fiber is inhabited exactly when the
designated fine chain has all its original local descent certificates.
A full coarse/fine Equiv therefore requires actual fine witness data.

These certified operations may change segment count and intermediate vertices.
Finite histories mix them with v4.69 presentation changes, original recuts,
inverses, composition and contexts. Their induced witness Equivs preserve
the exact source path, original P77 partial Hom and recovery; route and
presentation choices do not affect that induced map. Raw histories remain data.

The original target inverse of e01 followed by e01 gives a concrete boundary:
the composite has the genuine nil source witness, but its designated reverse
segment has NO source witness. Coarse reachability alone cannot authorize a
subdivision. No global target fullness, charge substitute, source reverse edge,
general sheaf, pentagonator or Gray restoration is asserted.

Append-only same-root; strict 空 central, independent Kuu a presentation.
Original F55/P77/P94A, physical C60 and north C60 CRT retain their authorities.
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

/-- Every tuple of designated raw patch indices, retaining dependent order. -/
def FivefoldP77RawPatchChainIndex
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) : Type :=
  match chain with
  | .nil _ => PUnit
  | .cons block tail =>
      block.Index × FivefoldP77RawPatchChainIndex f g h k tail

/-- Nonempty local families give a nonempty finite product of their indices. -/
theorem fivefoldP77RawPatchChainIndex_nonempty
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    Nonempty (FivefoldP77RawPatchChainIndex f g h k chain) := by
  induction chain with
  | nil _ => exact ⟨PUnit.unit⟩
  | cons block tail ih =>
      obtain ⟨i⟩ := block.nonempty
      obtain ⟨indices⟩ := ih
      exact ⟨(i, indices)⟩

/-- Actual original raw four-cell composition for each tuple, before quotienting. -/
def fivefoldP77RawPatchChainRaw
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    FivefoldP77RawPatchChainIndex f g h k chain →
      FivefoldP77LocalRaw f g h k u v := by
  induction chain with
  | nil vertex =>
      intro _
      exact .refl (fivefoldF55OriginalAt f g h k vertex.phase)
  | cons block tail ih =>
      intro indices
      exact .trans (block.raw indices.1) (ih indices.2)

/-- The coarse raw family contains ALL actual segmentwise composites. -/
def fivefoldP77RawPatchCompositeBlock
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    FivefoldP77RawPatchBlock f g h k u v where
  Index := FivefoldP77RawPatchChainIndex f g h k chain
  nonempty := fivefoldP77RawPatchChainIndex_nonempty f g h k chain
  raw := fivefoldP77RawPatchChainRaw f g h k chain

/-- Gluing realizes every composite representative, not merely chosen indices. -/
theorem fivefoldP77RawPatchChainPath_eval_all
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    ∀ (witness : FivefoldP77RawPatchChainWitness f g h k chain)
      (indices : FivefoldP77RawPatchChainIndex f g h k chain),
      (fivefoldP77ConservativeFunctor f g h k).map
          (fivefoldP77RawPatchChainPath f g h k chain witness) =
        fivefoldP77ConservativeClass f g h k
          (fivefoldP77RawPatchChainRaw f g h k chain indices) := by
  letI := fivefoldP77ConservativeCategory f g h k
  induction chain with
  | nil vertex =>
      intro _ _
      exact (fivefoldP77ConservativeFunctor f g h k).map_id vertex
  | cons block tail ih =>
      rintro ⟨head, rest⟩ ⟨i, indices⟩
      change (fivefoldP77ConservativeFunctor f g h k).map
          (head.val.comp (fivefoldP77RawPatchChainPath f g h k tail rest)) =
        fivefoldP77ConservativeClass f g h k
          (.trans (block.raw i) (fivefoldP77RawPatchChainRaw f g h k tail indices))
      calc
        (fivefoldP77ConservativeFunctor f g h k).map
            (head.val.comp (fivefoldP77RawPatchChainPath f g h k tail rest)) =
          (fivefoldP77ConservativeFunctor f g h k).map head.val ≫
            (fivefoldP77ConservativeFunctor f g h k).map
              (fivefoldP77RawPatchChainPath f g h k tail rest) :=
          (fivefoldP77ConservativeFunctor f g h k).map_comp _ _
        _ = fivefoldP77ConservativeCompose f g h k
              (fivefoldP77ConservativeClass f g h k (block.raw i))
              (fivefoldP77ConservativeClass f g h k
                (fivefoldP77RawPatchChainRaw f g h k tail indices)) := by
          rw [head.property i, ih rest indices]
          rfl
        _ = _ := fivefoldP77ConservativeCompose_class f g h k _ _

/-- Unconditional forward gluing of genuine fine witnesses. -/
def fivefoldP77RawPatchCompositeGlue
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    FivefoldP77RawPatchBlockWitness f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) :=
  ⟨fivefoldP77RawPatchChainPath f g h k chain witness,
    fivefoldP77RawPatchChainPath_eval_all f g h k chain witness⟩

/-- Glue to a specified coarse presentation using actual original five-cell data. -/
def fivefoldP77RawPatchSubdivisionGlue
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    FivefoldP77RawPatchBlockWitness f g h k block :=
  fivefoldP77RawPatchBlockComparisonEquiv f g h k comparison
    (fivefoldP77RawPatchCompositeGlue f g h k chain witness)

/-- The coarse witness stores the exact concatenation of the fine source paths. -/
theorem fivefoldP77RawPatchSubdivisionGlue_val
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    (fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison witness).val =
      fivefoldP77RawPatchChainPath f g h k chain witness := rfl

/-- Unconditional naturality of real gluing under covered changes of both fine
and coarse presentations. The proof compares their actual source paths. -/
theorem fivefoldP77RawPatchSubdivisionGlue_presentation_natural
    {u v : FivefoldPathVertex}
    {sourceChain targetChain : FivefoldP77RawPatchChain f g h k u v}
    {sourceBlock targetBlock : FivefoldP77RawPatchBlock f g h k u v}
    (fineChange : FivefoldP77RawPatchChainComparison f g h k sourceChain targetChain)
    (coarseChange : FivefoldP77RawPatchBlockComparison f g h k sourceBlock targetBlock)
    (sourceComparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k sourceChain) sourceBlock)
    (targetComparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k targetChain) targetBlock)
    (witness : FivefoldP77RawPatchChainWitness f g h k sourceChain) :
    fivefoldP77RawPatchSubdivisionGlue f g h k targetChain targetBlock
        targetComparison (fivefoldP77RawPatchChainComparisonEquiv f g h k
          fineChange witness) =
      fivefoldP77RawPatchBlockComparisonEquiv f g h k coarseChange
        (fivefoldP77RawPatchSubdivisionGlue f g h k sourceChain sourceBlock
          sourceComparison witness) := by
  apply Subtype.ext
  exact fivefoldP77RawPatchChainComparison_path f g h k fineChange witness

/-- Genuine fine data over a FIXED coarse witness, with exact path equality. -/
def FivefoldP77RawPatchSubdivisionFiber
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k block) : Type :=
  {fine : FivefoldP77RawPatchChainWitness f g h k chain //
    fivefoldP77RawPatchChainPath f g h k chain fine = coarse.val}

/-- No existence hypothesis: fine witnesses are equivalent to coarse witnesses
WITH their actual fine factorization. Empty witness Types remain legitimate. -/
def fivefoldP77RawPatchSubdivisionTotalEquiv
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block) :
    FivefoldP77RawPatchChainWitness f g h k chain ≃
      Σ coarse : FivefoldP77RawPatchBlockWitness f g h k block,
        FivefoldP77RawPatchSubdivisionFiber f g h k chain block coarse := by
  refine {
    toFun := fun fine =>
      ⟨fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison fine,
        ⟨fine, rfl⟩⟩
    invFun := fun data => data.2.val
    left_inv := fun _ => rfl
    right_inv := ?_ }
  rintro ⟨coarse, ⟨fine, hfine⟩⟩
  have heq : fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison
      fine = coarse := Subtype.ext hfine
  cases heq
  rfl

/-- The designated fine local descent conditions are exactly the obstruction
to factorizing ANY fixed coarse source witness. Coarse existence alone is weaker. -/
theorem fivefoldP77RawPatchSubdivisionFiber_nonempty_iff
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k block) :
    Nonempty (FivefoldP77RawPatchSubdivisionFiber f g h k chain block coarse) ↔
      fivefoldP77RawPatchChainCompatible f g h k chain := by
  constructor
  · rintro ⟨⟨fine, _⟩⟩
    exact (fivefoldP77RawPatchChain_witness_iff f g h k chain).1 ⟨fine⟩
  · intro hc
    obtain ⟨fine⟩ := (fivefoldP77RawPatchChain_witness_iff f g h k chain).2 hc
    letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k block
    refine ⟨⟨fine, ?_⟩⟩
    exact congrArg Subtype.val (Subsingleton.elim
      (fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison fine)
      coarse)

/-- A fully reversible subdivision explicitly supplies an ACTUAL fine witness.
The inverse is real gluing; uniqueness comes from original source faithfulness. -/
def fivefoldP77RawPatchSubdivisionEquiv
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k chain) :
    FivefoldP77RawPatchBlockWitness f g h k block ≃
      FivefoldP77RawPatchChainWitness f g h k chain := by
  letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k block
  letI := fivefoldP77RawPatchChain_witness_subsingleton f g h k chain
  exact {
    toFun := fun _ => fine
    invFun := fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison
    left_inv := fun _ => Subsingleton.elim _ _
    right_inv := fun _ => Subsingleton.elim _ _ }

/-- Subdivide then genuinely glue: the original coarse Type value is recovered. -/
theorem fivefoldP77RawPatchSubdivisionEquiv_glue_split
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k chain)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k block) :
    fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison
        (fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine
          coarse) = coarse :=
  (fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine).symm_apply_apply coarse

/-- Genuinely glue then subdivide: every factorwise Type value is recovered. -/
theorem fivefoldP77RawPatchSubdivisionEquiv_split_glue
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (fine witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine
        (fivefoldP77RawPatchSubdivisionGlue f g h k chain block comparison witness) =
      witness :=
  (fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine).apply_symm_apply witness

/-- Certified subdivision recovers exactly the specified coarse source path. -/
theorem fivefoldP77RawPatchSubdivisionEquiv_path
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k chain) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k chain)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k block) :
    fivefoldP77RawPatchChainPath f g h k chain
        (fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine
          coarse) = coarse.val := by
  exact congrArg Subtype.val
    ((fivefoldP77RawPatchSubdivisionEquiv f g h k chain block comparison fine).symm_apply_apply coarse)

/-- A single coarse block viewed as a cut tree, with its legitimate empty tail. -/
def fivefoldP77RawPatchBlockTree
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    FivefoldP77RawPatchCutTree f g h k u v :=
  .leaf (.cons block (.nil v))

/-- Mathlib's actual product-unit equivalence, retaining the block source value. -/
def fivefoldP77RawPatchBlockTreeEquiv
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    FivefoldP77RawPatchTreeWitness f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) ≃
      FivefoldP77RawPatchBlockWitness f g h k block :=
  Equiv.prodPUnit _

/-- The empty tail of a single-block tree leaves its exact source path unchanged. -/
theorem fivefoldP77RawPatchBlockTree_path
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (fivefoldP77RawPatchBlockTree f g h k block)) :
    fivefoldP77RawPatchTreePath f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) witness =
      (fivefoldP77RawPatchBlockTreeEquiv f g h k block witness).val := by
  change witness.1.val.comp Quiver.Path.nil = witness.1.val
  rfl

/-- Change actual segment count and vertices, then restore any fine parenthesization. -/
def fivefoldP77RawPatchTreeSubdivisionEquiv
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree)) :
    FivefoldP77RawPatchTreeWitness f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) ≃
      FivefoldP77RawPatchTreeWitness f g h k tree :=
  ((fivefoldP77RawPatchBlockTreeEquiv f g h k block).trans
    (fivefoldP77RawPatchSubdivisionEquiv f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree) block comparison fine)).trans
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree).symm

/-- Subdivision commutes with normalization on actual Type-valued witnesses. -/
theorem fivefoldP77RawPatchTreeSubdivisionEquiv_normalize
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree))
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (fivefoldP77RawPatchBlockTree f g h k block)) :
    fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree
        (fivefoldP77RawPatchTreeSubdivisionEquiv f g h k block tree comparison fine
          witness) =
      fivefoldP77RawPatchSubdivisionEquiv f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree) block comparison fine
          (fivefoldP77RawPatchBlockTreeEquiv f g h k block witness) :=
  (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree).apply_symm_apply _

/-- Actual segment subdivision preserves the whole original typed source path. -/
theorem fivefoldP77RawPatchTreeSubdivision_path
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) block)
    (fine : FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree))
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (fivefoldP77RawPatchBlockTree f g h k block)) :
    fivefoldP77RawPatchTreePath f g h k tree
        (fivefoldP77RawPatchTreeSubdivisionEquiv f g h k block tree comparison fine
          witness) =
      fivefoldP77RawPatchTreePath f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) witness := by
  rw [fivefoldP77RawPatchTreePath_normalize,
    fivefoldP77RawPatchTreeSubdivisionEquiv_normalize,
    fivefoldP77RawPatchSubdivisionEquiv_path]
  exact (fivefoldP77RawPatchBlockTree_path f g h k block witness).symm

/-- Finite actual histories of certified subdivision/merging, old presentation
changes and recuts, at arbitrary depth. No Equiv is postulated as input data. -/
inductive FivefoldP77RawPatchSubdivisionRoute
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      FivefoldP77RawPatchCutTree f g h k u v →
      FivefoldP77RawPatchCutTree f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | presentation {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
      FivefoldP77RawPatchSubdivisionRoute f g h k source target
  | subdivide {u v : FivefoldPathVertex}
      (block : FivefoldP77RawPatchBlock f g h k u v)
      (tree : FivefoldP77RawPatchCutTree f g h k u v)
      (comparison : FivefoldP77RawPatchBlockComparison f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k tree)) block)
      (fine : FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) :
      FivefoldP77RawPatchSubdivisionRoute f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) tree
  | symm {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
      FivefoldP77RawPatchSubdivisionRoute f g h k target source
  | trans {u v : FivefoldPathVertex}
      {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
      (firstRoute : FivefoldP77RawPatchSubdivisionRoute f g h k source middle)
      (secondRoute : FivefoldP77RawPatchSubdivisionRoute f g h k middle target) :
      FivefoldP77RawPatchSubdivisionRoute f g h k source target
  | left {u v w : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
      (right : FivefoldP77RawPatchCutTree f g h k v w) :
      FivefoldP77RawPatchSubdivisionRoute f g h k
        (.node source right) (.node target right)
  | right {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      {source target : FivefoldP77RawPatchCutTree f g h k v w}
      (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
      FivefoldP77RawPatchSubdivisionRoute f g h k
        (.node left source) (.node left target)

/-- Evaluate each actual certified operation by its constructed witness Equiv. -/
def fivefoldP77RawPatchSubdivisionRouteEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    FivefoldP77RawPatchTreeWitness f g h k source ≃
      FivefoldP77RawPatchTreeWitness f g h k target := by
  induction route with
  | presentation route => exact fivefoldP77RawPatchPresentationRouteEquiv f g h k route
  | subdivide block tree comparison fine =>
      exact fivefoldP77RawPatchTreeSubdivisionEquiv f g h k block tree comparison fine
  | symm route ih => exact ih.symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih => exact Equiv.prodCongr ih (Equiv.refl _)
  | right left route ih => exact Equiv.prodCongr (Equiv.refl _) ih

/-- Every permitted finite mixed history keeps the exact original source path. -/
theorem fivefoldP77RawPatchSubdivisionRoute_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k source,
      fivefoldP77RawPatchTreePath f g h k target
          (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness) =
        fivefoldP77RawPatchTreePath f g h k source witness := by
  induction route with
  | presentation route => exact fivefoldP77RawPatchPresentationRoute_path f g h k route
  | subdivide block tree comparison fine =>
      exact fivefoldP77RawPatchTreeSubdivision_path f g h k block tree comparison fine
  | symm route ih =>
      intro witness
      have hpath := ih
        ((fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route).symm witness)
      simpa only [Equiv.apply_symm_apply] using hpath.symm
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro witness
      exact (ihSecond (fivefoldP77RawPatchSubdivisionRouteEquiv
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

/-- All actual routes with fixed endpoints induce the same witness Equiv.
This identifies neither raw five-cell histories nor the different segment chains. -/
theorem fivefoldP77RawPatchSubdivisionRouteEquiv_independent
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route₁ route₂ : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route₁ =
      fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route₂ := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchTree_witness_subsingleton f g h k target
  exact Subsingleton.elim _ _

/-- Any square mixing certified subdivisions with prior presentation changes
commutes on actual witness Equivs. All four edges remain explicit data. -/
theorem fivefoldP77RawPatchSubdivisionRoute_presentation_natural
    {u v : FivefoldPathVertex}
    {source source' target target' : FivefoldP77RawPatchCutTree f g h k u v}
    (sourceChange : FivefoldP77RawPatchPresentationRoute f g h k source source')
    (targetChange : FivefoldP77RawPatchPresentationRoute f g h k target target')
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (route' : FivefoldP77RawPatchSubdivisionRoute f g h k source' target') :
    (fivefoldP77RawPatchPresentationRouteEquiv f g h k sourceChange).trans
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route') =
      (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route).trans
        (fivefoldP77RawPatchPresentationRouteEquiv f g h k targetChange) := by
  exact fivefoldP77RawPatchSubdivisionRouteEquiv_independent f g h k
    (.trans (.presentation sourceChange) route')
    (.trans route (.presentation targetChange))

/-- Original source-certified partial Homs survive every certified segment change. -/
theorem fivefoldP77RawPatchSubdivisionRoute_certified
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeCertified f g h k target
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness) =
      fivefoldP77RawPatchTreeCertified f g h k source witness := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  change (fivefoldP77ImageFactor f g h k).map
      (fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k target)
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k target
          (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness))) =
    (fivefoldP77ImageFactor f g h k).map
      (fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k source)
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k source witness))
  apply congrArg (fun path : Quiver.Path u v =>
    (fivefoldP77ImageFactor f g h k).map path)
  exact (fivefoldP77RawPatchTreePath_normalize f g h k target _).symm.trans
    ((fivefoldP77RawPatchSubdivisionRoute_path f g h k route witness).trans
      (fivefoldP77RawPatchTreePath_normalize f g h k source witness))

/-- Even when actual segment count changes, the realized original P77 target agrees. -/
theorem fivefoldP77RawPatchSubdivisionRoute_target
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k target) =
      fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k source) := by
  exact (fivefoldP77RawPatchTreeCertified_val f g h k target
    (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness)).symm.trans
      ((congrArg (fun A : FivefoldP77PartialDomain f g h k u v => A.val)
        (fivefoldP77RawPatchSubdivisionRoute_certified f g h k route witness)).trans
          (fivefoldP77RawPatchTreeCertified_val f g h k source witness))

/-- Recovery returns the original whole source path after any permitted mixed history. -/
theorem fivefoldP77RawPatchSubdivisionRoute_recover
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77RawPatchTreeCertified f g h k target
          (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness)) =
      fivefoldP77RawPatchTreePath f g h k source witness :=
  (fivefoldP77RawPatchTreeCertified_recover f g h k target _).trans
    (fivefoldP77RawPatchSubdivisionRoute_path f g h k route witness)

/-- Compatibility transfers only along the explicitly certified finite operations. -/
theorem fivefoldP77RawPatchSubdivisionRoute_compatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchTreeCompatible f g h k source ↔
      fivefoldP77RawPatchTreeCompatible f g h k target := by
  constructor
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k source).2 hc
    exact (fivefoldP77RawPatchTree_witness_iff f g h k target).1
      ⟨fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness⟩
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k target).2 hc
    exact (fivefoldP77RawPatchTree_witness_iff f g h k source).1
      ⟨(fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route).symm witness⟩

/-- Actual fine certificates prevent a certified route from erasing an obstruction. -/
theorem fivefoldP77RawPatchSubdivisionRoute_obstructed_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchTreeObstructed f g h k source ↔
      fivefoldP77RawPatchTreeObstructed f g h k target := by
  rw [fivefoldP77RawPatchTree_obstructed_iff,
    fivefoldP77RawPatchTree_obstructed_iff]
  exact not_congr (fivefoldP77RawPatchSubdivisionRoute_compatible_iff f g h k route)

/-- The original target reverse e01 as a singleton raw family, with no source inverse. -/
def fivefoldP77Reverse01PatchBlock :
    FivefoldP77RawPatchBlock f g h k (fivefoldPathVertex 1) (fivefoldPathVertex 0) where
  Index := PUnit
  nonempty := ⟨PUnit.unit⟩
  raw _ := .symm (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01))

/-- The actual forward e01 original raw family. -/
def fivefoldP77Forward01PatchBlock :
    FivefoldP77RawPatchBlock f g h k (fivefoldPathVertex 0) (fivefoldPathVertex 1) where
  Index := PUnit
  nonempty := ⟨PUnit.unit⟩
  raw _ := fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01)

/-- A genuine target cancellation with an obstructed designated first source segment. -/
def fivefoldP77ReverseForwardPatchChain :
    FivefoldP77RawPatchChain f g h k (fivefoldPathVertex 1) (fivefoldPathVertex 1) :=
  .cons (fivefoldP77Reverse01PatchBlock f g h k)
    (.cons (fivefoldP77Forward01PatchBlock f g h k) (.nil (fivefoldPathVertex 1)))

/-- The composite is genuinely realized by the nil source path through original
unit and inverse five-cells, with no appeal to charge equality. -/
def fivefoldP77ReverseForwardCompositeWitness :
    FivefoldP77RawPatchBlockWitness f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k)) := by
  refine ⟨Quiver.Path.nil, ?_⟩
  intro indices
  change fivefoldP77ConservativeClass f g h k
      (.refl (fivefoldF55OriginalAt f g h k (fivefoldPathVertex 1).phase)) =
    fivefoldP77ConservativeClass f g h k
      (.trans
        (.symm (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01)))
        (.trans (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01))
          (.refl (fivefoldF55OriginalAt f g h k (fivefoldPathVertex 1).phase))))
  apply (fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
  exact ⟨.symm (.trans
    (.verticalRight
      (.symm (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01)))
      (.verticalRightUnit
        (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01))))
    (.inverseRight (fivefoldArrowOriginalP77 f g h k (fivefoldPathArrowOf .e01))))⟩

/-- The same designated fine chain has no source witness: its first factor would
realize the original reverse e01, contradicting the proved oriented obstruction. -/
theorem fivefoldP77ReverseForwardPatchChain_noWitness :
    ¬ Nonempty (FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77ReverseForwardPatchChain f g h k)) := by
  rintro ⟨witness⟩
  apply fivefoldP77OriginalReverse01_not_reachable f g h k
  exact ⟨witness.1.val, witness.1.property PUnit.unit⟩

/-- Concrete strictness of coarse reachability versus designated factorwise descent. -/
theorem fivefoldP77RawPatchSubdivision_coarse_not_fine :
    Nonempty (FivefoldP77RawPatchBlockWitness f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k))) ∧
      ¬ Nonempty (FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k)) :=
  ⟨⟨fivefoldP77ReverseForwardCompositeWitness f g h k⟩,
    fivefoldP77ReverseForwardPatchChain_noWitness f g h k⟩

/-- Even the specific genuine nil coarse witness has an empty designated fine fiber. -/
theorem fivefoldP77ReverseForwardSubdivisionFiber_empty :
    ¬ Nonempty (FivefoldP77RawPatchSubdivisionFiber f g h k
      (fivefoldP77ReverseForwardPatchChain f g h k)
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k))
      (fivefoldP77ReverseForwardCompositeWitness f g h k)) := by
  rintro ⟨fine⟩
  exact fivefoldP77ReverseForwardPatchChain_noWitness f g h k ⟨fine.val⟩

#print axioms FivefoldP77RawPatchChainIndex
#print axioms fivefoldP77RawPatchChainIndex_nonempty
#print axioms fivefoldP77RawPatchChainRaw
#print axioms fivefoldP77RawPatchCompositeBlock
#print axioms fivefoldP77RawPatchChainPath_eval_all
#print axioms fivefoldP77RawPatchCompositeGlue
#print axioms fivefoldP77RawPatchSubdivisionGlue
#print axioms fivefoldP77RawPatchSubdivisionGlue_val
#print axioms fivefoldP77RawPatchSubdivisionGlue_presentation_natural
#print axioms FivefoldP77RawPatchSubdivisionFiber
#print axioms fivefoldP77RawPatchSubdivisionTotalEquiv
#print axioms fivefoldP77RawPatchSubdivisionFiber_nonempty_iff
#print axioms fivefoldP77RawPatchSubdivisionEquiv
#print axioms fivefoldP77RawPatchSubdivisionEquiv_glue_split
#print axioms fivefoldP77RawPatchSubdivisionEquiv_split_glue
#print axioms fivefoldP77RawPatchSubdivisionEquiv_path
#print axioms fivefoldP77RawPatchBlockTree
#print axioms fivefoldP77RawPatchBlockTreeEquiv
#print axioms fivefoldP77RawPatchBlockTree_path
#print axioms fivefoldP77RawPatchTreeSubdivisionEquiv
#print axioms fivefoldP77RawPatchTreeSubdivisionEquiv_normalize
#print axioms fivefoldP77RawPatchTreeSubdivision_path
#print axioms FivefoldP77RawPatchSubdivisionRoute
#print axioms fivefoldP77RawPatchSubdivisionRouteEquiv
#print axioms fivefoldP77RawPatchSubdivisionRoute_path
#print axioms fivefoldP77RawPatchSubdivisionRouteEquiv_independent
#print axioms fivefoldP77RawPatchSubdivisionRoute_presentation_natural
#print axioms fivefoldP77RawPatchSubdivisionRoute_certified
#print axioms fivefoldP77RawPatchSubdivisionRoute_target
#print axioms fivefoldP77RawPatchSubdivisionRoute_recover
#print axioms fivefoldP77RawPatchSubdivisionRoute_compatible_iff
#print axioms fivefoldP77RawPatchSubdivisionRoute_obstructed_iff
#print axioms fivefoldP77Reverse01PatchBlock
#print axioms fivefoldP77Forward01PatchBlock
#print axioms fivefoldP77ReverseForwardPatchChain
#print axioms fivefoldP77ReverseForwardCompositeWitness
#print axioms fivefoldP77ReverseForwardPatchChain_noWitness
#print axioms fivefoldP77RawPatchSubdivision_coarse_not_fine
#print axioms fivefoldP77ReverseForwardSubdivisionFiber_empty

end
end KUOS.Architecture.WuxingPentagonUnified
