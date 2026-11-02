import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5PIndexChangeNaturality
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5Q — actual comparison between sequential and Mathlib-composite
pointwise category-equivalence changes for finite heterogeneous typed functor paths.

Given genuine e_i : C_i ≌ D_i and g_i : D_i ≌ E_i, Mathlib Equivalence.trans
contains the actual composite inverse (g_i.inverse ⋙ e_i.inverse) and
forward (e_i.functor ⋙ g_i.functor). The two ways of conjugating a
WHOLE atom are related by a genuine Mathlib NatIso eqToIso of an
explicitly proved Functor-associativity equality, not by an
unsupported definitional equality of distinct presentations.

The word/tree transports have a proved typed equality. The whole
path NatIso square compares the *actual two-stage path* with the
*actual single-stage composite-equivalence path* via the genuine
endpoint comparison NatIso. It is stronger than separately proving
each route coherent (GK5P), and relies on GK5D's certified
PathIso=eqToIso(path equality), not a fabricated higher cell.

Scope: fixed universe pair, finite typed GK5D paths, genuine
Mathlib category equivalences. We do NOT claim that recursive
GK5GChangeTreeIso Phi under e then g agrees with the Phi for e.trans g,
nor strict equality of nontrivial unit/counit or compositor witnesses.
The latter is a separate remaining obstruction.

Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, strict 空 center / independent Kuu a presentation.
Protected validation-only #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC

section CompositeEquivalenceComparison
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i) (g : ∀ i : I, D i ≌ E i)

/-- Two real sequential conjugations of ANY whole Mathlib functor
equal the actual `Equivalence.trans` conjugation, by the genuine
Functor.assoc law. This equality does not strictify the equivalences
or their nontrivial unit/counit witnesses. -/
theorem nativeGK5QChangeAtom_comp
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom g (nativeGK5GChangeAtom e R) =
      nativeGK5GChangeAtom (fun k : I => (e k).trans (g k)) R := by
  simp only [nativeGK5GChangeAtom, Equivalence.trans_functor,
    Equivalence.trans_inverse, Functor.assoc]

/-- A genuine whole Mathlib NatIso between the two atomic
presentations; it has an actual functor-associativity equality
as witness, rather than being postulated or treated as a strict
identity of their written presentations. -/
noncomputable def nativeGK5QAtomComparison
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom g (nativeGK5GChangeAtom e R) ≅
      nativeGK5GChangeAtom (fun k : I => (e k).trans (g k)) R :=
  eqToIso (nativeGK5QChangeAtom_comp e g R)

/-- All dependent word boundaries, including their indexed
intermediate categories, agree after the two real changes. -/
theorem nativeGK5QChangeWord_comp
    {i j : I} (w : NativeGK5DTypedWord C i j) :
    nativeGK5GChangeWord g (nativeGK5GChangeWord e w) =
      nativeGK5GChangeWord (fun k : I => (e k).trans (g k)) w := by
  induction w with
  | empty _ => rfl
  | cons R xs ih =>
      simp only [nativeGK5GChangeWord]
      rw [nativeGK5QChangeAtom_comp e g R, ih]

/-- Genuine finite dependent trees commute with composition of
equivalences, retaining all typed units and binary contexts. -/
theorem nativeGK5QChangeTree_comp
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeTree g (nativeGK5GChangeTree e t) =
      nativeGK5GChangeTree (fun k : I => (e k).trans (g k)) t := by
  induction t with
  | unit _ => rfl
  | atom R =>
      simpa only [nativeGK5GChangeTree] using
        congrArg NativeGK5DTypedTree.atom (nativeGK5QChangeAtom_comp e g R)
  | paste left right hl hr =>
      simp only [nativeGK5GChangeTree]
      rw [hl, hr]

/-- Their complete ordered dependently typed leaves also coincide
with the changed whole original word. -/
theorem nativeGK5QChangeTreeLeaves_comp
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeLeaves
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) =
    nativeGK5GChangeWord (fun k : I => (e k).trans (g k))
      (nativeGK5DTreeLeaves t) := by
  rw [nativeGK5QChangeTree_comp e g t, nativeGK5GChangeTree_leaves]

/-- The canonical actual endpoint comparison, as a whole NatIso
between REAL evaluated finite trees. No recursive Phi comparison
is smuggled in by this definition. -/
noncomputable def nativeGK5QTreeComparison
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≅
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree (fun k : I => (e k).trans (g k)) t) :=
  eqToIso (congrArg (fun x => nativeGK5DTreeComposite x)
    (nativeGK5QChangeTree_comp e g t))

