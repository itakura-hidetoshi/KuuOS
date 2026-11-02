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

/-- The genuine middle-unit compositor is exactly the same whole
Mathlib NatIso at the same concrete category objects, independently
of whether indices are represented in I or via f in J. -/
private theorem nativeGK5AACompIso_index
    {i j k : I} (R : C (f i) ⥤ C (f j)) (S : C (f j) ⥤ C (f k)) :
    nativeGK5GChangeCompIso (fun x : I => e (f x)) R S =
      nativeGK5GChangeCompIso e R S := by
  rfl

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
        Iso.refl_trans, Iso.trans_refl, Iso.trans_assoc, eqToIso_trans]
  | atom R =>
      simp only [nativeGK5AASingleSourceEq, nativeGK5AASingleTargetEq,
        nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
        nativeGK5FTreeReindex, nativeGK5DTreeComposite,
        eqToIso_refl, Iso.refl_trans, Iso.trans_refl]
  | paste left right hl hr =>
      let pR := (nativeGK5FTreeComposite_reindex f C left).symm
      let pS := (nativeGK5FTreeComposite_reindex f C right).symm
      let pA := nativeGK5AASingleSourceEq f e left
      let pB := nativeGK5AASingleSourceEq f e right
      let H0 := Functor.isoWhiskerRight
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) left)
          (nativeGK5DTreeComposite (C := fun x : I => D (f x))
            (nativeGK5GChangeTree (fun x : I => e (f x)) right)) ≪≫
        Functor.isoWhiskerLeft
          (nativeGK5GChangeAtom (fun x : I => e (f x))
            (nativeGK5DTreeComposite (C := fun x : I => C (f x)) left))
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) right)
      let H1 := Functor.isoWhiskerRight
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C left))
          (nativeGK5DTreeComposite
            (nativeGK5GChangeTree e (nativeGK5FTreeReindex f C right))) ≪≫
        Functor.isoWhiskerLeft
          (nativeGK5GChangeAtom e
            (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C left)))
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C right))
      let K0 := nativeGK5GChangeCompIso e
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) left) (nativeGK5DTreeComposite (C := fun x : I => C (f x)) right)
      let K1 := nativeGK5GChangeCompIso e
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C left))
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C right))
      let PS := congrArg₂ (fun X Y => X ⋙ Y) pA pB
      let PM := congrArg₂ (fun X Y => X ⋙ Y)
        (congrArg (nativeGK5GChangeAtom e) pR)
        (congrArg (nativeGK5GChangeAtom e) pS)
      let PT := congrArg (nativeGK5GChangeAtom e)
        (congrArg₂ (fun X Y => X ⋙ Y) pR pS)
      have hsource :
          nativeGK5AASingleSourceEq f e (.paste left right) = PS :=
        Subsingleton.elim _ _
      have htarget :
          nativeGK5AASingleTargetEq f e (.paste left right) = PT :=
        Subsingleton.elim _ _
      have hhorizontal : H0 ≪≫ eqToIso PM = eqToIso PS ≪≫ H1 :=
        nativeGK5AAHorizontal_natural pA
          (congrArg (nativeGK5GChangeAtom e) pR)
          pB (congrArg (nativeGK5GChangeAtom e) pS)
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) left)
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C left))
          (nativeGK5GChangeTreeIso (fun x : I => e (f x)) right)
          (nativeGK5GChangeTreeIso e (nativeGK5FTreeReindex f C right))
          hl hr
      have hcomp : K0 ≪≫ eqToIso PT = eqToIso PM ≪≫ K1 :=
        nativeGK5AACompIso_natural e pR pS
      have hchain :
          (H0 ≪≫ K0) ≪≫ eqToIso PT =
            eqToIso PS ≪≫ (H1 ≪≫ K1) := by
        calc
          _ = H0 ≪≫ (K0 ≪≫ eqToIso PT) := by
            simp only [Iso.trans_assoc]
          _ = H0 ≪≫ (eqToIso PM ≪≫ K1) :=
            congrArg (fun iso => H0 ≪≫ iso) hcomp
          _ = (H0 ≪≫ eqToIso PM) ≪≫ K1 := by
            simp only [Iso.trans_assoc]
          _ = (eqToIso PS ≪≫ H1) ≪≫ K1 := by
            rw [hhorizontal]
          _ = eqToIso PS ≪≫ (H1 ≪≫ K1) := by
            simp only [Iso.trans_assoc]
      have hK0 : nativeGK5GChangeCompIso
          (fun x : I => e (f x))
          (nativeGK5DTreeComposite (C := fun x : I => C (f x)) left)
          (nativeGK5DTreeComposite (C := fun x : I => C (f x)) right) =
          K0 := nativeGK5AACompIso_index f e _ _
      simpa only [nativeGK5GChangeTreeIso,
        nativeGK5GChangeTree, nativeGK5FTreeReindex,
        nativeGK5DTreeComposite, hsource, htarget, hK0,
        H0, H1, K0, K1, PS, PT, Iso.trans_assoc] using hchain

