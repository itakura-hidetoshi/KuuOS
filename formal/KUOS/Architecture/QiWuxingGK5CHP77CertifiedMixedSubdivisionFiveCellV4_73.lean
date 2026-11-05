import KUOS.Architecture.QiWuxingGK5CHP77RawCutTreeFiveCellCoherenceV4_72
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.73 — CERTIFIED MIXED SUBDIVISION RAW FIVE-CELL COMPARISON.

The prior v4.72 canonical raw cut-tree comparison is extended to the
actual v4.70 CERTIFIED arbitrary finite subdivision/merging histories:
- the coarse one-block tree has a genuine raw right-unit five-cell;
- any certified change of segment count obtains a two-sided comparison
  from the original GK5CG cells already supplied for the subdivision,
  and the genuine v4.72 normalization cells of its fine cut tree;
- changing left/right context constructs original vertical whisker
  five-cells at EVERY full tuple of raw patch indices;
- arbitrary finite recut, presentation change, subdivision, inverse,
  composition and context histories retain actual chosen five-cell data.

An actual original conservative five-cell links the raw source/target
four-cell composites of every permitted mixed route, even when the
requested segment count changes. The witness transport commutes with
this raw comparison, preserving the exact typed Quiver.Path and
source-certified P77 partial Hom. Independently obtained raw routes
induce the same witness Equiv; this does NOT identify original five-cell
histories or assert their higher proof coherence.

Crucially, comparison of COARSE raw cells is weaker than certified
factor splitting. A concrete inverse-e01 then forward-e01 coarse raw
family admits an actual five-cell comparison with the designated
fine tree, yet NO certified subdivision route can exist because
the reverse first segment has no original source witness. We keep
this obstruction instead of erasing it by a postulated equivalence.

Append-only same-root. Strict 空 center; independent Kuu is a presentation.
F55/P77/P94A, physical C60 and north C60 CRT remain distinct.
Public root 107; protected #1558 validation-only Draft/open/unmerged.
No new axioms, sorry, admit, native_decide. Lean v4.30.0-rc2;
pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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




/-- The raw singleton-tree family is not definitionally identical to its
coarse original block: the empty tail contributes a genuine right unit.
Construct BOTH directions using the original GK5CG vertical right-unit cell. -/
def fivefoldP77RawPatchBlockTreeRawComparison
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (fivefoldP77RawPatchBlockTree f g h k block)) block where
  forwardIndex j := (j, PUnit.unit)
  forwardCell j :=
    NativeGK5CGConservativeFiveCell.verticalRightUnit (block.raw j)
  backwardIndex i := i.1
  backwardCell i :=
    (NativeGK5CGConservativeFiveCell.verticalRightUnit (block.raw i.1)).symm

/-- The ACTUAL five-cell comparison of a certified coarse single-block tree
and a fine arbitrary cut tree is built without postulating a direct Equiv.
The supplied comparison contains real original cells for every fine
composite and every coarse patch; tree normalization adds its own cells. -/
def fivefoldP77RawPatchTreeSubdivisionRawComparison
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree)) block) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (fivefoldP77RawPatchBlockTree f g h k block))
      (fivefoldP77RawPatchTreeRawBlock f g h k tree) :=
  fivefoldP77RawPatchBlockComparisonTrans f g h k
    (fivefoldP77RawPatchBlockTreeRawComparison f g h k block)
    (fivefoldP77RawPatchBlockComparisonTrans f g h k
      (fivefoldP77RawPatchBlockComparisonSymm f g h k comparison)
      (fivefoldP77RawPatchBlockComparisonSymm f g h k
        (fivefoldP77RawPatchTreeRawNormalizeComparison f g h k tree)))

/-- Left context of ANY original raw comparison: all right-hand indices are
retained, and every original left source/target five-cell is whiskered by
the exact same original right raw four-cell. -/
def fivefoldP77RawPatchTreeRawComparison_left
    {u v w : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target))
    (right : FivefoldP77RawPatchCutTree f g h k v w) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k (.node source right))
      (fivefoldP77RawPatchTreeRawBlock f g h k (.node target right)) where
  forwardIndex j := (comparison.forwardIndex j.1, j.2)
  forwardCell j :=
    NativeGK5CGConservativeFiveCell.verticalLeft
      (comparison.forwardCell j.1)
      (fivefoldP77RawPatchTreeRaw f g h k right j.2)
  backwardIndex i := (comparison.backwardIndex i.1, i.2)
  backwardCell i :=
    NativeGK5CGConservativeFiveCell.verticalLeft
      (comparison.backwardCell i.1)
      (fivefoldP77RawPatchTreeRaw f g h k right i.2)

