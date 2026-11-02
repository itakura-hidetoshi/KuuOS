import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5OWhiskeringFullPathCoherence
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5FIndexRelabelingCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5P — exchange of genuine pointwise category equivalence
changes with typed index relabeling, and unconditional whole NatIso/
NatTrans finite-path naturality through relabeling and composition.

The STRICT exchange proved here is only between the syntactic
dependent word/tree transformations GK5F and GK5G. It does NOT
strictify an equivalence or identify different functor categories.
The path squares remain genuine whole Mathlib NatIso equalities,
using GK5O. A sequential pair of equivalences and its actual
Mathlib composite are both covered, without asserting an unsupported
strict equality of their separately assembled pseudofunctor
compositors or recursively constructed tree comparison isos.

All index maps are allowed (even noninjective). Finite typed
paths and fixed universe pair only. Same-root107, append-only;
Lean v4.30.0-rc2 and pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI uJ vC uC

section IndexChangeExchange
variable {I : Type uI} {J : Type uJ}
variable (f : I → J) {C D : J → Cat.{vC,uC}}
variable (e : ∀ j : J, C j ≌ D j)

/-- Changing every actual category by the pullback family and then
relabeling all dependent word boundaries equals relabeling the
original word first and then changing its actual categories.
Every atom is still conjugated by its genuine equivalences. -/
theorem nativeGK5PChangeWord_reindex
    {i j : I} (w : NativeGK5DTypedWord (fun z : I => C (f z)) i j) :
    nativeGK5FWordReindex f D
      (nativeGK5GChangeWord (fun z : I => e (f z)) w) =
    nativeGK5GChangeWord e (nativeGK5FWordReindex f C w) := by
  induction w with
  | empty _ => rfl
  | cons R xs ih =>
      simp only [nativeGK5GChangeWord, nativeGK5FWordReindex]
      rw [ih]
      simp only [nativeGK5GChangeAtom]

/-- The same exact exchange for complete heterogeneous binary trees,
including every unit, atom, and genuinely typed intermediate category.
This is a theorem about reindexing the SYNTACTIC tree, not strict
equality of the nonstrict whole comparison NatIso Phi. -/
theorem nativeGK5PChangeTree_reindex
    {i j : I} (t : NativeGK5DTypedTree (fun z : I => C (f z)) i j) :
    nativeGK5FTreeReindex f D
      (nativeGK5GChangeTree (fun z : I => e (f z)) t) =
    nativeGK5GChangeTree e (nativeGK5FTreeReindex f C t) := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste left right hl hr =>
      simp only [nativeGK5GChangeTree, nativeGK5FTreeReindex]
      rw [hl, hr]

/-- The exact exchange preserves the entire dependently typed
ordered leaf word. In particular, it is NOT an untyped List map
or an assertion that noninjective index maps reflect equality. -/
theorem nativeGK5PChangeTreeLeaves_reindex
    {i j : I} (t : NativeGK5DTypedTree (fun z : I => C (f z)) i j) :
    nativeGK5DTreeLeaves
        (nativeGK5FTreeReindex f D
          (nativeGK5GChangeTree (fun z : I => e (f z)) t)) =
      nativeGK5GChangeWord e
        (nativeGK5FWordReindex f C (nativeGK5DTreeLeaves t)) := by
  rw [nativeGK5PChangeTree_reindex f e t,
    nativeGK5GChangeTree_leaves,
    nativeGK5FTreeLeaves_reindex]

/-- Any actual finite proof-relevant path can first be relabeled
through an arbitrary index map, then its whole NatIso square
commutes under genuine pointwise category equivalences: no
generator-compatibility premise remains after GK5O. -/
theorem nativeGK5PRelabeledPath_whole
    {i j : I}
    {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath e (nativeGK5FPathReindex f C q)) ≪≫
      nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C b) =
    nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C a) ≪≫
      nativeGK5GChangeIso e
        (nativeGK5DPathIso (nativeGK5FPathReindex f C q)) :=
  nativeGK5OAllFinitePaths e (nativeGK5FPathReindex f C q)

