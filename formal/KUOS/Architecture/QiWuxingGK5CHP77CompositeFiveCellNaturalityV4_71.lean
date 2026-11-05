import KUOS.Architecture.QiWuxingGK5CHP77CertifiedSegmentSubdivisionV4_70
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.71 — ACTUAL ORIGINAL P77 COMPOSITE-FAMILY FIVE-CELL NATURALITY.

Every segmentwise two-sided comparison with original GK5CG Type-valued
five-cells induces a two-sided comparison of the ACTUAL original raw
composite families on ALL tuples of patch indices. The construction
uses the original vertical five-cell whiskering and never postulates
comparison of composite families or loses a patch.

This is stronger than comparing witness Types: actual conservative
five-cell comparison and original quotient equality exist even when
both original source witness Types are empty. Genuine gluing commutes
with comparison on exactly preserved original typed source paths.

Fixed coarse-source factorization fibers transport as explicit Equivs
under independent covered changes in fine and coarse presentations.
A certified subdivision route still requires a genuine fine witness;
coarse reachability never provides inverse factorization by itself.
Induced routes are compared, not histories or five-cell proof terms.

Append-only same-root; strict 空 central, independent Kuu as presentation.
Original F55/P77/P94A, physical C60 and north C60 remain distinct.
Public root107, #1558 validation-only Draft/open/unmerged; pinned
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit or native_decide.
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


/-- Lift every target index tuple to a source tuple, retaining each segment. -/
def fivefoldP77CompositeComparisonForwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    FivefoldP77RawPatchChainIndex f g h k target →
      FivefoldP77RawPatchChainIndex f g h k source := by
  induction change with
  | nil vertex => exact id
  | cons block tail ih =>
      exact fun indices => (block.forwardIndex indices.1, ih indices.2)

/-- Reverse coverage is recorded independently, with no assumed inverse index maps. -/
def fivefoldP77CompositeComparisonBackwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    FivefoldP77RawPatchChainIndex f g h k source →
      FivefoldP77RawPatchChainIndex f g h k target := by
  induction change with
  | nil vertex => exact id
  | cons block tail ih =>
      exact fun indices => (block.backwardIndex indices.1, ih indices.2)

/-- True original five-cell comparison of the complete source/target raw
composites: every inductive step pastes the GIVEN head five-cell with
the tail five-cell, using genuine vertical whiskering. -/
def fivefoldP77CompositeComparisonForwardCell
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    ∀ indices : FivefoldP77RawPatchChainIndex f g h k target,
      NativeGK5CGConservativeFiveCell first last
        (fivefoldP77RawPatchChainRaw f g h k source
          (fivefoldP77CompositeComparisonForwardIndex f g h k change indices))
        (fivefoldP77RawPatchChainRaw f g h k target indices) := by
  induction change with
  | nil vertex =>
      intro indices
      exact .refl _
  | @cons u v w sourceBlock targetBlock sourceTail targetTail block tail ih =>
      rintro ⟨j, indices⟩
      change NativeGK5CGConservativeFiveCell first last
        (.trans (sourceBlock.raw (block.forwardIndex j))
          (fivefoldP77RawPatchChainRaw f g h k sourceTail
            (fivefoldP77CompositeComparisonForwardIndex f g h k tail indices)))
        (.trans (targetBlock.raw j)
          (fivefoldP77RawPatchChainRaw f g h k targetTail indices))
      exact .trans
        (.verticalLeft (block.forwardCell j)
          (fivefoldP77RawPatchChainRaw f g h k sourceTail
            (fivefoldP77CompositeComparisonForwardIndex f g h k tail indices)))
        (.verticalRight (targetBlock.raw j) (ih indices))