#print axioms nativeGK5AASingleSourceEq
#print axioms nativeGK5AASingleTargetEq
#print axioms nativeGK5AASinglePhi_reindex_whole

end SingleChangePhiReindex

section IndependentFourfoldPhiReindex
variable {I : Type uI} {J : Type uJ}
variable (f : I → J)
variable {C D E F G : J → Cat.{vC,uC}}
variable (e : ∀ j : J, C j ≌ D j)
variable (g : ∀ j : J, D j ≌ E j)
variable (h : ∀ j : J, E j ≌ F j)
variable (k : ∀ j : J, F j ≌ G j)

/-- True whole NatIso comparison of TWO distinct nonstrict recursive
Phi witnesses under arbitrary dependent reindexing.
The source tree is a genuine fourfold Equivalence change; the
two source equalities pI and pJ are actual typed-tree certificates.
They must be carried through whole EqToIso boundary transports,
and are NOT identified definitionally across different index types. -/
private theorem nativeGK5AAFourfoldPhiBridge
    (a : ∀ j : J, C j ≌ G j)
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j)
    (pI :
      nativeGK5XFourTree (fun x : I => e (f x))
        (fun x : I => g (f x)) (fun x : I => h (f x))
        (fun x : I => k (f x)) t =
      nativeGK5GChangeTree (fun x : I => a (f x)) t)
    (pJ :
      nativeGK5XFourTree e g h k
        (nativeGK5FTreeReindex f C t) =
      nativeGK5GChangeTree a (nativeGK5FTreeReindex f C t)) :
    (eqToIso (congrArg nativeGK5DTreeComposite pI) ≪≫
      nativeGK5GChangeTreeIso (fun x : I => a (f x)) t) ≪≫
        eqToIso (nativeGK5AASingleTargetEq f a t) =
      nativeGK5ZSourceIso f e g h k t ≪≫
        (eqToIso (congrArg nativeGK5DTreeComposite pJ) ≪≫
          nativeGK5GChangeTreeIso a
            (nativeGK5FTreeReindex f C t)) := by
  have hfront :
      eqToIso (congrArg nativeGK5DTreeComposite pI) ≪≫
        eqToIso (nativeGK5AASingleSourceEq f a t) =
      nativeGK5ZSourceIso f e g h k t ≪≫
        eqToIso (congrArg nativeGK5DTreeComposite pJ) := by
    simp only [nativeGK5ZSourceIso, eqToIso_trans]
  calc
    _ = eqToIso (congrArg nativeGK5DTreeComposite pI) ≪≫
        (nativeGK5GChangeTreeIso (fun x : I => a (f x)) t ≪≫
          eqToIso (nativeGK5AASingleTargetEq f a t)) := by
            simp only [Iso.trans_assoc]
    _ = eqToIso (congrArg nativeGK5DTreeComposite pI) ≪≫
        (eqToIso (nativeGK5AASingleSourceEq f a t) ≪≫
          nativeGK5GChangeTreeIso a
            (nativeGK5FTreeReindex f C t)) := by
              rw [nativeGK5AASinglePhi_reindex_whole f a t]
    _ = (eqToIso (congrArg nativeGK5DTreeComposite pI) ≪≫
        eqToIso (nativeGK5AASingleSourceEq f a t)) ≪≫
          nativeGK5GChangeTreeIso a
            (nativeGK5FTreeReindex f C t) := by
              simp only [Iso.trans_assoc]
    _ = (nativeGK5ZSourceIso f e g h k t ≪≫
        eqToIso (congrArg nativeGK5DTreeComposite pJ)) ≪≫
          nativeGK5GChangeTreeIso a
            (nativeGK5FTreeReindex f C t) := by
              rw [hfront]
    _ = _ := by simp only [Iso.trans_assoc]

