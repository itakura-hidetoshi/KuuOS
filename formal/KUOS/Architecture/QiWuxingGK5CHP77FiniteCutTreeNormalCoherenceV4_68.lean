import KUOS.Architecture.QiWuxingGK5CHP77WitnessCutTripleCoherenceV4_67
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.68 — ORIGINAL P77 FINITE CUT-TREE NORMAL FORMS AND COHERENCE.

An endpoint-indexed binary cut tree retains arbitrary finite original
F55/P77 patch chains at its leaves. Its flattening is the original
dependent patch chain, with every raw patch block and typed boundary.
Its witness TYPE is the recursively parenthesized product of genuine
source-path witness Types. An explicit Equiv normalizes this Type to
the v4.65 witness Type of the flattened chain, using the v4.67 cut Equiv.

Finite transformation histories have actual cut, association, inverse,
composition and left/right-context constructors. They are TYPE-valued
histories, not quotient classes. Every tree has a finite normalization
history; two trees are connected exactly when their original flattened
chains agree. The induced Equiv is built from the ACTUAL cut maps and
product associator. All histories with fixed endpoints induce the same
witness Equiv, original free source path and certified P77 partial Hom.
History values themselves are NOT identified.

The proof uses the already established faithful source-witness uniqueness;
it does not assert uniqueness of original raw four-cell or five-cell histories.
Failure at any designated leaf obstructs that factorwise realization and
survives every permitted finite recut. No inference about arbitrary target
factorizations, global target fullness, general sheaves or a pentagonator.
Original F55/P77/P94A, C60 physical gauge and north C60 CRT remain distinct.

Append-only same-root; strict 空 central, independent Kuu a presentation.
Public root107; protected validation-only PR #1558 Draft/open/unmerged.
No new axioms, sorry, admit or native_decide. Lean v4.30.0-rc2,
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

/-- An arbitrary finite parenthesization of original dependent chains.
Empty chains are legitimate leaves; each node keeps its actual cut vertex. -/
inductive FivefoldP77RawPatchCutTree
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    FivefoldPathVertex → FivefoldPathVertex →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | leaf {u v : FivefoldPathVertex}
      (chain : FivefoldP77RawPatchChain f g h k u v) :
      FivefoldP77RawPatchCutTree f g h k u v
  | node {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      (right : FivefoldP77RawPatchCutTree f g h k v w) :
      FivefoldP77RawPatchCutTree f g h k u w

/-- The normal form retains the actual ordered raw blocks, not their charges. -/
def fivefoldP77RawPatchTreeFlatten
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchChain f g h k u v :=
  match tree with
  | .leaf chain => chain
  | .node left right =>
      fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left)
        (fivefoldP77RawPatchTreeFlatten f g h k right)

/-- The genuine Type-valued source witnesses, with the tree's parenthesization. -/
def FivefoldP77RawPatchTreeWitness
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) : Type :=
  match tree with
  | .leaf chain => FivefoldP77RawPatchChainWitness f g h k chain
  | .node left right =>
      FivefoldP77RawPatchTreeWitness f g h k left ×
        FivefoldP77RawPatchTreeWitness f g h k right

/-- Explicit normalization and inverse, recursively using the original cut maps. -/
def fivefoldP77RawPatchTreeNormalizeEquiv
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchTreeWitness f g h k tree ≃
      FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree) := by
  induction tree with
  | leaf chain => exact Equiv.refl _
  | node left right ihLeft ihRight =>
      exact (Equiv.prodCongr ihLeft ihRight).trans
        (fivefoldP77RawPatchChainCutWitnessEquiv f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k left)
          (fivefoldP77RawPatchTreeFlatten f g h k right)).symm

/-- At most one genuine source-path family, by previously proved P77 faithfulness. -/
theorem fivefoldP77RawPatchTree_witness_subsingleton
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    Subsingleton (FivefoldP77RawPatchTreeWitness f g h k tree) := by
  constructor
  intro w₁ w₂
  apply (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree).injective
  letI : Subsingleton (FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k tree)) :=
    fivefoldP77RawPatchChain_witness_subsingleton f g h k _
  exact Subsingleton.elim _ _

/-- Original local five-cell conditions at EVERY leaf, without a global assumption. -/
def fivefoldP77RawPatchTreeCompatible
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) : Prop :=
  match tree with
  | .leaf chain => fivefoldP77RawPatchChainCompatible f g h k chain
  | .node left right =>
      fivefoldP77RawPatchTreeCompatible f g h k left ∧
        fivefoldP77RawPatchTreeCompatible f g h k right

