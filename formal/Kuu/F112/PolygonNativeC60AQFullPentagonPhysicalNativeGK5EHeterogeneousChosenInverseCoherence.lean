import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5DTypedManyCategoryFunctorChains
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5E — genuine chosen-inverse target coherence for arbitrary
finite MANY-CATEGORY, source-and-target-indexed target-functor trees.

GK5D constructs actual typed finite words, binary trees, associator /
unitor / whiskering rewrite paths and their canonical reachability.
GK5E combines those real paths with GK4BM's arbitrary chosen inverse
and GK4BT/GK4BW/GK4BU's genuine Mathlib chosen-inverse comparison.

For every typed finite tree t : Tree C i j we recursively paste actual
GK4BW whole NatIso values, then prove equality to the direct GK4BT
comparison at its entire composite functor. No strict naturality of
the arbitrary chosen inverse is assumed. Every genuine typed path
yields a whole NatTrans modification square and an exact both-end
eqToIso transport equality, including concrete normalization paths.

Scope: fixed-universe-pair bundled Mathlib categories, finite typed
functor chains and their real structural rewrites. No original raw
F54/F55/P92B Type-valued high cells, arbitrary universe-varying
chains, unconstrained source-Q axioms, Gray or hyperdescent.
Chosen Q and explicit P are NOT identified definitionally.
Existing GK4BQ's genuine kappa comparison remains essential.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uI vC uC

section HeterogeneousChosenInverse
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {I : Type uI} {C : I → Cat.{vC,uC}}

/-- Recursively pasted GENUINE chosen-inverse whole NatIso for every
finite, source-and-target-indexed tree of target functors. Each paste
uses the already proved GK4BW typed binary-pasting construction. -/
noncomputable def nativeGK5EChosenInverse_treeIso
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      (nativeGK4BNPostcompCompatible p ma mb pa pb
          (nativeGK5DTreeComposite t) ⋙
        nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≅
      (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb ⋙
        nativeGK4BNPostcompAttained p ma mb pa pb
          (nativeGK5DTreeComposite t))
  | _, _, .unit i =>
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 (C i))
  | _, _, .atom R =>
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R
  | _, _, .paste left right =>
      nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb
        (nativeGK5DTreeComposite left)
        (nativeGK5DTreeComposite right)
        (nativeGK5EChosenInverse_treeIso p ma mb pa pb left)
        (nativeGK5EChosenInverse_treeIso p ma mb pa pb right)

/-- Every recursively pasted GENUINE heterogeneous GK4BW NatIso is
equal as a WHOLE Mathlib NatIso to direct GK4BT Theta for the
entire composite. Neither inverse presentation is strictified. -/
theorem nativeGK5EChosenInverse_treeIso_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5EChosenInverse_treeIso p ma mb pa pb t =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb
        (nativeGK5DTreeComposite t) := by
  induction t with
  | unit _ => rfl
  | atom R => rfl
  | paste left right hl hr =>
      change nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb
          (nativeGK5DTreeComposite left)
          (nativeGK5DTreeComposite right)
          (nativeGK5EChosenInverse_treeIso p ma mb pa pb left)
          (nativeGK5EChosenInverse_treeIso p ma mb pa pb right) =
        nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb
          (nativeGK5DTreeComposite left ⋙ nativeGK5DTreeComposite right)
      rw [hl, hr]
      exact
        (nativeGK4BWChosenInverse_binaryPasting_ofTheta p ma mb pa pb
          (nativeGK5DTreeComposite left)
          (nativeGK5DTreeComposite right)).trans
        (nativeGK4BVChosenInverse_composition_coherence p ma mb pa pb
          (nativeGK5DTreeComposite left)
          (nativeGK5DTreeComposite right))

