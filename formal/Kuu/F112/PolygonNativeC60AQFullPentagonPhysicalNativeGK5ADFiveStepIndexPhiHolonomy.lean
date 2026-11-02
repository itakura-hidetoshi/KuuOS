import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ACIdentityReindexPhiAction
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AD — five genuine dependent-index reclassifications
and their actual whole Mathlib NatIso Phi coherence.

The source is the full typed GK5D finite tree, never a strictified
equivalence record. The five sequential GK5F reindexings and
their composite reindexing are connected by a genuine tree equality.
For every GK5X independent recursive bracket witness P0..P4,
the five-step presentation and single-composite presentation
agree as WHOLE NatIsos with both source and target eqToIso
boundaries retained. The independent order-five closure hypothesis
has actual category-family equality as its descent certificate;
there is no illegal definitional equality of different index types.
Qi FivePhase/C60 is a downstream witness of the order-five condition.

Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, public root107, strict 空 centered,
independent Kuu a presentation, protected #1558 unchanged.
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

/-- The actual fivefold composite endomap. -/
def nativeGK5ADFiveIndex (f : I → I) : I → I :=
  fun i => f (f (f (f (f i))))

variable (f : I → I) (C : I → Cat.{vC,uC})

/-- FIVE distinct GK5F reindex operations, each retaining
genuinely dependent typed intermediate categories. -/
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

/-- Exact source and target typed-tree identity between
five successive dependent reindexings and their one-shot
composite index map. No assumption on f is required. -/
theorem nativeGK5ADFiveTreeReindex_eq
    {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    nativeGK5ADFiveTreeReindex f C t =
      nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t := by
  simp only [nativeGK5ADFiveTreeReindex,
    nativeGK5FTreeReindex_comp]
  rfl

/-- The actual whole equality-induced NatIso of the five-step
typed-tree fusion is canceled by its genuine inverse. -/
theorem nativeGK5ADFiveTreeFusion_whole
    {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    eqToIso (congrArg nativeGK5DTreeComposite
      (nativeGK5ADFiveTreeReindex_eq f C t)) ≪≫
      (eqToIso (congrArg nativeGK5DTreeComposite
        (nativeGK5ADFiveTreeReindex_eq f C t))).symm =
    Iso.refl (nativeGK5DTreeComposite
      (nativeGK5ADFiveTreeReindex f C t)) := by
  simp only [Iso.self_symm_id]

/-- Order five returns EVERY index point exactly, as a theorem,
not a judgmental equality of typed-tree expressions. -/
theorem nativeGK5ADFiveIndex_closed
    (hf : nativeGK5ADFiveIndex f = id) (i : I) :
    nativeGK5ADFiveIndex f i = i := congrFun hf i

/-- The order-five action has exactly the original category
family after the final step. No category-equivalence record
or physical edge is reinterpreted as an equality. -/
theorem nativeGK5ADFiveFamily_closed
    (hf : nativeGK5ADFiveIndex f = id) :
    (fun i : I => C (nativeGK5ADFiveIndex f i)) = C := by
  funext i
  exact congrArg C (nativeGK5ADFiveIndex_closed f hf i)

end FiveStepIndex

section FiveStepWholePhi
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ i : I, C i ≌ D i)
variable (e₂ : ∀ i : I, D i ≌ E i)
variable (e₃ : ∀ i : I, E i ≌ F i)
variable (e₄ : ∀ i : I, F i ≌ G i)

/-- Whole NatIso naturality under an equality of real
fully typed trees: both actual source and target EqToIso
boundaries appear, not objectwise isomorphism components. -/
private theorem nativeGK5ADPhi_tree_transport
    (a : ∀ x : I, C x ≌ G x)
    (φ : ∀ {i j : I} (s : NativeGK5DTypedTree C i j),
      nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ s) ≅
      nativeGK5GChangeAtom a (nativeGK5DTreeComposite s))
    {i j : I} {s t : NativeGK5DTypedTree C i j}
    (p : s = t) :
    (eqToIso (congrArg
      (fun q => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ q)) p.symm) ≪≫
      φ s) ≪≫
      eqToIso (congrArg
        (fun q => nativeGK5GChangeAtom a
          (nativeGK5DTreeComposite q)) p) = φ t := by
  cases p
  simp only [congrArg, eqToIso_refl, Iso.refl_trans,
    Iso.trans_refl]


