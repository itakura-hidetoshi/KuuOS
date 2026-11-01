import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5EHeterogeneousChosenInverseCoherence
import Mathlib.CategoryTheory.Category.Cat
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5F — genuine typed index-RELABELING for arbitrary finite
many-category functor words, trees, rewrite paths, and chosen inverses.

For an arbitrary index map f : I → J and actual Mathlib category family
C : J → Cat.{vC,uC}, the pullback family i ↦ C(f i) has exactly the
same underlying genuine category at each source index. We construct
actual recursively relabeled indexed words, trees, rewrite steps and
paths; prove that ordered leaves, true whole-functor evaluation,
binary pasting, and canonical right-associated trees are preserved.

We retain actual Mathlib associator/unitor/iso-whiskering path evidence,
and identify whole path NatIsos after BOTH genuine eqToIso boundary
transports. GK5E's arbitrary-choice inverse Q, distinct from explicit
P and linked by true kappa, obeys the same fully typed two-endpoint
whole NatIso transport and whole NatTrans path square after relabeling.

Index reclassification is NOT a genuine change of category objects:
this proves no arbitrary comparison for an unrelated family D over I,
no converse reflection of equal words under a noninjective f, and no
unbounded universe-varying category transport. No raw F54/F55/P92B
Type-valued high cells, source-Q axioms, Gray, or hyperdescent.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Lean v4.30.0-rc2, mathlib
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
universe uI uJ uK vC uC uD vD uE vE

section IndexRelabeling
variable {I : Type uI} {J : Type uJ}
variable (f : I → J) (C : J → Cat.{vC,uC})

/-- Relabel a truly dependent finite word through f; the actual
intermediate category is exactly C(f i) at EVERY step. -/
def nativeGK5FWordReindex :
    ∀ {i j : I},
      NativeGK5DTypedWord (fun k : I => C (f k)) i j →
      NativeGK5DTypedWord C (f i) (f j)
  | _, _, .empty i => .empty (f i)
  | _, _, .cons F xs => .cons F (nativeGK5FWordReindex xs)

/-- Relabel the source/target indices at EVERY binary tree node,
retaining the same genuine Mathlib functors at atoms. -/
def nativeGK5FTreeReindex :
    ∀ {i j : I},
      NativeGK5DTypedTree (fun k : I => C (f k)) i j →
      NativeGK5DTypedTree C (f i) (f j)
  | _, _, .unit i => .unit (f i)
  | _, _, .atom F => .atom F
  | _, _, .paste a b =>
      .paste (nativeGK5FTreeReindex a) (nativeGK5FTreeReindex b)

/-- Relabeling commutes with genuinely typed concatenation of words,
not an untyped list append. -/
theorem nativeGK5FWordReindex_append
    {i j k : I}
    (xs : NativeGK5DTypedWord (fun z : I => C (f z)) i j)
    (ys : NativeGK5DTypedWord (fun z : I => C (f z)) j k) :
    nativeGK5FWordReindex f C (nativeGK5DWordAppend xs ys) =
      nativeGK5DWordAppend
        (nativeGK5FWordReindex f C xs) (nativeGK5FWordReindex f C ys) := by
  induction xs with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5FWordReindex f C (nativeGK5DWordAppend xs ys)) =
        NativeGK5DTypedWord.cons F
          (nativeGK5DWordAppend
            (nativeGK5FWordReindex f C xs)
            (nativeGK5FWordReindex f C ys))
      rw [ih]

/-- Index relabeling does not change a whole Mathlib functor denoted
by a typed ordered word: both source/target categories are identical. -/
theorem nativeGK5FWordComposite_reindex
    {i j : I} (w : NativeGK5DTypedWord (fun z : I => C (f z)) i j) :
    nativeGK5DWordComposite (nativeGK5FWordReindex f C w) =
      nativeGK5DWordComposite w := by
  induction w with
  | empty _ => rfl
  | cons F xs ih =>
      change F ⋙ nativeGK5DWordComposite (nativeGK5FWordReindex f C xs) =
        F ⋙ nativeGK5DWordComposite
          (C := fun z : I => C (f z)) xs
      rw [ih]

