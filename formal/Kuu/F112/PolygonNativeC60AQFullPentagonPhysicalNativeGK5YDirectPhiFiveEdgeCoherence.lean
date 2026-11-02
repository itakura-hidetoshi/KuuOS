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
  have hleft :
      eqToIso (congrArg nativeGK5DTreeComposite
        (p.trans (nativeGK5WLeftTreeEq a b c t))) =
      eqToIso (congrArg nativeGK5DTreeComposite p) ≪≫
        eqToIso (congrArg nativeGK5DTreeComposite
          (nativeGK5WLeftTreeEq a b c t)) :=
    (eqToIso_trans _ _).symm
  have hright :
      eqToIso (congrArg nativeGK5DTreeComposite
        (p.trans (nativeGK5WRightTreeEq a b c t))) =
      eqToIso (congrArg nativeGK5DTreeComposite p) ≪≫
        eqToIso (congrArg nativeGK5DTreeComposite
          (nativeGK5WRightTreeEq a b c t)) :=
    (eqToIso_trans _ _).symm
  rw [hleft, hright]
  simpa only [nativeGK5WLeftDirectPhi, nativeGK5WRightDirectPhi,
    nativeGK5WLeftTreeIso, nativeGK5WRightTreeIso,
    Iso.trans_assoc] using
    congrArg
      (fun iso => eqToIso (congrArg nativeGK5DTreeComposite p) ≪≫ iso)
      (nativeGK5WAllTrees_direct_assoc_whole a b c t)

end ThreeInFour


section GenuinePostcontext
variable {I : Type uI} {A B T : I → Cat.{vC,uC}}
variable (p q : ∀ i : I, A i ≌ B i)
variable (z : ∀ i : I, B i ≌ T i)

/-- Transport of equality-induced whole Mathlib NatIso through a
real third equivalence, with both genuine whiskerings preserved. -/
private theorem nativeGK5YChangeIso_eqToIso
    {i j : I} {R S : B i ⥤ B j} (h : R = S) :
    nativeGK5GChangeIso z (eqToIso h) =
      eqToIso (congrArg (nativeGK5GChangeAtom z) h) := by
  cases h
  simp only [eqToIso_refl, nativeGK5GChangeIso, nativeGK5GChangeAtom,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl]

/-- Genuine GK5G recursive Phi is natural along an equality of
complete typed trees, with no strictification of its unit/counit. -/
private theorem nativeGK5YTreePhi_eqToIso_square
    {i j : I} {u v : NativeGK5DTypedTree B i j} (h : u = v) :
    eqToIso (congrArg
      (fun x : NativeGK5DTypedTree B i j =>
        nativeGK5DTreeComposite (nativeGK5GChangeTree z x)) h) ≪≫
      nativeGK5GChangeTreeIso z v =
    nativeGK5GChangeTreeIso z u ≪≫
      nativeGK5GChangeIso z
        (eqToIso (congrArg nativeGK5DTreeComposite h)) := by
  cases h
  simp only [congrArg, eqToIso_refl, Iso.refl_trans, Iso.trans_refl,
    nativeGK5GChangeIso, nativeGK5GChangeAtom,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl]

/-- A pointwise actual atom equality between two real equivalences
induces an atom equality after right composition with z. -/
private theorem nativeGK5YPostAtomEq
    (hAtom : ∀ {i j : I} (R : A i ⥤ A j),
      nativeGK5GChangeAtom p R = nativeGK5GChangeAtom q R)
    {i j : I} (R : A i ⥤ A j) :
    nativeGK5GChangeAtom (fun x : I => (p x).trans (z x)) R =
      nativeGK5GChangeAtom (fun x : I => (q x).trans (z x)) R := by
  calc
    _ = nativeGK5GChangeAtom z (nativeGK5GChangeAtom p R) :=
      (nativeGK5QChangeAtom_comp p z R).symm
    _ = nativeGK5GChangeAtom z (nativeGK5GChangeAtom q R) :=
      congrArg (nativeGK5GChangeAtom z) (hAtom R)
    _ = _ := nativeGK5QChangeAtom_comp q z R