/-- P0 fivefold WHOLE recursive Phi naturality: five ACTUAL
dependent GK5F reindexings yield exactly the same whole NatIso
as reindexing by their composite, after both genuine EqToIso
boundary transports. Nontrivial equivalence structure retained. -/
theorem nativeGK5ADFiveDirectPhi0_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    (nativeGK5XDirectPhi0
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t)) := by
  have hnat := nativeGK5AAFourDirectPhi0_reindex_whole
    (nativeGK5ADFiveIndex f) e₁ e₂ e₃ e₄ t
  have htree := nativeGK5ADPhi_tree_transport e₁ e₂ e₃ e₄
    (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
    (fun {_ _} s => nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ s)
    (nativeGK5ADFiveTreeReindex_eq f C t)
  calc
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t) := by
          simpa only [nativeGK5ZTransportedPhi0] using hnat
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        ((eqToIso (congrArg
          (fun s => nativeGK5DTreeComposite
            (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
          (nativeGK5ADFiveTreeReindex_eq f C t).symm) ≪≫
          nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
            (nativeGK5ADFiveTreeReindex f C t)) ≪≫
          eqToIso (congrArg
            (fun s => nativeGK5GChangeAtom
              (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
              (nativeGK5DTreeComposite s))
            (nativeGK5ADFiveTreeReindex_eq f C t))) := by
          rw [htree]
    _ = _ := by simp only [Iso.trans_assoc]


/-- P1 fivefold WHOLE recursive Phi naturality: five ACTUAL
dependent GK5F reindexings yield exactly the same whole NatIso
as reindexing by their composite, after both genuine EqToIso
boundary transports. Nontrivial equivalence structure retained. -/
theorem nativeGK5ADFiveDirectPhi1_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    (nativeGK5XDirectPhi1
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t)) := by
  have hnat := nativeGK5AAFourDirectPhi1_reindex_whole
    (nativeGK5ADFiveIndex f) e₁ e₂ e₃ e₄ t
  have htree := nativeGK5ADPhi_tree_transport e₁ e₂ e₃ e₄
    (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
    (fun {_ _} s => nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ s)
    (nativeGK5ADFiveTreeReindex_eq f C t)
  calc
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t) := by
          simpa only [nativeGK5ZTransportedPhi1] using hnat
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        ((eqToIso (congrArg
          (fun s => nativeGK5DTreeComposite
            (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
          (nativeGK5ADFiveTreeReindex_eq f C t).symm) ≪≫
          nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
            (nativeGK5ADFiveTreeReindex f C t)) ≪≫
          eqToIso (congrArg
            (fun s => nativeGK5GChangeAtom
              (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
              (nativeGK5DTreeComposite s))
            (nativeGK5ADFiveTreeReindex_eq f C t))) := by
          rw [htree]
    _ = _ := by simp only [Iso.trans_assoc]


/-- P2 fivefold WHOLE recursive Phi naturality: five ACTUAL
dependent GK5F reindexings yield exactly the same whole NatIso
as reindexing by their composite, after both genuine EqToIso
boundary transports. Nontrivial equivalence structure retained. -/
theorem nativeGK5ADFiveDirectPhi2_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    (nativeGK5XDirectPhi2
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t)) := by
  have hnat := nativeGK5AAFourDirectPhi2_reindex_whole
    (nativeGK5ADFiveIndex f) e₁ e₂ e₃ e₄ t
  have htree := nativeGK5ADPhi_tree_transport e₁ e₂ e₃ e₄
    (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
    (fun {_ _} s => nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ s)
    (nativeGK5ADFiveTreeReindex_eq f C t)
  calc
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t) := by
          simpa only [nativeGK5ZTransportedPhi2] using hnat
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        ((eqToIso (congrArg
          (fun s => nativeGK5DTreeComposite
            (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
          (nativeGK5ADFiveTreeReindex_eq f C t).symm) ≪≫
          nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
            (nativeGK5ADFiveTreeReindex f C t)) ≪≫
          eqToIso (congrArg
            (fun s => nativeGK5GChangeAtom
              (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
              (nativeGK5DTreeComposite s))
            (nativeGK5ADFiveTreeReindex_eq f C t))) := by
          rw [htree]
    _ = _ := by simp only [Iso.trans_assoc]


/-- P3 fivefold WHOLE recursive Phi naturality: five ACTUAL
dependent GK5F reindexings yield exactly the same whole NatIso
as reindexing by their composite, after both genuine EqToIso
boundary transports. Nontrivial equivalence structure retained. -/
theorem nativeGK5ADFiveDirectPhi3_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    (nativeGK5XDirectPhi3
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t)) := by
  have hnat := nativeGK5AAFourDirectPhi3_reindex_whole
    (nativeGK5ADFiveIndex f) e₁ e₂ e₃ e₄ t
  have htree := nativeGK5ADPhi_tree_transport e₁ e₂ e₃ e₄
    (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
    (fun {_ _} s => nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ s)
    (nativeGK5ADFiveTreeReindex_eq f C t)
  calc
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t) := by
          simpa only [nativeGK5ZTransportedPhi3] using hnat
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        ((eqToIso (congrArg
          (fun s => nativeGK5DTreeComposite
            (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
          (nativeGK5ADFiveTreeReindex_eq f C t).symm) ≪≫
          nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
            (nativeGK5ADFiveTreeReindex f C t)) ≪≫
          eqToIso (congrArg
            (fun s => nativeGK5GChangeAtom
              (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
              (nativeGK5DTreeComposite s))
            (nativeGK5ADFiveTreeReindex_eq f C t))) := by
          rw [htree]
    _ = _ := by simp only [Iso.trans_assoc]


/-- P4 fivefold WHOLE recursive Phi naturality: five ACTUAL
dependent GK5F reindexings yield exactly the same whole NatIso
as reindexing by their composite, after both genuine EqToIso
boundary transports. Nontrivial equivalence structure retained. -/
theorem nativeGK5ADFiveDirectPhi4_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    (nativeGK5XDirectPhi4
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t)) := by
  have hnat := nativeGK5AAFourDirectPhi4_reindex_whole
    (nativeGK5ADFiveIndex f) e₁ e₂ e₃ e₄ t
  have htree := nativeGK5ADPhi_tree_transport e₁ e₂ e₃ e₄
    (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
    (fun {_ _} s => nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ s)
    (nativeGK5ADFiveTreeReindex_eq f C t)
  calc
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
          (nativeGK5FTreeReindex (nativeGK5ADFiveIndex f) C t) := by
          simpa only [nativeGK5ZTransportedPhi4] using hnat
    _ = nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
        ((eqToIso (congrArg
          (fun s => nativeGK5DTreeComposite
            (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
          (nativeGK5ADFiveTreeReindex_eq f C t).symm) ≪≫
          nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
            (nativeGK5ADFiveTreeReindex f C t)) ≪≫
          eqToIso (congrArg
            (fun s => nativeGK5GChangeAtom
              (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
              (nativeGK5DTreeComposite s))
            (nativeGK5ADFiveTreeReindex_eq f C t))) := by
          rw [htree]
    _ = _ := by simp only [Iso.trans_assoc]

/-- A bundle of all five independently recursive, genuinely
non-strict whole Phi squares for FIVE successive typed index
reclassifications, with both real EqToIso boundaries. -/
theorem nativeGK5ADAllFiveDirectPhi_reindex_whole
    (f : I → I) {i j : I}
    (t : NativeGK5DTypedTree
      (fun x : I => C (nativeGK5ADFiveIndex f x)) i j) :
    ((nativeGK5XDirectPhi0
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket0 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket0 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t))) ∧
    ((nativeGK5XDirectPhi1
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket1 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket1 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t))) ∧
    ((nativeGK5XDirectPhi2
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket2 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket2 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t))) ∧
    ((nativeGK5XDirectPhi3
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket3 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t))) ∧
    ((nativeGK5XDirectPhi4
      (fun x : I => e₁ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₂ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₃ (nativeGK5ADFiveIndex f x))
      (fun x : I => e₄ (nativeGK5ADFiveIndex f x)) t ≪≫
      eqToIso (nativeGK5AASingleTargetEq
        (nativeGK5ADFiveIndex f)
        (nativeGK5XBracket4 e₁ e₂ e₃ e₄) t)) =
    ((nativeGK5ZSourceIso (nativeGK5ADFiveIndex f)
        e₁ e₂ e₃ e₄ t ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5DTreeComposite
          (nativeGK5XFourTree e₁ e₂ e₃ e₄ s))
        (nativeGK5ADFiveTreeReindex_eq f C t).symm)) ≪≫
      nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄
        (nativeGK5ADFiveTreeReindex f C t)) ≪≫
      eqToIso (congrArg
        (fun s => nativeGK5GChangeAtom
          (nativeGK5XBracket4 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite s))
        (nativeGK5ADFiveTreeReindex_eq f C t))) := by
  exact ⟨nativeGK5ADFiveDirectPhi0_reindex_whole e₁ e₂ e₃ e₄ f t,
    nativeGK5ADFiveDirectPhi1_reindex_whole e₁ e₂ e₃ e₄ f t,
    nativeGK5ADFiveDirectPhi2_reindex_whole e₁ e₂ e₃ e₄ f t,
    nativeGK5ADFiveDirectPhi3_reindex_whole e₁ e₂ e₃ e₄ f t,
    nativeGK5ADFiveDirectPhi4_reindex_whole e₁ e₂ e₃ e₄ f t⟩

#print axioms nativeGK5ADAllFiveDirectPhi_reindex_whole
#print axioms nativeGK5ADFiveDirectPhi0_reindex_whole
#print axioms nativeGK5ADFiveDirectPhi1_reindex_whole
#print axioms nativeGK5ADFiveDirectPhi2_reindex_whole
#print axioms nativeGK5ADFiveDirectPhi3_reindex_whole
#print axioms nativeGK5ADFiveDirectPhi4_reindex_whole

end FiveStepWholePhi

#print axioms nativeGK5ADFiveTreeReindex_eq
#print axioms nativeGK5ADFiveTreeFusion_whole
#print axioms nativeGK5ADFiveIndex_closed
#print axioms nativeGK5ADFiveFamily_closed

end
end Kuu.F112.Physical