/-- Right context of ANY original raw comparison: all left-hand indices are
retained, and every original five-cell is whiskered by that left raw cell. -/
def fivefoldP77RawPatchTreeRawComparison_right
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchCutTree f g h k u v)
    {source target : FivefoldP77RawPatchCutTree f g h k v w}
    (comparison : FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target)) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k (.node left source))
      (fivefoldP77RawPatchTreeRawBlock f g h k (.node left target)) where
  forwardIndex j := (j.1, comparison.forwardIndex j.2)
  forwardCell j :=
    NativeGK5CGConservativeFiveCell.verticalRight
      (fivefoldP77RawPatchTreeRaw f g h k left j.1)
      (comparison.forwardCell j.2)
  backwardIndex i := (i.1, comparison.backwardIndex i.2)
  backwardCell i :=
    NativeGK5CGConservativeFiveCell.verticalRight
      (fivefoldP77RawPatchTreeRaw f g h k left i.1)
      (comparison.backwardCell i.2)

/-- Old finite presentation/recut routes now carry a genuine comparison of
their original PARENTHESIZED raw families, at any contextual depth. -/
def fivefoldP77RawPatchPresentationRouteRawComparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target) := by
  induction route with
  | recut route =>
      exact fivefoldP77RawPatchCutRouteRawComparison f g h k route
  | presentation source target comparison =>
      exact fivefoldP77RawPatchTreeRawComparison f g h k source target comparison
  | symm route ih =>
      exact fivefoldP77RawPatchBlockComparisonSymm f g h k ih
  | trans route₁ route₂ ih₁ ih₂ =>
      exact fivefoldP77RawPatchBlockComparisonTrans f g h k ih₁ ih₂
  | left route right ih =>
      exact fivefoldP77RawPatchTreeRawComparison_left f g h k ih right
  | right left route ih =>
      exact fivefoldP77RawPatchTreeRawComparison_right f g h k left ih

/-- Main v4.73 construction: EVERY finite certified mixed operation has real
two-sided GK5CG conservative five-cell comparison on its original raw
parenthesized four-cell families. No arbitrary comparison is assumed. -/
def fivefoldP77RawPatchSubdivisionRouteRawComparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target) := by
  induction route with
  | presentation route =>
      exact fivefoldP77RawPatchPresentationRouteRawComparison f g h k route
  | subdivide block tree comparison fine =>
      exact fivefoldP77RawPatchTreeSubdivisionRawComparison f g h k
        block tree comparison
  | symm route ih =>
      exact fivefoldP77RawPatchBlockComparisonSymm f g h k ih
  | trans route₁ route₂ ih₁ ih₂ =>
      exact fivefoldP77RawPatchBlockComparisonTrans f g h k ih₁ ih₂
  | left route right ih =>
      exact fivefoldP77RawPatchTreeRawComparison_left f g h k ih right
  | right left route ih =>
      exact fivefoldP77RawPatchTreeRawComparison_right f g h k left ih

/-- Even WITHOUT a source witness, actual original raw quotient classes
transport along the finite certified history's genuine five-cells. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawClass_forward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (j : (fivefoldP77RawPatchTreeRawBlock f g h k target).Index) :
    fivefoldP77ConservativeClass f g h k
        ((fivefoldP77RawPatchTreeRawBlock f g h k source).raw
          ((fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).forwardIndex j)) =
      fivefoldP77ConservativeClass f g h k
        ((fivefoldP77RawPatchTreeRawBlock f g h k target).raw j) :=
  (fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
    ⟨(fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).forwardCell j⟩

/-- Reverse coverage is also a genuine source five-cell, not an assumed
inverse map of patch indices. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawClass_backward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (i : (fivefoldP77RawPatchTreeRawBlock f g h k source).Index) :
    fivefoldP77ConservativeClass f g h k
        ((fivefoldP77RawPatchTreeRawBlock f g h k target).raw
          ((fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).backwardIndex i)) =
      fivefoldP77ConservativeClass f g h k
        ((fivefoldP77RawPatchTreeRawBlock f g h k source).raw i) :=
  (fivefoldP77ConservativeClass_eq_iff f g h k _ _).2
    ⟨(fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).backwardCell i⟩

/-- GK5CG signed associator charge is a CONSEQUENCE of the actual
five-cell, not a substitute for its Type-valued source evidence. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawCharge_forward
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (j : (fivefoldP77RawPatchTreeRawBlock f g h k target).Index) :
    ((fivefoldP77RawPatchTreeRawBlock f g h k source).raw
      ((fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).forwardIndex j)).gk5cgAssocCharge =
      ((fivefoldP77RawPatchTreeRawBlock f g h k target).raw j).gk5cgAssocCharge :=
  (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route).forwardCell j
    |>.assocCharge_sound

/-- New genuine raw comparison and old certified witness transport commute
on the exact TYPE-valued original source Quiver.Path. -/
theorem fivefoldP77RawPatchSubdivisionRouteRawGlue_natural
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness) =
      fivefoldP77RawPatchTreeRawGlue f g h k target
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness) := by
  apply Subtype.ext
  calc
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route)
        (fivefoldP77RawPatchTreeRawGlue f g h k source witness)).val =
      (fivefoldP77RawPatchTreeRawGlue f g h k source witness).val :=
        fivefoldP77RawPatchBlockComparisonEquiv_val f g h k _ _
    _ = fivefoldP77RawPatchTreePath f g h k source witness :=
      fivefoldP77RawPatchTreeRawGlue_val f g h k source witness
    _ = fivefoldP77RawPatchTreePath f g h k target
          (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness) :=
        (fivefoldP77RawPatchSubdivisionRoute_path f g h k route witness).symm
    _ = (fivefoldP77RawPatchTreeRawGlue f g h k target
          (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness)).val :=
        (fivefoldP77RawPatchTreeRawGlue_val f g h k target _).symm