/-- A natural whole equality-induced comparison commutes with the
genuine GK5Q two-stage atomic theta, even after the additional
nonstrict equivalence z. -/
private theorem nativeGK5YPostAtomSquare
    (hAtom : ∀ {i j : I} (R : A i ⥤ A j),
      nativeGK5GChangeAtom p R = nativeGK5GChangeAtom q R)
    {i j : I} (R : A i ⥤ A j) :
    nativeGK5GChangeIso z (eqToIso (hAtom R)) ≪≫
      nativeGK5QAtomComparison q z R =
    nativeGK5QAtomComparison p z R ≪≫
      eqToIso (nativeGK5YPostAtomEq p q z hAtom R) := by
  rw [nativeGK5YChangeIso_eqToIso z (hAtom R)]
  simp only [nativeGK5QAtomComparison, eqToIso_trans]

/-- Independently direct genuine two-stage Phi, with a changed
source tree u whose equality with the p-transported tree is proved
rather than silently assumed. -/
private noncomputable def nativeGK5YPostDirect
    (a : ∀ i : I, A i ≌ B i)
    {i j : I} (t : NativeGK5DTypedTree A i j)
    (u : NativeGK5DTypedTree B i j)
    (hu : u = nativeGK5GChangeTree a t) :
    nativeGK5DTreeComposite (nativeGK5GChangeTree z u) ≅
      nativeGK5GChangeAtom (fun x : I => (a x).trans (z x))
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      ((congrArg (nativeGK5GChangeTree z) hu).trans
        (nativeGK5QChangeTree_comp a z t))) ≪≫
    nativeGK5GChangeTreeIso
      (fun x : I => (a x).trans (z x)) t

/-- Actual GK5U normalization of the preceding direct two-stage
recursive Phi through the true middle unit and the whole NatIso
map of the already established original direct Phi. -/
private theorem nativeGK5YPostDirect_normalize
    (a : ∀ i : I, A i ≌ B i)
    {i j : I} (t : NativeGK5DTypedTree A i j)
    (u : NativeGK5DTypedTree B i j)
    (hu : u = nativeGK5GChangeTree a t) :
    nativeGK5YPostDirect z a t u hu =
      (nativeGK5GChangeTreeIso z u ≪≫
        nativeGK5GChangeIso z
          (eqToIso (congrArg nativeGK5DTreeComposite hu) ≪≫
            nativeGK5GChangeTreeIso a t)) ≪≫
        nativeGK5QAtomComparison a z (nativeGK5DTreeComposite t) := by
  have hsplit :
      eqToIso (congrArg nativeGK5DTreeComposite
        ((congrArg (nativeGK5GChangeTree z) hu).trans
          (nativeGK5QChangeTree_comp a z t))) =
      eqToIso (congrArg nativeGK5DTreeComposite
        (congrArg (nativeGK5GChangeTree z) hu)) ≪≫
        nativeGK5QTreeComparison a z t :=
    (eqToIso_trans _ _).symm
  calc
    _ = (eqToIso (congrArg nativeGK5DTreeComposite
        (congrArg (nativeGK5GChangeTree z) hu)) ≪≫
        nativeGK5QTreeComparison a z t) ≪≫
        nativeGK5GChangeTreeIso
          (fun x : I => (a x).trans (z x)) t := by
          simpa only [nativeGK5YPostDirect] using
            congrArg (fun iso => iso ≪≫ nativeGK5GChangeTreeIso
              (fun x : I => (a x).trans (z x)) t) hsplit
    _ = eqToIso (congrArg nativeGK5DTreeComposite
        (congrArg (nativeGK5GChangeTree z) hu)) ≪≫
        nativeGK5RDirectCompositePhi a z t := by
          simp only [nativeGK5RDirectCompositePhi, Iso.trans_assoc]
    _ = eqToIso (congrArg nativeGK5DTreeComposite
        (congrArg (nativeGK5GChangeTree z) hu)) ≪≫
        nativeGK5RSequentialCompositePhi a z t := by
          rw [nativeGK5UAllTrees_unconditional a z t]
    _ = ((eqToIso (congrArg nativeGK5DTreeComposite
          (congrArg (nativeGK5GChangeTree z) hu)) ≪≫
        nativeGK5GChangeTreeIso z (nativeGK5GChangeTree a t)) ≪≫
        nativeGK5GChangeIso z (nativeGK5GChangeTreeIso a t)) ≪≫
        nativeGK5QAtomComparison a z (nativeGK5DTreeComposite t) := by
          simp only [nativeGK5RSequentialCompositePhi,
            nativeGK5RSequentialPhi, Iso.trans_assoc]
    _ = ((nativeGK5GChangeTreeIso z u ≪≫
        nativeGK5GChangeIso z
          (eqToIso (congrArg nativeGK5DTreeComposite hu))) ≪≫
        nativeGK5GChangeIso z (nativeGK5GChangeTreeIso a t)) ≪≫
        nativeGK5QAtomComparison a z (nativeGK5DTreeComposite t) := by
          rw [nativeGK5YTreePhi_eqToIso_square z hu]
    _ = _ := by
      simp only [nativeGK5HChangeIso_trans, Iso.trans_assoc]

