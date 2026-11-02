import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5UBinaryCompositorExchange
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5V — actual THREE-stage category-equivalence composition
coherence for finite heterogeneous typed functor trees. This is a
new, append-only development from GK5U's unconditional two-stage
whole Mathlib NatIso coherence.

For genuine e : C_i ≌ D_i, g : D_i ≌ E_i, h : E_i ≌ F_i,
the left-associated and right-associated Mathlib Equivalence.trans
values are not silently identified as equivalences: their actual
functor/inverse associativity supplies explicitly proved comparison
equalities and WHOLE eqToIso witnesses. The recursive three-stage Phi
still uses every genuine GK5G tree Iso, unit/counit and compositor.

The atomic comparison cocycle is proved with actual whole Mathlib
NatIso composition, including whiskered equality-induced comparisons.
It is lifted to arbitrary finite typed trees with their real recursive
Phi witnesses. The left route additionally admits a genuine GK5U
two-stage collapse. This is NOT a recovery of raw higher cells, global
Gray structure or unrestricted hyperdescent.

Fixed Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, strict 空 center, independent Kuu a
presentation; protected PR #1558 remains Draft/open/unmerged.
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

section ThreeStageCoherence
variable {I : Type uI} {C D E F : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)
variable (h : ∀ i : I, E i ≌ F i)

/-- Left- and right-bracketed true Equivalence.trans conjugations
of each original typed atom agree as functors, by Mathlib
Functor.assoc on BOTH their genuine forward and inverse functors.
This does not assert an equality of the equivalence structures. -/
theorem nativeGK5VChangeAtom_assoc
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom
        (fun k : I => ((e k).trans (g k)).trans (h k)) R =
      nativeGK5GChangeAtom
        (fun k : I => (e k).trans ((g k).trans (h k))) R := by
  simp only [nativeGK5GChangeAtom, Equivalence.trans_functor,
    Equivalence.trans_inverse, Functor.assoc]

/-- The actual WHOLE Mathlib NatIso associativity comparison
at a typed atom, without declaring either equivalence strict. -/
noncomputable def nativeGK5VAssocAtomIso
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom
        (fun k : I => ((e k).trans (g k)).trans (h k)) R ≅
      nativeGK5GChangeAtom
        (fun k : I => (e k).trans ((g k).trans (h k))) R :=
  eqToIso (nativeGK5VChangeAtom_assoc e g h R)

/-- Genuine whole NatIso transport respects the equality-induced
comparison, not only its component at one selected object. -/
private theorem nativeGK5VChangeIso_eqToIso
    {i j : I} {R S : E i ⥤ E j} (p : R = S) :
    nativeGK5GChangeIso h (eqToIso p) =
      eqToIso (congrArg (nativeGK5GChangeAtom h) p) := by
  cases p
  simp only [eqToIso_refl, nativeGK5GChangeIso,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl]

/-- The core three-equivalence cocycle: two ways of combining true
two-stage GK5Q whole NatIso witnesses agree after the canonical
left/right associativity NatIso. This is a genuine 2-dimensional
composition identity, not an equality of Equivalence.trans data. -/
theorem nativeGK5VAtomCocycle_whole
    {i j : I} (R : C i ⥤ C j) :
    (nativeGK5GChangeIso h (nativeGK5QAtomComparison e g R) ≪≫
        nativeGK5QAtomComparison
          (fun k : I => (e k).trans (g k)) h R) ≪≫
      nativeGK5VAssocAtomIso e g h R =
    nativeGK5QAtomComparison g h (nativeGK5GChangeAtom e R) ≪≫
      nativeGK5QAtomComparison e
        (fun k : I => (g k).trans (h k)) R := by
  simp only [nativeGK5QAtomComparison, nativeGK5VAssocAtomIso,
    nativeGK5VChangeIso_eqToIso, eqToIso_trans]

/-- True pointwise trans associativity also preserves the complete
finite dependently typed tree, including unit and paste nodes. -/
theorem nativeGK5VChangeTree_assoc
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeTree
        (fun k : I => ((e k).trans (g k)).trans (h k)) t =
      nativeGK5GChangeTree
        (fun k : I => (e k).trans ((g k).trans (h k))) t := by
  induction t with
  | unit i => rfl
  | atom R =>
      simpa only [nativeGK5GChangeTree] using
        congrArg NativeGK5DTypedTree.atom
          (nativeGK5VChangeAtom_assoc e g h R)
  | paste left right hl hr =>
      simp only [nativeGK5GChangeTree, hl, hr]

/-- Whole NatIso associator on the evaluated changed finite tree. -/
noncomputable def nativeGK5VAssocTreeIso
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
        (nativeGK5GChangeTree
          (fun k : I => ((e k).trans (g k)).trans (h k)) t) ≅
      nativeGK5DTreeComposite
        (nativeGK5GChangeTree
          (fun k : I => (e k).trans ((g k).trans (h k))) t) :=
  eqToIso (congrArg nativeGK5DTreeComposite
    (nativeGK5VChangeTree_assoc e g h t))

/-- All THREE original genuine tree Phi witnesses, in order.
They act on real transported categories; no inverse or middle unit
has been replaced with an equality or strict identity. -/
noncomputable def nativeGK5VThreeStageSequentialPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
        (nativeGK5GChangeTree h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
      nativeGK5GChangeAtom h
        (nativeGK5GChangeAtom g
          (nativeGK5GChangeAtom e (nativeGK5DTreeComposite t))) :=
  (nativeGK5GChangeTreeIso h
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
    nativeGK5GChangeIso h
      (nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t))) ≪≫
    nativeGK5GChangeIso h
      (nativeGK5GChangeIso g (nativeGK5GChangeTreeIso e t))

