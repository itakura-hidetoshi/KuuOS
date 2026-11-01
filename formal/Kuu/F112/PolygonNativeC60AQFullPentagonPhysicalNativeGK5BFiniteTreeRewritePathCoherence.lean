import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFiniteEndofunctorTreeCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5B — actual finite target-tree associator/unitor rewrite
PATHS, their genuine Mathlib NatIso witnesses and exact normalization.

GK5A already proves the recursively constructed chosen-inverse whole
NatIso equals direct GK4BT Theta for EVERY finite binary endofunctor
tree. GK5B goes beyond endpoint equality and introduces proof-relevant
actual rewrite steps: associator, left/right unitor, and their genuine
left/right whiskering. Finite paths contain identity, single step,
reversal and typed concatenation. Path evaluation uses actual Mathlib
NatIso compositions, not invented raw source higher cells.

We prove every real rewrite-path NatIso equals the canonical eqToIso
of its whole-functor equality, hence all actual paths with the same
typed endpoints agree as whole NatIso. Rewrite paths preserve ordered
leaf words; normalization by GK5A's finite-list fold commutes with
arbitrary paths after exact eqToIso leaf transport. The genuine
chosen-inverse Theta transport is independent of rewrite-path
presentation by GK5A/GK4BU; an explicit associator/right-unitor
two-route example gives nontrivial real paths.

Scoped to finite endofunctor trees of ONE actual target category.
No definitional Q_T = P_T, source-Q category laws, raw F54/F55/P92B
Type-valued higher cells, original S unconditional faithfulness,
ambient unattained integer matrices, global Gray, or hyperdescent.
Strict 空 centered; independent Kuu one presentation.
Append-only, tighten-only, overwrite-forbidden, same-root107.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

/-- Proof-relevant, typed REAL Mathlib target rewrite steps.
The constructors refer to GK5A finite endofunctor trees, not
original raw F54/F55/P92B higher cells. -/
inductive NativeGK5BRewriteStep (T : Type uT) [Category.{vT} T] :
    NativeGK5AFiniteTargetTree T → NativeGK5AFiniteTargetTree T → Type _ where
  | assoc (a b c : NativeGK5AFiniteTargetTree T) :
      NativeGK5BRewriteStep T (.paste (.paste a b) c) (.paste a (.paste b c))
  | leftUnit (a : NativeGK5AFiniteTargetTree T) :
      NativeGK5BRewriteStep T (.paste .unit a) a
  | rightUnit (a : NativeGK5AFiniteTargetTree T) :
      NativeGK5BRewriteStep T (.paste a .unit) a
  | whiskerRight {a b : NativeGK5AFiniteTargetTree T}
      (h : NativeGK5BRewriteStep T a b) (c : NativeGK5AFiniteTargetTree T) :
      NativeGK5BRewriteStep T (.paste a c) (.paste b c)
  | whiskerLeft (a : NativeGK5AFiniteTargetTree T)
      {b c : NativeGK5AFiniteTargetTree T}
      (h : NativeGK5BRewriteStep T b c) :
      NativeGK5BRewriteStep T (.paste a b) (.paste a c)

/-- A finite proof-relevant path made of genuine associator/unitor
steps, reversals, and actual concatenation. -/
inductive NativeGK5BRewritePath (T : Type uT) [Category.{vT} T] :
    NativeGK5AFiniteTargetTree T → NativeGK5AFiniteTargetTree T → Type _ where
  | refl (a : NativeGK5AFiniteTargetTree T) :
      NativeGK5BRewritePath T a a
  | basic {a b : NativeGK5AFiniteTargetTree T}
      (h : NativeGK5BRewriteStep T a b) :
      NativeGK5BRewritePath T a b
  | reverse {a b : NativeGK5AFiniteTargetTree T}
      (p : NativeGK5BRewritePath T a b) :
      NativeGK5BRewritePath T b a
  | trans {a b c : NativeGK5AFiniteTargetTree T}
      (p : NativeGK5BRewritePath T a b)
      (q : NativeGK5BRewritePath T b c) :
      NativeGK5BRewritePath T a c

section ActualRewritePaths
variable {T : Type uT} [Category.{vT} T]

/-- Every single genuine rewrite has an equality of WHOLE Mathlib
target endofunctors, from real associativity and left/right unit. -/
def nativeGK5BStepEq :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewriteStep T a b →
        nativeGK5ATreeComposite a = nativeGK5ATreeComposite b
  | _, _, .assoc a b c =>
      Functor.assoc (nativeGK5ATreeComposite a)
        (nativeGK5ATreeComposite b) (nativeGK5ATreeComposite c)
  | _, _, .leftUnit a =>
      Functor.id_comp (nativeGK5ATreeComposite a)
  | _, _, .rightUnit a =>
      Functor.comp_id (nativeGK5ATreeComposite a)
  | _, _, .whiskerRight h c =>
      congrArg
        (fun F : T ⥤ T => F ⋙ nativeGK5ATreeComposite c)
        (nativeGK5BStepEq h)
  | _, _, .whiskerLeft a h =>
      congrArg
        (fun F : T ⥤ T => nativeGK5ATreeComposite a ⋙ F)
        (nativeGK5BStepEq h)

