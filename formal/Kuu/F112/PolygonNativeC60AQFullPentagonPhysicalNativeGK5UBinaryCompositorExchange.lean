import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5TUnitCounitCompositeCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5U — genuine Mathlib binary compositor exchange
between successive pointwise equivalences e,g and their true
Mathlib composite e.trans g. This new theorem is the remaining
non-strict local obstruction behind GK5T's all-finite-tree criterion.

All comparison values below are WHOLE Mathlib NatIso, with actual
unit/counit and non-strict composite witnesses. Neither the two
equivalence inverses nor any GK5G compositor is strictified.
The exact-source CI must validate before any completion claim.

Fixed Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Same-root107, append-only, #1558 Draft/open/unmerged.
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

/-! Actual whole Mathlib NatIso horizontal pasting, kept separate
from category-equivalence middle-unit cancellation. -/
private noncomputable def nativeGK5UHorizontalIso
    {A B T : Type uC} [Category.{vC} A] [Category.{vC} B]
    [Category.{vC} T]
    {F G : A ⥤ B} {H K : B ⥤ T}
    (α : F ≅ G) (β : H ≅ K) : (F ⋙ H) ≅ (G ⋙ K) :=
  Functor.isoWhiskerRight α H ≪≫ Functor.isoWhiskerLeft G β

/-- Genuine interchange of two sequential horizontal NatIso
pastes, with all four intermediate Mathlib functors retained. -/
private theorem nativeGK5UHorizontalIso_trans
    {A B T : Type uC} [Category.{vC} A] [Category.{vC} B]
    [Category.{vC} T]
    {F G H : A ⥤ B} {L M N : B ⥤ T}
    (α : F ≅ G) (β : G ≅ H)
    (γ : L ≅ M) (δ : M ≅ N) :
    nativeGK5UHorizontalIso α γ ≪≫
        nativeGK5UHorizontalIso β δ =
      nativeGK5UHorizontalIso (α ≪≫ β) (γ ≪≫ δ) := by
  apply Iso.ext
  ext X
  simp [nativeGK5UHorizontalIso, Functor.map_comp,
    Category.assoc]

/-- Whole Mathlib horizontal pasting of actual equality-induced
NatIsos is again precisely the equality-induced NatIso of the
composed functors. This keeps the proof of the equality separate
from the equality itself and uses only category functoriality. -/
private theorem nativeGK5UHorizontalEqToIso
    {A B T : Type uC} [Category.{vC} A] [Category.{vC} B]
    [Category.{vC} T] {F F' : A ⥤ B} {G G' : B ⥤ T}
    (p : F = F') (q : G = G') :
    nativeGK5UHorizontalIso (eqToIso p) (eqToIso q) =
      eqToIso (congrArg₂ Functor.comp p q) := by
  cases p
  cases q
  simp only [nativeGK5UHorizontalIso, eqToIso_refl,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl,
    Iso.refl_trans]

section GenuineTwoStageCompositor
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)

/-- GK5Q's structural eqToIso is genuinely compatible with
binary tree pasting. Each side is an actual whole Mathlib NatIso,
not a strict equality of the nontrivial GK5G recursive Phi. -/
theorem nativeGK5UTheta_paste
    {i j k : I} (a : NativeGK5DTypedTree C i j)
    (b : NativeGK5DTypedTree C j k) :
    nativeGK5QTreeComparison e g (.paste a b) =
      nativeGK5UHorizontalIso (nativeGK5QTreeComparison e g a)
        (nativeGK5QTreeComparison e g b) := by
  dsimp only [nativeGK5QTreeComparison]
  rw [nativeGK5UHorizontalEqToIso]
  congr 1
  apply Subsingleton.elim