/-- Reverse composite five-cells are genuine separately selected source data. -/
def fivefoldP77CompositeComparisonBackwardCell
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    ∀ indices : FivefoldP77RawPatchChainIndex f g h k source,
      NativeGK5CGConservativeFiveCell first last
        (fivefoldP77RawPatchChainRaw f g h k target
          (fivefoldP77CompositeComparisonBackwardIndex f g h k change indices))
        (fivefoldP77RawPatchChainRaw f g h k source indices) := by
  induction change with
  | nil vertex =>
      intro indices
      exact .refl _
  | @cons u v w sourceBlock targetBlock sourceTail targetTail block tail ih =>
      rintro ⟨i, indices⟩
      change NativeGK5CGConservativeFiveCell first last
        (.trans (targetBlock.raw (block.backwardIndex i))
          (fivefoldP77RawPatchChainRaw f g h k targetTail
            (fivefoldP77CompositeComparisonBackwardIndex f g h k tail indices)))
        (.trans (sourceBlock.raw i)
          (fivefoldP77RawPatchChainRaw f g h k sourceTail indices))
      exact .trans
        (.verticalLeft (block.backwardCell i)
          (fivefoldP77RawPatchChainRaw f g h k targetTail
            (fivefoldP77CompositeComparisonBackwardIndex f g h k tail indices)))
        (.verticalRight (sourceBlock.raw i) (ih indices))

/-- A block comparison is constructed at every complete index tuple without
requiring any source path witness. It retains both original five-cell values. -/
def fivefoldP77CompositeBlockComparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k source)
      (fivefoldP77RawPatchCompositeBlock f g h k target) where
  forwardIndex := fivefoldP77CompositeComparisonForwardIndex f g h k change
  forwardCell := fivefoldP77CompositeComparisonForwardCell f g h k change
  backwardIndex := fivefoldP77CompositeComparisonBackwardIndex f g h k change
  backwardCell := fivefoldP77CompositeComparisonBackwardCell f g h k change

/-- Original quotient equality of every compared raw composite follows from
the actual original GK5CG five-cell, not equality of charges. -/
theorem fivefoldP77CompositeComparison_class_forward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (indices : FivefoldP77RawPatchChainIndex f g h k target) :
    fivefoldP77ConservativeClass f g h k
        (fivefoldP77RawPatchChainRaw f g h k source
          (fivefoldP77CompositeComparisonForwardIndex f g h k change indices)) =
      fivefoldP77ConservativeClass f g h k
        (fivefoldP77RawPatchChainRaw f g h k target indices) :=
  (fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
    ⟨fivefoldP77CompositeComparisonForwardCell f g h k change indices⟩

/-- Independent backward coverage yields the opposite raw quotient comparison. -/
theorem fivefoldP77CompositeComparison_class_backward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (indices : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77ConservativeClass f g h k
        (fivefoldP77RawPatchChainRaw f g h k target
          (fivefoldP77CompositeComparisonBackwardIndex f g h k change indices)) =
      fivefoldP77ConservativeClass f g h k
        (fivefoldP77RawPatchChainRaw f g h k source indices) :=
  (fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
    ⟨fivefoldP77CompositeComparisonBackwardCell f g h k change indices⟩

/-- Every actual original conservative five-cell preserves four-associator
charge, but charge equality is NOT used to construct the five-cell. -/
theorem fivefoldP77CompositeComparison_charge_forward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (indices : FivefoldP77RawPatchChainIndex f g h k target) :
    (fivefoldP77RawPatchChainRaw f g h k source
      (fivefoldP77CompositeComparisonForwardIndex f g h k change indices)).gk5cgAssocCharge =
      (fivefoldP77RawPatchChainRaw f g h k target indices).gk5cgAssocCharge :=
  (fivefoldP77CompositeComparisonForwardCell f g h k change indices).assocCharge_sound

/-- The new composite-family equivalence agrees with the old factorwise
equivalence on all genuinely source-certified witnesses. -/
theorem fivefoldP77CompositeComparison_glue_natural
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (witness : FivefoldP77RawPatchChainWitness f g h k source) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77CompositeBlockComparison f g h k change)
        (fivefoldP77RawPatchCompositeGlue f g h k source witness) =
      fivefoldP77RawPatchCompositeGlue f g h k target
        (fivefoldP77RawPatchChainComparisonEquiv f g h k change witness) := by
  apply Subtype.ext
  exact (fivefoldP77RawPatchChainComparison_path f g h k change witness).symm

/-- Even when both fine witness Types are empty, the two composite-block
compatibility conditions transport along genuine raw five-cell data. -/
theorem fivefoldP77CompositeComparison_coarseCompatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    fivefoldP77RawPatchBlockCompatible f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k source) ↔
      fivefoldP77RawPatchBlockCompatible f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k target) :=
  fivefoldP77RawPatchBlockComparison_compatible_iff f g h k
    (fivefoldP77CompositeBlockComparison f g h k change)

