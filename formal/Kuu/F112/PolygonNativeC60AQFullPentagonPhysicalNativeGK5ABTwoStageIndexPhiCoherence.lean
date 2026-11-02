import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AAIndependentPhiReindexNaturality
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5AB — genuine whole-NatIso path independence of
two successive index maps I → J → K versus their composite,
for all five true four-equivalence parenthesizations.

This is not a strict equality of equivalence records. At each
stage the actual source equality EqToIso is retained, and the
final target equality is the actual GK5F typed-tree composition
certificate. Both arbitrary index maps may be noninjective.
All finite GK5D unit/atom/paste typed trees are supported.

Fixed Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same public root 107, strict 空 center;
independent Kuu is a presentation. Protected PR #1558 unchanged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI uJ uK vC uC

section TwoStageIndexPhi
variable {I : Type uI} {J : Type uJ} {K : Type uK}
variable (f : I → J) (g : J → K)
variable {C D E F G : K → Cat.{vC,uC}}
variable (e₁ : ∀ x : K, C x ≌ D x)
variable (e₂ : ∀ x : K, D x ≌ E x)
variable (e₃ : ∀ x : K, E x ≌ F x)
variable (e₄ : ∀ x : K, F x ≌ G x)

/-- The true source whole NatIso from TWO independent GK5Z
reindexings equals the source NatIso for the composite index map.
The connecting iso is precisely the GK5F typed-tree fusion equality. -/
theorem nativeGK5ABSourceIso_comp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    (nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZSourceIso (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simp only [nativeGK5ZSourceIso, eqToIso_trans]
  exact congrArg eqToIso (Subsingleton.elim _ _)

/-- Whole NatIso naturality under an actual equality of fully
typed GK5D trees, for any witness, not just a selected Phi. -/
private theorem nativeGK5ABPhi_tree_transport
    (a : ∀ x : K, C x ≌ G x)
    (φ : ∀ {i j : K} (s : NativeGK5DTypedTree C i j),
      nativeGK5DTreeComposite (nativeGK5XFourTree e₁ e₂ e₃ e₄ s) ≅
      nativeGK5GChangeAtom a (nativeGK5DTreeComposite s))
    {i j : K} {s t : NativeGK5DTypedTree C i j}
    (p : s = t) :
    φ s ≪≫ eqToIso
      (congrArg (fun q => nativeGK5GChangeAtom a
        (nativeGK5DTreeComposite q)) p) =
    eqToIso
      (congrArg (fun q => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ q)) p) ≪≫ φ t := by
  cases p
  simp only [congrArg, eqToIso_refl, Iso.trans_refl, Iso.refl_trans]

/-- Abstract composition principle: the witness at the twice-reindexed
tree is connected to the witness at the once-composite-reindexed tree
by its genuine whole source AND target EqToIso boundaries.
No extensional replacement of Mathlib Equivalence records occurs. -/
theorem nativeGK5ABTwoStagePhi_comp_whole
    (a : ∀ x : K, C x ≌ G x)
    (φ : ∀ {i j : K} (s : NativeGK5DTypedTree C i j),
      nativeGK5DTreeComposite (nativeGK5XFourTree e₁ e₂ e₃ e₄ s) ≅
      nativeGK5GChangeAtom a (nativeGK5DTreeComposite s))
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      φ (nativeGK5FTreeReindex g C
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom a (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZSourceIso (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t ≪≫
      φ (nativeGK5FTreeReindex (fun x : I => g (f x)) C t) := by
  have hφ := nativeGK5ABPhi_tree_transport e₁ e₂ e₃ e₄ a φ
    (nativeGK5FTreeReindex_comp f g C t)
  have hs := nativeGK5ABSourceIso_comp_whole f g e₁ e₂ e₃ e₄ t
  calc
    _ = (nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      (φ (nativeGK5FTreeReindex g C
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
       eqToIso (congrArg
         (fun s => nativeGK5GChangeAtom a (nativeGK5DTreeComposite s))
         (nativeGK5FTreeReindex_comp f g C t))) := by
           simp only [Iso.trans_assoc]
    _ = (nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      (eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5FTreeReindex_comp f g C t)) ≪≫
       φ (nativeGK5FTreeReindex (fun x : I => g (f x)) C t)) := by
           rw [hφ]
    _ = ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5FTreeReindex_comp f g C t))) ≪≫
      φ (nativeGK5FTreeReindex (fun x : I => g (f x)) C t) := by
          simp only [Iso.trans_assoc]
    _ = _ := by rw [hs]

/-- Genuine all-tree whole NatIso comparison at pentagon vertex P0:
two index transports have exactly the same outcome as their composite. -/
theorem nativeGK5ABFourDirectPhi0_indexComp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex g C
          (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZTransportedPhi0 (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simpa only [nativeGK5ZTransportedPhi0] using
    nativeGK5ABTwoStagePhi_comp_whole f g e₁ e₂ e₃ e₄
      (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
      (fun {_ _} s => nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ s) t


/-- Genuine all-tree whole NatIso comparison at pentagon vertex P1:
two index transports have exactly the same outcome as their composite. -/
theorem nativeGK5ABFourDirectPhi1_indexComp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex g C
          (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZTransportedPhi1 (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simpa only [nativeGK5ZTransportedPhi1] using
    nativeGK5ABTwoStagePhi_comp_whole f g e₁ e₂ e₃ e₄
      (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
      (fun {_ _} s => nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ s) t


/-- Genuine all-tree whole NatIso comparison at pentagon vertex P2:
two index transports have exactly the same outcome as their composite. -/
theorem nativeGK5ABFourDirectPhi2_indexComp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex g C
          (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZTransportedPhi2 (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simpa only [nativeGK5ZTransportedPhi2] using
    nativeGK5ABTwoStagePhi_comp_whole f g e₁ e₂ e₃ e₄
      (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
      (fun {_ _} s => nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ s) t


/-- Genuine all-tree whole NatIso comparison at pentagon vertex P3:
two index transports have exactly the same outcome as their composite. -/
theorem nativeGK5ABFourDirectPhi3_indexComp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex g C
          (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZTransportedPhi3 (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simpa only [nativeGK5ZTransportedPhi3] using
    nativeGK5ABTwoStagePhi_comp_whole f g e₁ e₂ e₃ e₄
      (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
      (fun {_ _} s => nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ s) t


/-- Genuine all-tree whole NatIso comparison at pentagon vertex P4:
two index transports have exactly the same outcome as their composite. -/
theorem nativeGK5ABFourDirectPhi4_indexComp_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (g (f x))) i j) :
    ((nativeGK5ZSourceIso f
        (fun x : J => e₁ (g x)) (fun x : J => e₂ (g x))
        (fun x : J => e₃ (g x)) (fun x : J => e₄ (g x)) t ≪≫
      nativeGK5ZSourceIso g e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex f (fun x : J => C (g x)) t)) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex g C
          (nativeGK5FTreeReindex f (fun x : J => C (g x)) t))) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_comp f g C t)) =
    nativeGK5ZTransportedPhi4 (fun x : I => g (f x))
      e₁ e₂ e₃ e₄ t := by
  simpa only [nativeGK5ZTransportedPhi4] using
    nativeGK5ABTwoStagePhi_comp_whole f g e₁ e₂ e₃ e₄
      (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
      (fun {_ _} s => nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ s) t

#print axioms nativeGK5ABSourceIso_comp_whole
#print axioms nativeGK5ABTwoStagePhi_comp_whole
#print axioms nativeGK5ABFourDirectPhi0_indexComp_whole
#print axioms nativeGK5ABFourDirectPhi1_indexComp_whole
#print axioms nativeGK5ABFourDirectPhi2_indexComp_whole
#print axioms nativeGK5ABFourDirectPhi3_indexComp_whole
#print axioms nativeGK5ABFourDirectPhi4_indexComp_whole

end TwoStageIndexPhi
end
end Kuu.F112.Physical
