import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelForgetful
import Mathlib.Tactic

/-!
F112-P94D3GK4AB — complete backward-count fiber normal form.

The genuine original Type-valued F54 proof syntax, original P92B
comparison quotient Q, independent structural quotient S, and the
separate second observational quotients K_AA and K_X remain distinct.

For ANY fully dependent original F45 typed Hom and ANY fixed actual
K_X kernel class, the true K_AA -> K_X fiber embeds in Nat by its
actual backward RotationEdge count. It is canonically equivalent to
the SUBSET of Nat that is attained, not necessarily the full Nat.

For a truly witnessed F54 local rotation, GK4Z's genuine balanced
route tower fills EVERY strictly-positive backward-count stratum in
the fiber over its original enriched value (false,-2), and EACH such
stratum contains exactly one new K_AA class. Only the zero-backward
stratum is undecided. If it exists, it contains at most one class.
Thus the entire true fiber is exactly the tower, optionally plus
one extra zero-backward class, with a precise necessary-and-sufficient
obstruction for surjectivity of the actual tower map.

This does NOT prove faithfulness or nonfaithfulness of S -> K_AA.
It does NOT invent a Type-valued P92B 3-cell from numeric equality,
nor prove original Q category laws, unconditional 14D Countable,
19D filler, global strict n or hyperdescent.
Keep strict 空 central, independent Kuu one presentation; no Gray.
Append-only; same root 107; protected #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section AllTrueDependentF45Fibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- The actual third coordinate of a TRUE K_AA second-kernel class. -/
def nativeGK4ABKernelBackward
    (z : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) first middle) : Nat :=
  (nativeGK4AAEnhancedKernelValue first middle z).2

@[simp] theorem nativeGK4ABKernelBackward_class
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4ABKernelBackward first middle
        (nativeGK4SKernelClass
          (nativeGK4AATripleP92Family p D E) first middle q) =
      nativeGK4ZBackwardP92 first middle q := rfl

theorem nativeGK4ABKernelBackward_comparison
    (s : NativeGK4EStructuralRouteClasses first middle) :
    nativeGK4ABKernelBackward first middle
        (nativeGK4AATripleComparison first middle s) =
      nativeGK4ZBackwardStructural first middle s := by
  change ((nativeGK4SKernelImageEquiv
    (nativeGK4AATripleP92Family p D E) first middle
    (nativeGK4AATripleComparison first middle s)).val).2 =
      nativeGK4ZBackwardStructural first middle s
  rw [nativeGK4AATripleComparison_value]
  rfl

theorem nativeGK4ABKernelBackward_compose
    (u : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) first middle)
    (v : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) middle last) :
    nativeGK4ABKernelBackward first last
      (nativeGK4AAEnhancedKernelCompose first middle last u v) =
      nativeGK4ABKernelBackward first middle u +
        nativeGK4ABKernelBackward middle last v := by
  have h := nativeGK4AAEnhancedKernelValue_compose first middle last u v
  simpa only [nativeGK4ABKernelBackward, nativeGK4AACombine] using
    congrArg Prod.snd h

@[simp] theorem nativeGK4ABKernelBackward_unit :
    nativeGK4ABKernelBackward first first
      (nativeGK4AAEnhancedKernelUnit first) = 0 := rfl

/-- The true fiber of K_AA -> K_X over ANY actual enhanced P92B
second-kernel class, with full F45 source and target types retained. -/
abbrev NativeGK4ABFixedEnhancedFiber
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle) :=
  {z : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) first middle //
    nativeGK4AAForgetBackward first middle z = target}

/-- Extract the genuine F54 backward count from an actual
dependent second-kernel forgetful fiber. -/
def nativeGK4ABFiberBackward
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle)
    (z : NativeGK4ABFixedEnhancedFiber first middle target) : Nat :=
  nativeGK4ABKernelBackward first middle z.1

/-- The exact new information INSIDE a fixed old observation class
is precisely the actual original backward count: equality of the
third coordinate reflects equality in the true K_AA second quotient.
No analogous claim is made about the independent S quotient. -/
theorem nativeGK4ABFiberBackward_injective
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle) :
    Function.Injective (nativeGK4ABFiberBackward first middle target) := by
  intro u v hb
  apply Subtype.ext
  apply nativeGK4AAEnhancedKernelValue_injective first middle
  apply Prod.ext
  · have hforget :
        nativeGK4AAForgetBackward first middle u.1 =
          nativeGK4AAForgetBackward first middle v.1 :=
      u.2.trans v.2.symm
    have hval := congrArg (nativeGK4YEnhancedKernelValue first middle) hforget
    simpa only [nativeGK4AAForgetBackward_value] using hval
  · exact hb

/-- Two actual K_AA fiber classes are equal IFF their genuine backward
numbers agree, while their original GK4X enhanced value is fixed. -/
theorem nativeGK4ABFiber_eq_iff_backward
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle)
    (u v : NativeGK4ABFixedEnhancedFiber first middle target) :
    u = v ↔
      nativeGK4ABFiberBackward first middle target u =
        nativeGK4ABFiberBackward first middle target v := by
  constructor
  · intro h
    exact congrArg (nativeGK4ABFiberBackward first middle target) h
  · exact nativeGK4ABFiberBackward_injective first middle target

