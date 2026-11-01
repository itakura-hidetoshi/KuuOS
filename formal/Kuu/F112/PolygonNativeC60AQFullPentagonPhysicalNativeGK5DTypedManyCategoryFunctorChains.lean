import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFiniteTreeNormalizationReachability
import Mathlib.CategoryTheory.Category.Cat
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5D — genuine many-category FINITE typed functor-chain
coherence, constructive normalization, and exact reachability.

The family C : I → Cat.{vT,uT} bundles genuinely different Mathlib
categories, while EVERY tree, word, rewrite and composite retains
its source and target indices. No untyped list of functors is used.

This extends the FINITE syntactic coherence of GK5A/GK5B/GK5C:
unit/atom/paste, actual Functor.associator and left/rightUnitor,
both genuine iso whiskerings, explicit normalization paths, and
an if-and-only-if between actual rewrite reachability and equality
of the same-typed ordered leaf words.

Scope: families of categories with fixed universe pair (vT,uT),
not arbitrary size-changing universes or raw F54/F55/P92B Type-valued
higher cells. It does NOT identify arbitrary chosen inverse Q_T with
explicit inverse P_T. Cross-category chosen-inverse GK4BM/GK4BU
naturality is not asserted here and needs separately typed inputs.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vT uT

/-- A finite word of genuinely composable functors between DIFFERENT
categories. Its source and target are retained in dependent indices. -/
inductive NativeGK5DTypedWord {I : Type uI} (C : I → Cat.{vT,uT}) :
    I → I → Type _ where
  | empty (i : I) : NativeGK5DTypedWord C i i
  | cons {i j k : I} (F : C i ⥤ C j)
      (rest : NativeGK5DTypedWord C j k) :
      NativeGK5DTypedWord C i k

/-- A genuinely typed finite binary tree of composable functors. -/
inductive NativeGK5DTypedTree {I : Type uI} (C : I → Cat.{vT,uT}) :
    I → I → Type _ where
  | unit (i : I) : NativeGK5DTypedTree C i i
  | atom {i j : I} (F : C i ⥤ C j) : NativeGK5DTypedTree C i j
  | paste {i j k : I}
      (left : NativeGK5DTypedTree C i j)
      (right : NativeGK5DTypedTree C j k) :
      NativeGK5DTypedTree C i k

section TypedWords
variable {I : Type uI} {C : I → Cat.{vT,uT}}

/-- Concatenation exists only when the intermediate CATEGORY matches. -/
def nativeGK5DWordAppend :
    ∀ {i j k : I}, NativeGK5DTypedWord C i j →
      NativeGK5DTypedWord C j k → NativeGK5DTypedWord C i k
  | _, _, _, .empty _, ys => ys
  | _, _, _, .cons F xs, ys => .cons F (nativeGK5DWordAppend xs ys)

/-- Evaluate a typed finite word in Mathlib's actual functor category. -/
def nativeGK5DWordComposite :
    ∀ {i j : I}, NativeGK5DTypedWord C i j → (C i ⥤ C j)
  | _, _, .empty i => 𝟭 (C i)
  | _, _, .cons F xs => F ⋙ nativeGK5DWordComposite xs

/-- Evaluate a typed binary tree in actual Mathlib functors. -/
def nativeGK5DTreeComposite :
    ∀ {i j : I}, NativeGK5DTypedTree C i j → (C i ⥤ C j)
  | _, _, .unit i => 𝟭 (C i)
  | _, _, .atom F => F
  | _, _, .paste left right =>
      nativeGK5DTreeComposite left ⋙ nativeGK5DTreeComposite right

/-- Leaf normalization forgets ONLY inserted identities and brackets,
never their dependent category types or leaf order. -/
def nativeGK5DTreeLeaves :
    ∀ {i j : I}, NativeGK5DTypedTree C i j → NativeGK5DTypedWord C i j
  | _, _, .unit i => .empty i
  | _, _, .atom F => .cons F (.empty _)
  | _, _, .paste left right =>
      nativeGK5DWordAppend (nativeGK5DTreeLeaves left)
        (nativeGK5DTreeLeaves right)

/-- Right-associated tree presentation of a truly typed word. -/
def nativeGK5DTreeOfWord :
    ∀ {i j : I}, NativeGK5DTypedWord C i j → NativeGK5DTypedTree C i j
  | _, _, .empty i => .unit i
  | _, _, .cons F rest => .paste (.atom F) (nativeGK5DTreeOfWord rest)