/-- GK5AA: independently and genuinely RECURSIVE fourfold direct
Phi for P0 over the pullback I-indexed family agrees with the
J-indexed independently direct Phi after the actual two whole EqToIso
reclassification boundaries. No injectivity, no unit strictification. -/
theorem nativeGK5AAFourDirectPhi0_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5XDirectPhi0
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f
        (nativeGK5XBracket0 e g h k) t) =
    nativeGK5ZTransportedPhi0 f e g h k t := by
  simpa only [nativeGK5XDirectPhi0,
    nativeGK5ZTransportedPhi0] using
    nativeGK5AAFourfoldPhiBridge f e g h k
      (nativeGK5XBracket0 e g h k) t
      (nativeGK5XFourTreeEq0
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t)
      (nativeGK5XFourTreeEq0 e g h k
        (nativeGK5FTreeReindex f C t))

/-- GK5AA: independently and genuinely RECURSIVE fourfold direct
Phi for P1 over the pullback I-indexed family agrees with the
J-indexed independently direct Phi after the actual two whole EqToIso
reclassification boundaries. No injectivity, no unit strictification. -/
theorem nativeGK5AAFourDirectPhi1_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5XDirectPhi1
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f
        (nativeGK5XBracket1 e g h k) t) =
    nativeGK5ZTransportedPhi1 f e g h k t := by
  simpa only [nativeGK5XDirectPhi1,
    nativeGK5ZTransportedPhi1] using
    nativeGK5AAFourfoldPhiBridge f e g h k
      (nativeGK5XBracket1 e g h k) t
      (nativeGK5XFourTreeEq1
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t)
      (nativeGK5XFourTreeEq1 e g h k
        (nativeGK5FTreeReindex f C t))

/-- GK5AA: independently and genuinely RECURSIVE fourfold direct
Phi for P2 over the pullback I-indexed family agrees with the
J-indexed independently direct Phi after the actual two whole EqToIso
reclassification boundaries. No injectivity, no unit strictification. -/
theorem nativeGK5AAFourDirectPhi2_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5XDirectPhi2
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f
        (nativeGK5XBracket2 e g h k) t) =
    nativeGK5ZTransportedPhi2 f e g h k t := by
  simpa only [nativeGK5XDirectPhi2,
    nativeGK5ZTransportedPhi2] using
    nativeGK5AAFourfoldPhiBridge f e g h k
      (nativeGK5XBracket2 e g h k) t
      (nativeGK5XFourTreeEq2
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t)
      (nativeGK5XFourTreeEq2 e g h k
        (nativeGK5FTreeReindex f C t))