/-- Whole target NatTrans naturality for ANY actual transformation
between composite functors of two trees with the SAME typed
source and destination categories, even if these categories differ. -/
theorem nativeGK5EChosenInverse_treeNat_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (left right : NativeGK5DTypedTree C i j)
    (ρ : nativeGK5DTreeComposite left ⟶ nativeGK5DTreeComposite right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) := by
  simpa only [nativeGK5EChosenInverse_treeIso_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb ρ)

/-- Every proof-relevant heterogeneous GK5D rewrite path yields an
ACTUAL whole Mathlib NatTrans naturality square for the arbitrary
choice-based GK4BM inverse and its GK4BQ comparison. -/
theorem nativeGK5EChosenInverse_rewritePath_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} {left right : NativeGK5DTypedTree C i j}
    (path : NativeGK5DTypedPath C left right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso path).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso path).hom) :=
  nativeGK5EChosenInverse_treeNat_square p ma mb pa pb left right
    (nativeGK5DPathIso path).hom

/-- All real rewrite paths with the same typed endpoints induce
identical entire left/right chosen-inverse pastings, not merely
pointwise component agreement or a new informal high cell. -/
theorem nativeGK5EChosenInverse_twoPaths_agree
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} {left right : NativeGK5DTypedTree C i j}
    (pathA pathB : NativeGK5DTypedPath C left right) :
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso pathA).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb right).hom) =
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso pathB).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb right).hom) ∧
    ((nativeGK5EChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso pathA).hom)) =
    ((nativeGK5EChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso pathB).hom)) := by
  rw [nativeGK5DPath_independent pathA pathB]
  all_goals simp

/-- Real double boundary eqToIso transport between ANY equal whole
heterogeneous target functors. The chosen inverse Q_i, Q_j are NOT
definitionally equal to explicit inverses P_i, P_j. -/
theorem nativeGK5EChosenInverse_eqTransport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (F G : C i ⥤ C j) (h : F = G) :
    eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) h) ≪≫
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb G ≪≫
      eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K) h.symm) =
    nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb F := by
  cases h
  simp

/-- Whole chosen-inverse NatIso agreement along every actual typed
rewrite path, using genuine eqToIso at BOTH boundary functors. -/
theorem nativeGK5EChosenInverse_rewritePath_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} {left right : NativeGK5DTypedTree C i j}
    (path : NativeGK5DTypedPath C left right) :
    eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb)
        (nativeGK5DPathEq path)) ≪≫
      nativeGK5EChosenInverse_treeIso p ma mb pa pb right ≪≫
      eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5DPathEq path).symm) =
    nativeGK5EChosenInverse_treeIso p ma mb pa pb left := by
  simpa only [nativeGK5EChosenInverse_treeIso_eq_direct] using
    (nativeGK5EChosenInverse_eqTransport p ma mb pa pb
      (nativeGK5DTreeComposite left)
      (nativeGK5DTreeComposite right) (nativeGK5DPathEq path))

/-- Nonvacuous selected-inverse target-NatTrans compatibility along
the GK5D CONSTRUCTED normalizing path for EVERY heterogeneous tree. -/
theorem nativeGK5EChosenInverse_normalization_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5DNormalizePath t)).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t))).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb t).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5DNormalizePath t)).hom) :=
  nativeGK5EChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5DNormalizePath t)

/-- Both actual eqToIso boundaries on the chosen-inverse WHOLE NatIso
agree along the specifically CONSTRUCTED normalization path. -/
theorem nativeGK5EChosenInverse_normalization_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb)
        (nativeGK5DPathEq (nativeGK5DNormalizePath t))) ≪≫
      nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t)) ≪≫
      eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5DPathEq (nativeGK5DNormalizePath t)).symm) =
    nativeGK5EChosenInverse_treeIso p ma mb pa pb t :=
  nativeGK5EChosenInverse_rewritePath_transport p ma mb pa pb
    (nativeGK5DNormalizePath t)