/-- The genuine atomic NatIso comparison commutes with the image
of any equality-induced NatIso, no assumption of strict inverses.
This applies in particular to every certified GK5D path NatIso. -/
theorem nativeGK5QAtomComparison_eqToIso_square
    {i j : I} {R S : C i ⥤ C j} (h : R = S) :
    nativeGK5GChangeIso g (nativeGK5GChangeIso e (eqToIso h)) ≪≫
      nativeGK5QAtomComparison e g S =
    nativeGK5QAtomComparison e g R ≪≫
      nativeGK5GChangeIso
        (fun k : I => (e k).trans (g k)) (eqToIso h) := by
  cases h
  simp [nativeGK5QAtomComparison, nativeGK5GChangeIso]

/-- Substitution with a REAL whole NatIso interpretation of ANY
proof-relevant finite typed path gives atomic change-composition
naturality. This is not restricted to any generator subclass. -/
theorem nativeGK5QAtomComparison_path_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5GChangeIso g
        (nativeGK5GChangeIso e (nativeGK5DPathIso q)) ≪≫
      nativeGK5QAtomComparison e g (nativeGK5DTreeComposite b) =
    nativeGK5QAtomComparison e g (nativeGK5DTreeComposite a) ≪≫
      nativeGK5GChangeIso
        (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) := by
  rw [nativeGK5DPathIso_eqToIso q]
  exact nativeGK5QAtomComparison_eqToIso_square e g (nativeGK5DPathEq q)

/-- MAIN NEW GLUING SQUARE: the actual TWO-STAGE transformed
finite path Iso commutes with the actual SINGLE-STAGE composite
equivalence transformed path Iso, through the genuine whole
Mathlib NatIso comparisons of its original typed endpoints.
GK5D's existing PathIso/eqToIso agreement guarantees the
square for identity, basic, inverse and concatenation alike. -/
theorem nativeGK5QAllFinitePaths_composition_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
      nativeGK5QTreeComparison e g b =
    nativeGK5QTreeComparison e g a ≪≫
      nativeGK5DPathIso
        (nativeGK5GChangePath (fun k : I => (e k).trans (g k)) q) := by
  simp only [nativeGK5DPathIso_eqToIso, nativeGK5QTreeComparison,
    eqToIso_trans]

/-- The same composition-coherence square as an equality of whole
Mathlib NatTrans homs, not merely equality at selected objects. -/
theorem nativeGK5QAllFinitePaths_composition_natTrans
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    (nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q))).hom ≫
      (nativeGK5QTreeComparison e g b).hom =
    (nativeGK5QTreeComparison e g a).hom ≫
      (nativeGK5DPathIso
        (nativeGK5GChangePath (fun k : I => (e k).trans (g k)) q)).hom := by
  simpa only [Iso.trans_hom] using
    congrArg Iso.hom (nativeGK5QAllFinitePaths_composition_square e g q)

/-- A constructive GK5D canonical normalization path satisfies
this actual non-strict comparison square without any local
compatibility condition, derived from the all-finite-path theorem. -/
theorem nativeGK5QNormalization_composition_square
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g
          (nativeGK5GChangePath e (nativeGK5DNormalizePath t))) ≪≫
      nativeGK5QTreeComparison e g
        (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t)) =
    nativeGK5QTreeComparison e g t ≪≫
      nativeGK5DPathIso
        (nativeGK5GChangePath (fun k : I => (e k).trans (g k))
          (nativeGK5DNormalizePath t)) :=
  nativeGK5QAllFinitePaths_composition_square e g (nativeGK5DNormalizePath t)

#print axioms nativeGK5QChangeAtom_comp
#print axioms nativeGK5QAtomComparison
#print axioms nativeGK5QChangeWord_comp
#print axioms nativeGK5QChangeTree_comp
#print axioms nativeGK5QChangeTreeLeaves_comp
#print axioms nativeGK5QTreeComparison
#print axioms nativeGK5QAtomComparison_eqToIso_square
#print axioms nativeGK5QAtomComparison_path_square
#print axioms nativeGK5QAllFinitePaths_composition_square
#print axioms nativeGK5QAllFinitePaths_composition_natTrans
#print axioms nativeGK5QNormalization_composition_square

end CompositeEquivalenceComparison
end
end Kuu.F112.Physical
