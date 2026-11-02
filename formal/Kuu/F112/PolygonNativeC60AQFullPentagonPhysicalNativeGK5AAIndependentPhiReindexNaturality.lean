import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ZTypedIndexPentagonExchange
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5AA — actual WHOLE Mathlib NatIso naturality of the
independently recursively constructed GK5G Phi under any
dependent-index reclassification f : I → J (noninjective allowed).

The I-indexed and J-indexed recursive Phi values are different
constructions; exact genuine source and target whole EqToIso boundary
transport is required to compare them. No strictification of
pointwise category-equivalence inverse, units/counits/compositor.
Extension to GK5Z's five independent direct Phi is the next step.
Fixed Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, strict 空 centered, independent Kuu
one presentation, protected #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI uJ vC uC

section SingleChangePhiReindex
variable {I : Type uI} {J : Type uJ}
variable (f : I → J) {C D : J → Cat.{vC,uC}}
variable (e : ∀ j : J, C j ≌ D j)

/-- The true whole source-functor equality across a single actual
category-equivalence change and GK5F dependent-index relabeling. -/
theorem nativeGK5AASingleSourceEq
    {i j : I} (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree (fun x : I => e (f x)) t) =
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree e
        (nativeGK5FTreeReindex f C t)) := by
  calc
    _ = nativeGK5DTreeComposite
      (nativeGK5FTreeReindex f D
        (nativeGK5GChangeTree (fun x : I => e (f x)) t)) :=
          (nativeGK5FTreeComposite_reindex f D _).symm
    _ = _ := congrArg nativeGK5DTreeComposite
      (nativeGK5PChangeTree_reindex f e t)

/-- True whole target-functor equality along the same
dependent-index relabeling, with no equality of equivalence records. -/
theorem nativeGK5AASingleTargetEq
    {i j : I} (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5GChangeAtom (fun x : I => e (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) =
      nativeGK5GChangeAtom e
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) := by
  exact congrArg (nativeGK5GChangeAtom e)
    (nativeGK5FTreeComposite_reindex f C t).symm

/-- Genuine recursive GK5G Phi naturality square under arbitrary
noninjective dependent-index reclassification; TRUE whole NatIso. -/
theorem nativeGK5AASinglePhi_reindex_whole
    {i j : I} (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5GChangeTreeIso (fun x : I => e (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f e t) =
    eqToIso (nativeGK5AASingleSourceEq f e t) ≪≫
      nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C t) := by
  induction t with
  | unit i =>
      rfl
  | atom R =>
      rfl
  | paste left right hl hr =>
      apply Iso.ext
      simp_all [nativeGK5AASingleSourceEq, nativeGK5AASingleTargetEq,
        nativeGK5GChangeTreeIso, nativeGK5GChangeCompIso,
        nativeGK5DTreeComposite, nativeGK5GChangeTree,
        nativeGK5FTreeReindex, Category.assoc]

#print axioms nativeGK5AASingleSourceEq
#print axioms nativeGK5AASingleTargetEq
#print axioms nativeGK5AASinglePhi_reindex_whole

end SingleChangePhiReindex
end
end Kuu.F112.Physical