/-- GK5AA: independently and genuinely RECURSIVE fourfold direct
Phi for P3 over the pullback I-indexed family agrees with the
J-indexed independently direct Phi after the actual two whole EqToIso
reclassification boundaries. No injectivity, no unit strictification. -/
theorem nativeGK5AAFourDirectPhi3_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5XDirectPhi3
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f
        (nativeGK5XBracket3 e g h k) t) =
    nativeGK5ZTransportedPhi3 f e g h k t := by
  simpa only [nativeGK5XDirectPhi3,
    nativeGK5ZTransportedPhi3] using
    nativeGK5AAFourfoldPhiBridge f e g h k
      (nativeGK5XBracket3 e g h k) t
      (nativeGK5XFourTreeEq3
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t)
      (nativeGK5XFourTreeEq3 e g h k
        (nativeGK5FTreeReindex f C t))

/-- GK5AA: independently and genuinely RECURSIVE fourfold direct
Phi for P4 over the pullback I-indexed family agrees with the
J-indexed independently direct Phi after the actual two whole EqToIso
reclassification boundaries. No injectivity, no unit strictification. -/
theorem nativeGK5AAFourDirectPhi4_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5XDirectPhi4
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq f
        (nativeGK5XBracket4 e g h k) t) =
    nativeGK5ZTransportedPhi4 f e g h k t := by
  simpa only [nativeGK5XDirectPhi4,
    nativeGK5ZTransportedPhi4] using
    nativeGK5AAFourfoldPhiBridge f e g h k
      (nativeGK5XBracket4 e g h k) t
      (nativeGK5XFourTreeEq4
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t)
      (nativeGK5XFourTreeEq4 e g h k
        (nativeGK5FTreeReindex f C t))

/-- All FIVE independent direct recursive Φ computations,
constructed separately in I and J, exchange with arbitrary
(noninjective allowed) truly typed dependent index maps. -/
theorem nativeGK5AAAllFiveDirectPhi_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    (nativeGK5XDirectPhi0
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
        eqToIso (nativeGK5AASingleTargetEq f
          (nativeGK5XBracket0 e g h k) t) =
      nativeGK5ZTransportedPhi0 f e g h k t) ∧
    (nativeGK5XDirectPhi1
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
        eqToIso (nativeGK5AASingleTargetEq f
          (nativeGK5XBracket1 e g h k) t) =
      nativeGK5ZTransportedPhi1 f e g h k t) ∧
    (nativeGK5XDirectPhi2
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
        eqToIso (nativeGK5AASingleTargetEq f
          (nativeGK5XBracket2 e g h k) t) =
      nativeGK5ZTransportedPhi2 f e g h k t) ∧
    (nativeGK5XDirectPhi3
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
        eqToIso (nativeGK5AASingleTargetEq f
          (nativeGK5XBracket3 e g h k) t) =
      nativeGK5ZTransportedPhi3 f e g h k t) ∧
    (nativeGK5XDirectPhi4
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t ≪≫
        eqToIso (nativeGK5AASingleTargetEq f
          (nativeGK5XBracket4 e g h k) t) =
      nativeGK5ZTransportedPhi4 f e g h k t) := by
  exact ⟨nativeGK5AAFourDirectPhi0_reindex_whole f e g h k t,
    nativeGK5AAFourDirectPhi1_reindex_whole f e g h k t,
    nativeGK5AAFourDirectPhi2_reindex_whole f e g h k t,
    nativeGK5AAFourDirectPhi3_reindex_whole f e g h k t,
    nativeGK5AAFourDirectPhi4_reindex_whole f e g h k t⟩

#print axioms nativeGK5AAFourDirectPhi0_reindex_whole
#print axioms nativeGK5AAFourDirectPhi1_reindex_whole
#print axioms nativeGK5AAFourDirectPhi2_reindex_whole
#print axioms nativeGK5AAFourDirectPhi3_reindex_whole
#print axioms nativeGK5AAFourDirectPhi4_reindex_whole
#print axioms nativeGK5AAAllFiveDirectPhi_reindex_whole

end IndependentFourfoldPhiReindex

end
end Kuu.F112.Physical