/-- Strict associativity of the dependent word concatenation. -/
theorem nativeGK5DWordAppend_assoc
    {i j k l : I}
    (xs : NativeGK5DTypedWord C i j)
    (ys : NativeGK5DTypedWord C j k)
    (zs : NativeGK5DTypedWord C k l) :
    nativeGK5DWordAppend (nativeGK5DWordAppend xs ys) zs =
      nativeGK5DWordAppend xs (nativeGK5DWordAppend ys zs) := by
  induction xs with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5DWordAppend (nativeGK5DWordAppend xs ys) zs) =
        NativeGK5DTypedWord.cons F
          (nativeGK5DWordAppend xs (nativeGK5DWordAppend ys zs))
      rw [ih]

/-- Inserting a terminal empty word has no effect on typed leaves. -/
theorem nativeGK5DWordAppend_empty
    {i j : I} (xs : NativeGK5DTypedWord C i j) :
    nativeGK5DWordAppend xs (.empty j) = xs := by
  induction xs with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5DWordAppend xs (.empty _)) =
        NativeGK5DTypedWord.cons F xs
      rw [ih]

/-- True functor composition is a typed monoid-like fold, where
intermediate source and target categories may differ. -/
theorem nativeGK5DWordComposite_append
    {i j k : I}
    (xs : NativeGK5DTypedWord C i j)
    (ys : NativeGK5DTypedWord C j k) :
    nativeGK5DWordComposite (nativeGK5DWordAppend xs ys) =
      nativeGK5DWordComposite xs ⋙ nativeGK5DWordComposite ys := by
  induction xs with
  | empty _ =>
      change nativeGK5DWordComposite ys =
        (𝟭 _) ⋙ nativeGK5DWordComposite ys
      exact (Functor.id_comp (nativeGK5DWordComposite ys)).symm
  | cons F xs ih =>
      change F ⋙ nativeGK5DWordComposite (nativeGK5DWordAppend xs ys) =
        (F ⋙ nativeGK5DWordComposite xs) ⋙ nativeGK5DWordComposite ys
      rw [ih]
      rfl

/-- The entire heterogeneous binary composite equals the canonical
whole functor of its ordered and dependently typed leaf word. -/
theorem nativeGK5DTreeComposite_eq_word
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite t =
      nativeGK5DWordComposite (nativeGK5DTreeLeaves t) := by
  induction t with
  | unit _ => rfl
  | atom F =>
      change F = F ⋙ (𝟭 _)
      exact (Functor.comp_id F).symm
  | paste left right hl hr =>
      change nativeGK5DTreeComposite left ⋙ nativeGK5DTreeComposite right =
        nativeGK5DWordComposite
          (nativeGK5DWordAppend (nativeGK5DTreeLeaves left)
            (nativeGK5DTreeLeaves right))
      rw [hl, hr, nativeGK5DWordComposite_append]

/-- No semantic faithfulness claim: this is an implication from
the equality of FULL typed words, not its converse. -/
theorem nativeGK5DTreeComposite_eq_of_leaves
    {i j : I} (a b : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b) :
    nativeGK5DTreeComposite a = nativeGK5DTreeComposite b := by
  rw [nativeGK5DTreeComposite_eq_word,
    nativeGK5DTreeComposite_eq_word, h]

/-- A canonical right-associated tree has exactly the original
ordered and typed leaves, including all intermediate categories. -/
theorem nativeGK5DTreeOfWord_leaves
    {i j : I} (xs : NativeGK5DTypedWord C i j) :
    nativeGK5DTreeLeaves (nativeGK5DTreeOfWord xs) = xs := by
  induction xs with
  | empty _ => rfl
  | cons F xs ih =>
      change NativeGK5DTypedWord.cons F
          (nativeGK5DTreeLeaves (nativeGK5DTreeOfWord xs)) =
        NativeGK5DTypedWord.cons F xs
      rw [ih]

/-- The canonical tree evaluates to the genuine typed word fold. -/
theorem nativeGK5DTreeOfWord_eval
    {i j : I} (xs : NativeGK5DTypedWord C i j) :
    nativeGK5DTreeComposite (nativeGK5DTreeOfWord xs) =
      nativeGK5DWordComposite xs := by
  induction xs with
  | empty _ => rfl
  | cons F xs ih =>
      change F ⋙ nativeGK5DTreeComposite (nativeGK5DTreeOfWord xs) =
        F ⋙ nativeGK5DWordComposite xs
      rw [ih]