/-- Every TRUE forgetful fiber embeds in Nat regardless of any
global countability assumptions on D/E or source raw F54 proofs. -/
theorem nativeGK4ABFixedFiber_countable
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle) :
    Countable (NativeGK4ABFixedEnhancedFiber first middle target) :=
  (nativeGK4ABFiberBackward_injective first middle target).countable

/-- Exact normal-form classifier: the genuine typed fiber is
equivalent to its ACTUALLY ATTAINED backward-count subset of Nat.
No unjustified claim that every Nat is represented. -/
def nativeGK4ABFixedFiberEquivRange
    (target : NativeGK4SKernelClasses
      (nativeGK4XEnhancedP92Family p D E) first middle) :
    NativeGK4ABFixedEnhancedFiber first middle target ≃
      Set.range (nativeGK4ABFiberBackward first middle target) where
  toFun z :=
    ⟨nativeGK4ABFiberBackward first middle target z, ⟨z, rfl⟩⟩
  invFun y := Classical.choose y.2
  left_inv := by
    intro z
    apply nativeGK4ABFiberBackward_injective first middle target
    exact Classical.choose_spec
      (show ∃ w : NativeGK4ABFixedEnhancedFiber first middle target,
        nativeGK4ABFiberBackward first middle target w =
          nativeGK4ABFiberBackward first middle target z from ⟨z, rfl⟩)
  right_inv := by
    intro y
    apply Subtype.ext
    exact Classical.choose_spec y.2

end AllTrueDependentF45Fibers

section WitnessedPhysicalRotationFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Each genuine R_k represents precisely its original backward
rotation count, AFTER passing to the true second observational quotient. -/
theorem nativeGK4ABBalancedTower_backward (k : Nat) :
    nativeGK4ABKernelBackward before before
        (nativeGK4AABalancedTowerForgetFiber rot k).1 = k + 1 := by
  change ((nativeGK4SKernelImageEquiv
    (nativeGK4AATripleP92Family p D E) before before
    (nativeGK4AATripleComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot k)))).val).2 = k + 1
  rw [nativeGK4AATripleComparison_value,
    nativeGK4AABalancedTower_observation]

/-- For any genuine local rotation, the backward-count projection
is injective on the ACTUAL K_AA-to-K_X fiber over the R_0 class. -/
theorem nativeGK4ABLocalFiberBackward_injective :
    Function.Injective
      (fun z : NativeGK4AAForgetFiber rot =>
        nativeGK4ABKernelBackward before before z.1) := by
  exact nativeGK4ABFiberBackward_injective before before
    (nativeGK4XEnhancedComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot 0)))

/-- COMPLETE POSITIVE NORMAL FORM: every genuine K_AA class above the
fixed R_0 K_X image with at least one actual backward physical rotation
is exactly ONE of the explicit genuine F54 balanced routes R_k.
Only backwardCount = 0 can still obstruct full exhaustiveness. -/
theorem nativeGK4ABLocalFiber_zero_or_tower
    (z : NativeGK4AAForgetFiber rot) :
    nativeGK4ABKernelBackward before before z.1 = 0 ∨
      ∃ k : Nat, z = nativeGK4AABalancedTowerForgetFiber rot k := by
  by_cases hz : nativeGK4ABKernelBackward before before z.1 = 0
  · exact Or.inl hz
  · right
    let k := nativeGK4ABKernelBackward before before z.1 - 1
    refine ⟨k, ?_⟩
    apply nativeGK4ABLocalFiberBackward_injective rot
    rw [nativeGK4ABBalancedTower_backward]
    dsimp [k]
    omega

/-- A genuine K_AA local fiber class is a balanced tower class
EXACTLY when it carries a positive number of original backward
physical rotations; this uses no countability or choice of raw proof. -/
theorem nativeGK4ABLocalFiber_tower_iff_positive
    (z : NativeGK4AAForgetFiber rot) :
    (∃ k : Nat, z = nativeGK4AABalancedTowerForgetFiber rot k) ↔
      0 < nativeGK4ABKernelBackward before before z.1 := by
  constructor
  · rintro ⟨k, rfl⟩
    rw [nativeGK4ABBalancedTower_backward]
    omega
  · intro h
    rcases nativeGK4ABLocalFiber_zero_or_tower rot z with hz | ht
    · omega
    · exact ht

/-- The genuine balanced F54 tower exhausts the ENTIRE second-kernel
fiber IFF the exceptional backward-zero class does NOT exist.
The right-hand side is an explicit, sharply localized obstruction. -/
theorem nativeGK4ABLocalFiber_tower_surjective_iff
    : Function.Surjective (nativeGK4AABalancedTowerForgetFiber rot) ↔
      ∀ z : NativeGK4AAForgetFiber rot,
        nativeGK4ABKernelBackward before before z.1 ≠ 0 := by
  constructor
  · intro hs z hz
    obtain ⟨k, hk⟩ := hs z
    rw [← hk, nativeGK4ABBalancedTower_backward] at hz
    omega
  · intro hn z
    rcases nativeGK4ABLocalFiber_zero_or_tower rot z with hz | ⟨k, hk⟩
    · exact False.elim (hn z hz)
    · exact ⟨k, hk.symm⟩

