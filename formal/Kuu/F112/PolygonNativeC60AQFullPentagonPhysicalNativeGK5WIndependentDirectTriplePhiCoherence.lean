import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5VTripleNatIsoAssociativity
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5W — true independent direct recursive Phi comparison
for both bracketings of THREE genuine category-equivalence changes.

GK5V proved a whole NatIso cocycle on one common three-stage recursively
assembled Phi. This new theorem compares that shared sequential witness
with EACH independently constructed genuine direct recursive GK5G Phi:
Phi_((e.trans g).trans h) and Phi_(e.trans (g.trans h)).
The two direct witnesses are joined through the actual Mathlib
eqToIso associator, never an equality of entire Equivalence records.

This development retains genuine quasi-inverses, units/counits,
binary compositor and whole NatIso horizontal composition. The
key additional ingredient is GK5Q atomic comparison naturality for
an arbitrary WHOLE NatIso, not only eqToIso path certificates.
No raw source higher cells, Gray recovery or unrestricted descent.

Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Canonical root107, append-only/tighten-only, strict 空 center;
independent Kuu is one presentation; #1558 validation-only protected.
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

section EqualityNaturality
variable {I : Type uI} {A B : I → Cat.{vC,uC}}
variable (k : ∀ i : I, A i ≌ B i)

/-- A genuine recursive GK5G whole NatIso Phi is natural for
an equality of WHOLE finite typed trees, in addition to the
previously certified arbitrary proof-relevant GK5D path laws. -/
private theorem nativeGK5WTreePhi_eqToIso_square
    {i j : I} {a b : NativeGK5DTypedTree A i j} (p : a = b) :
    eqToIso (congrArg
      (fun x : NativeGK5DTypedTree A i j =>
        nativeGK5DTreeComposite (nativeGK5GChangeTree k x)) p) ≪≫
      nativeGK5GChangeTreeIso k b =
    nativeGK5GChangeTreeIso k a ≪≫
      nativeGK5GChangeIso k
        (eqToIso (congrArg nativeGK5DTreeComposite p)) := by
  cases p
  simp only [congrArg, eqToIso_refl, Iso.refl_trans,
    Iso.trans_refl, nativeGK5GChangeIso, nativeGK5GChangeAtom,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl]

end EqualityNaturality

section TripleIndependentDirectPhi
variable {I : Type uI} {C D E F : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)
variable (h : ∀ i : I, E i ≌ F i)

/-- Arbitrary WHOLE Mathlib NatIso naturality of GK5Q's true
atomic two-equivalence comparator. Neither the input NatIso nor
the equivalence unit/counit is equality-induced or strict. -/
theorem nativeGK5WAtomComparison_natIso
    {i j : I} {R S : D i ⥤ D j} (α : R ≅ S) :
    nativeGK5GChangeIso h (nativeGK5GChangeIso g α) ≪≫
      nativeGK5QAtomComparison g h S =
    nativeGK5QAtomComparison g h R ≪≫
      nativeGK5GChangeIso (fun k : I => (g k).trans (h k)) α := by
  apply Iso.ext
  ext X
  simp [nativeGK5QAtomComparison, nativeGK5QChangeAtom_comp,
    nativeGK5GChangeIso, nativeGK5GChangeAtom,
    Equivalence.trans, Functor.comp_map, Functor.map_comp, Category.assoc]

/-- Actual left-bracketed THREE-stage typed-tree equality,
built from two distinct certified GK5Q equalities. -/
theorem nativeGK5WLeftTreeEq
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) =
      nativeGK5GChangeTree
        (fun k : I => ((e k).trans (g k)).trans (h k)) t := by
  calc
    _ = nativeGK5GChangeTree h
        (nativeGK5GChangeTree
          (fun k : I => (e k).trans (g k)) t) :=
            congrArg (nativeGK5GChangeTree h)
              (nativeGK5QChangeTree_comp e g t)
    _ = _ := nativeGK5QChangeTree_comp
      (fun k : I => (e k).trans (g k)) h t

/-- Actual right-bracketed THREE-stage typed-tree equality. -/
theorem nativeGK5WRightTreeEq
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) =
      nativeGK5GChangeTree
        (fun k : I => (e k).trans ((g k).trans (h k))) t := by
  calc
    _ = nativeGK5GChangeTree
        (fun k : I => (g k).trans (h k))
          (nativeGK5GChangeTree e t) :=
            nativeGK5QChangeTree_comp g h (nativeGK5GChangeTree e t)
    _ = _ := nativeGK5QChangeTree_comp e
      (fun k : I => (g k).trans (h k)) t