end TypedWords

/-- Actual individual typed Mathlib associator/unitor steps. -/
inductive NativeGK5DTypedStep {I : Type uI} (C : I → Cat.{vT,uT}) :
    ∀ {i j : I}, NativeGK5DTypedTree C i j →
      NativeGK5DTypedTree C i j → Type _ where
  | assoc {i j k l : I}
      (a : NativeGK5DTypedTree C i j)
      (b : NativeGK5DTypedTree C j k)
      (c : NativeGK5DTypedTree C k l) :
      NativeGK5DTypedStep C (.paste (.paste a b) c) (.paste a (.paste b c))
  | leftUnit {i j : I} (a : NativeGK5DTypedTree C i j) :
      NativeGK5DTypedStep C (.paste (.unit i) a) a
  | rightUnit {i j : I} (a : NativeGK5DTypedTree C i j) :
      NativeGK5DTypedStep C (.paste a (.unit j)) a
  | whiskerRight {i j k : I}
      {a b : NativeGK5DTypedTree C i j}
      (h : NativeGK5DTypedStep C a b)
      (c : NativeGK5DTypedTree C j k) :
      NativeGK5DTypedStep C (.paste a c) (.paste b c)
  | whiskerLeft {i j k : I}
      (a : NativeGK5DTypedTree C i j)
      {b c : NativeGK5DTypedTree C j k}
      (h : NativeGK5DTypedStep C b c) :
      NativeGK5DTypedStep C (.paste a b) (.paste a c)

/-- A proof-relevant finite sequence of real typed rewrites. -/
inductive NativeGK5DTypedPath {I : Type uI} (C : I → Cat.{vT,uT}) :
    ∀ {i j : I}, NativeGK5DTypedTree C i j →
      NativeGK5DTypedTree C i j → Type _ where
  | refl {i j : I} (a : NativeGK5DTypedTree C i j) : NativeGK5DTypedPath C a a
  | basic {i j : I} {a b : NativeGK5DTypedTree C i j}
      (h : NativeGK5DTypedStep C a b) : NativeGK5DTypedPath C a b
  | reverse {i j : I} {a b : NativeGK5DTypedTree C i j}
      (p : NativeGK5DTypedPath C a b) : NativeGK5DTypedPath C b a
  | trans {i j : I} {a b c : NativeGK5DTypedTree C i j}
      (p : NativeGK5DTypedPath C a b)
      (q : NativeGK5DTypedPath C b c) : NativeGK5DTypedPath C a c

section TypedRewrites
variable {I : Type uI} {C : I → Cat.{vT,uT}}

/-- Each basic step induces equality of WHOLE heterogeneous functors. -/
def nativeGK5DStepEq :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedStep C a b →
        nativeGK5DTreeComposite a = nativeGK5DTreeComposite b
  | _, _, _, _, .assoc a b c =>
      Functor.assoc (nativeGK5DTreeComposite a)
        (nativeGK5DTreeComposite b) (nativeGK5DTreeComposite c)
  | _, _, _, _, .leftUnit a =>
      Functor.id_comp (nativeGK5DTreeComposite a)
  | _, _, _, _, .rightUnit a =>
      Functor.comp_id (nativeGK5DTreeComposite a)
  | _, _, _, _, .whiskerRight h c =>
      congrArg
        (fun F => F ⋙ nativeGK5DTreeComposite c) (nativeGK5DStepEq h)
  | _, _, _, _, .whiskerLeft a h =>
      congrArg
        (fun F => nativeGK5DTreeComposite a ⋙ F) (nativeGK5DStepEq h)

