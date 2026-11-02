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


section WholeNatIsoHorizontalNaturality
variable {A B T : Type*} [Category A] [Category B] [Category T]

/-- Horizontal composition of TRUE whole NatIsos respects four
actual functor equalities. This is a genuine bifunctoriality
statement, not an equality of source equivalence records. -/
private theorem nativeGK5AAHorizontal_natural
    {F F' G G' : A ⥤ B} {H H' K K' : B ⥤ T}
    (pF : F = F') (pG : G = G')
    (pH : H = H') (pK : K = K')
    (α : F ≅ G) (α' : F' ≅ G')
    (β : H ≅ K) (β' : H' ≅ K')
    (hα : α ≪≫ eqToIso pG = eqToIso pF ≪≫ α')
    (hβ : β ≪≫ eqToIso pK = eqToIso pH ≪≫ β') :
    (Functor.isoWhiskerRight α H ≪≫
      Functor.isoWhiskerLeft G β) ≪≫
        eqToIso (congrArg₂ (fun X Y => X ⋙ Y) pG pK) =
      eqToIso (congrArg₂ (fun X Y => X ⋙ Y) pF pH) ≪≫
        (Functor.isoWhiskerRight α' H' ≪≫
          Functor.isoWhiskerLeft G' β') := by
  cases pF
  cases pG
  cases pH
  cases pK
  simp only [eqToIso_refl, Iso.trans_refl, Iso.refl_trans] at hα hβ ⊢
  rw [hα, hβ]

end WholeNatIsoHorizontalNaturality

section GenuineCompositorNaturality
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- Whole NatIso naturality of the TRUE middle-unit compositor
when both of its input functors are transported across equalities. -/
private theorem nativeGK5AACompIso_natural
    {i j k : I} {R R' : C i ⥤ C j} {S S' : C j ⥤ C k}
    (pR : R = R') (pS : S = S') :
    nativeGK5GChangeCompIso e R S ≪≫
      eqToIso (congrArg (nativeGK5GChangeAtom e)
        (congrArg₂ (fun X Y => X ⋙ Y) pR pS)) =
    eqToIso (congrArg₂ (fun X Y => X ⋙ Y)
        (congrArg (nativeGK5GChangeAtom e) pR)
        (congrArg (nativeGK5GChangeAtom e) pS)) ≪≫
      nativeGK5GChangeCompIso e R' S' := by
  cases pR
  cases pS
  simp only [congrArg, eqToIso_refl, Iso.trans_refl, Iso.refl_trans]

end GenuineCompositorNaturality

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
      simp only [nativeGK5AASingleSourceEq, nativeGK5AASingleTargetEq,
        nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
        nativeGK5FTreeReindex, nativeGK5DTreeComposite,
        nativeGK5GChangeUnitIso, eqToIso_refl,
        Iso.refl_trans, Iso.trans_refl]
  | atom R =>
      simp only [nativeGK5AASingleSourceEq, nativeGK5AASingleTargetEq,
        nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
        nativeGK5FTreeReindex, nativeGK5DTreeComposite,
        eqToIso_refl, Iso.refl_trans, Iso.trans_refl]
  | paste left right hl hr =>
      let pR := nativeGK5FTreeComposite_reindex f C left
      let pS := nativeGK5FTreeComposite_reindex f C right
      let pA := nativeGK5AASingleSourceEq f e left
      let pB := nativeGK5AASingleSourceEq f e right
      have hhorizontal :=
        nativeGK5AAHorizontal_natural pA
          (congrArg (nativeGK5GChangeAtom e) pR)
          pB (congrArg (nativeGK5GChangeAtom e) pS)
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) left)
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C left))
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) right)
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C right))
          hl hr
      have hcomp := nativeGK5AACompIso_natural e pR pS
      simp only [nativeGK5GChangeTreeIso,
        nativeGK5GChangeTree, nativeGK5FTreeReindex,
        nativeGK5DTreeComposite, Iso.trans_assoc]
      apply Iso.ext
      simp_all [nativeGK5AASingleSourceEq,
        nativeGK5AASingleTargetEq, Category.assoc]

#print axioms nativeGK5AASingleSourceEq
#print axioms nativeGK5AASingleTargetEq
#print axioms nativeGK5AASinglePhi_reindex_whole

end SingleChangePhiReindex
end
end Kuu.F112.Physical