/-- First left tree comparison, changing GK5Q's (e,g)
structural typed-tree equality by the third real equivalence. -/
private noncomputable def nativeGK5WLeftInitialTreeIso
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree
          (fun k : I => (e k).trans (g k)) t)) :=
  eqToIso (congrArg
    (fun x : NativeGK5DTypedTree E i j =>
      nativeGK5DTreeComposite (nativeGK5GChangeTree h x))
    (nativeGK5QChangeTree_comp e g t))

/-- The FULL left tree associator, without using Phi recursively. -/
noncomputable def nativeGK5WLeftTreeIso
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree
        (fun k : I => ((e k).trans (g k)).trans (h k)) t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
    (nativeGK5WLeftTreeEq e g h t))

/-- The FULL right tree associator, built independently. -/
noncomputable def nativeGK5WRightTreeIso
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree
        (fun k : I => (e k).trans ((g k).trans (h k))) t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
    (nativeGK5WRightTreeEq e g h t))

/-- Left structural tree comparison factors through the actual
two-stage GK5Q tree equality and its transport under h. -/
private theorem nativeGK5WLeftTreeIso_factor
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WLeftTreeIso e g h t =
      nativeGK5WLeftInitialTreeIso e g h t ≪≫
        nativeGK5QTreeComparison
          (fun k : I => (e k).trans (g k)) h t := by
  simp only [nativeGK5WLeftTreeIso, nativeGK5WLeftInitialTreeIso,
    nativeGK5QTreeComparison, eqToIso_trans]

/-- Right structural tree comparison factors through the genuine
(g,h) transformed subtree and the actual e,(g.trans h) tree. -/
private theorem nativeGK5WRightTreeIso_factor
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WRightTreeIso e g h t =
      nativeGK5QTreeComparison g h (nativeGK5GChangeTree e t) ≪≫
        nativeGK5QTreeComparison e
          (fun k : I => (g k).trans (h k)) t := by
  simp only [nativeGK5WRightTreeIso, nativeGK5QTreeComparison,
    eqToIso_trans]

/-- The LEFT directly constructed recursive Phi, built only
from the true left-composite GK5GChangeTreeIso and the canonical
whole eqToIso comparison of the fully transformed tree. -/
noncomputable def nativeGK5WLeftDirectPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
    nativeGK5GChangeAtom
      (fun k : I => ((e k).trans (g k)).trans (h k))
      (nativeGK5DTreeComposite t) :=
  nativeGK5WLeftTreeIso e g h t ≪≫
    nativeGK5GChangeTreeIso
      (fun k : I => ((e k).trans (g k)).trans (h k)) t

/-- The RIGHT independently directly constructed recursive Phi. -/
noncomputable def nativeGK5WRightDirectPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
    nativeGK5GChangeAtom
      (fun k : I => (e k).trans ((g k).trans (h k)))
      (nativeGK5DTreeComposite t) :=
  nativeGK5WRightTreeIso e g h t ≪≫
    nativeGK5GChangeTreeIso
      (fun k : I => (e k).trans ((g k).trans (h k))) t

/-- The whole typed-tree left and right structural comparisons
obey the REAL Mathlib whole NatIso associativity triangle. -/
theorem nativeGK5WTreeAssociator_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WLeftTreeIso e g h t ≪≫
        nativeGK5VAssocTreeIso e g h t =
      nativeGK5WRightTreeIso e g h t := by
  simp only [nativeGK5WLeftTreeIso, nativeGK5VAssocTreeIso,
    nativeGK5WRightTreeIso, eqToIso_trans]