/-- Actual typed Mathlib NatIso corresponding to EACH rewrite step.
Functor.associator, leftUnitor, rightUnitor and iso-whiskering
are retained as genuine constructed proof objects. -/
noncomputable def nativeGK5BStepIso :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewriteStep T a b →
        nativeGK5ATreeComposite a ≅ nativeGK5ATreeComposite b
  | _, _, .assoc a b c =>
      Functor.associator (nativeGK5ATreeComposite a)
        (nativeGK5ATreeComposite b) (nativeGK5ATreeComposite c)
  | _, _, .leftUnit a =>
      Functor.leftUnitor (nativeGK5ATreeComposite a)
  | _, _, .rightUnit a =>
      Functor.rightUnitor (nativeGK5ATreeComposite a)
  | _, _, .whiskerRight h c =>
      Functor.isoWhiskerRight (nativeGK5BStepIso h)
        (nativeGK5ATreeComposite c)
  | _, _, .whiskerLeft a h =>
      Functor.isoWhiskerLeft (nativeGK5ATreeComposite a)
        (nativeGK5BStepIso h)

/-- The canonical whole-functor equality induced by a path.
Proof relevance is retained in its path, but equality proofs
are propositionally proof-irrelevant in Lean. -/
def nativeGK5BPathEq :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewritePath T a b →
        nativeGK5ATreeComposite a = nativeGK5ATreeComposite b
  | _, _, .refl _ => rfl
  | _, _, .basic h => nativeGK5BStepEq h
  | _, _, .reverse p => (nativeGK5BPathEq p).symm
  | _, _, .trans p q => (nativeGK5BPathEq p).trans (nativeGK5BPathEq q)

/-- Genuine whole NatIso denotation for an arbitrary rewrite path.
It is built by composing REAL Mathlib associators and unitors. -/
noncomputable def nativeGK5BPathIso :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewritePath T a b →
        nativeGK5ATreeComposite a ≅ nativeGK5ATreeComposite b
  | _, _, .refl _ => Iso.refl _
  | _, _, .basic h => nativeGK5BStepIso h
  | _, _, .reverse p => (nativeGK5BPathIso p).symm
  | _, _, .trans p q => nativeGK5BPathIso p ≪≫ nativeGK5BPathIso q

private theorem nativeGK5BWhiskerRight_eqToIso
    {F G : T ⥤ T} (h : F = G) (H : T ⥤ T) :
    Functor.isoWhiskerRight (eqToIso h) H =
      eqToIso (congrArg (fun K : T ⥤ T => K ⋙ H) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerRight_refl]

private theorem nativeGK5BWhiskerLeft_eqToIso
    (F : T ⥤ T) {G H : T ⥤ T} (h : G = H) :
    Functor.isoWhiskerLeft F (eqToIso h) =
      eqToIso (congrArg (fun K : T ⥤ T => F ⋙ K) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerLeft_refl]

private theorem nativeGK5BEqToIso_symm
    {F G : T ⥤ T} (h : F = G) :
    (eqToIso h).symm = eqToIso h.symm := by
  cases h
  rfl

/-- The ACTUAL Mathlib associator/unitor and their typed
whiskerings are the canonical equality transports of the
corresponding true whole-functor equations. -/
theorem nativeGK5BStepIso_eqToIso
    {a b : NativeGK5AFiniteTargetTree T}
    (h : NativeGK5BRewriteStep T a b) :
    nativeGK5BStepIso h = eqToIso (nativeGK5BStepEq h) := by
  induction h with
  | assoc a b c =>
      apply Iso.ext
      ext Z
      rfl
  | leftUnit a =>
      apply Iso.ext
      ext Z
      rfl
  | rightUnit a =>
      apply Iso.ext
      ext Z
      rfl
  | whiskerRight h c ih =>
      simpa only [nativeGK5BStepIso, nativeGK5BStepEq, ih] using
        (nativeGK5BWhiskerRight_eqToIso (nativeGK5BStepEq h)
          (nativeGK5ATreeComposite c))
  | whiskerLeft a h ih =>
      simpa only [nativeGK5BStepIso, nativeGK5BStepEq, ih] using
        (nativeGK5BWhiskerLeft_eqToIso (nativeGK5ATreeComposite a)
          (nativeGK5BStepEq h))