/-- Index relabeling does not change the genuine WHOLE composite
functor of a finite heterogeneous typed binary tree. -/
theorem nativeGK5FTreeComposite_reindex
    {i j : I} (t : NativeGK5DTypedTree (fun z : I => C (f z)) i j) :
    nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t) =
      nativeGK5DTreeComposite t := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste left right hl hr =>
      change nativeGK5DTreeComposite (nativeGK5FTreeReindex f C left) ⋙
          nativeGK5DTreeComposite (nativeGK5FTreeReindex f C right) =
        nativeGK5DTreeComposite (C := fun z : I => C (f z)) left ⋙
          nativeGK5DTreeComposite (C := fun z : I => C (f z)) right
      rw [hl, hr]

/-- The entire ordered typed leaf word commutes exactly with
reclassification of the category index; no leaves are permuted. -/
theorem nativeGK5FTreeLeaves_reindex
    {i j : I} (t : NativeGK5DTypedTree (fun z : I => C (f z)) i j) :
    nativeGK5DTreeLeaves (nativeGK5FTreeReindex f C t) =
      nativeGK5FWordReindex f C (nativeGK5DTreeLeaves t) := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste left right hl hr =>
      change nativeGK5DWordAppend
          (nativeGK5DTreeLeaves (nativeGK5FTreeReindex f C left))
          (nativeGK5DTreeLeaves (nativeGK5FTreeReindex f C right)) =
        nativeGK5FWordReindex f C
          (nativeGK5DWordAppend (nativeGK5DTreeLeaves left)
            (nativeGK5DTreeLeaves right))
      rw [nativeGK5FWordReindex_append, hl, hr]

/-- Actual canonical right-associated trees are preserved by the
dependent index reclassification, as equality of typed trees. -/
theorem nativeGK5FTreeOfWord_reindex
    {i j : I} (w : NativeGK5DTypedWord (fun z : I => C (f z)) i j) :
    nativeGK5FTreeReindex f C (nativeGK5DTreeOfWord w) =
      nativeGK5DTreeOfWord (nativeGK5FWordReindex f C w) := by
  induction w with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedTree.paste (.atom F)
          (nativeGK5FTreeReindex f C (nativeGK5DTreeOfWord xs)) =
        NativeGK5DTypedTree.paste (.atom F)
          (nativeGK5DTreeOfWord (nativeGK5FWordReindex f C xs))
      rw [ih]

end IndexRelabeling

section RelabelingIdentityComposition
variable {I : Type uI} {J : Type uJ} {K : Type uK}

/-- Reclassification by the identity is strictly the same typed word. -/
theorem nativeGK5FWordReindex_id
    (C : I → Cat.{vC,uC}) {i j : I}
    (w : NativeGK5DTypedWord C i j) :
    nativeGK5FWordReindex (id : I → I) C w = w := by
  induction w with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5FWordReindex (id : I → I) C xs) =
        NativeGK5DTypedWord.cons F xs
      rw [ih]
      rfl

/-- Reclassification by identity preserves all finite binary trees. -/
theorem nativeGK5FTreeReindex_id
    (C : I → Cat.{vC,uC}) {i j : I}
    (t : NativeGK5DTypedTree C i j) :
    nativeGK5FTreeReindex (id : I → I) C t = t := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste a b ha hb =>
      change NativeGK5DTypedTree.paste
          (nativeGK5FTreeReindex (id : I → I) C a)
          (nativeGK5FTreeReindex (id : I → I) C b) =
        NativeGK5DTypedTree.paste a b
      rw [ha, hb]
      rfl

/-- Successive reclassifications f then g are identical as FULL
dependent finite words to reclassification by their composite. -/
theorem nativeGK5FWordReindex_comp
    (f : I → J) (g : J → K) (C : K → Cat.{vC,uC})
    {i j : I}
    (w : NativeGK5DTypedWord (fun z : I => C (g (f z))) i j) :
    nativeGK5FWordReindex g C
        (nativeGK5FWordReindex f (fun z : J => C (g z)) w) =
      nativeGK5FWordReindex (fun z : I => g (f z)) C w := by
  induction w with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5FWordReindex g C
            (nativeGK5FWordReindex f (fun z : J => C (g z)) xs)) =
        NativeGK5DTypedWord.cons F
          (nativeGK5FWordReindex (fun z : I => g (f z)) C xs)
      rw [ih]

