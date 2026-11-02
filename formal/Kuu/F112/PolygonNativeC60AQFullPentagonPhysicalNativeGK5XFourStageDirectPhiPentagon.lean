import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5WIndependentDirectTriplePhiCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5X — genuine four-stage Mathlib equivalences and the
whole-NatIso five-parenthesization pentagon for finite heterogeneous
typed functor trees.

Five independently defined direct recursive GK5G Phi witnesses retain
all nonstrict unit/counit and chosen quasi-inverse data. The five true
composite equivalence records are NOT assumed or asserted equal.
Their changed functors possess canonical eqToIso associators, whose
two paths around the genuine five-vertex pentagon coincide as whole
Mathlib NatIso and NatTrans. Their five genuinely target-typed direct
Phi values induce source-valued relative automorphism defects.
The product of defects is independent of the two pentagon paths.

IMPORTANT BOUNDARY: The five individual direct-Phi edge defects are
not here claimed to be refl. Their triviality is the separate stronger
four-stage pseudofunctor compatibility obligation. No source-Q/raw
higher cells, global Gray, or unrestricted hyperdescent is inferred.

Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, canonical main, same-root107, strict 空 centered,
independent Kuu one presentation, #1558 Draft/open/unmerged.
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

section FourEquivalencePentagon
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)
variable (h : ∀ i : I, E i ≌ F i)
variable (k : ∀ i : I, F i ≌ G i)

/- The five actual Catalan parenthesizations, as true Mathlib
Equivalence.trans values, not new formal strict associative data. -/

/-- Actual four-stage parenthesization P0. -/
def nativeGK5XBracket0 : ∀ i : I, C i ≌ G i :=
  fun i : I => (((e i).trans (g i)).trans (h i)).trans (k i)

/-- Actual four-stage parenthesization P1. -/
def nativeGK5XBracket1 : ∀ i : I, C i ≌ G i :=
  fun i : I => ((e i).trans ((g i).trans (h i))).trans (k i)

/-- Actual four-stage parenthesization P2. -/
def nativeGK5XBracket2 : ∀ i : I, C i ≌ G i :=
  fun i : I => (e i).trans (((g i).trans (h i)).trans (k i))

/-- Actual four-stage parenthesization P3. -/
def nativeGK5XBracket3 : ∀ i : I, C i ≌ G i :=
  fun i : I => (e i).trans ((g i).trans ((h i).trans (k i)))

/-- Actual four-stage parenthesization P4. -/
def nativeGK5XBracket4 : ∀ i : I, C i ≌ G i :=
  fun i : I => ((e i).trans (g i)).trans ((h i).trans (k i))

/- Canonical atom equalities retain the true two-sided conjugation
functors and use only Mathlib Equivalence.trans_functor /
Equivalence.trans_inverse and Functor.assoc. None identifies units. -/

/-- True changed-atom equality for pentagon vertices P0 and P1. -/
theorem nativeGK5XAtomEq01
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket0, nativeGK5XBracket1,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P1 and P2. -/
theorem nativeGK5XAtomEq12
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket1, nativeGK5XBracket2,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P2 and P3. -/
theorem nativeGK5XAtomEq23
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket2, nativeGK5XBracket3,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P0 and P4. -/
theorem nativeGK5XAtomEq04
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket0, nativeGK5XBracket4,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P4 and P3. -/
theorem nativeGK5XAtomEq43
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket4, nativeGK5XBracket3,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P0 and P2. -/
theorem nativeGK5XAtomEq02
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket0, nativeGK5XBracket2,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- True changed-atom equality for pentagon vertices P0 and P3. -/
theorem nativeGK5XAtomEq03
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R =
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k) R := by
  simp only [nativeGK5GChangeAtom,
    nativeGK5XBracket0, nativeGK5XBracket3,
    Equivalence.trans_functor, Equivalence.trans_inverse,
    Functor.assoc]

/-- A source-type-preserving finite typed tree change follows
any pointwise equality of genuinely conjugated atomic functors. -/
private theorem nativeGK5XTreeEqOfAtoms
    (p q : ∀ i : I, C i ≌ G i)
    (heq : ∀ {i j : I} (R : C i ⥤ C j),
      nativeGK5GChangeAtom p R = nativeGK5GChangeAtom q R)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeTree p t = nativeGK5GChangeTree q t := by
  induction t with
  | unit i => rfl
  | atom R =>
      simpa only [nativeGK5GChangeTree] using
        congrArg NativeGK5DTypedTree.atom (heq R)
  | paste left right hl hr =>
      simp only [nativeGK5GChangeTree, hl, hr]