/-- Each real step is interpreted by the genuine WHOLE Mathlib NatIso. -/
noncomputable def nativeGK5DStepIso :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedStep C a b →
        (nativeGK5DTreeComposite a ≅ nativeGK5DTreeComposite b)
  | _, _, _, _, .assoc a b c =>
      Functor.associator (nativeGK5DTreeComposite a)
        (nativeGK5DTreeComposite b) (nativeGK5DTreeComposite c)
  | _, _, _, _, .leftUnit a =>
      Functor.leftUnitor (nativeGK5DTreeComposite a)
  | _, _, _, _, .rightUnit a =>
      Functor.rightUnitor (nativeGK5DTreeComposite a)
  | _, _, _, _, .whiskerRight h c =>
      Functor.isoWhiskerRight (nativeGK5DStepIso h)
        (nativeGK5DTreeComposite c)
  | _, _, _, _, .whiskerLeft a h =>
      Functor.isoWhiskerLeft (nativeGK5DTreeComposite a)
        (nativeGK5DStepIso h)

/-- Equality denotation of an actual finite typed path. -/
def nativeGK5DPathEq :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedPath C a b →
        nativeGK5DTreeComposite a = nativeGK5DTreeComposite b
  | _, _, _, _, .refl _ => rfl
  | _, _, _, _, .basic h => nativeGK5DStepEq h
  | _, _, _, _, .reverse p => (nativeGK5DPathEq p).symm
  | _, _, _, _, .trans p q => (nativeGK5DPathEq p).trans (nativeGK5DPathEq q)

/-- Full NatIso for a true path, not a fabricated higher cell. -/
noncomputable def nativeGK5DPathIso :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedPath C a b →
        (nativeGK5DTreeComposite a ≅ nativeGK5DTreeComposite b)
  | _, _, _, _, .refl _ => Iso.refl _
  | _, _, _, _, .basic h => nativeGK5DStepIso h
  | _, _, _, _, .reverse p => (nativeGK5DPathIso p).symm
  | _, _, _, _, .trans p q => nativeGK5DPathIso p ≪≫ nativeGK5DPathIso q

private theorem nativeGK5DWhiskerRight_eqToIso
    {i j k : I} {F G : C i ⥤ C j} (h : F = G) (H : C j ⥤ C k) :
    Functor.isoWhiskerRight (eqToIso h) H =
      eqToIso (congrArg (fun K : C i ⥤ C j => K ⋙ H) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerRight_refl]

private theorem nativeGK5DWhiskerLeft_eqToIso
    {i j k : I} (F : C i ⥤ C j) {G H : C j ⥤ C k} (h : G = H) :
    Functor.isoWhiskerLeft F (eqToIso h) =
      eqToIso (congrArg (fun K : C j ⥤ C k => F ⋙ K) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerLeft_refl]

private theorem nativeGK5DEqToIso_symm
    {i j : I} {F G : C i ⥤ C j} (h : F = G) :
    (eqToIso h).symm = eqToIso h.symm := by
  cases h
  rfl

/-- The REAL heterogeneous NatIso of each step is its eqToIso. -/
theorem nativeGK5DStepIso_eqToIso
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (h : NativeGK5DTypedStep C a b) :
    nativeGK5DStepIso h = eqToIso (nativeGK5DStepEq h) := by
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
      simpa only [nativeGK5DStepIso, nativeGK5DStepEq, ih] using
        (nativeGK5DWhiskerRight_eqToIso
          (nativeGK5DStepEq h) (nativeGK5DTreeComposite c))
  | whiskerLeft a h ih =>
      simpa only [nativeGK5DStepIso, nativeGK5DStepEq, ih] using
        (nativeGK5DWhiskerLeft_eqToIso
          (nativeGK5DTreeComposite a) (nativeGK5DStepEq h))

/-- Every actual finite typed rewrite path has canonical whole NatIso.
The explicitly indexed motive is reduced by constructor-pattern recursion:
a separate tactic induction leaves the source/target tree indices opaque. -/
theorem nativeGK5DPathIso_eqToIso :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j}
      (p : NativeGK5DTypedPath C a b),
      nativeGK5DPathIso p = eqToIso (nativeGK5DPathEq p)
  | _, _, _, _, .refl _ => by
      simp only [nativeGK5DPathIso, nativeGK5DPathEq, eqToIso_refl]
  | _, _, _, _, .basic h => by
      simpa only [nativeGK5DPathIso, nativeGK5DPathEq] using
        (nativeGK5DStepIso_eqToIso h)
  | _, _, _, _, .reverse p => by
      simpa only [nativeGK5DPathIso, nativeGK5DPathEq,
        nativeGK5DPathIso_eqToIso p, nativeGK5DEqToIso_symm]
  | _, _, _, _, .trans p q => by
      simpa only [nativeGK5DPathIso, nativeGK5DPathEq,
        nativeGK5DPathIso_eqToIso p, nativeGK5DPathIso_eqToIso q,
        eqToIso_trans]