/-- Successive reclassifications compose strictly on all typed
binary trees, retaining every genuinely typed intermediate object. -/
theorem nativeGK5FTreeReindex_comp
    (f : I → J) (g : J → K) (C : K → Cat.{vC,uC})
    {i j : I}
    (t : NativeGK5DTypedTree (fun z : I => C (g (f z))) i j) :
    nativeGK5FTreeReindex g C
        (nativeGK5FTreeReindex f (fun z : J => C (g z)) t) =
      nativeGK5FTreeReindex (fun z : I => g (f z)) C t := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste a b ha hb =>
      change NativeGK5DTypedTree.paste
          (nativeGK5FTreeReindex g C
            (nativeGK5FTreeReindex f (fun z : J => C (g z)) a))
          (nativeGK5FTreeReindex g C
            (nativeGK5FTreeReindex f (fun z : J => C (g z)) b)) =
        NativeGK5DTypedTree.paste
          (nativeGK5FTreeReindex (fun z : I => g (f z)) C a)
          (nativeGK5FTreeReindex (fun z : I => g (f z)) C b)
      rw [ha, hb]
end RelabelingIdentityComposition

section RelabelingRewritePaths
variable {I : Type uI} {J : Type uJ}
variable (f : I → J) (C : J → Cat.{vC,uC})

/-- Relabel EVERY real proof-relevant associator, unitor, and
whiskering step, retaining its genuine Mathlib denotation. -/
def nativeGK5FStepReindex :
    ∀ {i j : I} {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j},
      NativeGK5DTypedStep (fun z : I => C (f z)) a b →
      NativeGK5DTypedStep C
        (nativeGK5FTreeReindex f C a) (nativeGK5FTreeReindex f C b)
  | _, _, _, _, .assoc a b c =>
      .assoc (nativeGK5FTreeReindex f C a)
        (nativeGK5FTreeReindex f C b) (nativeGK5FTreeReindex f C c)
  | _, _, _, _, .leftUnit a =>
      .leftUnit (nativeGK5FTreeReindex f C a)
  | _, _, _, _, .rightUnit a =>
      .rightUnit (nativeGK5FTreeReindex f C a)
  | _, _, _, _, .whiskerRight h c =>
      .whiskerRight (nativeGK5FStepReindex h)
        (nativeGK5FTreeReindex f C c)
  | _, _, _, _, .whiskerLeft a h =>
      .whiskerLeft (nativeGK5FTreeReindex f C a)
        (nativeGK5FStepReindex h)

/-- Entire proof-relevant finite paths, including reversals and
concatenations, remain true paths under index reclassification. -/
def nativeGK5FPathReindex :
    ∀ {i j : I} {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j},
      NativeGK5DTypedPath (fun z : I => C (f z)) a b →
      NativeGK5DTypedPath C
        (nativeGK5FTreeReindex f C a) (nativeGK5FTreeReindex f C b)
  | _, _, _, _, .refl a => .refl (nativeGK5FTreeReindex f C a)
  | _, _, _, _, .basic h => .basic (nativeGK5FStepReindex f C h)
  | _, _, _, _, .reverse q => .reverse (nativeGK5FPathReindex q)
  | _, _, _, _, .trans q r =>
      .trans (nativeGK5FPathReindex q) (nativeGK5FPathReindex r)

