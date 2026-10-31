import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ATCrossMatrixModThree
import Mathlib.Data.Int.ModEq
import Mathlib.Tactic

/-!
F112-P94D3GK4AT — a genuinely STRICT refinement of the full AS=AR
arithmetic slice, for EVERY genuine fixed old K_AG class q:
  attained(q) subset AT(q) strictly subset AS(q) = AR(q).
AT retains every AS/AO/AP/AQ/AR condition and additionally requires
all four AH entries to agree mod3 with q's retained old AF matrix.

Use an ACTUALLY attained fiber point, whose existence follows from
the already proved genuine K_AI -> K_AG surjectivity. Multiplying
its AH matrix on the right by U(16) retains ALL AS arithmetic but
cannot retain its mod3 value: otherwise the whole first column
would vanish mod3, contradicting determinant one. The shifted matrix
is an arithmetic witness ONLY, NOT a purported F54 source route.

The coprime moduli then give same-fiber equality mod48 in entries
11/21/22 and mod12 in entry12, via pinned Mathlib Int.ModEq CRT.
No fixed infinite fiber, arithmetic surjectivity, synthetic source
cell, original Q category laws, Gray or hyperdescent asserted.
Append-only/tighten-only/same-root107; preserve #1558 unmerged.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- An arithmetic matrix, not a newly postulated source path. -/
def nativeGK4ATArithmeticShift : NativeGK4AHMatrix := ((1, 16), (0, 1))

def nativeGK4ATUpperTwist (M : NativeGK4AHMatrix) : NativeGK4AHMatrix :=
  nativeGK4AHMul M nativeGK4ATArithmeticShift

/-- U(16) obeys the entire previous AS predicate at zero AD data. -/
theorem nativeGK4ATArithmeticShift_AS :
    nativeGK4ASDiagonalLinked nativeGK4ADZero nativeGK4ATArithmeticShift := by
  apply (nativeGK4ASDiagonalLinked_iff_AR _ _).2
  refine ⟨⟨⟨?_, ⟨4, ?_⟩⟩, ⟨0, ?_⟩⟩, ⟨0, ?_⟩⟩
  · exact ⟨by decide, ⟨0, by decide⟩, ⟨0, by decide⟩, ⟨0, by decide⟩⟩
  · decide
  · decide
  · decide

/-- Multiplying an AS-admissible arithmetic matrix by U(16) leaves
all its old AD-linked congruences and determinant one unchanged. -/
theorem nativeGK4ATUpperTwist_preserves_AS
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix)
    (h : nativeGK4ASDiagonalLinked v M) :
    nativeGK4ASDiagonalLinked v (nativeGK4ATUpperTwist M) := by
  have ht := nativeGK4ASDiagonalLinked_mul v nativeGK4ADZero
    M nativeGK4ATArithmeticShift h nativeGK4ATArithmeticShift_AS
  rw [nativeGK4ADCombine_rightUnit] at ht
  exact ht

/-- A determinant-one matrix and its U(16) right translate cannot
have the same four mod3 residues. Det=1 rules out a zero first column
mod3; no assumption about the arithmetic shift being attainable. -/
theorem nativeGK4ATUpperTwist_not_modThree
    (P : NativeGK4AFMatrix) (M : NativeGK4AHMatrix)
    (hdet : nativeGK4AODet M = 1)
    (hM : nativeGK4ATModThree P M) :
    ¬ nativeGK4ATModThree P (nativeGK4ATUpperTwist M) := by
  intro ht
  have hb := hM.2.1.symm.trans ht.2.1
  have hd := hM.2.2.2.symm.trans ht.2.2.2
  change M.1.2 % 3 = (M.1.1 * 16 + M.1.2 * 1) % 3 at hb
  change M.2.2 % 3 = (M.2.1 * 16 + M.2.2 * 1) % 3 at hd
  simp only [mul_one] at hb hd
  have ha : Int.ModEq 3 M.1.1 0 := by
    change M.1.1 % 3 = 0 % 3
    omega
  have hc : Int.ModEq 3 M.2.1 0 := by
    change M.2.1 % 3 = 0 % 3
    omega
  have hz := (ha.mul (Int.ModEq.refl M.2.2)).sub
    ((Int.ModEq.refl M.1.2).mul hc)
  have hbad : Int.ModEq 3 (nativeGK4AODet M) 0 := by
    simpa only [nativeGK4AODet, zero_mul, mul_zero, sub_self] using hz
  rw [hdet] at hbad
  norm_num [Int.ModEq] at hbad