/-- The fully genuinely changed fourfold finite typed tree, with
all intermediate category families preserved in the source term. -/
def nativeGK5XFourTree
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    NativeGK5DTypedTree G i j :=
  nativeGK5GChangeTree k
    (nativeGK5GChangeTree h
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)))

/-- The first fourfold tree evaluation equality is a genuine
composition of three certified GK5Q dependent-tree equalities. -/
theorem nativeGK5XFourTreeEq0
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t := by
  calc
    _ = nativeGK5GChangeTree k
        (nativeGK5GChangeTree h
          (nativeGK5GChangeTree
            (fun x : I => (e x).trans (g x)) t)) := by
          dsimp only [nativeGK5XFourTree]
          rw [nativeGK5QChangeTree_comp e g t]
    _ = nativeGK5GChangeTree k
        (nativeGK5GChangeTree
          (fun x : I => ((e x).trans (g x)).trans (h x)) t) := by
          rw [nativeGK5QChangeTree_comp
            (fun x : I => (e x).trans (g x)) h t]
    _ = nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t :=
      nativeGK5QChangeTree_comp
        (fun x : I => ((e x).trans (g x)).trans (h x)) k t

/-- Independently typed direct-tree comparison for P1. -/
theorem nativeGK5XFourTreeEq1
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree (nativeGK5XBracket1 e g h k) t := by
  calc
    _ = nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t :=
      nativeGK5XFourTreeEq0 e g h k t
    _ = _ := nativeGK5XTreeEqOfAtoms (nativeGK5XBracket0 e g h k) (nativeGK5XBracket1 e g h k)
      (nativeGK5XAtomEq01 e g h k) t

/-- Independently typed direct-tree comparison for P2. -/
theorem nativeGK5XFourTreeEq2
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree (nativeGK5XBracket2 e g h k) t := by
  calc
    _ = nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t :=
      nativeGK5XFourTreeEq0 e g h k t
    _ = _ := nativeGK5XTreeEqOfAtoms (nativeGK5XBracket0 e g h k) (nativeGK5XBracket2 e g h k)
      (nativeGK5XAtomEq02 e g h k) t

/-- Independently typed direct-tree comparison for P3. -/
theorem nativeGK5XFourTreeEq3
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree (nativeGK5XBracket3 e g h k) t := by
  calc
    _ = nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t :=
      nativeGK5XFourTreeEq0 e g h k t
    _ = _ := nativeGK5XTreeEqOfAtoms (nativeGK5XBracket0 e g h k) (nativeGK5XBracket3 e g h k)
      (nativeGK5XAtomEq03 e g h k) t

/-- Independently typed direct-tree comparison for P4. -/
theorem nativeGK5XFourTreeEq4
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XFourTree e g h k t =
      nativeGK5GChangeTree (nativeGK5XBracket4 e g h k) t := by
  calc
    _ = nativeGK5GChangeTree (nativeGK5XBracket0 e g h k) t :=
      nativeGK5XFourTreeEq0 e g h k t
    _ = _ := nativeGK5XTreeEqOfAtoms (nativeGK5XBracket0 e g h k) (nativeGK5XBracket4 e g h k)
      (nativeGK5XAtomEq04 e g h k) t


/- The next five witnesses are all independently assembled DIRECT
recursive GK5G Phi for the actual bracketed equivalence, preceded
only by the true eqToIso of its independently proved tree equality.
They share a source but preserve their distinct actual equivalences. -/

/-- Genuine independently constructed direct recursive Phi for P0. -/
noncomputable def nativeGK5XDirectPhi0
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k)
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5XFourTreeEq0 e g h k t)) ≪≫
    nativeGK5GChangeTreeIso (nativeGK5XBracket0 e g h k) t

/-- Genuine independently constructed direct recursive Phi for P1. -/
noncomputable def nativeGK5XDirectPhi1
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k)
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5XFourTreeEq1 e g h k t)) ≪≫
    nativeGK5GChangeTreeIso (nativeGK5XBracket1 e g h k) t

/-- Genuine independently constructed direct recursive Phi for P2. -/
noncomputable def nativeGK5XDirectPhi2
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k)
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5XFourTreeEq2 e g h k t)) ≪≫
    nativeGK5GChangeTreeIso (nativeGK5XBracket2 e g h k) t

