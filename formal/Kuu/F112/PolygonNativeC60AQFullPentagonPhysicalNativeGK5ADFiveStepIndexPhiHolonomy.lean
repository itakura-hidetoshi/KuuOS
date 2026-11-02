import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ACIdentityReindexPhiAction
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AD — finite-order-five dependent-index reclassification,
five ACTUAL typed-tree reindexing steps, and whole NatIso Φ holonomy
relative to the actual equality-induced source and target boundaries.

The endomap need not be injective in intermediate reasoning; the order-five
hypothesis is explicit. No original chosen inverse, unit/counit or
middle compositor is strictified. All five independently recursive
GK5X direct Phi are compared on genuine finite GK5D unit/atom/paste trees.
Pure independent Kuu: no KUOS/Qi import or Gray restoration.
Qi FivePhase/C60 gives one concrete order-five map downstream.

Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; canonical main, same-root 107, protected #1558 unchanged.
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

section FiveStepIndex
variable {I : Type uI}

/-- True fivefold composite of a single index map; no quotient
or added degree-of-freedom to the actual indexing type. -/
def nativeGK5ADFiveIndex (f : I → I) : I → I :=
  fun i => f (f (f (f (f i))))

variable (f : I → I) (C : I → Cat.{vC,uC})

/-- Five actual GK5F reindexings, with their complete dependent
source/target families retained at ALL five stages. -/
def nativeGK5ADFiveTreeReindex
    {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    NativeGK5DTypedTree C
      (nativeGK5ADFiveIndex f i) (nativeGK5ADFiveIndex f j) :=
  nativeGK5FTreeReindex f C
    (nativeGK5FTreeReindex f (fun x : I => C (f x))
      (nativeGK5FTreeReindex f (fun x : I => C (f (f x)))
        (nativeGK5FTreeReindex f (fun x : I => C (f (f (f x))))
          (nativeGK5FTreeReindex f
            (fun x : I => C (f (f (f (f x))))) t))))

/-- The true five-step dependent typed tree is the very same typed
tree as one reindexing by the fivefold composite map. -/
theorem nativeGK5ADFiveTreeReindex_eq
    {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    nativeGK5ADFiveTreeReindex f C t =
      nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t := by
  simp only [nativeGK5ADFiveTreeReindex,
    nativeGK5FTreeReindex_comp, nativeGK5ADFiveIndex]

/-- The whole NatIso induced by equality of the two true
fivefold dependent-tree evaluations is the identity after
the actual typed-tree fusion proof, not by strictifying Phi. -/
theorem nativeGK5ADFiveTreeFusion_whole
    {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5ADFiveTreeReindex_eq f C t)) =
    Iso.refl (nativeGK5DTreeComposite
      (nativeGK5ADFiveTreeReindex f C t)) := by
  cases nativeGK5ADFiveTreeReindex_eq f C t
  simp only [congrArg, eqToIso_refl]

end FiveStepIndex

section ClosedFiveStep
variable {I : Type uI} {C : I → Cat.{vC,uC}}

/-- Transport an original typed tree to the ACTUAL order-five
pullback indexed family, using an explicit equality of index maps. -/
noncomputable def nativeGK5ADClosedTree
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j := by
  have hC : (fun x : I => C (nativeGK5ADFiveIndex f x)) = C := by
    funext x
    exact congrArg C (congrFun hf x)
  rw [hC]
  exact t

/-- Five REAL successive GK5F reclassifications return the
original typed tree under any proved order-five index action. -/
theorem nativeGK5ADFiveTree_closed
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5ADFiveTreeReindex f C
      (nativeGK5ADClosedTree f hf t) = t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5FTreeReindex_id]

section FiveIndependentPhi
variable {D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ x : I, C x ≌ D x)
variable (e₂ : ∀ x : I, D x ≌ E x)
variable (e₃ : ∀ x : I, E x ≌ F x)
variable (e₄ : ∀ x : I, F x ≌ G x)


/-- P0 true whole NatIso five-step holonomy: independent recursive
Phi returns to itself through the genuine fivefold index/tree
composition and equality-induced source/target transport. -/
theorem nativeGK5ADFiveDirectPhi0_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5ADFiveTree_closed] using
    (nativeGK5ACFourDirectPhi0_unit_whole e₁ e₂ e₃ e₄ t)


/-- P1 true whole NatIso five-step holonomy: independent recursive
Phi returns to itself through the genuine fivefold index/tree
composition and equality-induced source/target transport. -/
theorem nativeGK5ADFiveDirectPhi1_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5ADFiveTree_closed] using
    (nativeGK5ACFourDirectPhi1_unit_whole e₁ e₂ e₃ e₄ t)


/-- P2 true whole NatIso five-step holonomy: independent recursive
Phi returns to itself through the genuine fivefold index/tree
composition and equality-induced source/target transport. -/
theorem nativeGK5ADFiveDirectPhi2_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5ADFiveTree_closed] using
    (nativeGK5ACFourDirectPhi2_unit_whole e₁ e₂ e₃ e₄ t)


/-- P3 true whole NatIso five-step holonomy: independent recursive
Phi returns to itself through the genuine fivefold index/tree
composition and equality-induced source/target transport. -/
theorem nativeGK5ADFiveDirectPhi3_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5ADFiveTree_closed] using
    (nativeGK5ACFourDirectPhi3_unit_whole e₁ e₂ e₃ e₄ t)


/-- P4 true whole NatIso five-step holonomy: independent recursive
Phi returns to itself through the genuine fivefold index/tree
composition and equality-induced source/target transport. -/
theorem nativeGK5ADFiveDirectPhi4_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t := by
  rw [nativeGK5ADFiveTreeReindex_eq]
  cases hf
  simpa only [nativeGK5ADClosedTree,
    nativeGK5ADFiveTree_closed] using
    (nativeGK5ACFourDirectPhi4_unit_whole e₁ e₂ e₃ e₄ t)

/-- Five separately and genuinely recursive whole Phi witnesses
all have trivial order-five dependent-index holonomy relative to
real EqToIso boundaries (not an equality of source histories). -/
theorem nativeGK5ADAllFiveDirectPhi_closed_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ (nativeGK5ADClosedTree f hf t) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C
          (nativeGK5ADClosedTree f hf t))) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTree_closed f hf t))) =
    nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t) := by
  exact ⟨nativeGK5ADFiveDirectPhi0_closed_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5ADFiveDirectPhi1_closed_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5ADFiveDirectPhi2_closed_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5ADFiveDirectPhi3_closed_whole e₁ e₂ e₃ e₄ f hf t,
    nativeGK5ADFiveDirectPhi4_closed_whole e₁ e₂ e₃ e₄ f hf t⟩

#print axioms nativeGK5ADAllFiveDirectPhi_closed_whole
#print axioms nativeGK5ADFiveDirectPhi0_closed_whole
#print axioms nativeGK5ADFiveDirectPhi1_closed_whole
#print axioms nativeGK5ADFiveDirectPhi2_closed_whole
#print axioms nativeGK5ADFiveDirectPhi3_closed_whole
#print axioms nativeGK5ADFiveDirectPhi4_closed_whole

end FiveIndependentPhi
#print axioms nativeGK5ADFiveTree_closed
end ClosedFiveStep

#print axioms nativeGK5ADFiveTreeReindex_eq
#print axioms nativeGK5ADFiveTreeFusion_whole

end
end Kuu.F112.Physical
