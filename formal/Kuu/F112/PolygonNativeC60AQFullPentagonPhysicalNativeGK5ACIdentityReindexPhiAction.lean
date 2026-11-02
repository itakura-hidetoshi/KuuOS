import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ABTwoStageIndexPhiCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AC — identity unit laws for genuine recursively constructed
whole Mathlib NatIso Φ under dependent index reclassification.

GK5F already proves identity/composition of the actual finite typed trees;
GK5AA proves one-map recursive Φ naturality and GK5AB proves its
two-map composition for all five actual Mathlib four-equivalence brackets.
GK5AC discharges the missing WHOLE NatIso identity law. It keeps BOTH
actual source and target EqToIso boundary transports before cancellation;
nothing strictifies the chosen inverse, unit, counit or compositor.

No injectivity, no synthetic strict equality of equivalence records.
Valid for all GK5D typed trees, including unit/atom/paste.
This independent Kuu module does NOT import the KUOS/Qi presentation;
an architecture-side five-phase bridge may depend on this module,
never vice versa.

Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same public root 107, protected #1558 untouched.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC uX vX

/-- The genuine whole equality-induced NatIso along an equality
followed by an inverse boundary equality is the identity. This
uses ONLY equality elimination, no strictification of nontrivial
category-equivalence units or counits. -/
private theorem nativeGK5ACCancelEqToIso
    {X : Type uX} [Category.{vX,uX} X]
    {a b : X} (p : a = b) (q : b = a) :
    eqToIso p ≪≫ eqToIso q = Iso.refl a := by
  cases p
  cases q
  simp only [eqToIso_refl, Iso.refl_trans]

section SingleEquivalenceUnit
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ x : I, C x ≌ D x)

/-- The independently recursively constructed single-equivalence Φ
is the actual UNIT of the reindexing action. Both source and target
EqToIso are present in the naturality square, and the target id
boundary is canceled only AFTER using GK5AA's whole naturality. -/
theorem nativeGK5ACSinglePhi_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((eqToIso (nativeGK5AASingleSourceEq (id : I → I) e t) ≪≫
      nativeGK5GChangeTreeIso e
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom e (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5GChangeTreeIso e t := by
  have hnat := nativeGK5AASinglePhi_reindex_whole (id : I → I) e t
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I) e t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom e (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5GChangeTreeIso e t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I) e t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom e (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom e (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5GChangeTreeIso e t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I) e t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom e (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5GChangeTreeIso e t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5GChangeTreeIso e t ≪≫ iso) hcancel
    _ = nativeGK5GChangeTreeIso e t := by
            simp only [Iso.trans_refl]

end SingleEquivalenceUnit

section FourEquivalenceUnit
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ x : I, C x ≌ D x)
variable (e₂ : ∀ x : I, D x ≌ E x)
variable (e₃ : ∀ x : I, E x ≌ F x)
variable (e₄ : ∀ x : I, F x ≌ G x)

/-- The real fourfold source reindexing EqToIso is a unit after
the GK5F identity typed-tree equality; no equality of full
Equivalence records is used. -/
theorem nativeGK5ACSourceIso_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5DTreeComposite (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5FTreeReindex_id C t)) =
      Iso.refl (nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ t)) := by
  simpa only [nativeGK5ZSourceIso] using
    nativeGK5ACCancelEqToIso
      (nativeGK5ZFourComposite_reindex (id : I → I) e₁ e₂ e₃ e₄ t)
      (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5DTreeComposite (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5FTreeReindex_id C t))


/-- Pentagon vertex P0: independently recursive genuine whole Φ
satisfies identity reindexing, with both actual equality boundaries. -/
theorem nativeGK5ACFourDirectPhi0_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t := by
  have hnat :
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
        eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t) =
      nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (id : I → I) C t) := by
    simpa only [nativeGK5ZTransportedPhi0] using
      (nativeGK5AAFourDirectPhi0_reindex_whole
        (id : I → I) e₁ e₂ e₃ e₄ t)
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫ iso) hcancel
    _ = nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t := by
            simp only [Iso.trans_refl]


/-- Pentagon vertex P1: independently recursive genuine whole Φ
satisfies identity reindexing, with both actual equality boundaries. -/
theorem nativeGK5ACFourDirectPhi1_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t := by
  have hnat :
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫
        eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t) =
      nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (id : I → I) C t) := by
    simpa only [nativeGK5ZTransportedPhi1] using
      (nativeGK5AAFourDirectPhi1_reindex_whole
        (id : I → I) e₁ e₂ e₃ e₄ t)
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫ iso) hcancel
    _ = nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t := by
            simp only [Iso.trans_refl]