/-- Both genuine equality boundaries identify the whole Mathlib
NatIso of each reindexed real STEP with the ORIGINAL step NatIso. -/
theorem nativeGK5FStepIso_reindex_transport
    {i j : I} {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (s : NativeGK5DTypedStep (fun z : I => C (f z)) a b) :
    eqToIso (nativeGK5FTreeComposite_reindex f C a).symm ≪≫
      nativeGK5DStepIso (nativeGK5FStepReindex f C s) ≪≫
      eqToIso (nativeGK5FTreeComposite_reindex f C b) =
    nativeGK5DStepIso s := by
  simp only [nativeGK5DStepIso_eqToIso, eqToIso_trans]

/-- Every proof-relevant path's genuine whole Mathlib NatIso is
preserved after the two real boundary eqToIso transports. -/
theorem nativeGK5FPathIso_reindex_transport
    {i j : I} {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    eqToIso (nativeGK5FTreeComposite_reindex f C a).symm ≪≫
      nativeGK5DPathIso (nativeGK5FPathReindex f C q) ≪≫
      eqToIso (nativeGK5FTreeComposite_reindex f C b) =
    nativeGK5DPathIso q := by
  simp only [nativeGK5DPathIso_eqToIso, eqToIso_trans]

/-- A concrete original path remains a concrete path after relabeling;
this is stronger than merely transporting existence. -/
theorem nativeGK5FPath_reachable_reindex
    {i j : I} {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    Nonempty (NativeGK5DTypedPath C
      (nativeGK5FTreeReindex f C a) (nativeGK5FTreeReindex f C b)) :=
  ⟨nativeGK5FPathReindex f C q⟩

/-- Literal equality of complete typed leaf words carries an ACTUAL
constructed target path, using GK5D normal forms before relabeling. -/
theorem nativeGK5FSameLeaves_reachable_reindex
    {i j : I}
    (a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j)
    (h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b) :
    Nonempty (NativeGK5DTypedPath C
      (nativeGK5FTreeReindex f C a) (nativeGK5FTreeReindex f C b)) :=
  ⟨nativeGK5FPathReindex f C
    (nativeGK5DPathBetweenOfSameLeaves a b h)⟩

end RelabelingRewritePaths

section ChosenInverseIndexRelabeling
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {I : Type uI} {J : Type uJ}
variable (f : I → J) (C : J → Cat.{vC,uC})

/-- Source and target transports make the GK5E recursively pasted
WHOLE chosen-inverse NatIso invariant under exact index relabeling.
The arbitrary chosen Q is NOT definitionally identified with P. -/
theorem nativeGK5FChosenInverse_reindex_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree (fun z : I => C (f z)) i j) :
    eqToIso (congrArg
        (fun K : C (f i) ⥤ C (f j) =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor
              (T := C (f j)) p ma mb pa pb)
        (nativeGK5FTreeComposite_reindex f C t).symm) ≪≫
      nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5FTreeReindex f C t) ≪≫
      eqToIso (congrArg
        (fun K : C (f i) ⥤ C (f j) =>
          nativeGK4BMCompatibleReverseFunctor
            (T := C (f i)) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5FTreeComposite_reindex f C t)) =
    nativeGK5EChosenInverse_treeIso p ma mb pa pb t := by
  simpa only [nativeGK5EChosenInverse_treeIso_eq_direct] using
    (nativeGK5EChosenInverse_eqTransport p ma mb pa pb
      (nativeGK5DTreeComposite t)
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))
      (nativeGK5FTreeComposite_reindex f C t).symm)

/-- The original arbitrary-choice inverse's genuine whole NatTrans
modification remains valid along the relabeled *actual path*. -/
theorem nativeGK5FChosenInverse_reindexedPath_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} {left right :
      NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) left right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5FPathReindex f C q)).hom)
        (nativeGK4BMCompatibleReverseFunctor
          (T := C (f j)) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5FTreeReindex f C right)).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb
      (nativeGK5FTreeReindex f C left)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor
          (T := C (f i)) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5FPathReindex f C q)).hom) :=
  nativeGK5EChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5FPathReindex f C q)

end ChosenInverseIndexRelabeling

#print axioms nativeGK5FWordReindex
#print axioms nativeGK5FTreeReindex
#print axioms nativeGK5FWordReindex_append
#print axioms nativeGK5FWordComposite_reindex
#print axioms nativeGK5FTreeComposite_reindex
#print axioms nativeGK5FTreeLeaves_reindex
#print axioms nativeGK5FTreeOfWord_reindex
#print axioms nativeGK5FWordReindex_id
#print axioms nativeGK5FTreeReindex_id
#print axioms nativeGK5FWordReindex_comp
#print axioms nativeGK5FTreeReindex_comp
#print axioms nativeGK5FStepReindex
#print axioms nativeGK5FPathReindex
#print axioms nativeGK5FStepIso_reindex_transport
#print axioms nativeGK5FPathIso_reindex_transport
#print axioms nativeGK5FPath_reachable_reindex
#print axioms nativeGK5FSameLeaves_reachable_reindex
#print axioms nativeGK5FChosenInverse_reindex_transport
#print axioms nativeGK5FChosenInverse_reindexedPath_square

end
end Kuu.F112.Physical