/-- Normalization preserves exactly all original local compatibility conditions. -/
theorem fivefoldP77RawPatchTree_compatible_flatten
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    fivefoldP77RawPatchTreeCompatible f g h k tree ↔
      fivefoldP77RawPatchChainCompatible f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree) := by
  induction tree with
  | leaf chain => rfl
  | node left right ihLeft ihRight =>
      exact (and_congr ihLeft ihRight).trans
        (fivefoldP77RawPatchChainAppend_compatible_iff f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k left)
          (fivefoldP77RawPatchTreeFlatten f g h k right)).symm

/-- Arbitrary finite cut-tree source descent is equivalent to genuine leaf evidence. -/
theorem fivefoldP77RawPatchTree_witness_iff
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    Nonempty (FivefoldP77RawPatchTreeWitness f g h k tree) ↔
      fivefoldP77RawPatchTreeCompatible f g h k tree := by
  constructor
  · rintro ⟨witness⟩
    apply (fivefoldP77RawPatchTree_compatible_flatten f g h k tree).2
    exact (fivefoldP77RawPatchChain_witness_iff f g h k _).1
      ⟨fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness⟩
  · intro hc
    obtain ⟨witness⟩ := (fivefoldP77RawPatchChain_witness_iff f g h k _).2
      ((fivefoldP77RawPatchTree_compatible_flatten f g h k tree).1 hc)
    exact ⟨(fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree).symm witness⟩

/-- Actual finite transformation histories. No equality between these histories
is assumed or concluded. The constructors permit cuts at arbitrary depth. -/
inductive FivefoldP77RawPatchCutRoute
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      FivefoldP77RawPatchCutTree f g h k u v →
      FivefoldP77RawPatchCutTree f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | refl {u v : FivefoldPathVertex}
      (tree : FivefoldP77RawPatchCutTree f g h k u v) :
      FivefoldP77RawPatchCutRoute f g h k tree tree
  | cut {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchChain f g h k u v)
      (right : FivefoldP77RawPatchChain f g h k v w) :
      FivefoldP77RawPatchCutRoute f g h k
        (.leaf (fivefoldP77RawPatchChainAppend f g h k left right))
        (.node (.leaf left) (.leaf right))
  | assoc {u v w t : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      (middle : FivefoldP77RawPatchCutTree f g h k v w)
      (right : FivefoldP77RawPatchCutTree f g h k w t) :
      FivefoldP77RawPatchCutRoute f g h k
        (.node (.node left middle) right) (.node left (.node middle right))
  | symm {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchCutRoute f g h k source target) :
      FivefoldP77RawPatchCutRoute f g h k target source
  | trans {u v : FivefoldPathVertex}
      {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
      (firstRoute : FivefoldP77RawPatchCutRoute f g h k source middle)
      (secondRoute : FivefoldP77RawPatchCutRoute f g h k middle target) :
      FivefoldP77RawPatchCutRoute f g h k source target
  | left {u v w : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchCutRoute f g h k source target)
      (right : FivefoldP77RawPatchCutTree f g h k v w) :
      FivefoldP77RawPatchCutRoute f g h k (.node source right) (.node target right)
  | right {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      {source target : FivefoldP77RawPatchCutTree f g h k v w}
      (route : FivefoldP77RawPatchCutRoute f g h k source target) :
      FivefoldP77RawPatchCutRoute f g h k (.node left source) (.node left target)

/-- Every finite cut/inverse/reassociation/context history preserves the full chain. -/
theorem fivefoldP77RawPatchCutRoute_flatten
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    fivefoldP77RawPatchTreeFlatten f g h k source =
      fivefoldP77RawPatchTreeFlatten f g h k target := by
  induction route with
  | refl tree => rfl
  | cut left right => rfl
  | assoc left middle right =>
      exact fivefoldP77RawPatchChainAppend_assoc f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left)
        (fivefoldP77RawPatchTreeFlatten f g h k middle)
        (fivefoldP77RawPatchTreeFlatten f g h k right)
  | symm route ih => exact ih.symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih =>
      exact congrArg (fun chain => fivefoldP77RawPatchChainAppend f g h k
        chain (fivefoldP77RawPatchTreeFlatten f g h k right)) ih
  | right left route ih =>
      exact congrArg (fun chain => fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k left) chain) ih

/-- Constructive finite normalization by contextual moves and inverse cuts. -/
def fivefoldP77RawPatchTreeNormalizeRoute
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchCutRoute f g h k tree
      (.leaf (fivefoldP77RawPatchTreeFlatten f g h k tree)) := by
  induction tree with
  | leaf chain => exact .refl _
  | node left right ihLeft ihRight =>
      exact .trans (.left ihLeft right)
        (.trans (.right (.leaf (fivefoldP77RawPatchTreeFlatten f g h k left)) ihRight)
          (.symm (.cut (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right))))

/-- Complete normal-form criterion for existence of a finite cut/reassociation history. -/
theorem fivefoldP77RawPatchCutRoute_nonempty_iff
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v) :
    Nonempty (FivefoldP77RawPatchCutRoute f g h k source target) ↔
      fivefoldP77RawPatchTreeFlatten f g h k source =
        fivefoldP77RawPatchTreeFlatten f g h k target := by
  constructor
  · rintro ⟨route⟩
    exact fivefoldP77RawPatchCutRoute_flatten f g h k route
  · intro hflat
    have bridge : FivefoldP77RawPatchCutRoute f g h k
        (.leaf (fivefoldP77RawPatchTreeFlatten f g h k source))
        (.leaf (fivefoldP77RawPatchTreeFlatten f g h k target)) := by
      rw [hflat]
      exact .refl _
    exact ⟨.trans (fivefoldP77RawPatchTreeNormalizeRoute f g h k source)
      (.trans bridge (.symm (fivefoldP77RawPatchTreeNormalizeRoute f g h k target)))⟩