/-- Exact v4.70 source-certified P77 partial Hom is preserved by the
actual certified route that generates the genuine raw five-cell comparison. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawCertified_natural
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeCertified f g h k target
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route witness) =
      fivefoldP77RawPatchTreeCertified f g h k source witness :=
  fivefoldP77RawPatchSubdivisionRoute_certified f g h k route witness

/-- Both forward and inverse real source-witness maps along any certified
history preserve genuine raw gluing, not merely its numeric charge. -/
theorem fivefoldP77RawPatchSubdivisionRouteRawGlue_symm_natural
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k target) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k (.symm route))
        (fivefoldP77RawPatchTreeRawGlue f g h k target witness) =
      fivefoldP77RawPatchTreeRawGlue f g h k source
        (fivefoldP77RawPatchSubdivisionRouteEquiv f g h k (.symm route) witness) :=
  fivefoldP77RawPatchSubdivisionRouteRawGlue_natural f g h k (.symm route) witness

/-- Raw coarse compatibility is preserved by any actual bidirectional
five-cell comparison, even if one specified fine factorization is obstructed. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawCompatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchBlockCompatible f g h k
        (fivefoldP77RawPatchTreeRawBlock f g h k source) ↔
      fivefoldP77RawPatchBlockCompatible f g h k
        (fivefoldP77RawPatchTreeRawBlock f g h k target) :=
  fivefoldP77RawPatchBlockComparison_compatible_iff f g h k
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route)

/-- The designated fine factorwise obstruction is also invariant, but it
is NOT logically equivalent to the coarse raw reachability obstruction. -/
theorem fivefoldP77RawPatchSubdivisionRoute_fineObstructed_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchTreeObstructed f g h k source ↔
      fivefoldP77RawPatchTreeObstructed f g h k target :=
  fivefoldP77RawPatchSubdivisionRoute_obstructed_iff f g h k route

/-- Any two permitted histories with the same trees yield the same raw
witness equivalence, even though their Type-valued GK5CG five-cell histories
and their intermediate cuts remain DISTINCT presentation data. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawEquiv_independent
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (r₁ r₂ : FivefoldP77RawPatchSubdivisionRoute f g h k source target) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k r₁) =
      fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k r₂) := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k
    (fivefoldP77RawPatchTreeRawBlock f g h k target)
  exact Subsingleton.elim _ _

/-- Real five-cell raw comparison is functorial at the level of induced
witness maps along any pair of composable certified histories. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawEquiv_trans
    {u v : FivefoldPathVertex}
    {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
    (r₁ : FivefoldP77RawPatchSubdivisionRoute f g h k source middle)
    (r₂ : FivefoldP77RawPatchSubdivisionRoute f g h k middle target) :
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
      (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k r₁)).trans
      (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k r₂)) =
      fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k (.trans r₁ r₂)) := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k
    (fivefoldP77RawPatchTreeRawBlock f g h k target)
  exact Subsingleton.elim _ _

/-- A square made of four REAL certified subdivision/presentation/recut
histories commutes on induced raw witness maps without identifying
four different actual five-cell proof histories. -/
theorem fivefoldP77RawPatchSubdivisionRoute_rawSquare
    {u v : FivefoldPathVertex}
    {a b c d : FivefoldP77RawPatchCutTree f g h k u v}
    (top : FivefoldP77RawPatchSubdivisionRoute f g h k a b)
    (right : FivefoldP77RawPatchSubdivisionRoute f g h k b d)
    (left : FivefoldP77RawPatchSubdivisionRoute f g h k a c)
    (bottom : FivefoldP77RawPatchSubdivisionRoute f g h k c d) :
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
      (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k top)).trans
      (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k right)) =
    (fivefoldP77RawPatchBlockComparisonEquiv f g h k
      (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k left)).trans
      (fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k bottom)) := by
  apply Equiv.ext
  intro witness
  letI := fivefoldP77RawPatchBlock_witness_subsingleton f g h k
    (fivefoldP77RawPatchTreeRawBlock f g h k d)
  exact Subsingleton.elim _ _

