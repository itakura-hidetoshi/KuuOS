import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ADFiveStepIndexPhiHolonomy
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AE — the original typed source/target presentation after
a genuine five-step dependent index cycle.

A proof f^5 = id lives in Prop. It is NOT definitional equality between
dependent endpoint types. First transport the original tree into the
fivefold pullback family by a real Eq.rec/cast; then execute all five
GK5F reindexings; finally transport both genuine typed endpoints
by the exact f^5=index equality. The returned entire typed tree,
not only its leaf word, agrees with the original tree.

For each of the five independent recursive Mathlib whole NatIso Phi
values, a whole source and target eqToIso square compares the returned
tree and the actual original Phi. GK5AD separately certifies the whole
five-step vs one-step Phi index-transport path for the same source tree.
Nothing collapses a raw higher history or strictifies a chosen inverse,
unit/counit or middle compositor.

Canonical main / pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / tighten-only / overwrite-forbidden, same public root107.
Independent Kuu presentation, strict 空 authority, PR #1558 untouched.
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

section FiveCycleTrueEndpointTransport
variable {I : Type uI} (f : I → I)
variable (C : I → Cat.{vC,uC})
variable (hf : nativeGK5ADFiveIndex f = id)

/-- Explicit genuine Eq.rec transport of a full typed tree from the
original category family to the proved equal fivefold pullback family. -/
def nativeGK5AEOriginalAsFivePullback
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j :=
  cast (congrArg
    (fun F : I → Cat.{vC,uC} => NativeGK5DTypedTree F i j)
    (nativeGK5ADFiveFamily_closed f C hf).symm) t

/-- Actual dependent endpoint type equality, not an unproved
definitional identification of C(f^5 i) with C i. -/
theorem nativeGK5AEEndpointTreeTypeEq (i j : I) :
    NativeGK5DTypedTree C
      (nativeGK5ADFiveIndex f i) (nativeGK5ADFiveIndex f j) =
    NativeGK5DTypedTree C i j := by
  rw [nativeGK5ADFiveIndex_closed f hf i,
    nativeGK5ADFiveIndex_closed f hf j]

/-- Execute the real five GK5F steps; then explicitly cast BOTH
indexed endpoints back to the original typed-tree source/target. -/
def nativeGK5AEClosedFiveTree
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    NativeGK5DTypedTree C i j :=
  cast (nativeGK5AEEndpointTreeTypeEq f C hf i j)
    (nativeGK5ADFiveTreeReindex f C
      (nativeGK5AEOriginalAsFivePullback f C hf t))

/-- The complete fivefold dependent-tree reclassification really
returns the entire ORIGINAL typed tree after the family and both
endpoint transports. No quotient and no source-path collapse. -/
theorem nativeGK5AEClosedFiveTree_eq
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5AEClosedFiveTree f C hf t = t := by
  cases hf
  simp [nativeGK5AEClosedFiveTree,
    nativeGK5AEOriginalAsFivePullback,
    nativeGK5AEEndpointTreeTypeEq,
    nativeGK5ADFiveTreeReindex_eq,
    nativeGK5FTreeReindex_id]

#print axioms nativeGK5AEClosedFiveTree_eq

end FiveCycleTrueEndpointTransport

section WholePhiReturnedToOriginal
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ x : I, C x ≌ D x)
variable (e₂ : ∀ x : I, D x ≌ E x)
variable (e₃ : ∀ x : I, E x ≌ F x)
variable (e₄ : ∀ x : I, F x ≌ G x)

/-- Any real tree equality transports a genuine entire Mathlib
whole NatIso Phi along both induced source/target functor equalities.
This is NOT a comparison of objectwise components alone. -/
private theorem nativeGK5AEWholePhiNaturality
    (a : ∀ x : I, C x ≌ G x)
    (φ : ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      nativeGK5DTreeComposite (nativeGK5XFourTree e₁ e₂ e₃ e₄ t) ≅
        nativeGK5GChangeAtom a (nativeGK5DTreeComposite t))
    {i j : I} {s t : NativeGK5DTypedTree C i j}
    (p : s = t) :
    φ s ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom a
          (nativeGK5DTreeComposite u)) p) =
    eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) p) ≪≫ φ t := by
  cases p
  simp only [congrArg, eqToIso_refl,
    Iso.trans_refl, Iso.refl_trans]