/-- Genuine postcomposition contextual coherence: if two real
recursive Phi comparisons agree up to the equality-induced whole
atom NatIso, the direct recursive Phi for their compositions with
any third genuine equivalence z agrees with no additional premise. -/
private theorem nativeGK5YPostCoherent
    (hAtom : ∀ {i j : I} (R : A i ⥤ A j),
      nativeGK5GChangeAtom p R = nativeGK5GChangeAtom q R)
    {i j : I} (t : NativeGK5DTypedTree A i j)
    (u : NativeGK5DTypedTree B i j)
    (hp : u = nativeGK5GChangeTree p t)
    (hq : u = nativeGK5GChangeTree q t)
    (hPhi :
      (eqToIso (congrArg nativeGK5DTreeComposite hp) ≪≫
        nativeGK5GChangeTreeIso p t) ≪≫
        eqToIso (hAtom (nativeGK5DTreeComposite t)) =
      eqToIso (congrArg nativeGK5DTreeComposite hq) ≪≫
        nativeGK5GChangeTreeIso q t) :
    nativeGK5YPostDirect z p t u hp ≪≫
        eqToIso (nativeGK5YPostAtomEq p q z hAtom
          (nativeGK5DTreeComposite t)) =
      nativeGK5YPostDirect z q t u hq := by
  let Wp := eqToIso (congrArg nativeGK5DTreeComposite hp) ≪≫
    nativeGK5GChangeTreeIso p t
  let Wq := eqToIso (congrArg nativeGK5DTreeComposite hq) ≪≫
    nativeGK5GChangeTreeIso q t
  let α := eqToIso (hAtom (nativeGK5DTreeComposite t))
  let θp := nativeGK5QAtomComparison p z (nativeGK5DTreeComposite t)
  let θq := nativeGK5QAtomComparison q z (nativeGK5DTreeComposite t)
  let β := eqToIso (nativeGK5YPostAtomEq p q z hAtom
    (nativeGK5DTreeComposite t))
  let ι := nativeGK5GChangeTreeIso z u
  have hmap : nativeGK5GChangeIso z Wp ≪≫
      nativeGK5GChangeIso z α =
    nativeGK5GChangeIso z Wq := by
    rw [← nativeGK5HChangeIso_trans]
    exact congrArg (nativeGK5GChangeIso z) hPhi
  have hsquare : nativeGK5GChangeIso z α ≪≫ θq = θp ≪≫ β :=
    nativeGK5YPostAtomSquare p q z hAtom
      (nativeGK5DTreeComposite t)
  calc
    _ = (ι ≪≫ nativeGK5GChangeIso z Wp) ≪≫ (θp ≪≫ β) := by
      simpa only [Wp, θp, β, ι, Iso.trans_assoc] using
        congrArg (fun iso => iso ≪≫ β)
          (nativeGK5YPostDirect_normalize z p t u hp)
    _ = (ι ≪≫ nativeGK5GChangeIso z Wp) ≪≫
        (nativeGK5GChangeIso z α ≪≫ θq) := by rw [hsquare]
    _ = (ι ≪≫ (nativeGK5GChangeIso z Wp ≪≫
        nativeGK5GChangeIso z α)) ≪≫ θq := by
          simp only [Iso.trans_assoc]
    _ = (ι ≪≫ nativeGK5GChangeIso z Wq) ≪≫ θq := by rw [hmap]
    _ = nativeGK5YPostDirect z q t u hq := by
      simpa only [Wq, θq, ι] using
        (nativeGK5YPostDirect_normalize z q t u hq).symm

