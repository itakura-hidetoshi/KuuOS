import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5XFourStageDirectPhiPentagon
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5Y — genuine four-stage direct Phi edge coherence.
Beginning with the three edges that are actual triple-equivalence
GK5W associativity after a certified typed-tree source transport.

All terms are whole Mathlib NatIso; no equivalence unit/counit
strictification, hypothesis weakening or raw higher cells.
Further contextual edges are the next proof obligations.

Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Canonical main, same-root107, append-only/tighten-only;
strict 空 center, independent Kuu one presentation;
protected #1558 Draft/open/unmerged.
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

section ThreeInFour
variable {I : Type uI} {A B C D : I → Cat.{vC,uC}}
variable (a : ∀ i : I, A i ≌ B i)
variable (b : ∀ i : I, B i ≌ C i)
variable (c : ∀ i : I, C i ≌ D i)

/-- An actual equality of the complete changed typed-tree SOURCE
may be prefixed to the true GK5W direct/direct triple associativity
without changing any nonstrict recursive Phi or its unit/counit.
This is a whole Mathlib NatIso pasting equation. -/
private theorem nativeGK5YLiftThree
    {i j : I} (t : NativeGK5DTypedTree A i j)
    (s : NativeGK5DTypedTree D i j)
    (p : s =
      nativeGK5GChangeTree c
        (nativeGK5GChangeTree b (nativeGK5GChangeTree a t))) :
    (eqToIso (congrArg nativeGK5DTreeComposite
        (p.trans (nativeGK5WLeftTreeEq a b c t))) ≪≫
      nativeGK5GChangeTreeIso
        (fun x : I => ((a x).trans (b x)).trans (c x)) t) ≪≫
        nativeGK5VAssocAtomIso a b c
          (nativeGK5DTreeComposite t) =
    eqToIso (congrArg nativeGK5DTreeComposite
        (p.trans (nativeGK5WRightTreeEq a b c t))) ≪≫
      nativeGK5GChangeTreeIso
        (fun x : I => (a x).trans ((b x).trans (c x))) t := by
  simpa only [nativeGK5WLeftDirectPhi, nativeGK5WRightDirectPhi,
    nativeGK5WLeftTreeIso, nativeGK5WRightTreeIso,
    eqToIso_trans, Iso.trans_assoc] using
    congrArg
      (fun iso => eqToIso (congrArg nativeGK5DTreeComposite p) ≪≫ iso)
      (nativeGK5WAllTrees_direct_assoc_whole a b c t)

end ThreeInFour

section FourGroupEdges
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)
variable (h : ∀ i : I, E i ≌ F i)
variable (k : ∀ i : I, F i ≌ G i)

/-- The genuine fully changed tree is equal to the threefold
changed tree for e, the REAL composite (g.trans h), and k.
This source equality precedes the GK5W 12-edge square. -/
private theorem nativeGK5YSource12
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree k
        (nativeGK5GChangeTree
          (fun x : I => (g x).trans (h x))
          (nativeGK5GChangeTree e t)) := by
  exact congrArg (nativeGK5GChangeTree k)
    (nativeGK5QChangeTree_comp g h (nativeGK5GChangeTree e t))

/-- The genuine fully changed tree is equal to the threefold
changed tree for (e.trans g), h, k. -/
private theorem nativeGK5YSource04
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree k
        (nativeGK5GChangeTree h
          (nativeGK5GChangeTree
            (fun x : I => (e x).trans (g x)) t)) := by
  exact congrArg (nativeGK5GChangeTree k)
    (congrArg (nativeGK5GChangeTree h)
      (nativeGK5QChangeTree_comp e g t))

/-- The genuine fully changed tree is equal to the threefold
changed tree for e, g, the REAL composite (h.trans k). -/
private theorem nativeGK5YSource43
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree
        (fun x : I => (h x).trans (k x))
        (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) := by
  exact nativeGK5QChangeTree_comp h k
    (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))

/-- Edge P1->P2 is a TRUE GK5W three-equivalence associativity
at the (e, g.trans h, k) grouping, transported through an actual
GK5Q typed-tree equality. This is the complete direct-Phi equation. -/
theorem nativeGK5YEdge12_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi1 e g h k t ≪≫
      nativeGK5XEdge12 e g h k (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi2 e g h k t := by
  simpa only [nativeGK5XDirectPhi1, nativeGK5XDirectPhi2,
    nativeGK5XEdge12] using
    (nativeGK5YLiftThree e
      (fun x : I => (g x).trans (h x)) k t
      (nativeGK5XFourTree e g h k t)
      (nativeGK5YSource12 e g h k t))

/-- Edge P0->P4 is a TRUE GK5W three-equivalence associativity
for ((e.trans g), h, k), with an independently certified whole
changed-tree equality at the original source. -/
theorem nativeGK5YEdge04_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi0 e g h k t ≪≫
      nativeGK5XEdge04 e g h k (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi4 e g h k t := by
  simpa only [nativeGK5XDirectPhi0, nativeGK5XDirectPhi4,
    nativeGK5XEdge04] using
    (nativeGK5YLiftThree
      (fun x : I => (e x).trans (g x)) h k t
      (nativeGK5XFourTree e g h k t)
      (nativeGK5YSource04 e g h k t))

/-- Edge P4->P3 is the true GK5W associativity for
(e, g, (h.trans k)), including nonstrict three-stage unit/counit
and every finite typed binary tree. -/
theorem nativeGK5YEdge43_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi4 e g h k t ≪≫
      nativeGK5XEdge43 e g h k (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi3 e g h k t := by
  simpa only [nativeGK5XDirectPhi4, nativeGK5XDirectPhi3,
    nativeGK5XEdge43] using
    (nativeGK5YLiftThree e g
      (fun x : I => (h x).trans (k x)) t
      (nativeGK5XFourTree e g h k t)
      (nativeGK5YSource43 e g h k t))

/-- Genuine independently assembled source automorphism vanishes
along the full P1->P2 direct-Phi associativity edge. -/
theorem nativeGK5YDefect12_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect12 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect12
  rw [nativeGK5YEdge12_whole]
  simp only [Iso.symm_self_id]

/-- Genuine independently assembled source automorphism vanishes
along the full P0->P4 direct-Phi associativity edge. -/
theorem nativeGK5YDefect04_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect04 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect04
  rw [nativeGK5YEdge04_whole]
  simp only [Iso.symm_self_id]

/-- Genuine independently assembled source automorphism vanishes
along the full P4->P3 direct-Phi associativity edge. -/
theorem nativeGK5YDefect43_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect43 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect43
  rw [nativeGK5YEdge43_whole]
  simp only [Iso.symm_self_id]

#print axioms nativeGK5YEdge12_whole
#print axioms nativeGK5YEdge04_whole
#print axioms nativeGK5YEdge43_whole
#print axioms nativeGK5YDefect12_refl
#print axioms nativeGK5YDefect04_refl
#print axioms nativeGK5YDefect43_refl

end FourGroupEdges
end
end Kuu.F112.Physical