/-- Source-factor compatibility is a STRICTLY separate condition from the
coarse composite: its transfer uses all genuine per-segment evidence. -/
theorem fivefoldP77CompositeComparison_fineCompatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    fivefoldP77RawPatchChainCompatible f g h k source ↔
      fivefoldP77RawPatchChainCompatible f g h k target := by
  constructor
  · intro hc
    obtain ⟨w⟩ := (fivefoldP77RawPatchChain_witness_iff f g h k source).2 hc
    exact (fivefoldP77RawPatchChain_witness_iff f g h k target).1
      ⟨fivefoldP77RawPatchChainComparisonEquiv f g h k change w⟩
  · intro hc
    obtain ⟨w⟩ := (fivefoldP77RawPatchChain_witness_iff f g h k target).2 hc
    exact (fivefoldP77RawPatchChain_witness_iff f g h k source).1
      ⟨(fivefoldP77RawPatchChainComparisonEquiv f g h k change).symm w⟩

/-- The whole specified-factor obstruction is invariant under actual
segmentwise family comparison, even with no coarse realization hypothesis. -/
theorem fivefoldP77CompositeComparison_fineMissing_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target) :
    ¬ Nonempty (FivefoldP77RawPatchChainWitness f g h k source) ↔
      ¬ Nonempty (FivefoldP77RawPatchChainWitness f g h k target) := by
  constructor
  · intro hmissing ⟨w⟩
    exact hmissing ⟨(fivefoldP77RawPatchChainComparisonEquiv f g h k change).symm w⟩
  · intro hmissing ⟨w⟩
    exact hmissing ⟨fivefoldP77RawPatchChainComparisonEquiv f g h k change w⟩

/-- A fixed coarse source path can be transported between two independently
covered coarse families along with its actual, not inferred, fine factorization.
This is an Equiv of the FULL Type-valued factorization fibers. -/
def fivefoldP77SubdivisionFiberComparisonEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    {sourceBlock targetBlock : FivefoldP77RawPatchBlock f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (coarseChange : FivefoldP77RawPatchBlockComparison f g h k sourceBlock targetBlock)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k sourceBlock) :
    FivefoldP77RawPatchSubdivisionFiber f g h k source sourceBlock coarse ≃
      FivefoldP77RawPatchSubdivisionFiber f g h k target targetBlock
        (fivefoldP77RawPatchBlockComparisonEquiv f g h k coarseChange coarse) := by
  let chainEquiv := fivefoldP77RawPatchChainComparisonEquiv f g h k change
  refine {
    toFun := fun datum =>
      ⟨chainEquiv datum.val, by
        exact (fivefoldP77RawPatchChainComparison_path f g h k change datum.val).trans
          (datum.property.trans
            (fivefoldP77RawPatchBlockComparisonEquiv_val f g h k coarseChange coarse).symm)⟩
    invFun := fun datum =>
      ⟨chainEquiv.symm datum.val, by
        have hpath := fivefoldP77RawPatchChainComparison_path f g h k
          change (chainEquiv.symm datum.val)
        rw [chainEquiv.apply_symm_apply] at hpath
        exact hpath.symm.trans (datum.property.trans
          (fivefoldP77RawPatchBlockComparisonEquiv_val f g h k coarseChange coarse))⟩
    left_inv := ?_
    right_inv := ?_ }
  · intro datum
    apply Subtype.ext
    exact chainEquiv.symm_apply_apply datum.val
  · intro datum
    apply Subtype.ext
    exact chainEquiv.apply_symm_apply datum.val