/-- Evaluate a history using the ACTUAL original cut Equiv and product associator. -/
def fivefoldP77RawPatchCutRouteEquiv
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    FivefoldP77RawPatchTreeWitness f g h k source ≃
      FivefoldP77RawPatchTreeWitness f g h k target := by
  induction route with
  | refl tree => exact Equiv.refl _
  | cut left right => exact fivefoldP77RawPatchChainCutWitnessEquiv f g h k left right
  | assoc left middle right => exact Equiv.prodAssoc _ _ _
  | symm route ih => exact ih.symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih => exact Equiv.prodCongr ih (Equiv.refl _)
  | right left route ih => exact Equiv.prodCongr (Equiv.refl _) ih

/-- Canonical comparison through the common, exact original flattened chain. -/
def fivefoldP77RawPatchTreeComparisonEquiv
    {u v : FivefoldPathVertex}
    (source target : FivefoldP77RawPatchCutTree f g h k u v)
    (hflat : fivefoldP77RawPatchTreeFlatten f g h k source =
      fivefoldP77RawPatchTreeFlatten f g h k target) :
    FivefoldP77RawPatchTreeWitness f g h k source ≃
      FivefoldP77RawPatchTreeWitness f g h k target :=
  ((fivefoldP77RawPatchTreeNormalizeEquiv f g h k source).trans
    (Equiv.cast (congrArg (FivefoldP77RawPatchChainWitness f g h k) hflat))).trans
      (fivefoldP77RawPatchTreeNormalizeEquiv f g h k target).symm

/-- Every finite history induces precisely the canonical normal-form comparison. -/
theorem fivefoldP77RawPatchCutRouteEquiv_eq_comparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    fivefoldP77RawPatchCutRouteEquiv f g h k route =
      fivefoldP77RawPatchTreeComparisonEquiv f g h k source target
        (fivefoldP77RawPatchCutRoute_flatten f g h k route) := by
  apply Equiv.ext
  intro witness
  letI : Subsingleton (FivefoldP77RawPatchTreeWitness f g h k target) :=
    fivefoldP77RawPatchTree_witness_subsingleton f g h k target
  exact Subsingleton.elim _ _

/-- Arbitrary finite cut-order coherence of the actual induced Type equivalences.
This does NOT assert equality of the transformation histories themselves. -/
theorem fivefoldP77RawPatchCutRouteEquiv_independent
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route₁ route₂ : FivefoldP77RawPatchCutRoute f g h k source target) :
    fivefoldP77RawPatchCutRouteEquiv f g h k route₁ =
      fivefoldP77RawPatchCutRouteEquiv f g h k route₂ := by
  rw [fivefoldP77RawPatchCutRouteEquiv_eq_comparison,
    fivefoldP77RawPatchCutRouteEquiv_eq_comparison]

/-- The normalized original Type witness is conserved through every finite history. -/
theorem fivefoldP77RawPatchCutRouteEquiv_normalize
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeNormalizeEquiv f g h k target
        (fivefoldP77RawPatchCutRouteEquiv f g h k route witness) =
      Eq.mp (congrArg (FivefoldP77RawPatchChainWitness f g h k)
        (fivefoldP77RawPatchCutRoute_flatten f g h k route))
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k source witness) := by
  letI : Subsingleton (FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchTreeFlatten f g h k target)) :=
    fivefoldP77RawPatchChain_witness_subsingleton f g h k _
  exact Subsingleton.elim _ _