/-- Arbitrary different-category paths with IDENTICAL typed endpoints
give equal genuine WHOLE Mathlib natural isomorphisms. -/
theorem nativeGK5DPath_independent
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (p q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso p = nativeGK5DPathIso q := by
  rw [nativeGK5DPathIso_eqToIso p, nativeGK5DPathIso_eqToIso q]

/-- Associator, unitor and whiskering preserve the full typed word. -/
theorem nativeGK5DStepLeaves
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (h : NativeGK5DTypedStep C a b) :
    nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b := by
  induction h with
  | assoc a b c =>
      exact nativeGK5DWordAppend_assoc
        (nativeGK5DTreeLeaves a) (nativeGK5DTreeLeaves b)
        (nativeGK5DTreeLeaves c)
  | leftUnit a => rfl
  | rightUnit a =>
      exact nativeGK5DWordAppend_empty (nativeGK5DTreeLeaves a)
  | whiskerRight h c ih =>
      exact congrArg
        (fun rs => nativeGK5DWordAppend rs (nativeGK5DTreeLeaves c)) ih
  | whiskerLeft a h ih =>
      exact congrArg
        (fun rs => nativeGK5DWordAppend (nativeGK5DTreeLeaves a) rs) ih

/-- Paths preserve the ACTUAL ordered typed functor-word. -/
theorem nativeGK5DPathLeaves
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (p : NativeGK5DTypedPath C a b) :
    nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b := by
  induction p with
  | refl _ => rfl
  | basic h => exact nativeGK5DStepLeaves h
  | reverse p ih => exact ih.symm
  | trans p q ihp ihq => exact ihp.trans ihq
end TypedRewrites

section TypedNormalization
variable {I : Type uI} {C : I → Cat.{vT,uT}}

/-- Actual left whiskering of an entire finite typed rewrite path. -/
def nativeGK5DPathWhiskerLeft
    {i j k : I} (fixed : NativeGK5DTypedTree C i j) :
    ∀ {a b : NativeGK5DTypedTree C j k},
      NativeGK5DTypedPath C a b →
      NativeGK5DTypedPath C (.paste fixed a) (.paste fixed b)
  | _, _, .refl _ => .refl _
  | _, _, .basic h => .basic (.whiskerLeft fixed h)
  | _, _, .reverse p => .reverse (nativeGK5DPathWhiskerLeft fixed p)
  | _, _, .trans p q =>
      .trans (nativeGK5DPathWhiskerLeft fixed p)
        (nativeGK5DPathWhiskerLeft fixed q)

/-- Actual right whiskering of an entire finite typed rewrite path. -/
def nativeGK5DPathWhiskerRight
    {i j k : I} :
    ∀ {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedPath C a b →
      (fixed : NativeGK5DTypedTree C j k) →
      NativeGK5DTypedPath C (.paste a fixed) (.paste b fixed)
  | _, _, .refl _, _ => .refl _
  | _, _, .basic h, fixed => .basic (.whiskerRight h fixed)
  | _, _, .reverse p, fixed => .reverse (nativeGK5DPathWhiskerRight p fixed)
  | _, _, .trans p q, fixed =>
      .trans (nativeGK5DPathWhiskerRight p fixed)
        (nativeGK5DPathWhiskerRight q fixed)

/-- Genuine recursive associator/unitor path for dependent word append. -/
def nativeGK5DAppendPath :
    ∀ {i j k : I}
      (xs : NativeGK5DTypedWord C i j)
      (ys : NativeGK5DTypedWord C j k),
      NativeGK5DTypedPath C
        (.paste (nativeGK5DTreeOfWord xs) (nativeGK5DTreeOfWord ys))
        (nativeGK5DTreeOfWord (nativeGK5DWordAppend xs ys))
  | _, _, _, .empty _, ys =>
      .basic (.leftUnit (nativeGK5DTreeOfWord ys))
  | _, _, _, .cons F xs, ys =>
      .trans
        (.basic (.assoc (.atom F)
          (nativeGK5DTreeOfWord xs) (nativeGK5DTreeOfWord ys)))
        (nativeGK5DPathWhiskerLeft (.atom F)
          (nativeGK5DAppendPath xs ys))

/-- Every genuinely typed finite many-category tree normalizes via
CONSTRUCTED real Mathlib associator/unitor/whiskering steps. -/
def nativeGK5DNormalizePath :
    ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      NativeGK5DTypedPath C t
        (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t))
  | _, _, .unit i => .refl _
  | _, _, .atom F => .reverse (.basic (.rightUnit (.atom F)))
  | _, _, .paste left right =>
      .trans
        (nativeGK5DPathWhiskerRight (nativeGK5DNormalizePath left) right)
        (.trans
          (nativeGK5DPathWhiskerLeft
            (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves left))
            (nativeGK5DNormalizePath right))
          (nativeGK5DAppendPath
            (nativeGK5DTreeLeaves left) (nativeGK5DTreeLeaves right)))