/-- Arbitrary finite real rewrite path: its genuine whole Mathlib
NatIso is EXACTLY the canonical eqToIso of the path's actual
whole target-functor equality, by structural induction on paths. -/
theorem nativeGK5BPathIso_eqToIso
    {a b : NativeGK5AFiniteTargetTree T}
    (p : NativeGK5BRewritePath T a b) :
    nativeGK5BPathIso p = eqToIso (nativeGK5BPathEq p) := by
  induction p with
  | refl _ => rfl
  | basic h =>
      exact nativeGK5BStepIso_eqToIso h
  | reverse p ih =>
      simpa only [nativeGK5BPathIso, nativeGK5BPathEq, ih,
        nativeGK5BEqToIso_symm]
  | trans p q ihp ihq =>
      simpa only [nativeGK5BPathIso, nativeGK5BPathEq,
        ihp, ihq, eqToIso_trans]

/-- PATH INDEPENDENCE: ANY two real Mathlib associator/unitor
rewrite paths with the same typed endpoints have IDENTICAL
whole NatIso witnesses. This compares ACTUAL constructed
pasting morphisms, not new raw higher-dimensional fillers. -/
theorem nativeGK5BPath_independent
    {a b : NativeGK5AFiniteTargetTree T}
    (p q : NativeGK5BRewritePath T a b) :
    nativeGK5BPathIso p = nativeGK5BPathIso q := by
  rw [nativeGK5BPathIso_eqToIso p, nativeGK5BPathIso_eqToIso q]
  rfl

/-- Every genuine individual step respects the ordered leaf
sequence, including associator, left/right unit and whiskering. -/
theorem nativeGK5BStepLeaves
    {a b : NativeGK5AFiniteTargetTree T}
    (h : NativeGK5BRewriteStep T a b) :
    nativeGK5ATreeLeaves a = nativeGK5ATreeLeaves b := by
  induction h with
  | assoc a b c =>
      simp only [nativeGK5ATreeLeaves, List.append_assoc]
  | leftUnit a =>
      simp [nativeGK5ATreeLeaves]
  | rightUnit a =>
      simp [nativeGK5ATreeLeaves]
  | whiskerRight h c ih =>
      change nativeGK5ATreeLeaves _ ++ nativeGK5ATreeLeaves c =
        nativeGK5ATreeLeaves _ ++ nativeGK5ATreeLeaves c
      exact congrArg (fun rs => rs ++ nativeGK5ATreeLeaves c) ih
  | whiskerLeft a h ih =>
      change nativeGK5ATreeLeaves a ++ nativeGK5ATreeLeaves _ =
        nativeGK5ATreeLeaves a ++ nativeGK5ATreeLeaves _
      exact congrArg (fun rs => nativeGK5ATreeLeaves a ++ rs) ih

/-- Every finite rewrite path preserves the complete ordered
list of actual non-unit target endofunctors. -/
theorem nativeGK5BPathLeaves
    {a b : NativeGK5AFiniteTargetTree T}
    (p : NativeGK5BRewritePath T a b) :
    nativeGK5ATreeLeaves a = nativeGK5ATreeLeaves b := by
  induction p with
  | refl _ => rfl
  | basic h => exact nativeGK5BStepLeaves h
  | reverse p ih => exact ih.symm
  | trans p q ihp ihq => exact ihp.trans ihq

/-- Canonical finite target normalization iso, with a real
Mathlib eqToIso witness of GK5A's finite-list fold theorem. -/
noncomputable def nativeGK5BTreeNormalization
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5ATreeComposite t ≅
      nativeGK5AListComposite (nativeGK5ATreeLeaves t) :=
  eqToIso (nativeGK5ATreeComposite_eq_list t)

/-- Normalization is PATH-INDEPENDENT: for EVERY actually constructed
finite rewrite path a→b, its genuine NatIso followed by b's
finite-word normalization and the leaf equality transport is
EXACTLY a's normalization. This proves real confluence relative to
all paths that already exist; no global rewrite reachability claim. -/
theorem nativeGK5BPath_normalization
    {a b : NativeGK5AFiniteTargetTree T}
    (p : NativeGK5BRewritePath T a b) :
    nativeGK5BPathIso p ≪≫ nativeGK5BTreeNormalization b ≪≫
      eqToIso (congrArg
        (fun rs : List (T ⥤ T) => nativeGK5AListComposite rs)
        (nativeGK5BPathLeaves p).symm) =
    nativeGK5BTreeNormalization a := by
  simp only [nativeGK5BPathIso_eqToIso,
    nativeGK5BTreeNormalization, eqToIso_trans]

end ActualRewritePaths