/-- True left collapse: two uses of GK5U, plus equality-induced
naturality of the third actual recursive GK5G Phi. -/
theorem nativeGK5WLeftDirect_eq_recursive
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WLeftDirectPhi e g h t =
      nativeGK5VLeftPhi e g h t := by
  have htree :
      nativeGK5WLeftInitialTreeIso e g h t ≪≫
        nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree
            (fun k : I => (e k).trans (g k)) t) =
      nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5QTreeComparison e g t) := by
    simpa only [nativeGK5WLeftInitialTreeIso,
      nativeGK5QTreeComparison] using
      (nativeGK5WTreePhi_eqToIso_square h
        (nativeGK5QChangeTree_comp e g t))
  have hmid :
      nativeGK5WLeftInitialTreeIso e g h t ≪≫
        nativeGK5RSequentialCompositePhi
          (fun k : I => (e k).trans (g k)) h t =
      (nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5RDirectCompositePhi e g t)) ≪≫
        nativeGK5QAtomComparison
          (fun k : I => (e k).trans (g k)) h
          (nativeGK5DTreeComposite t) := by
    calc
      _ = ((nativeGK5WLeftInitialTreeIso e g h t ≪≫
          nativeGK5GChangeTreeIso h
            (nativeGK5GChangeTree
              (fun k : I => (e k).trans (g k)) t)) ≪≫
          nativeGK5GChangeIso h
            (nativeGK5GChangeTreeIso
              (fun k : I => (e k).trans (g k)) t)) ≪≫
          nativeGK5QAtomComparison
            (fun k : I => (e k).trans (g k)) h
            (nativeGK5DTreeComposite t) := by
              simp only [nativeGK5RSequentialCompositePhi,
                nativeGK5RSequentialPhi, Iso.trans_assoc]
      _ = ((nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
          nativeGK5GChangeIso h (nativeGK5QTreeComparison e g t)) ≪≫
          nativeGK5GChangeIso h
            (nativeGK5GChangeTreeIso
              (fun k : I => (e k).trans (g k)) t)) ≪≫
          nativeGK5QAtomComparison
            (fun k : I => (e k).trans (g k)) h
            (nativeGK5DTreeComposite t) := by rw [htree]
      _ = ((nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
          nativeGK5GChangeIso h
            (nativeGK5RDirectCompositePhi e g t)) ≪≫
          nativeGK5QAtomComparison
            (fun k : I => (e k).trans (g k)) h
            (nativeGK5DTreeComposite t)) := by
              simp only [nativeGK5RDirectCompositePhi,
                nativeGK5HChangeIso_trans, Iso.trans_assoc]
  calc
    _ = nativeGK5WLeftInitialTreeIso e g h t ≪≫
      nativeGK5RDirectCompositePhi
        (fun k : I => (e k).trans (g k)) h t := by
          simp only [nativeGK5WLeftDirectPhi,
            nativeGK5WLeftTreeIso_factor,
            nativeGK5RDirectCompositePhi, Iso.trans_assoc]
    _ = nativeGK5WLeftInitialTreeIso e g h t ≪≫
      nativeGK5RSequentialCompositePhi
        (fun k : I => (e k).trans (g k)) h t := by
          rw [nativeGK5UAllTrees_unconditional
            (fun k : I => (e k).trans (g k)) h t]
    _ = (nativeGK5GChangeTreeIso h
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5RDirectCompositePhi e g t)) ≪≫
        nativeGK5QAtomComparison
          (fun k : I => (e k).trans (g k)) h
          (nativeGK5DTreeComposite t) := hmid
    _ = nativeGK5VLeftPhi e g h t :=
      (nativeGK5VLeftPhi_viaGK5U e g h t).symm