/-- LEFT parenthesization of the full three-stage recursive Phi,
by the real e,g and (e.trans g),h Mathlib whole NatIso comparators. -/
noncomputable def nativeGK5VLeftPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
        (nativeGK5GChangeTree h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
      nativeGK5GChangeAtom
        (fun k : I => ((e k).trans (g k)).trans (h k))
        (nativeGK5DTreeComposite t) :=
  (nativeGK5VThreeStageSequentialPhi e g h t ≪≫
    nativeGK5GChangeIso h
      (nativeGK5QAtomComparison e g (nativeGK5DTreeComposite t))) ≪≫
    nativeGK5QAtomComparison
      (fun k : I => (e k).trans (g k)) h
      (nativeGK5DTreeComposite t)

/-- RIGHT parenthesization of the SAME actual three-stage recursive
Phi, by the real g,h and e,(g.trans h) whole NatIso comparators. -/
noncomputable def nativeGK5VRightPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
        (nativeGK5GChangeTree h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t))) ≅
      nativeGK5GChangeAtom
        (fun k : I => (e k).trans ((g k).trans (h k)))
        (nativeGK5DTreeComposite t) :=
  (nativeGK5VThreeStageSequentialPhi e g h t ≪≫
    nativeGK5QAtomComparison g h
      (nativeGK5GChangeAtom e (nativeGK5DTreeComposite t))) ≪≫
    nativeGK5QAtomComparison e
      (fun k : I => (g k).trans (h k))
      (nativeGK5DTreeComposite t)

/-- Main genuine THREE-stage whole NatIso associativity coherence
for EVERY finite dependently typed GK5D binary functor tree:
two actual rebracketings of its nonstrict recursively assembled
Phi agree through the canonical true associativity comparison. -/
theorem nativeGK5VAllTrees_assoc_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5VLeftPhi e g h t ≪≫
        nativeGK5VAssocAtomIso e g h (nativeGK5DTreeComposite t) =
      nativeGK5VRightPhi e g h t := by
  simpa only [nativeGK5VLeftPhi, nativeGK5VRightPhi, Iso.trans_assoc] using
    congrArg (fun α => nativeGK5VThreeStageSequentialPhi e g h t ≪≫ α)
      (nativeGK5VAtomCocycle_whole e g h (nativeGK5DTreeComposite t))

/-- The left triple route really collapses its first TWO actual
recursive stages by GK5U's unconditional theorem, not by assuming
strict unit/counit or strict compositors. -/
theorem nativeGK5VLeftPhi_viaGK5U
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5VLeftPhi e g h t =
      (nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5RDirectCompositePhi e g t)) ≪≫
        nativeGK5QAtomComparison
          (fun k : I => (e k).trans (g k)) h
          (nativeGK5DTreeComposite t) := by
  calc
    _ = (nativeGK5GChangeTreeIso h
          (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≪≫
        nativeGK5GChangeIso h
          (nativeGK5RSequentialCompositePhi e g t)) ≪≫
        nativeGK5QAtomComparison
          (fun k : I => (e k).trans (g k)) h
          (nativeGK5DTreeComposite t) := by
            simp only [nativeGK5VLeftPhi, nativeGK5VThreeStageSequentialPhi,
              nativeGK5RSequentialCompositePhi, nativeGK5RSequentialPhi,
              nativeGK5HChangeIso_trans, Iso.trans_assoc]
    _ = _ := by rw [nativeGK5UAllTrees_unconditional e g t]

/-- Concrete genuine typed unit case of the same whole NatIso
three-stage associativity theorem. -/
theorem nativeGK5VUnit_assoc_whole (i : I) :
    nativeGK5VLeftPhi e g h (.unit i) ≪≫
      nativeGK5VAssocAtomIso e g h (nativeGK5DTreeComposite (.unit i)) =
      nativeGK5VRightPhi e g h (.unit i) :=
  nativeGK5VAllTrees_assoc_whole e g h (.unit i)

/-- Concrete genuinely typed binary paste case at arbitrary depth. -/
theorem nativeGK5VPaste_assoc_whole
    {i j k : I} (left : NativeGK5DTypedTree C i j)
    (right : NativeGK5DTypedTree C j k) :
    nativeGK5VLeftPhi e g h (.paste left right) ≪≫
      nativeGK5VAssocAtomIso e g h
        (nativeGK5DTreeComposite (.paste left right)) =
      nativeGK5VRightPhi e g h (.paste left right) :=
  nativeGK5VAllTrees_assoc_whole e g h (.paste left right)

#print axioms nativeGK5VChangeAtom_assoc
#print axioms nativeGK5VAssocAtomIso
#print axioms nativeGK5VAtomCocycle_whole
#print axioms nativeGK5VChangeTree_assoc
#print axioms nativeGK5VAssocTreeIso
#print axioms nativeGK5VThreeStageSequentialPhi
#print axioms nativeGK5VLeftPhi
#print axioms nativeGK5VRightPhi
#print axioms nativeGK5VAllTrees_assoc_whole
#print axioms nativeGK5VLeftPhi_viaGK5U
#print axioms nativeGK5VUnit_assoc_whole
#print axioms nativeGK5VPaste_assoc_whole

end ThreeStageCoherence
end
end Kuu.F112.Physical