/-- Even if a backward-zero class exists, it is UNIQUE in the new
K_AA observation kernel above the fixed enhanced (false,-2) class. -/
theorem nativeGK4ABLocalFiber_zero_unique
    (u v : NativeGK4AAForgetFiber rot)
    (hu : nativeGK4ABKernelBackward before before u.1 = 0)
    (hv : nativeGK4ABKernelBackward before before v.1 = 0) :
    u = v :=
  nativeGK4ABLocalFiberBackward_injective rot (hu.trans hv.symm)

/-- Normal form at a witnessed physical F54 rotation:
the EXACT range of attainable K_AA backward counts over the old
R_0 enhanced class is all POSITIVE naturals, plus zero IFF such a
zero class really exists in the original second quotient.
No claim is made about whether the zero obstruction is inhabited. -/
theorem nativeGK4ABLocalFiber_backward_range :
    Set.range (fun z : NativeGK4AAForgetFiber rot =>
      nativeGK4ABKernelBackward before before z.1) =
      {k : Nat | 0 < k ∨
        (k = 0 ∧ ∃ z : NativeGK4AAForgetFiber rot,
          nativeGK4ABKernelBackward before before z.1 = 0)} := by
  ext k
  constructor
  · rintro ⟨z, rfl⟩
    by_cases hz : nativeGK4ABKernelBackward before before z.1 = 0
    · exact Or.inr ⟨hz, ⟨z, hz⟩⟩
    · exact Or.inl (Nat.pos_of_ne_zero hz)
  · intro hk
    rcases hk with hp | ⟨hk, hex⟩
    · let j := k - 1
      refine ⟨nativeGK4AABalancedTowerForgetFiber rot j, ?_⟩
      rw [nativeGK4ABBalancedTower_backward]
      dsimp [j]
      omega
    · obtain ⟨z, hz⟩ := hex
      exact ⟨z, hz.trans hk.symm⟩

/-- If the one explicit exceptional zero-obstruction is absent,
the real original F54 balanced tower is a BIJECTION onto the full
fixed enhanced-kernel second-quotient fiber. -/
theorem nativeGK4ABLocalFiber_tower_bijective_if_no_zero
    (hzero : ∀ z : NativeGK4AAForgetFiber rot,
      nativeGK4ABKernelBackward before before z.1 ≠ 0) :
    Function.Bijective (nativeGK4AABalancedTowerForgetFiber rot) := by
  exact ⟨nativeGK4AABalancedTowerForgetFiber_injective rot,
    (nativeGK4ABLocalFiber_tower_surjective_iff rot).mpr hzero⟩

end WitnessedPhysicalRotationFiber

section ActualC60North

/-- Unconditional certified physical C60 north specialization:
all positive backward-count classes of the true K_AA->K_X fiber
are uniquely represented by actual F54 balanced source routes.
A possible zero class remains the only classification obstruction. -/
theorem nativeGK4AB_physical_north_positive_normal_form
    (z : NativeGK4AAForgetFiber northHexagonNativeLeftRotation)
    (hz : 0 < nativeGK4ABKernelBackward
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple z.1) :
    ∃ k : Nat,
      z = nativeGK4AABalancedTowerForgetFiber
        northHexagonNativeLeftRotation k := by
  exact (nativeGK4ABLocalFiber_tower_iff_positive
    northHexagonNativeLeftRotation z).mpr hz

end ActualC60North

#print axioms nativeGK4ABKernelBackward
#print axioms nativeGK4ABKernelBackward_class
#print axioms nativeGK4ABKernelBackward_comparison
#print axioms nativeGK4ABKernelBackward_compose
#print axioms nativeGK4ABKernelBackward_unit
#print axioms NativeGK4ABFixedEnhancedFiber
#print axioms nativeGK4ABFiberBackward
#print axioms nativeGK4ABFiberBackward_injective
#print axioms nativeGK4ABFiber_eq_iff_backward
#print axioms nativeGK4ABFixedFiber_countable
#print axioms nativeGK4ABFixedFiberEquivRange
#print axioms nativeGK4ABBalancedTower_backward
#print axioms nativeGK4ABLocalFiberBackward_injective
#print axioms nativeGK4ABLocalFiber_zero_or_tower
#print axioms nativeGK4ABLocalFiber_tower_iff_positive
#print axioms nativeGK4ABLocalFiber_tower_surjective_iff
#print axioms nativeGK4ABLocalFiber_zero_unique
#print axioms nativeGK4ABLocalFiber_backward_range
#print axioms nativeGK4ABLocalFiber_tower_bijective_if_no_zero
#print axioms nativeGK4AB_physical_north_positive_normal_form

end
end Kuu.F112.Physical
