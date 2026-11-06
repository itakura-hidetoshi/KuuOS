import KUOS.Architecture.QiWuxingGK5CHP77FiniteRefinementScheduleCoherenceV4_75

/-!
Qi v4.76: structural raw-index coherence for the original finite recut Type.
The old normalization-based five-cell comparison is linked to the actual
cut/product reassociation map on every raw index. No raw history is identified.
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

/-- Transport only the original chain indices along an exact chain equality. -/
def fivefoldP77RawPatchChainIndexCast
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target) :
    FivefoldP77RawPatchChainIndex f g h k source →
      FivefoldP77RawPatchChainIndex f g h k target :=
  Eq.mp (congrArg (FivefoldP77RawPatchChainIndex f g h k) e)

theorem fivefoldP77RawPatchChainIndexCast_refl
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (i : FivefoldP77RawPatchChainIndex f g h k chain) :
    fivefoldP77RawPatchChainIndexCast f g h k (rfl : chain = chain) i = i := rfl

theorem fivefoldP77RawPatchChainIndexCast_trans
    {u v : FivefoldPathVertex}
    {source middle target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = middle) (d : middle = target)
    (i : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77RawPatchChainIndexCast f g h k d
        (fivefoldP77RawPatchChainIndexCast f g h k e i) =
      fivefoldP77RawPatchChainIndexCast f g h k (e.trans d) i := by
  cases e
  cases d
  rfl

theorem fivefoldP77RawPatchChainIndexCast_symm_apply
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target)
    (i : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77RawPatchChainIndexCast f g h k e.symm
        (fivefoldP77RawPatchChainIndexCast f g h k e i) = i := by
  cases e
  rfl

theorem fivefoldP77RawPatchChainIndexCast_cons
    {u v w : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    {source target : FivefoldP77RawPatchChain f g h k v w}
    (e : source = target) (i : block.Index)
    (j : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77RawPatchChainIndexCast f g h k
        (congrArg (fun tail => FivefoldP77RawPatchChain.cons block tail) e) (i, j) =
      (i, fivefoldP77RawPatchChainIndexCast f g h k e j) := by
  cases e
  rfl

/-- Appending indices respects exact transport of the left chain. -/
theorem fivefoldP77RawPatchChainAppendIndexEquiv_cast_left
    {u v w : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target) (right : FivefoldP77RawPatchChain f g h k v w)
    (i : FivefoldP77RawPatchChainIndex f g h k source)
    (j : FivefoldP77RawPatchChainIndex f g h k right) :
    fivefoldP77RawPatchChainIndexCast f g h k
        (congrArg (fun chain => fivefoldP77RawPatchChainAppend f g h k chain right) e)
        (fivefoldP77RawPatchChainAppendIndexEquiv f g h k source right (i, j)) =
      fivefoldP77RawPatchChainAppendIndexEquiv f g h k target right
        (fivefoldP77RawPatchChainIndexCast f g h k e i, j) := by
  cases e
  rfl

/-- Appending indices respects exact transport of the right chain. -/
theorem fivefoldP77RawPatchChainAppendIndexEquiv_cast_right
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    {source target : FivefoldP77RawPatchChain f g h k v w}
    (e : source = target)
    (i : FivefoldP77RawPatchChainIndex f g h k left)
    (j : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77RawPatchChainIndexCast f g h k
        (congrArg (fun chain => fivefoldP77RawPatchChainAppend f g h k left chain) e)
        (fivefoldP77RawPatchChainAppendIndexEquiv f g h k left source (i, j)) =
      fivefoldP77RawPatchChainAppendIndexEquiv f g h k left target
        (i, fivefoldP77RawPatchChainIndexCast f g h k e j) := by
  cases e
  rfl

/-- The index associativity square uses the actual dependent chain associator.
It is proved by the ordered original blocks, without any uniqueness assumption. -/
theorem fivefoldP77RawPatchChainAppendIndexEquiv_assoc
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t) :
    ∀ (i : FivefoldP77RawPatchChainIndex f g h k left)
      (j : FivefoldP77RawPatchChainIndex f g h k middle)
      (l : FivefoldP77RawPatchChainIndex f g h k right),
      fivefoldP77RawPatchChainIndexCast f g h k
        (fivefoldP77RawPatchChainAppend_assoc f g h k left middle right)
        (fivefoldP77RawPatchChainAppendIndexEquiv f g h k
          (fivefoldP77RawPatchChainAppend f g h k left middle) right
          (fivefoldP77RawPatchChainAppendIndexEquiv f g h k left middle (i, j), l)) =
      fivefoldP77RawPatchChainAppendIndexEquiv f g h k left
        (fivefoldP77RawPatchChainAppend f g h k middle right)
        (i, fivefoldP77RawPatchChainAppendIndexEquiv f g h k middle right (j, l)) := by
  induction left with
  | nil vertex =>
      intro i j l
      rfl
  | cons block tail ih =>
      rintro ⟨i, rest⟩ j l
      change fivefoldP77RawPatchChainIndexCast f g h k
        (congrArg (fun chain => FivefoldP77RawPatchChain.cons block chain)
          (fivefoldP77RawPatchChainAppend_assoc f g h k tail middle right))
        (i, fivefoldP77RawPatchChainAppendIndexEquiv f g h k
          (fivefoldP77RawPatchChainAppend f g h k tail middle) right
          (fivefoldP77RawPatchChainAppendIndexEquiv f g h k tail middle (rest, j), l)) =
        (i, fivefoldP77RawPatchChainAppendIndexEquiv f g h k tail
          (fivefoldP77RawPatchChainAppend f g h k middle right)
          (rest, fivefoldP77RawPatchChainAppendIndexEquiv f g h k middle right (j, l)))
      rw [fivefoldP77RawPatchChainIndexCast_cons f g h k block
        (fivefoldP77RawPatchChainAppend_assoc f g h k tail middle right)]
      exact Prod.ext rfl (ih middle rest j l)

/-- Evaluate every original recut on full raw-index Types by its actual cut,
product associator, inverse, composition and contextual constructors. -/
def fivefoldP77RawPatchCutRouteIndexEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    FivefoldP77RawPatchTreeIndex f g h k source ≃
      FivefoldP77RawPatchTreeIndex f g h k target := by
  induction route with
  | refl tree => exact Equiv.refl _
  | cut left right =>
      exact (fivefoldP77RawPatchChainAppendIndexEquiv f g h k left right).symm
  | assoc left middle right => exact Equiv.prodAssoc _ _ _
  | symm route ih => exact ih.symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih => exact Equiv.prodCongr ih (Equiv.refl _)
  | right left route ih => exact Equiv.prodCongr (Equiv.refl _) ih

/-- Normalization intertwines actual recut index maps with exact chain transport. -/
theorem fivefoldP77RawPatchCutRouteIndexEquiv_normalize
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    ∀ i : FivefoldP77RawPatchTreeIndex f g h k source,
      fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target
        (fivefoldP77RawPatchCutRouteIndexEquiv f g h k route i) =
      fivefoldP77RawPatchChainIndexCast f g h k
        (fivefoldP77RawPatchCutRoute_flatten f g h k route)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source i) := by
  induction route with
  | refl tree => intro i; rfl
  | cut left right =>
      intro i
      exact (fivefoldP77RawPatchChainAppendIndexEquiv f g h k left right).apply_symm_apply i
  | assoc left middle right =>
      intro i
      exact (fivefoldP77RawPatchChainAppendIndexEquiv_assoc f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left)
        (fivefoldP77RawPatchTreeFlatten f g h k middle)
        (fivefoldP77RawPatchTreeFlatten f g h k right)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i.1.1)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k middle i.1.2)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k right i.2)).symm
  | @symm u v source target route ih =>
      intro i
      have hi := ih ((fivefoldP77RawPatchCutRouteIndexEquiv f g h k route).symm i)
      rw [Equiv.apply_symm_apply] at hi
      have hc := congrArg
        (fivefoldP77RawPatchChainIndexCast f g h k
          (fivefoldP77RawPatchCutRoute_flatten f g h k route).symm) hi
      rw [fivefoldP77RawPatchChainIndexCast_symm_apply] at hc
      exact hc.symm
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro i
      change fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k _
        (fivefoldP77RawPatchCutRouteIndexEquiv f g h k secondRoute
          (fivefoldP77RawPatchCutRouteIndexEquiv f g h k firstRoute i)) = _
      rw [ihSecond, ihFirst]
      exact fivefoldP77RawPatchChainIndexCast_trans f g h k _ _ _
  | @left u v w source target route right ih =>
      intro i
      change fivefoldP77RawPatchChainAppendIndexEquiv f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k target)
        (fivefoldP77RawPatchTreeFlatten f g h k right)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target
          (fivefoldP77RawPatchCutRouteIndexEquiv f g h k route i.1),
          fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k right i.2) = _
      rw [ih]
      exact (fivefoldP77RawPatchChainAppendIndexEquiv_cast_left f g h k
        (fivefoldP77RawPatchCutRoute_flatten f g h k route)
        (fivefoldP77RawPatchTreeFlatten f g h k right)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source i.1)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k right i.2)).symm
  | @right u v w left source target route ih =>
      intro i
      change fivefoldP77RawPatchChainAppendIndexEquiv f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left)
        (fivefoldP77RawPatchTreeFlatten f g h k target)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i.1,
          fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target
            (fivefoldP77RawPatchCutRouteIndexEquiv f g h k route i.2)) = _
      rw [ih]
      exact (fivefoldP77RawPatchChainAppendIndexEquiv_cast_right f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left)
        (fivefoldP77RawPatchCutRoute_flatten f g h k route)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k left i.1)
        (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source i.2)).symm