/-- Genuine independently constructed direct recursive Phi for P3. -/
noncomputable def nativeGK5XDirectPhi3
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k)
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5XFourTreeEq3 e g h k t)) ≪≫
    nativeGK5GChangeTreeIso (nativeGK5XBracket3 e g h k) t

/-- Genuine independently constructed direct recursive Phi for P4. -/
noncomputable def nativeGK5XDirectPhi4
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k)
        (nativeGK5DTreeComposite t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5XFourTreeEq4 e g h k t)) ≪≫
    nativeGK5GChangeTreeIso (nativeGK5XBracket4 e g h k) t

/- Edges are the actual whole Mathlib eqToIso of five true
associativity equalities between composite-conjugation functors.
Three edges are direct GK5V associators, with the other two
being their left/right contextual association comparisons. -/

/-- Genuine whole Mathlib NatIso along pentagon edge P0 -> P1. -/
noncomputable def nativeGK5XEdge01
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k) R :=
  eqToIso (nativeGK5XAtomEq01 e g h k R)

/-- Genuine whole Mathlib NatIso along pentagon edge P1 -> P2. -/
noncomputable def nativeGK5XEdge12
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k) R :=
  eqToIso (nativeGK5XAtomEq12 e g h k R)

/-- Genuine whole Mathlib NatIso along pentagon edge P2 -> P3. -/
noncomputable def nativeGK5XEdge23
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k) R :=
  eqToIso (nativeGK5XAtomEq23 e g h k R)

/-- Genuine whole Mathlib NatIso along pentagon edge P0 -> P4. -/
noncomputable def nativeGK5XEdge04
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k) R :=
  eqToIso (nativeGK5XAtomEq04 e g h k R)

/-- Genuine whole Mathlib NatIso along pentagon edge P4 -> P3. -/
noncomputable def nativeGK5XEdge43
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k) R :=
  eqToIso (nativeGK5XAtomEq43 e g h k R)

/-- The real Mathlib four-factor pentagon commutes as a WHOLE NatIso,
not only on a selected object: three association edges equal two. -/
theorem nativeGK5XPentagon_whole
    {i j : I} (R : C i ⥤ C j) :
    (nativeGK5XEdge01 e g h k R ≪≫
      nativeGK5XEdge12 e g h k R) ≪≫
      nativeGK5XEdge23 e g h k R =
    nativeGK5XEdge04 e g h k R ≪≫
      nativeGK5XEdge43 e g h k R := by
  simp only [nativeGK5XEdge01, nativeGK5XEdge12,
    nativeGK5XEdge23, nativeGK5XEdge04, nativeGK5XEdge43,
    eqToIso_trans]

/-- The pentagon as an equality of actual whole Mathlib NatTrans,
including all source and target functor category data. -/
theorem nativeGK5XPentagon_natTrans
    {i j : I} (R : C i ⥤ C j) :
    ((nativeGK5XEdge01 e g h k R ≪≫
        nativeGK5XEdge12 e g h k R) ≪≫
        nativeGK5XEdge23 e g h k R).hom =
      (nativeGK5XEdge04 e g h k R ≪≫
        nativeGK5XEdge43 e g h k R).hom :=
  congrArg Iso.hom (nativeGK5XPentagon_whole e g h k R)

/- Each EDGE DEFECT is a true whole NatIso automorphism of the same
original fourfold changed-tree evaluation, formed using the two
independent actual DIRECT recursive Phi witnesses at its endpoints.
Individual defect triviality is intentionally NOT assumed. -/

/-- Actual relative direct-Phi source automorphism for P0 -> P1. -/
noncomputable def nativeGK5XDefect01
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) :=
  (nativeGK5XDirectPhi0 e g h k t ≪≫
    nativeGK5XEdge01 e g h k (nativeGK5DTreeComposite t)) ≪≫
    (nativeGK5XDirectPhi1 e g h k t).symm

/-- Actual relative direct-Phi source automorphism for P1 -> P2. -/
noncomputable def nativeGK5XDefect12
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) :=
  (nativeGK5XDirectPhi1 e g h k t ≪≫
    nativeGK5XEdge12 e g h k (nativeGK5DTreeComposite t)) ≪≫
    (nativeGK5XDirectPhi2 e g h k t).symm

/-- Actual relative direct-Phi source automorphism for P2 -> P3. -/
noncomputable def nativeGK5XDefect23
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) :=
  (nativeGK5XDirectPhi2 e g h k t ≪≫
    nativeGK5XEdge23 e g h k (nativeGK5DTreeComposite t)) ≪≫
    (nativeGK5XDirectPhi3 e g h k t).symm