/-- Pinned mathlib's coprime-modulus theorem, specialized to 16 and 3. -/
theorem nativeGK4ATMod48_of_mod16_mod3 (a b : Int)
    (h16 : Int.ModEq 16 a b) (h3 : Int.ModEq 3 a b) :
    Int.ModEq 48 a b := by
  exact (Int.modEq_and_modEq_iff_modEq_mul
    (m := 16) (n := 3) (by decide)).mp ⟨h16, h3⟩

/-- The upper-right entry had only a mod4 old constraint. -/
theorem nativeGK4ATMod12_of_mod4_mod3 (a b : Int)
    (h4 : Int.ModEq 4 a b) (h3 : Int.ModEq 3 a b) :
    Int.ModEq 12 a b := by
  exact (Int.modEq_and_modEq_iff_modEq_mul
    (m := 4) (n := 3) (by decide)).mp ⟨h4, h3⟩

section GenuineFixedOldFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Full AS slice intersected with the retained OLD AF matrix mod3.
This does not replace or weaken any previous arithmetic condition. -/
def nativeGK4ATFiberArithmeticSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  {M | nativeGK4ASDiagonalLinked
      ((nativeGK4AGKernelValue first last target).1.2) M ∧
    nativeGK4ATModThree ((nativeGK4AGKernelValue first last target).2) M}

theorem nativeGK4ATSlice_subset_AS
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ATFiberArithmeticSlice first last target ⊆
      nativeGK4ASFiberArithmeticSlice first last target := by
  intro M h
  exact h.1

/-- All actually attained matrices satisfy the new simultaneous
compatibility between the two independently descended observers. -/
theorem nativeGK4ATAttained_subset_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      nativeGK4ATFiberArithmeticSlice first last target := by
  intro M h
  rcases h with ⟨z, rfl⟩
  exact ⟨nativeGK4ASFiber_sound first last target z,
    nativeGK4ATFiber_sound first last target z⟩

/-- EVERY genuine old q has a strictly smaller new AT slice.
The shifted arithmetic witness need not be an original source path. -/
theorem nativeGK4ATStrictInsideAS
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ATFiberArithmeticSlice first last target ⊆
      nativeGK4ASFiberArithmeticSlice first last target ∧
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4ASFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4ATFiberArithmeticSlice first last target := by
  refine ⟨nativeGK4ATSlice_subset_AS first last target, ?_⟩
  rcases nativeGK4AIForgetMatrix_surjective first last target with ⟨z, hz⟩
  let point : nativeGK4AJOldFiber first last target := ⟨z, hz⟩
  let M := nativeGK4AJFiberMatrix first last target point
  refine ⟨nativeGK4ATUpperTwist M,
    nativeGK4ATUpperTwist_preserves_AS _ M
      (nativeGK4ASFiber_sound first last target point), ?_⟩
  intro htwist
  exact nativeGK4ATUpperTwist_not_modThree _ M
    (nativeGK4AOFiber_sound first last target point).1
    (nativeGK4ATFiber_sound first last target point) htwist.2

/-- Strict set containment, not merely a refinement in notation. -/
theorem nativeGK4ATSlice_ssubset_AS
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ATFiberArithmeticSlice first last target ⊂
      nativeGK4ASFiberArithmeticSlice first last target := by
  refine ⟨(nativeGK4ATStrictInsideAS first last target).1, ?_⟩
  intro hrev
  rcases (nativeGK4ATStrictInsideAS first last target).2 with ⟨M, hAS, hnot⟩
  exact hnot (hrev hAS)

/-- The previous AS=AR region itself contains a newly excluded
matrix above each old q. Unlike GK4AS, this is NONREDUNDANT. -/
theorem nativeGK4ATUnattainableInsideAS
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4ASFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4ALAttainedMatrixSet first last target := by
  rcases (nativeGK4ATStrictInsideAS first last target).2 with ⟨M, hAS, hnot⟩
  exact ⟨M, hAS, fun h => hnot
    (nativeGK4ATAttained_subset_slice first last target h)⟩