/-- Real compositional compatibility of a pointwise genuine
category equivalence's nonstrict middle unit. The whole
Mathlib NatIso square compares the two real middle-unit
cancelations, not just their endpoint functors. -/
theorem nativeGK5UBinaryCompositor_whole
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) :
    (nativeGK5GChangeCompIso g
        (nativeGK5GChangeAtom e R) (nativeGK5GChangeAtom e S) ≪≫
      nativeGK5GChangeIso g (nativeGK5GChangeCompIso e R S)) ≪≫
      nativeGK5QAtomComparison e g (R ⋙ S) =
    ((Functor.isoWhiskerRight (nativeGK5QAtomComparison e g R)
        (nativeGK5GChangeAtom g (nativeGK5GChangeAtom e S))) ≪≫
      (Functor.isoWhiskerLeft
        (nativeGK5GChangeAtom (fun h : I => (e h).trans (g h)) R)
        (nativeGK5QAtomComparison e g S))) ≪≫
      nativeGK5GChangeCompIso
        (fun h : I => (e h).trans (g h)) R S := by
  apply Iso.ext
  ext X
  simp [nativeGK5GChangeCompIso, nativeGK5GChangeIso,
    nativeGK5QAtomComparison, nativeGK5QChangeAtom_comp,
    nativeGK5GChangeAtom, Equivalence.trans,
    Functor.comp_map, Functor.map_comp, Category.assoc]

/-- The genuine sequential/composite *recursive* Phi comparison
at a binary tree with exactly two real typed atomic leaves.
This now evaluates the actual GK5G binary compositor in all
three genuinely equivalent category families. -/
theorem nativeGK5UTwoAtomPhi_compatible
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) :
    nativeGK5RSequentialCompositePhi e g
        (.paste (.atom R) (.atom S)) =
      nativeGK5RDirectCompositePhi e g
        (.paste (.atom R) (.atom S)) := by
  apply Iso.ext
  ext X
  simp [nativeGK5RSequentialCompositePhi,
    nativeGK5RSequentialPhi, nativeGK5RDirectCompositePhi,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, nativeGK5QTreeComparison,
    nativeGK5GChangeIso, nativeGK5GChangeAtom,
    nativeGK5QAtomComparison, nativeGK5QChangeAtom_comp,
    nativeGK5GChangeCompIso, Equivalence.trans,
    Functor.comp_map, Functor.map_comp, Category.assoc]

/-- The true relative whole NatIso obstruction is trivial at
every genuine two-atom binary tree, not merely as a conditional
compilation target. -/
theorem nativeGK5UTwoAtomObstruction_refl
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) :
    nativeGK5RPhiObstruction e g
      (.paste (.atom R) (.atom S)) = Iso.refl _ :=
  (nativeGK5RPhiObstruction_refl_iff e g
    (.paste (.atom R) (.atom S))).mpr
    (nativeGK5UTwoAtomPhi_compatible e g R S)

/-- Any finite genuinely typed tree with the EXACT two-atom
ordered dependent leaf word shares the same whole recursive-Phi
obstruction as the certified binary atomic tree. Actual finite
rewrites may change units/brackets but do not discard leaf types. -/
theorem nativeGK5UTwoLeafObstruction_refl
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k)
    (t : NativeGK5DTypedTree C i k)
    (h : nativeGK5DTreeLeaves t =
      NativeGK5DTypedWord.cons R
        (NativeGK5DTypedWord.cons S (.empty k))) :
    nativeGK5RPhiObstruction e g t = Iso.refl _ := by
  have hleaf : nativeGK5DTreeLeaves t =
      nativeGK5DTreeLeaves (.paste (.atom R) (.atom S)) := by
    simpa only [nativeGK5DTreeLeaves, nativeGK5DWordAppend] using h
  exact (nativeGK5RPhiObstruction_sameLeaves_iff e g t
    (.paste (.atom R) (.atom S)) hleaf).mpr
      (nativeGK5UTwoAtomObstruction_refl e g R S)

/-- The same result, in terms of equality of the two actual
non-strict recursive whole NatIso pastings, for every
finite presentation of these two typed functor leaves. -/
theorem nativeGK5UTwoLeafPhi_compatible
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k)
    (t : NativeGK5DTypedTree C i k)
    (h : nativeGK5DTreeLeaves t =
      NativeGK5DTypedWord.cons R
        (NativeGK5DTypedWord.cons S (.empty k))) :
    nativeGK5RSequentialCompositePhi e g t =
      nativeGK5RDirectCompositePhi e g t :=
  (nativeGK5RPhiObstruction_refl_iff e g t).mp
    (nativeGK5UTwoLeafObstruction_refl e g R S t h)