/-- Compose the true source paths according to the tree, before flattening. -/
def fivefoldP77RawPatchTreePath
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    FivefoldP77RawPatchTreeWitness f g h k tree → Quiver.Path u v := by
  induction tree with
  | leaf chain => exact fivefoldP77RawPatchChainPath f g h k chain
  | node left right ihLeft ihRight =>
      intro witness
      exact (ihLeft witness.1).comp (ihRight witness.2)

/-- Tree-parenthesized path composition equals original chain normalization. -/
theorem fivefoldP77RawPatchTreePath_normalize
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k tree,
      fivefoldP77RawPatchTreePath f g h k tree witness =
        fivefoldP77RawPatchChainPath f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k tree)
          (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness) := by
  induction tree with
  | leaf chain => intro witness; rfl
  | node left right ihLeft ihRight =>
      rintro ⟨wLeft, wRight⟩
      change
        (fivefoldP77RawPatchTreePath f g h k left wLeft).comp
          (fivefoldP77RawPatchTreePath f g h k right wRight) =
        fivefoldP77RawPatchChainPath f g h k
          (fivefoldP77RawPatchChainAppend f g h k
            (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right))
          (fivefoldP77RawPatchChainAppendWitness f g h k
            (fivefoldP77RawPatchTreeFlatten f g h k left)
            (fivefoldP77RawPatchTreeFlatten f g h k right)
            (fivefoldP77RawPatchTreeNormalizeEquiv f g h k left wLeft)
            (fivefoldP77RawPatchTreeNormalizeEquiv f g h k right wRight))
      rw [fivefoldP77RawPatchChainAppend_path, ihLeft wLeft, ihRight wRight]

/-- Dependent transport preserves actual source paths, not merely their lengths. -/
theorem fivefoldP77RawPatchChainPath_transport
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchChain f g h k u v}
    (heq : source = target)
    (witness : FivefoldP77RawPatchChainWitness f g h k source) :
    fivefoldP77RawPatchChainPath f g h k target
      (Eq.mp (congrArg (FivefoldP77RawPatchChainWitness f g h k) heq) witness) =
      fivefoldP77RawPatchChainPath f g h k source witness := by
  cases heq
  rfl

/-- Every finite cut/reassociation history preserves the exact original source path. -/
theorem fivefoldP77RawPatchCutRoute_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreePath f g h k target
        (fivefoldP77RawPatchCutRouteEquiv f g h k route witness) =
      fivefoldP77RawPatchTreePath f g h k source witness := by
  rw [fivefoldP77RawPatchTreePath_normalize,
    fivefoldP77RawPatchCutRouteEquiv_normalize,
    fivefoldP77RawPatchChainPath_transport f g h k
      (fivefoldP77RawPatchCutRoute_flatten f g h k route)
      (fivefoldP77RawPatchTreeNormalizeEquiv f g h k source witness)]
  exact (fivefoldP77RawPatchTreePath_normalize f g h k source witness).symm

/-- The genuine original P77 target class with an actual source reachability proof. -/
def fivefoldP77RawPatchTreeCertified
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k tree) :
    FivefoldP77PartialDomain f g h k u v :=
  fivefoldP77RawPatchChainCertified f g h k
    (fivefoldP77RawPatchTreeFlatten f g h k tree)
    (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness)

/-- The certified value remains the actual original raw-patch target composite. -/
theorem fivefoldP77RawPatchTreeCertified_val
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k tree) :
    (fivefoldP77RawPatchTreeCertified f g h k tree witness).val =
      fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchTreeFlatten f g h k tree) :=
  fivefoldP77RawPatchChainCertified_val f g h k _ _

/-- Actual original partial recovery returns the tree-parenthesized source path. -/
theorem fivefoldP77RawPatchTreeCertified_recover
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v)
    (witness : FivefoldP77RawPatchTreeWitness f g h k tree) :
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77RawPatchTreeCertified f g h k tree witness) =
      fivefoldP77RawPatchTreePath f g h k tree witness :=
  (fivefoldP77RawPatchChainCertified_recover f g h k _ _).trans
    (fivefoldP77RawPatchTreePath_normalize f g h k tree witness).symm