/-- The constructed whole NatIso agrees with whole-functor
canonicalization after the REAL typed eqToIso endpoint transport. -/
theorem nativeGK5DNormalizePath_iso_eq_canonical
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DPathIso (nativeGK5DNormalizePath t) ≪≫
      eqToIso (nativeGK5DTreeOfWord_eval (nativeGK5DTreeLeaves t)) =
    eqToIso (nativeGK5DTreeComposite_eq_word t) := by
  simp only [nativeGK5DPathIso_eqToIso, eqToIso_trans]

/-- Construct a genuine typed path from equality of ordered
dependent functor words; NO extra semantic identification. -/
def nativeGK5DPathBetweenOfSameLeaves
    {i j : I} (a b : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b) :
    NativeGK5DTypedPath C a b := by
  have q : NativeGK5DTypedPath C b
      (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves a)) := by
    simpa only [h] using nativeGK5DNormalizePath b
  exact .trans (nativeGK5DNormalizePath a) (.reverse q)

/-- EXACT typed reachability criterion for real finite associator,
unitor and whiskering paths BETWEEN GENUINE DIFFERENT CATEGORIES. -/
theorem nativeGK5DReachable_iff_sameLeaves
    {i j : I} (a b : NativeGK5DTypedTree C i j) :
    Nonempty (NativeGK5DTypedPath C a b) ↔
      nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b := by
  constructor
  · rintro ⟨p⟩
    exact nativeGK5DPathLeaves p
  · intro h
    exact ⟨nativeGK5DPathBetweenOfSameLeaves a b h⟩

/-- Nonvacuous path-independence for genuinely typed paths. -/
theorem nativeGK5DPath_eq_canonical_of_path
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (p : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso p =
      nativeGK5DPathIso (nativeGK5DPathBetweenOfSameLeaves a b
        (nativeGK5DPathLeaves p)) :=
  nativeGK5DPath_independent p
    (nativeGK5DPathBetweenOfSameLeaves a b (nativeGK5DPathLeaves p))

/-- A concrete three-stage DIFFERENT-category associator, retained as
a genuine NatIso proof object rather than collapsed to an untyped path. -/
theorem nativeGK5DThreeStage_associator
    {i j k l : I}
    (F : C i ⥤ C j) (G : C j ⥤ C k) (H : C k ⥤ C l) :
    nativeGK5DStepIso
      (NativeGK5DTypedStep.assoc
        (NativeGK5DTypedTree.atom F)
        (NativeGK5DTypedTree.atom G)
        (NativeGK5DTypedTree.atom H)) =
      Functor.associator F G H := rfl

end TypedNormalization

#print axioms nativeGK5DWordAppend_assoc
#print axioms nativeGK5DWordAppend_empty
#print axioms nativeGK5DWordComposite_append
#print axioms nativeGK5DTreeComposite_eq_word
#print axioms nativeGK5DTreeComposite_eq_of_leaves
#print axioms nativeGK5DTreeOfWord_leaves
#print axioms nativeGK5DTreeOfWord_eval
#print axioms nativeGK5DStepIso_eqToIso
#print axioms nativeGK5DPathIso_eqToIso
#print axioms nativeGK5DPath_independent
#print axioms nativeGK5DStepLeaves
#print axioms nativeGK5DPathLeaves
#print axioms nativeGK5DNormalizePath_iso_eq_canonical
#print axioms nativeGK5DReachable_iff_sameLeaves
#print axioms nativeGK5DPath_eq_canonical_of_path
#print axioms nativeGK5DThreeStage_associator

end
end Kuu.F112.Physical