/-- Equal complete dependent leaf words give a CONSTRUCTED actual
path and its genuine whole chosen-inverse target-NatTrans square. -/
theorem nativeGK5EChosenInverse_sameLeaves_canonical_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (left right : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves left = nativeGK5DTreeLeaves right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso
            (nativeGK5DPathBetweenOfSameLeaves left right h)).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso
            (nativeGK5DPathBetweenOfSameLeaves left right h)).hom) :=
  nativeGK5EChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5DPathBetweenOfSameLeaves left right h)

/-- Equal typed ordered words imply same WHOLE chosen-inverse NatIso
after both real Mathlib eqToIso boundary transports. Not a
converse semantic faithfulness claim. -/
theorem nativeGK5EChosenInverse_sameLeaves_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (left right : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves left = nativeGK5DTreeLeaves right) :
    eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := C j) p ma mb pa pb)
        (nativeGK5DTreeComposite_eq_of_leaves left right h)) ≪≫
      nativeGK5EChosenInverse_treeIso p ma mb pa pb right ≪≫
      eqToIso (congrArg
        (fun K : C i ⥤ C j =>
          nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5DTreeComposite_eq_of_leaves left right h).symm) =
    nativeGK5EChosenInverse_treeIso p ma mb pa pb left := by
  simpa only [nativeGK5EChosenInverse_treeIso_eq_direct] using
    (nativeGK5EChosenInverse_eqTransport p ma mb pa pb
      (nativeGK5DTreeComposite left)
      (nativeGK5DTreeComposite right)
      (nativeGK5DTreeComposite_eq_of_leaves left right h))

/-- Genuine three-stage *heterogeneous* associator witness applied to
the arbitrary-choice inverse, not a fictitious raw higher filler. -/
theorem nativeGK5EChosenInverse_threeStage_associator_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j k l : I} (F : C i ⥤ C j) (G : C j ⥤ C k)
    (H : C k ⥤ C l) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DStepIso (NativeGK5DTypedStep.assoc
            (NativeGK5DTypedTree.atom F)
            (NativeGK5DTypedTree.atom G)
            (NativeGK5DTypedTree.atom H))).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := C l) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (NativeGK5DTypedTree.paste (NativeGK5DTypedTree.atom F)
          (NativeGK5DTypedTree.paste (NativeGK5DTypedTree.atom G)
            (NativeGK5DTypedTree.atom H)))).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb
      (NativeGK5DTypedTree.paste
        (NativeGK5DTypedTree.paste (NativeGK5DTypedTree.atom F)
          (NativeGK5DTypedTree.atom G)) (NativeGK5DTypedTree.atom H))).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := C i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DStepIso (NativeGK5DTypedStep.assoc
            (NativeGK5DTypedTree.atom F)
            (NativeGK5DTypedTree.atom G)
            (NativeGK5DTypedTree.atom H))).hom) := by
  simpa only [nativeGK5DPathIso] using
    (nativeGK5EChosenInverse_rewritePath_square p ma mb pa pb
      (.basic (.assoc (.atom F) (.atom G) (.atom H))))

end HeterogeneousChosenInverse

#print axioms nativeGK5EChosenInverse_treeIso
#print axioms nativeGK5EChosenInverse_treeIso_eq_direct
#print axioms nativeGK5EChosenInverse_treeNat_square
#print axioms nativeGK5EChosenInverse_rewritePath_square
#print axioms nativeGK5EChosenInverse_twoPaths_agree
#print axioms nativeGK5EChosenInverse_eqTransport
#print axioms nativeGK5EChosenInverse_rewritePath_transport
#print axioms nativeGK5EChosenInverse_normalization_square
#print axioms nativeGK5EChosenInverse_normalization_transport
#print axioms nativeGK5EChosenInverse_sameLeaves_canonical_square
#print axioms nativeGK5EChosenInverse_sameLeaves_transport
#print axioms nativeGK5EChosenInverse_threeStage_associator_square

end
end Kuu.F112.Physical