/-- Exact chain comparison transports every target index backwards. -/
theorem fivefoldP77RawPatchChainComparisonOfEq_forwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target) (i : FivefoldP77RawPatchChainIndex f g h k target) :
    fivefoldP77CompositeComparisonForwardIndex f g h k
      (fivefoldP77RawPatchChainComparisonOfEq f g h k e) i =
        fivefoldP77RawPatchChainIndexCast f g h k e.symm i := by
  cases e
  exact FivefoldP77FiniteRefinement.chainRefl_forward f g h k source i

/-- Exact chain comparison transports every source index forwards. -/
theorem fivefoldP77RawPatchChainComparisonOfEq_backwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (e : source = target) (i : FivefoldP77RawPatchChainIndex f g h k source) :
    fivefoldP77CompositeComparisonBackwardIndex f g h k
      (fivefoldP77RawPatchChainComparisonOfEq f g h k e) i =
        fivefoldP77RawPatchChainIndexCast f g h k e i := by
  cases e
  exact FivefoldP77FiniteRefinement.chainRefl_backward f g h k source i

/-- The existing raw comparison's reverse coverage is exactly the direct recut
equivalence, on the entire original source index Type. -/
theorem fivefoldP77RawPatchCutRouteRawComparison_backwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (i : FivefoldP77RawPatchTreeIndex f g h k source) :
    (fivefoldP77RawPatchCutRouteRawComparison f g h k route).backwardIndex i =
      fivefoldP77RawPatchCutRouteIndexEquiv f g h k route i := by
  change (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target).symm
    (fivefoldP77CompositeComparisonBackwardIndex f g h k
      (fivefoldP77RawPatchChainComparisonOfEq f g h k
        (fivefoldP77RawPatchCutRoute_flatten f g h k route))
      (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source i)) = _
  rw [fivefoldP77RawPatchChainComparisonOfEq_backwardIndex,
    ← fivefoldP77RawPatchCutRouteIndexEquiv_normalize f g h k route i]
  exact (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target).symm_apply_apply _