/-- True right collapse: GK5U on g,h and on e,(g.trans h),
and GK5Q NATURALITY for an arbitrary whole NatIso Phi_e(t).
This is not justified by the equality-induced path case alone. -/
theorem nativeGK5WRightDirect_eq_recursive
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WRightDirectPhi e g h t =
      nativeGK5VRightPhi e g h t := by
  have hnatural :=
    nativeGK5WAtomComparison_natIso g h
      (nativeGK5GChangeTreeIso e t)
  calc
    _ = nativeGK5QTreeComparison g h (nativeGK5GChangeTree e t) ≪≫
      nativeGK5RDirectCompositePhi e
        (fun k : I => (g k).trans (h k)) t := by
          simp only [nativeGK5WRightDirectPhi,
            nativeGK5WRightTreeIso_factor,
            nativeGK5RDirectCompositePhi, Iso.trans_assoc]
    _ = nativeGK5QTreeComparison g h (nativeGK5GChangeTree e t) ≪≫
      nativeGK5RSequentialCompositePhi e
        (fun k : I => (g k).trans (h k)) t := by
          rw [nativeGK5UAllTrees_unconditional e
            (fun k : I => (g k).trans (h k)) t]
    _ = ((nativeGK5QTreeComparison g h (nativeGK5GChangeTree e t) ≪≫
        nativeGK5GChangeTreeIso
          (fun k : I => (g k).trans (h k))
          (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso
          (fun k : I => (g k).trans (h k))
          (nativeGK5GChangeTreeIso e t)) ≪≫
        nativeGK5QAtomComparison e
          (fun k : I => (g k).trans (h k))
          (nativeGK5DTreeComposite t) := by
            simp only [nativeGK5RSequentialCompositePhi,
              nativeGK5RSequentialPhi, Iso.trans_assoc]
    _ = (nativeGK5RSequentialCompositePhi g h
          (nativeGK5GChangeTree e t) ≪≫
        nativeGK5GChangeIso
          (fun k : I => (g k).trans (h k))
          (nativeGK5GChangeTreeIso e t)) ≪≫
        nativeGK5QAtomComparison e
          (fun k : I => (g k).trans (h k))
          (nativeGK5DTreeComposite t) := by
            rw [nativeGK5UAllTrees_unconditional g h
              (nativeGK5GChangeTree e t)]
            rfl
    _ = (((nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t))) ≪≫
        nativeGK5QAtomComparison g h
          (nativeGK5DTreeComposite (nativeGK5GChangeTree e t))) ≪≫
        nativeGK5GChangeIso
          (fun k : I => (g k).trans (h k))
          (nativeGK5GChangeTreeIso e t)) ≪≫
        nativeGK5QAtomComparison e
          (fun k : I => (g k).trans (h k))
          (nativeGK5DTreeComposite t) := by
            rfl
    _ = (((nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t))) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5GChangeIso g (nativeGK5GChangeTreeIso e t))) ≪≫
        nativeGK5QAtomComparison g h
          (nativeGK5GChangeAtom e (nativeGK5DTreeComposite t))) ≪≫
        nativeGK5QAtomComparison e
          (fun k : I => (g k).trans (h k))
          (nativeGK5DTreeComposite t) := by
            simpa only [Iso.trans_assoc] using
              congrArg (fun β =>
                ((nativeGK5GChangeTreeIso h
                    (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
                  nativeGK5GChangeIso h
                    (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t))) ≪≫
                  β) ≪≫
                  nativeGK5QAtomComparison e
                    (fun k : I => (g k).trans (h k))
                    (nativeGK5DTreeComposite t)) hnatural.symm
    _ = nativeGK5VRightPhi e g h t := by
      simp only [nativeGK5VRightPhi, nativeGK5VThreeStageSequentialPhi,
        Iso.trans_assoc]

/-- Strong GK5W main theorem: the TWO INDEPENDENT genuine
direct recursive Phi witnesses for the left and right composite
equivalences agree through the real whole Mathlib associator. -/
theorem nativeGK5WAllTrees_direct_assoc_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5WLeftDirectPhi e g h t ≪≫
        nativeGK5VAssocAtomIso e g h (nativeGK5DTreeComposite t) =
      nativeGK5WRightDirectPhi e g h t := by
  rw [nativeGK5WLeftDirect_eq_recursive,
    nativeGK5WRightDirect_eq_recursive]
  exact nativeGK5VAllTrees_assoc_whole e g h t

/-- Genuine relative whole target automorphism obstruction
between independently built direct recursive left/right Phi
is the actual reflexivity Iso, for ALL finite typed trees. -/
theorem nativeGK5WDirectObstruction_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5WLeftDirectPhi e g h t ≪≫
      nativeGK5VAssocAtomIso e g h
        (nativeGK5DTreeComposite t)).symm ≪≫
      nativeGK5WRightDirectPhi e g h t = Iso.refl _ := by
  rw [nativeGK5WAllTrees_direct_assoc_whole]
  simp only [Iso.symm_self_id]

#print axioms nativeGK5WAtomComparison_natIso
#print axioms nativeGK5WLeftTreeEq
#print axioms nativeGK5WRightTreeEq
#print axioms nativeGK5WLeftTreeIso
#print axioms nativeGK5WRightTreeIso
#print axioms nativeGK5WTreeAssociator_whole
#print axioms nativeGK5WLeftDirectPhi
#print axioms nativeGK5WRightDirectPhi
#print axioms nativeGK5WLeftDirect_eq_recursive
#print axioms nativeGK5WRightDirect_eq_recursive
#print axioms nativeGK5WAllTrees_direct_assoc_whole
#print axioms nativeGK5WDirectObstruction_refl

end TripleIndependentDirectPhi
end
end Kuu.F112.Physical