/-- Any finite recut history preserves the entire source-certified partial Hom. -/
theorem fivefoldP77RawPatchCutRoute_certified
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k source) :
    fivefoldP77RawPatchTreeCertified f g h k target
        (fivefoldP77RawPatchCutRouteEquiv f g h k route witness) =
      fivefoldP77RawPatchTreeCertified f g h k source witness := by
  letI := fivefoldP77ConservativeCategory f g h k
  apply Subtype.ext
  rw [fivefoldP77RawPatchTreeCertified_val, fivefoldP77RawPatchTreeCertified_val]
  exact congrArg (fivefoldP77RawPatchChainTarget f g h k)
    (fivefoldP77RawPatchCutRoute_flatten f g h k route).symm

/-- Necessary-and-sufficient local evidence is invariant under every finite history. -/
theorem fivefoldP77RawPatchCutRoute_compatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target) :
    fivefoldP77RawPatchTreeCompatible f g h k source ↔
      fivefoldP77RawPatchTreeCompatible f g h k target := by
  rw [fivefoldP77RawPatchTree_compatible_flatten,
    fivefoldP77RawPatchTree_compatible_flatten,
    fivefoldP77RawPatchCutRoute_flatten f g h k route]

/-- At least one designated leaf lacks the genuine local five-cell certificate. -/
def fivefoldP77RawPatchTreeObstructed
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) : Prop :=
  match tree with
  | .leaf chain => ¬ fivefoldP77RawPatchChainCompatible f g h k chain
  | .node left right =>
      fivefoldP77RawPatchTreeObstructed f g h k left ∨
        fivefoldP77RawPatchTreeObstructed f g h k right

/-- Exact finite-tree obstruction boundary, still entirely factorwise. -/
theorem fivefoldP77RawPatchTree_obstructed_iff
    {u v : FivefoldPathVertex}
    (tree : FivefoldP77RawPatchCutTree f g h k u v) :
    fivefoldP77RawPatchTreeObstructed f g h k tree ↔
      ¬ fivefoldP77RawPatchTreeCompatible f g h k tree := by
  classical
  induction tree with
  | leaf chain => rfl
  | node left right ihLeft ihRight =>
      change (fivefoldP77RawPatchTreeObstructed f g h k left ∨
        fivefoldP77RawPatchTreeObstructed f g h k right) ↔
        ¬ (fivefoldP77RawPatchTreeCompatible f g h k left ∧
          fivefoldP77RawPatchTreeCompatible f g h k right)
      rw [ihLeft, ihRight]
      tauto

/-- No finite cut order or reparenthesization repairs a missing designated source
certificate. This says nothing about another factorization of a whole target Hom. -/
theorem fivefoldP77RawPatchCutRoute_obstruction
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (route : FivefoldP77RawPatchCutRoute f g h k source target)
    (hmissing : fivefoldP77RawPatchTreeObstructed f g h k source) :
    ¬ Nonempty (FivefoldP77RawPatchTreeWitness f g h k target) := by
  intro hw
  have hc := (fivefoldP77RawPatchTree_witness_iff f g h k target).1 hw
  exact ((fivefoldP77RawPatchTree_obstructed_iff f g h k source).1 hmissing)
    ((fivefoldP77RawPatchCutRoute_compatible_iff f g h k route).2 hc)

#print axioms fivefoldP77RawPatchTreeNormalizeEquiv
#print axioms fivefoldP77RawPatchTree_witness_subsingleton
#print axioms fivefoldP77RawPatchTree_compatible_flatten
#print axioms fivefoldP77RawPatchTree_witness_iff
#print axioms fivefoldP77RawPatchCutRoute_flatten
#print axioms fivefoldP77RawPatchTreeNormalizeRoute
#print axioms fivefoldP77RawPatchCutRoute_nonempty_iff
#print axioms fivefoldP77RawPatchCutRouteEquiv
#print axioms fivefoldP77RawPatchTreeComparisonEquiv
#print axioms fivefoldP77RawPatchCutRouteEquiv_eq_comparison
#print axioms fivefoldP77RawPatchCutRouteEquiv_independent
#print axioms fivefoldP77RawPatchCutRouteEquiv_normalize
#print axioms fivefoldP77RawPatchTreePath
#print axioms fivefoldP77RawPatchTreePath_normalize
#print axioms fivefoldP77RawPatchChainPath_transport
#print axioms fivefoldP77RawPatchCutRoute_path
#print axioms fivefoldP77RawPatchTreeCertified
#print axioms fivefoldP77RawPatchTreeCertified_val
#print axioms fivefoldP77RawPatchTreeCertified_recover
#print axioms fivefoldP77RawPatchCutRoute_certified
#print axioms fivefoldP77RawPatchCutRoute_compatible_iff
#print axioms fivefoldP77RawPatchTree_obstructed_iff
#print axioms fivefoldP77RawPatchCutRoute_obstruction

end
end KUOS.Architecture.WuxingPentagonUnified