/-- The true dependent fiber embeds into the new slice; no converse
surjectivity onto arbitrary arithmetic candidates is asserted. -/
def nativeGK4ATRestrictedFiberEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪
      {M : NativeGK4AHMatrix //
        M ∈ nativeGK4ATFiberArithmeticSlice first last target} where
  toFun z := ⟨nativeGK4AJFiberMatrix first last target z,
    nativeGK4ASFiber_sound first last target z,
    nativeGK4ATFiber_sound first last target z⟩
  inj' := by
    intro x y h
    apply nativeGK4AJFiberMatrix_injective first last target
    exact congrArg Subtype.val h

/-- Fixed old q now determines residues mod48 in entries 11/21/22,
and mod12 in entry12. These are statements about REAL fiber points. -/
theorem nativeGK4ATSameFiber_coprime_residues
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (x y : nativeGK4AJOldFiber first last target) :
    Int.ModEq 48 (nativeGK4AJFiberMatrix first last target x).1.1
      (nativeGK4AJFiberMatrix first last target y).1.1 ∧
    Int.ModEq 12 (nativeGK4AJFiberMatrix first last target x).1.2
      (nativeGK4AJFiberMatrix first last target y).1.2 ∧
    Int.ModEq 48 (nativeGK4AJFiberMatrix first last target x).2.1
      (nativeGK4AJFiberMatrix first last target y).2.1 ∧
    Int.ModEq 48 (nativeGK4AJFiberMatrix first last target x).2.2
      (nativeGK4AJFiberMatrix first last target y).2.2 := by
  have hx := nativeGK4ATFiber_sound first last target x
  have hy := nativeGK4ATFiber_sound first last target y
  refine ⟨?_, ?_, ?_, ?_⟩
  · apply nativeGK4ATMod48_of_mod16_mod3 _ _ ?_ (hx.1.symm.trans hy.1)
    rcases nativeGK4ARSameFiber_diagonal_residue first last target x y with ⟨t, ht⟩
    rw [ht]
    exact Int.modEq_add_fac_self
  · apply nativeGK4ATMod12_of_mod4_mod3 _ _ ?_ (hx.2.1.symm.trans hy.2.1)
    rcases nativeGK4APSameFiber_upper_residue first last target x y with ⟨t, ht⟩
    rw [ht]
    exact Int.modEq_add_fac_self
  · apply nativeGK4ATMod48_of_mod16_mod3 _ _ ?_ (hx.2.2.1.symm.trans hy.2.2.1)
    rcases nativeGK4AQSameFiber_lower_residue first last target x y with ⟨t, ht⟩
    rw [ht]
    exact Int.modEq_add_fac_self
  · apply nativeGK4ATMod48_of_mod16_mod3 _ _ ?_ (hx.2.2.2.symm.trans hy.2.2.2)
    rcases nativeGK4ASSameFiber_lowerDiagonal_residue first last target x y with ⟨t, ht⟩
    rw [ht]
    exact Int.modEq_add_fac_self

end GenuineFixedOldFibers

#print axioms nativeGK4ATArithmeticShift
#print axioms nativeGK4ATUpperTwist
#print axioms nativeGK4ATArithmeticShift_AS
#print axioms nativeGK4ATUpperTwist_preserves_AS
#print axioms nativeGK4ATUpperTwist_not_modThree
#print axioms nativeGK4ATMod48_of_mod16_mod3
#print axioms nativeGK4ATMod12_of_mod4_mod3
#print axioms nativeGK4ATFiberArithmeticSlice
#print axioms nativeGK4ATSlice_subset_AS
#print axioms nativeGK4ATAttained_subset_slice
#print axioms nativeGK4ATStrictInsideAS
#print axioms nativeGK4ATSlice_ssubset_AS
#print axioms nativeGK4ATUnattainableInsideAS
#print axioms nativeGK4ATRestrictedFiberEmbedding
#print axioms nativeGK4ATSameFiber_coprime_residues

end
end Kuu.F112.Physical