/-- P0: after five genuine dependent index reclassifications
and real family/both-endpoint Eq.rec transports, the independently
recursive whole Phi equals the ORIGINAL Phi via actual source and
target equality-induced whole NatIso boundaries. -/
theorem nativeGK5AEFourDirectPhi0_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t) := by
  exact nativeGK5AEWholePhiNaturality e₁ e₂ e₃ e₄
    (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
    (fun {_ _} u => nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ u)
    (nativeGK5AEClosedFiveTree_eq f C hf t)


/-- P1: after five genuine dependent index reclassifications
and real family/both-endpoint Eq.rec transports, the independently
recursive whole Phi equals the ORIGINAL Phi via actual source and
target equality-induced whole NatIso boundaries. -/
theorem nativeGK5AEFourDirectPhi1_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t) := by
  exact nativeGK5AEWholePhiNaturality e₁ e₂ e₃ e₄
    (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
    (fun {_ _} u => nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ u)
    (nativeGK5AEClosedFiveTree_eq f C hf t)


/-- P2: after five genuine dependent index reclassifications
and real family/both-endpoint Eq.rec transports, the independently
recursive whole Phi equals the ORIGINAL Phi via actual source and
target equality-induced whole NatIso boundaries. -/
theorem nativeGK5AEFourDirectPhi2_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t) := by
  exact nativeGK5AEWholePhiNaturality e₁ e₂ e₃ e₄
    (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
    (fun {_ _} u => nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ u)
    (nativeGK5AEClosedFiveTree_eq f C hf t)


/-- P3: after five genuine dependent index reclassifications
and real family/both-endpoint Eq.rec transports, the independently
recursive whole Phi equals the ORIGINAL Phi via actual source and
target equality-induced whole NatIso boundaries. -/
theorem nativeGK5AEFourDirectPhi3_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) := by
  exact nativeGK5AEWholePhiNaturality e₁ e₂ e₃ e₄
    (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
    (fun {_ _} u => nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ u)
    (nativeGK5AEClosedFiveTree_eq f C hf t)


/-- P4: after five genuine dependent index reclassifications
and real family/both-endpoint Eq.rec transports, the independently
recursive whole Phi equals the ORIGINAL Phi via actual source and
target equality-induced whole NatIso boundaries. -/
theorem nativeGK5AEFourDirectPhi4_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t) := by
  exact nativeGK5AEWholePhiNaturality e₁ e₂ e₃ e₄
    (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
    (fun {_ _} u => nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ u)
    (nativeGK5AEClosedFiveTree_eq f C hf t)

/-- Five separately and genuinely recursive whole Phi return squares,
all within the original indexed category family, each with real
source and target EqToIso and the five-stage endpoint cast certificate. -/
theorem nativeGK5AEAllFiveDirectPhi_return_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t) ∧
    (nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t) ∧
    (nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t) ∧
    (nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) ∧
    (nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t) := by
  exact ⟨nativeGK5AEFourDirectPhi0_return_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5AEFourDirectPhi1_return_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5AEFourDirectPhi2_return_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5AEFourDirectPhi3_return_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5AEFourDirectPhi4_return_whole e₁ e₂ e₃ e₄ f hf t⟩

#print axioms nativeGK5AEFourDirectPhi0_return_whole
#print axioms nativeGK5AEFourDirectPhi1_return_whole
#print axioms nativeGK5AEFourDirectPhi2_return_whole
#print axioms nativeGK5AEFourDirectPhi3_return_whole
#print axioms nativeGK5AEFourDirectPhi4_return_whole
#print axioms nativeGK5AEAllFiveDirectPhi_return_whole

end WholePhiReturnedToOriginal

end
end Kuu.F112.Physical