end GenuinePostcontext

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
  simp only [Iso.self_symm_id]

/-- Genuine independently assembled source automorphism vanishes
along the full P0->P4 direct-Phi associativity edge. -/
theorem nativeGK5YDefect04_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect04 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect04
  rw [nativeGK5YEdge04_whole]
  simp only [Iso.self_symm_id]

/-- Genuine independently assembled source automorphism vanishes
along the full P4->P3 direct-Phi associativity edge. -/
theorem nativeGK5YDefect43_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect43 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect43
  rw [nativeGK5YEdge43_whole]
  simp only [Iso.self_symm_id]


/-- The P0->P1 genuine four-stage direct-Phi edge is the actual
GK5W triple associativity under a further real category equivalence
k, via whole NatIso post-whiskering and both actual GK5U comparisons.
No composite equivalence record is identified strictly. -/
theorem nativeGK5YEdge01_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi0 e g h k t ≪≫
      nativeGK5XEdge01 e g h k (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi1 e g h k t := by
  let P : ∀ x : I, C x ≌ F x :=
    fun x : I => ((e x).trans (g x)).trans (h x)
  let Q : ∀ x : I, C x ≌ F x :=
    fun x : I => (e x).trans ((g x).trans (h x))
  let U : NativeGK5DTypedTree F i j :=
    nativeGK5GChangeTree h
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))
  have hAtom : ∀ {x y : I} (R : C x ⥤ C y),
      nativeGK5GChangeAtom P R = nativeGK5GChangeAtom Q R := by
    intro x y R
    exact nativeGK5VChangeAtom_assoc e g h R
  have hPhi :
      (eqToIso (congrArg nativeGK5DTreeComposite
          (nativeGK5WLeftTreeEq e g h t)) ≪≫
        nativeGK5GChangeTreeIso P t) ≪≫
        eqToIso (hAtom (nativeGK5DTreeComposite t)) =
      eqToIso (congrArg nativeGK5DTreeComposite
          (nativeGK5WRightTreeEq e g h t)) ≪≫
        nativeGK5GChangeTreeIso Q t := by
    simpa only [P, Q, nativeGK5WLeftDirectPhi,
      nativeGK5WRightDirectPhi, nativeGK5WLeftTreeIso,
      nativeGK5WRightTreeIso, nativeGK5VAssocAtomIso] using
        (nativeGK5WAllTrees_direct_assoc_whole e g h t)
  have hpost :=
    nativeGK5YPostCoherent P Q k hAtom t U
      (nativeGK5WLeftTreeEq e g h t)
      (nativeGK5WRightTreeEq e g h t) hPhi
  simpa only [nativeGK5XDirectPhi0, nativeGK5XDirectPhi1,
    nativeGK5XEdge01, nativeGK5YPostDirect, P, Q, U] using hpost

/-- The nonstrict source-valued direct-Phi edge defect P0->P1
unconditionally vanishes for every actual finite typed tree. -/
theorem nativeGK5YDefect01_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect01 e g h k t = Iso.refl _ := by
  unfold nativeGK5XDefect01
  rw [nativeGK5YEdge01_whole]
  simp only [Iso.self_symm_id]