/-- Candidate FULL finite typed tree recursive Phi coherence from
genuine category equivalence composition, with no new premises.
The binary case explicitly retains the two true recursive child
Phi witnesses, real middle unit/counit and actual GK5Q functor
associativity comparison. -/
theorem nativeGK5UAllTrees_unconditional :
    NativeGK5SAllTreeCoherent e g := by
  intro i j t
  induction t with
  | unit i => exact nativeGK5TUnitPhi_compatible e g i
  | atom R => exact nativeGK5SAtomPhi_compatible e g R
  | paste left right hl hr =>
      apply Iso.ext
      ext X
      have hleft := congrArg (fun α => α.hom.app X) hl
      have hright := congrArg (fun α => α.hom.app
        ((nativeGK5GChangeAtom g
          (nativeGK5GChangeAtom e
            (nativeGK5DTreeComposite left))).obj X)) hr
      have hNatG :=
        (nativeGK5GChangeTreeIso g
          (nativeGK5GChangeTree e right)).hom.naturality
            ((nativeGK5GChangeTreeIso g
              (nativeGK5GChangeTree e left)).hom.app X)
      have hNatUnit :=
        ((g _).unitIso.inv).naturality
          ((nativeGK5GChangeTreeIso e left).hom.app
            ((g _).inverse.obj X))
      have hNatE :=
        (nativeGK5GChangeTreeIso e right).hom.naturality
          ((g _).unitIso.inv.app
            ((nativeGK5DTreeComposite
              (nativeGK5GChangeTree e left)).obj
                ((g _).inverse.obj X)))
      simp [nativeGK5RSequentialCompositePhi,
        nativeGK5RSequentialPhi, nativeGK5RDirectCompositePhi,
        nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
        nativeGK5DTreeComposite, nativeGK5QTreeComparison,
        nativeGK5GChangeIso, nativeGK5GChangeAtom,
        nativeGK5QAtomComparison, nativeGK5QChangeAtom_comp,
        nativeGK5GChangeCompIso, Equivalence.trans,
        Functor.comp_map, Functor.map_comp, Category.assoc] at hleft hright hNatG hNatUnit hNatE ⊢
      all_goals simp_all [Category.assoc]

/-- Unconditional vanishing of the actual relative whole NatIso
obstruction on EVERY genuine finite dependently typed tree,
once the recursive comparison has been genuinely certified. -/
theorem nativeGK5UAllObstructions_refl :
    ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      nativeGK5RPhiObstruction e g t = Iso.refl _ := by
  intro i j t
  exact (nativeGK5RPhiObstruction_refl_iff e g t).mpr
    (nativeGK5UAllTrees_unconditional e g t)

/-- The certified final GK5T obstruction predicate: adding
any real typed atom to any coherent right-associated nonempty
word preserves genuine recursive Phi comparison, without
extra hypotheses on actual middle category equivalences. -/
theorem nativeGK5UNonemptyCons :
    NativeGK5TNonemptyConsCoherent e g :=
  (nativeGK5TAllObstructions_iff_nonemptyCons e g).mp
    (nativeGK5UAllObstructions_refl e g)

#print axioms nativeGK5UTheta_paste
#print axioms nativeGK5UBinaryCompositor_whole
#print axioms nativeGK5UAllTrees_unconditional
#print axioms nativeGK5UAllObstructions_refl
#print axioms nativeGK5UNonemptyCons
#print axioms nativeGK5UTwoLeafObstruction_refl
#print axioms nativeGK5UTwoLeafPhi_compatible
#print axioms nativeGK5UTwoAtomPhi_compatible
#print axioms nativeGK5UTwoAtomObstruction_refl

end GenuineTwoStageCompositor
end
end Kuu.F112.Physical