/-- The existing raw comparison's forward coverage is the inverse direct recut
equivalence, on the entire original target index Type. -/
theorem fivefoldP77RawPatchCutRouteRawComparison_forwardIndex
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (i : FivefoldP77RawPatchTreeIndex f g h k target) :
    (fivefoldP77RawPatchCutRouteRawComparison f g h k route).forwardIndex i =
      (fivefoldP77RawPatchCutRouteIndexEquiv f g h k route).symm i := by
  change (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source).symm
    (fivefoldP77CompositeComparisonForwardIndex f g h k
      (fivefoldP77RawPatchChainComparisonOfEq f g h k
        (fivefoldP77RawPatchCutRoute_flatten f g h k route))
      (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k target i)) = _
  rw [fivefoldP77RawPatchChainComparisonOfEq_forwardIndex]
  have hn := fivefoldP77RawPatchCutRouteIndexEquiv_normalize f g h k
    (.symm route) i
  rw [← hn]
  exact (fivefoldP77RawPatchTreeIndexNormalizeEquiv f g h k source).symm_apply_apply _

#print axioms fivefoldP77RawPatchChainIndexCast
#print axioms fivefoldP77RawPatchChainIndexCast_refl
#print axioms fivefoldP77RawPatchChainIndexCast_trans
#print axioms fivefoldP77RawPatchChainIndexCast_symm_apply
#print axioms fivefoldP77RawPatchChainIndexCast_cons
#print axioms fivefoldP77RawPatchChainAppendIndexEquiv_cast_left
#print axioms fivefoldP77RawPatchChainAppendIndexEquiv_cast_right
#print axioms fivefoldP77RawPatchChainAppendIndexEquiv_assoc
#print axioms fivefoldP77RawPatchCutRouteIndexEquiv
#print axioms fivefoldP77RawPatchCutRouteIndexEquiv_normalize
#print axioms fivefoldP77RawPatchChainComparisonOfEq_forwardIndex
#print axioms fivefoldP77RawPatchChainComparisonOfEq_backwardIndex
#print axioms fivefoldP77RawPatchCutRouteRawComparison_backwardIndex
#print axioms fivefoldP77RawPatchCutRouteRawComparison_forwardIndex

end
end KUOS.Architecture.WuxingPentagonUnified