/-- Actual relative direct-Phi source automorphism for P0 -> P4. -/
noncomputable def nativeGK5XDefect04
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) :=
  (nativeGK5XDirectPhi0 e g h k t ≪≫
    nativeGK5XEdge04 e g h k (nativeGK5DTreeComposite t)) ≪≫
    (nativeGK5XDirectPhi4 e g h k t).symm

/-- Actual relative direct-Phi source automorphism for P4 -> P3. -/
noncomputable def nativeGK5XDefect43
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) ≅
      nativeGK5DTreeComposite (nativeGK5XFourTree e g h k t) :=
  (nativeGK5XDirectPhi4 e g h k t ≪≫
    nativeGK5XEdge43 e g h k (nativeGK5DTreeComposite t)) ≪≫
    (nativeGK5XDirectPhi3 e g h k t).symm

/-- MAIN theorem: the two pentagon paths assemble the SAME
relative whole Mathlib NatIso source automorphism for FIVE
independently built nonstrict direct recursive Phi witnesses.

This is an unconditional *higher coherence* constraint on the
five actual edge obstructions. It does not claim any one edge
obstruction is already identity. -/
theorem nativeGK5XDirectDefectPentagon_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDefect01 e g h k t ≪≫
      nativeGK5XDefect12 e g h k t) ≪≫
      nativeGK5XDefect23 e g h k t =
    nativeGK5XDefect04 e g h k t ≪≫
      nativeGK5XDefect43 e g h k t := by
  have hp := nativeGK5XPentagon_whole e g h k
    (nativeGK5DTreeComposite t)
  have hglue := congrArg (fun α =>
      (nativeGK5XDirectPhi0 e g h k t ≪≫ α) ≪≫
        (nativeGK5XDirectPhi3 e g h k t).symm) hp
  apply Iso.ext
  simpa [nativeGK5XDefect01, nativeGK5XDefect12,
    nativeGK5XDefect23, nativeGK5XDefect04, nativeGK5XDefect43,
    Iso.trans_hom, Category.assoc] using congrArg Iso.hom hglue

/-- The genuine higher relative automorphism between both
pentagon defect paths is unconditionally the identity NatIso. -/
theorem nativeGK5XDirectDefectPentagon_obstruction_refl
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5XDefect01 e g h k t ≪≫
      nativeGK5XDefect12 e g h k t) ≪≫
      nativeGK5XDefect23 e g h k t).symm ≪≫
    (nativeGK5XDefect04 e g h k t ≪≫
      nativeGK5XDefect43 e g h k t) = Iso.refl _ := by
  rw [nativeGK5XDirectDefectPentagon_whole]
  simp only [Iso.symm_self_id]

/-- Genuine whole NatTrans consequence of the five-direct-Phi
source-valued relative automorphism pentagon. -/
theorem nativeGK5XDirectDefectPentagon_natTrans
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5XDefect01 e g h k t ≪≫
      nativeGK5XDefect12 e g h k t) ≪≫
      nativeGK5XDefect23 e g h k t).hom =
    (nativeGK5XDefect04 e g h k t ≪≫
      nativeGK5XDefect43 e g h k t).hom :=
  congrArg Iso.hom (nativeGK5XDirectDefectPentagon_whole e g h k t)

#print axioms nativeGK5XAtomEq01
#print axioms nativeGK5XAtomEq12
#print axioms nativeGK5XAtomEq23
#print axioms nativeGK5XAtomEq04
#print axioms nativeGK5XAtomEq43
#print axioms nativeGK5XFourTreeEq0
#print axioms nativeGK5XFourTreeEq1
#print axioms nativeGK5XFourTreeEq2
#print axioms nativeGK5XFourTreeEq3
#print axioms nativeGK5XFourTreeEq4
#print axioms nativeGK5XDirectPhi0
#print axioms nativeGK5XDirectPhi1
#print axioms nativeGK5XDirectPhi2
#print axioms nativeGK5XDirectPhi3
#print axioms nativeGK5XDirectPhi4
#print axioms nativeGK5XPentagon_whole
#print axioms nativeGK5XPentagon_natTrans
#print axioms nativeGK5XDirectDefectPentagon_whole
#print axioms nativeGK5XDirectDefectPentagon_obstruction_refl
#print axioms nativeGK5XDirectDefectPentagon_natTrans

end FourEquivalencePentagon
end
end Kuu.F112.Physical