/-- Pentagon vertex P2: independently recursive genuine whole Φ
satisfies identity reindexing, with both actual equality boundaries. -/
theorem nativeGK5ACFourDirectPhi2_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t := by
  have hnat :
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫
        eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t) =
      nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (id : I → I) C t) := by
    simpa only [nativeGK5ZTransportedPhi2] using
      (nativeGK5AAFourDirectPhi2_reindex_whole
        (id : I → I) e₁ e₂ e₃ e₄ t)
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫ iso) hcancel
    _ = nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t := by
            simp only [Iso.trans_refl]


/-- Pentagon vertex P3: independently recursive genuine whole Φ
satisfies identity reindexing, with both actual equality boundaries. -/
theorem nativeGK5ACFourDirectPhi3_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := by
  have hnat :
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t ≪≫
        eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t) =
      nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (id : I → I) C t) := by
    simpa only [nativeGK5ZTransportedPhi3] using
      (nativeGK5AAFourDirectPhi3_reindex_whole
        (id : I → I) e₁ e₂ e₃ e₄ t)
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t ≪≫ iso) hcancel
    _ = nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := by
            simp only [Iso.trans_refl]


/-- Pentagon vertex P4: independently recursive genuine whole Φ
satisfies identity reindexing, with both actual equality boundaries. -/
theorem nativeGK5ACFourDirectPhi4_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t := by
  have hnat :
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫
        eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t) =
      nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (id : I → I) C t) := by
    simpa only [nativeGK5ZTransportedPhi4] using
      (nativeGK5AAFourDirectPhi4_reindex_whole
        (id : I → I) e₁ e₂ e₃ e₄ t)
  have hcancel :
      eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) = Iso.refl _ :=
    nativeGK5ACCancelEqToIso _ _
  calc
    _ = (nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫ eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t)) ≪≫
          eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t)) := by
            exact congrArg
              (fun iso => iso ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) hnat.symm
    _ = nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫
          (eqToIso (nativeGK5AASingleTargetEq (id : I → I)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t) ≪≫ eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) := by
            simp only [Iso.trans_assoc]
    _ = nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫ Iso.refl _ := by
            exact congrArg (fun iso => nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫ iso) hcancel
    _ = nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t := by
            simp only [Iso.trans_refl]

/-- The five unit squares form the actual pentagon-wise unit
law of the same whole NatIso reindexing action whose general
two-map composition was proved in GK5AB. -/
theorem nativeGK5ACAllFiveDirectPhi_unit_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) ∧
    (((nativeGK5ZSourceIso (id : I → I) e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5FTreeReindex (id : I → I) C t)) ≪≫
      eqToIso (congrArg
        (fun s : NativeGK5DTypedTree C i j =>
          nativeGK5GChangeAtom (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
            (nativeGK5DTreeComposite s))
        (nativeGK5FTreeReindex_id C t))) =
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t) := by
  exact ⟨nativeGK5ACFourDirectPhi0_unit_whole e₁ e₂ e₃ e₄ t,
    nativeGK5ACFourDirectPhi1_unit_whole e₁ e₂ e₃ e₄ t,
    nativeGK5ACFourDirectPhi2_unit_whole e₁ e₂ e₃ e₄ t,
    nativeGK5ACFourDirectPhi3_unit_whole e₁ e₂ e₃ e₄ t,
    nativeGK5ACFourDirectPhi4_unit_whole e₁ e₂ e₃ e₄ t⟩

#print axioms nativeGK5ACSourceIso_unit_whole
#print axioms nativeGK5ACFourDirectPhi0_unit_whole
#print axioms nativeGK5ACFourDirectPhi1_unit_whole
#print axioms nativeGK5ACFourDirectPhi2_unit_whole
#print axioms nativeGK5ACFourDirectPhi3_unit_whole
#print axioms nativeGK5ACFourDirectPhi4_unit_whole
#print axioms nativeGK5ACAllFiveDirectPhi_unit_whole

end FourEquivalenceUnit
#print axioms nativeGK5ACSinglePhi_unit_whole

end
end Kuu.F112.Physical