/-- The existing original inverse-e01 / forward-e01 chain has a real
coarse composite source witness but no factorwise fine source witness.
Hence there cannot be ANY certified mixed subdivision history from
its coarse one-block tree to that specified fine leaf chain. -/
theorem fivefoldP77ReverseForward_noCertifiedMixedSubdivision :
    ¬ Nonempty (FivefoldP77RawPatchSubdivisionRoute f g h k
      (fivefoldP77RawPatchBlockTree f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k
          (fivefoldP77ReverseForwardPatchChain f g h k)))
      (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))) := by
  rintro ⟨route⟩
  let coarseBlock := fivefoldP77RawPatchCompositeBlock f g h k
    (fivefoldP77ReverseForwardPatchChain f g h k)
  have coarseWitness : FivefoldP77RawPatchTreeWitness f g h k
      (fivefoldP77RawPatchBlockTree f g h k coarseBlock) :=
    (fivefoldP77RawPatchBlockTreeEquiv f g h k coarseBlock).symm
      (fivefoldP77ReverseForwardCompositeWitness f g h k)
  exact fivefoldP77ReverseForwardPatchChain_noWitness f g h k
    ⟨fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route coarseWitness⟩

/-- Yet there IS an explicit original GK5CG five-cell comparison of the
same coarse/fine RAW tree families, even without a fine source witness.
Raw five-cell comparison is strictly weaker than certified factor splitting. -/
def fivefoldP77ReverseForward_rawOnlyComparison :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (fivefoldP77RawPatchBlockTree f g h k
          (fivefoldP77RawPatchCompositeBlock f g h k
            (fivefoldP77ReverseForwardPatchChain f g h k))))
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))) :=
  fivefoldP77RawPatchTreeSubdivisionRawComparison f g h k
    (fivefoldP77RawPatchCompositeBlock f g h k
      (fivefoldP77ReverseForwardPatchChain f g h k))
    (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))
    (fivefoldP77RawPatchBlockComparisonRefl f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k)))

/-- Concrete authority separation: real raw five-cell comparison exists,
but a certified mixed subdivision route is impossible for these endpoints. -/
theorem fivefoldP77ReverseForward_rawComparison_notCertifiedRoute :
    Nonempty (FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (fivefoldP77RawPatchBlockTree f g h k
          (fivefoldP77RawPatchCompositeBlock f g h k
            (fivefoldP77ReverseForwardPatchChain f g h k))))
      (fivefoldP77RawPatchTreeRawBlock f g h k
        (.leaf (fivefoldP77ReverseForwardPatchChain f g h k)))) ∧
      ¬ Nonempty (FivefoldP77RawPatchSubdivisionRoute f g h k
        (fivefoldP77RawPatchBlockTree f g h k
          (fivefoldP77RawPatchCompositeBlock f g h k
            (fivefoldP77ReverseForwardPatchChain f g h k)))
        (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))) :=
  ⟨⟨fivefoldP77ReverseForward_rawOnlyComparison f g h k⟩,
    fivefoldP77ReverseForward_noCertifiedMixedSubdivision f g h k⟩

#print axioms fivefoldP77RawPatchBlockTreeRawComparison
#print axioms fivefoldP77RawPatchTreeSubdivisionRawComparison
#print axioms fivefoldP77RawPatchTreeRawComparison_left
#print axioms fivefoldP77RawPatchTreeRawComparison_right
#print axioms fivefoldP77RawPatchPresentationRouteRawComparison
#print axioms fivefoldP77RawPatchSubdivisionRouteRawComparison
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawClass_forward
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawClass_backward
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawCharge_forward
#print axioms fivefoldP77RawPatchSubdivisionRouteRawGlue_natural
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawCertified_natural
#print axioms fivefoldP77RawPatchSubdivisionRouteRawGlue_symm_natural
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawCompatible_iff
#print axioms fivefoldP77RawPatchSubdivisionRoute_fineObstructed_iff
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawEquiv_independent
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawEquiv_trans
#print axioms fivefoldP77RawPatchSubdivisionRoute_rawSquare
#print axioms fivefoldP77ReverseForward_noCertifiedMixedSubdivision
#print axioms fivefoldP77ReverseForward_rawOnlyComparison
#print axioms fivefoldP77ReverseForward_rawComparison_notCertifiedRoute

end
end KUOS.Architecture.WuxingPentagonUnified