section ChosenInverseRewriteTransport
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- Every genuine rewrite path yields a whole target natural
transformation modification square for GK5A's recursive
chosen-inverse Θ, without claiming strict Q_T=P_T. -/
theorem nativeGK5BChosenInverse_rewritePath_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {left right : NativeGK5AFiniteTargetTree T}
    (path : NativeGK5BRewritePath T left right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5BPathIso path).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5AChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5BPathIso path).hom) :=
  nativeGK5AChosenInverse_treeNat_square p ma mb pa pb left right
    (nativeGK5BPathIso path).hom

/-- Any two actual rewrite paths induce identical WHOLE left
and right target-NatTrans pastings with the arbitrary-choice
inverse comparison. Both paths have the same real typed ends. -/
theorem nativeGK5BChosenInverse_twoPaths_agree
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {left right : NativeGK5AFiniteTargetTree T}
    (pathA pathB : NativeGK5BRewritePath T left right) :
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5BPathIso pathA).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb right).hom) =
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5BPathIso pathB).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb right).hom) ∧
    ((nativeGK5AChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5BPathIso pathA).hom)) =
    ((nativeGK5AChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5BPathIso pathB).hom)) := by
  rw [nativeGK5BPath_independent pathA pathB]
  all_goals simp

/-- The true whole chosen-inverse NatIso of each endpoint agrees
after applying the ACTUAL double eqToIso boundary transport arising
from any real associator/unitor rewrite path. -/
theorem nativeGK5BChosenInverse_rewritePath_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {left right : NativeGK5AFiniteTargetTree T}
    (path : NativeGK5BRewritePath T left right) :
    eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK5BPathEq path)) ≪≫
      nativeGK5AChosenInverse_treeIso p ma mb pa pb right ≪≫
      eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5BPathEq path).symm) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb left := by
  simpa only [nativeGK5AChosenInverse_treeIso_eq_direct] using
    (nativeGK5AChosenInverse_eqTransport p ma mb pa pb
      (nativeGK5ATreeComposite left)
      (nativeGK5ATreeComposite right)
      (nativeGK5BPathEq path))

end ChosenInverseRewriteTransport

section ConcreteTwoRoutes
variable {T : Type uT} [Category.{vT} T]

/-- A nontrivial route: eliminate the right identity inside the
left subtree before applying the genuine associator. -/
def nativeGK5BMiddleUnit_pathA
    (a b c : NativeGK5AFiniteTargetTree T) :
    NativeGK5BRewritePath T
      (.paste (.paste (.paste a .unit) b) c)
      (.paste a (.paste b c)) :=
  .trans
    (.basic (.whiskerRight
      (.whiskerRight (.rightUnit a) b) c))
    (.basic (.assoc a b c))

/-- A different genuine route: apply associator first, then
whisker the real right unitor across the right subtree. -/
def nativeGK5BMiddleUnit_pathB
    (a b c : NativeGK5AFiniteTargetTree T) :
    NativeGK5BRewritePath T
      (.paste (.paste (.paste a .unit) b) c)
      (.paste a (.paste b c)) :=
  .trans
    (.basic (.assoc (.paste a .unit) b c))
    (.basic (.whiskerRight (.rightUnit a) (.paste b c)))

/-- Exact whole NatIso equality of the above two physically
different genuine Mathlib associator/unitor pasting routes. -/
theorem nativeGK5BMiddleUnit_twoRoutes_coherent
    (a b c : NativeGK5AFiniteTargetTree T) :
    nativeGK5BPathIso (nativeGK5BMiddleUnit_pathA a b c) =
      nativeGK5BPathIso (nativeGK5BMiddleUnit_pathB a b c) :=
  nativeGK5BPath_independent
    (nativeGK5BMiddleUnit_pathA a b c)
    (nativeGK5BMiddleUnit_pathB a b c)

end ConcreteTwoRoutes

#print axioms nativeGK5BStepEq
#print axioms nativeGK5BStepIso
#print axioms nativeGK5BPathEq
#print axioms nativeGK5BPathIso
#print axioms nativeGK5BStepIso_eqToIso
#print axioms nativeGK5BPathIso_eqToIso
#print axioms nativeGK5BPath_independent
#print axioms nativeGK5BStepLeaves
#print axioms nativeGK5BPathLeaves
#print axioms nativeGK5BTreeNormalization
#print axioms nativeGK5BPath_normalization
#print axioms nativeGK5BChosenInverse_rewritePath_square
#print axioms nativeGK5BChosenInverse_twoPaths_agree
#print axioms nativeGK5BChosenInverse_rewritePath_transport
#print axioms nativeGK5BMiddleUnit_pathA
#print axioms nativeGK5BMiddleUnit_pathB
#print axioms nativeGK5BMiddleUnit_twoRoutes_coherent

end
end Kuu.F112.Physical