/-- The nonemptiness of any prescribed factorization fiber is naturally
invariant under genuine fine and coarse representation changes. -/
theorem fivefoldP77SubdivisionFiberComparison_nonempty_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    {sourceBlock targetBlock : FivefoldP77RawPatchBlock f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (coarseChange : FivefoldP77RawPatchBlockComparison f g h k sourceBlock targetBlock)
    (coarse : FivefoldP77RawPatchBlockWitness f g h k sourceBlock) :
    Nonempty (FivefoldP77RawPatchSubdivisionFiber f g h k source sourceBlock coarse) ↔
      Nonempty (FivefoldP77RawPatchSubdivisionFiber f g h k target targetBlock
        (fivefoldP77RawPatchBlockComparisonEquiv f g h k coarseChange coarse)) := by
  constructor
  · rintro ⟨datum⟩
    exact ⟨fivefoldP77SubdivisionFiberComparisonEquiv f g h k
      change coarseChange coarse datum⟩
  · rintro ⟨datum⟩
    exact ⟨(fivefoldP77SubdivisionFiberComparisonEquiv f g h k
      change coarseChange coarse).symm datum⟩

/-- The comparison of actual complete families is usable as the source of a
certified subdivision route precisely when a genuine target fine witness is
supplied. The reverse five-cell comparison is part of the constructed route. -/
def fivefoldP77CompositeComparisonAsSubdivisionRoute
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (fine : FivefoldP77RawPatchChainWitness f g h k target) :
    FivefoldP77RawPatchSubdivisionRoute f g h k
      (fivefoldP77RawPatchBlockTree f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k source))
      (.leaf target) :=
  .subdivide (fivefoldP77RawPatchCompositeBlock f g h k source) (.leaf target)
    (fivefoldP77RawPatchBlockComparisonSymm f g h k
      (fivefoldP77CompositeBlockComparison f g h k change)) fine

/-- Certified subdivision/reparenthesization reuses the exact original source
path. It does not assert equality of the chosen five-cell histories. -/
theorem fivefoldP77CompositeComparisonSubdivision_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (fine : FivefoldP77RawPatchChainWitness f g h k target)
    (coarse : FivefoldP77RawPatchTreeWitness f g h k
      (fivefoldP77RawPatchBlockTree f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k source))) :
    fivefoldP77RawPatchTreePath f g h k (.leaf target)
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k
          (fivefoldP77CompositeComparisonAsSubdivisionRoute f g h k change fine)
          coarse) =
      fivefoldP77RawPatchTreePath f g h k
        (fivefoldP77RawPatchBlockTree f g h k
          (fivefoldP77RawPatchCompositeBlock f g h k source)) coarse :=
  fivefoldP77RawPatchSubdivisionRoute_path f g h k
    (fivefoldP77CompositeComparisonAsSubdivisionRoute f g h k change fine) coarse

/-- If original fine source data exist, factorwise and certified-composite
comparisons produce the SAME final fine witness value. -/
theorem fivefoldP77CompositeComparisonSubdivision_agrees
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (change : FivefoldP77RawPatchChainComparison f g h k source target)
    (fineSource : FivefoldP77RawPatchChainWitness f g h k source)
    (fineTarget : FivefoldP77RawPatchChainWitness f g h k target) :
    fivefoldP77RawPatchSubdivisionRouteEquiv f g h k
        (fivefoldP77CompositeComparisonAsSubdivisionRoute f g h k change fineTarget)
        ((fivefoldP77RawPatchBlockTreeEquiv f g h k
          (fivefoldP77RawPatchCompositeBlock f g h k source)).symm
          (fivefoldP77RawPatchCompositeGlue f g h k source fineSource)) =
      fivefoldP77RawPatchChainComparisonEquiv f g h k change fineSource := by
  letI := fivefoldP77RawPatchChain_witness_subsingleton f g h k target
  exact Subsingleton.elim _ _

#print axioms fivefoldP77CompositeComparisonForwardIndex
#print axioms fivefoldP77CompositeComparisonBackwardIndex
#print axioms fivefoldP77CompositeComparisonForwardCell
#print axioms fivefoldP77CompositeComparisonBackwardCell
#print axioms fivefoldP77CompositeBlockComparison
#print axioms fivefoldP77CompositeComparison_class_forward
#print axioms fivefoldP77CompositeComparison_class_backward
#print axioms fivefoldP77CompositeComparison_charge_forward
#print axioms fivefoldP77CompositeComparison_glue_natural
#print axioms fivefoldP77CompositeComparison_coarseCompatible_iff
#print axioms fivefoldP77CompositeComparison_fineCompatible_iff
#print axioms fivefoldP77CompositeComparison_fineMissing_iff
#print axioms fivefoldP77SubdivisionFiberComparisonEquiv
#print axioms fivefoldP77SubdivisionFiberComparison_nonempty_iff
#print axioms fivefoldP77CompositeComparisonAsSubdivisionRoute
#print axioms fivefoldP77CompositeComparisonSubdivision_path
#print axioms fivefoldP77CompositeComparisonSubdivision_agrees

end
end KUOS.Architecture.WuxingPentagonUnified