/-- Hom projection of the WHOLE NatIso exchange square for every
relabeled path, not just a pointwise component statement. -/
theorem nativeGK5PRelabeledPath_natTrans
    {i j : I}
    {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    (nativeGK5DPathIso
      (nativeGK5GChangePath e (nativeGK5FPathReindex f C q))).hom ≫
        (nativeGK5GChangeTreeIso e
          (nativeGK5FTreeReindex f C b)).hom =
      (nativeGK5GChangeTreeIso e
        (nativeGK5FTreeReindex f C a)).hom ≫
        (nativeGK5GChangeIso e
          (nativeGK5DPathIso (nativeGK5FPathReindex f C q))).hom :=
  nativeGK5OAllFinitePaths_natTrans e (nativeGK5FPathReindex f C q)

/-- The other route is genuine pointwise change at the pullback
index family. This applies to the original real finite typed
path before reindexing its category boundaries. -/
theorem nativeGK5PPullbackPath_whole
    {i j : I}
    {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath (fun z : I => e (f z)) q) ≪≫
      nativeGK5GChangeTreeIso (fun z : I => e (f z)) b =
    nativeGK5GChangeTreeIso (fun z : I => e (f z)) a ≪≫
      nativeGK5GChangeIso (fun z : I => e (f z))
        (nativeGK5DPathIso q) :=
  nativeGK5OAllFinitePaths (fun z : I => e (f z)) q

/-- The second route also preserves the full NatTrans path square,
with every original typed endpoint retained. -/
theorem nativeGK5PPullbackPath_natTrans
    {i j : I}
    {a b : NativeGK5DTypedTree (fun z : I => C (f z)) i j}
    (q : NativeGK5DTypedPath (fun z : I => C (f z)) a b) :
    (nativeGK5DPathIso
        (nativeGK5GChangePath (fun z : I => e (f z)) q)).hom ≫
      (nativeGK5GChangeTreeIso (fun z : I => e (f z)) b).hom =
    (nativeGK5GChangeTreeIso (fun z : I => e (f z)) a).hom ≫
      (nativeGK5GChangeIso
        (C := fun z : I => C (f z)) (D := fun z : I => D (f z))
        (fun z : I => e (f z))
        (nativeGK5DPathIso (C := fun z : I => C (f z)) q)).hom :=
  nativeGK5OAllFinitePaths_natTrans (fun z : I => e (f z)) q

end IndexChangeExchange

section SuccessiveCategoryEquivalences
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i) (g : ∀ i : I, D i ≌ E i)

/-- After the FIRST true pointwise equivalence, all genuine
finite typed paths remain coherent for a SECOND equivalence.
This is not strict identification of iterated and composed Phi. -/
theorem nativeGK5PSequentialPath_whole
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
      nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e b) =
    nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e a) ≪≫
      nativeGK5GChangeIso g
        (nativeGK5DPathIso (nativeGK5GChangePath e q)) :=
  nativeGK5OAllFinitePaths g (nativeGK5GChangePath e q)

/-- Whole NatTrans naturality for the SECOND actual change of
categories, retaining genuine Mathlib whiskered path isos. -/
theorem nativeGK5PSequentialPath_natTrans
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    (nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q))).hom ≫
      (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e b)).hom =
    (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e a)).hom ≫
      (nativeGK5GChangeIso g
        (nativeGK5DPathIso (nativeGK5GChangePath e q))).hom :=
  nativeGK5OAllFinitePaths_natTrans g (nativeGK5GChangePath e q)

/-- The ACTUAL Mathlib composite equivalence (e_i.trans g_i)
also has unconditional all-finite-path whole NatIso coherence.
No comparison with the two-stage tree Phi is asserted here. -/
theorem nativeGK5PCompositePath_whole
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath (fun k : I => (e k).trans (g k)) q) ≪≫
      nativeGK5GChangeTreeIso (fun k : I => (e k).trans (g k)) b =
    nativeGK5GChangeTreeIso (fun k : I => (e k).trans (g k)) a ≪≫
      nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) :=
  nativeGK5OAllFinitePaths (fun k : I => (e k).trans (g k)) q

/-- Hom version for the actual composite equivalence, without
changing the hypotheses or promoting finite paths to high cells. -/
theorem nativeGK5PCompositePath_natTrans
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    (nativeGK5DPathIso
        (nativeGK5GChangePath (fun k : I => (e k).trans (g k)) q)).hom ≫
      (nativeGK5GChangeTreeIso (fun k : I => (e k).trans (g k)) b).hom =
    (nativeGK5GChangeTreeIso (fun k : I => (e k).trans (g k)) a).hom ≫
      (nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q)).hom :=
  nativeGK5OAllFinitePaths_natTrans
    (fun k : I => (e k).trans (g k)) q

end SuccessiveCategoryEquivalences

#print axioms nativeGK5PChangeWord_reindex
#print axioms nativeGK5PChangeTree_reindex
#print axioms nativeGK5PChangeTreeLeaves_reindex
#print axioms nativeGK5PRelabeledPath_whole
#print axioms nativeGK5PRelabeledPath_natTrans
#print axioms nativeGK5PPullbackPath_whole
#print axioms nativeGK5PPullbackPath_natTrans
#print axioms nativeGK5PSequentialPath_whole
#print axioms nativeGK5PSequentialPath_natTrans
#print axioms nativeGK5PCompositePath_whole
#print axioms nativeGK5PCompositePath_natTrans

end
end Kuu.F112.Physical