/-- The fifth direct-Phi edge defect vanishes by the CERTIFIED
GK5X genuine whole-NatIso pentagon, combined with the already
proved four edge defects. No new high cell or extra hypothesis. -/
theorem nativeGK5YDefect23_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect23 e g h k t = Iso.refl _ := by
  have hPentagon := nativeGK5XDirectDefectPentagon_whole e g h k t
  simpa only [nativeGK5YDefect01_refl, nativeGK5YDefect12_refl,
    nativeGK5YDefect04_refl, nativeGK5YDefect43_refl,
    Iso.refl_trans, Iso.trans_refl] using hPentagon

/-- The P2->P3 whole Mathlib NatIso square follows exactly from
the proven genuine relative direct-Phi defect obstruction being refl. -/
theorem nativeGK5YEdge23_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi2 e g h k t ≪≫
      nativeGK5XEdge23 e g h k (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi3 e g h k t := by
  have h := congrArg
    (fun iso => iso ≪≫ nativeGK5XDirectPhi3 e g h k t)
    (nativeGK5YDefect23_refl e g h k t)
  simpa only [nativeGK5XDefect23, Iso.trans_assoc,
    Iso.symm_self_id, Iso.trans_refl, Iso.refl_trans] using h

/-- Every one of the FIVE true four-stage direct-Phi associator
edges commutes as a whole Mathlib NatIso, unconditionally on all
finite genuine GK5D typed functor trees. -/
theorem nativeGK5YAllFiveEdges_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi0 e g h k t ≪≫
        nativeGK5XEdge01 e g h k (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi1 e g h k t) ∧
    (nativeGK5XDirectPhi1 e g h k t ≪≫
        nativeGK5XEdge12 e g h k (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi2 e g h k t) ∧
    (nativeGK5XDirectPhi2 e g h k t ≪≫
        nativeGK5XEdge23 e g h k (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi3 e g h k t) ∧
    (nativeGK5XDirectPhi0 e g h k t ≪≫
        nativeGK5XEdge04 e g h k (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi4 e g h k t) ∧
    (nativeGK5XDirectPhi4 e g h k t ≪≫
        nativeGK5XEdge43 e g h k (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi3 e g h k t) := by
  exact ⟨nativeGK5YEdge01_whole e g h k t,
    nativeGK5YEdge12_whole e g h k t,
    nativeGK5YEdge23_whole e g h k t,
    nativeGK5YEdge04_whole e g h k t,
    nativeGK5YEdge43_whole e g h k t⟩

/-- Unconditional complete five-edge relative obstruction
trivialization for all true Mathlib composite equivalences. -/
theorem nativeGK5YAllFiveDefects_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDefect01 e g h k t = Iso.refl _ ∧
    nativeGK5XDefect12 e g h k t = Iso.refl _ ∧
    nativeGK5XDefect23 e g h k t = Iso.refl _ ∧
    nativeGK5XDefect04 e g h k t = Iso.refl _ ∧
    nativeGK5XDefect43 e g h k t = Iso.refl _ := by
  exact ⟨nativeGK5YDefect01_refl e g h k t,
    nativeGK5YDefect12_refl e g h k t,
    nativeGK5YDefect23_refl e g h k t,
    nativeGK5YDefect04_refl e g h k t,
    nativeGK5YDefect43_refl e g h k t⟩

#print axioms nativeGK5YEdge01_whole
#print axioms nativeGK5YDefect01_refl
#print axioms nativeGK5YDefect23_refl
#print axioms nativeGK5YEdge23_whole
#print axioms nativeGK5YAllFiveEdges_whole
#print axioms nativeGK5YAllFiveDefects_refl

#print axioms nativeGK5YEdge12_whole
#print axioms nativeGK5YEdge04_whole
#print axioms nativeGK5YEdge43_whole
#print axioms nativeGK5YDefect12_refl
#print axioms nativeGK5YDefect04_refl
#print axioms nativeGK5YDefect43_refl

end FourGroupEdges
end
end Kuu.F112.Physical
