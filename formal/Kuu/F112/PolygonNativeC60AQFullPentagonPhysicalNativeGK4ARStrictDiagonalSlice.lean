import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARDiagonalMoment
import Mathlib.Tactic

/-!
F112-P94D3GK4AR — every fixed old K_AG q has a STRICTLY NARROWER
arithmetic target than GK4AQ's q-dependent mod4/mod16 slice:
  M_11 ≡ 1+4*(orderedMoment(q)+triangle(backwardCount(q))) (mod 16).
This is the actual F54 ordered-history obstruction at the DIAGONAL.

To establish strictness for EVERY q without assuming a false
surjectivity/representability claim, construct TWO explicit SL2(Z)
matrices inside the old GK4AQ q-slice:
  Base(v)  = U(rho(v)) * L(4*beta(v))
  Twist(v) = Base(v) * [[5,4],[16,13]]
where rho = charge + beta. The second factor has determinant 1 and
is AQ-compatible with zero old AD value. Both matrices match the
old upper-right mod4 and lower-left mod16 constraints; however their
upper-left entries differ by 4 modulo 16. So they CANNOT BOTH
satisfy the new orderedMoment diagonal congruence. At least one
actual integer matrix is in old AQ-slice but not new AR-slice and is
unattainable over the genuine q fiber.
No new Type-valued 3-cells, no invented original Q category laws,
no claim of single infinite fiber, full image, Gray or hyperdescent.
Append-only/tighten-only/same-root107. Protect #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- A canonical arithmetic matrix with all previous GK4AQ residues
for arbitrary old AD data. Never claim an actual source word for it. -/
def nativeGK4ARBaseMatrix (v : NativeGK4ADValue) : NativeGK4AHMatrix :=
  ((1 + 4 * nativeGK4APOldUpperResidue v * (v.1.2 : Int),
      nativeGK4APOldUpperResidue v),
    (4 * (v.1.2 : Int), 1))

/-- An arithmetic SL2 matrix fixing the GK4AQ mod4/mod16 residues
of a zero old AD class; not a purported genuine F54 word. -/
def nativeGK4ARArithmeticTwister : NativeGK4AHMatrix :=
  ((5, 4), (16, 13))

/-- Exact genuine 2x2 multiplication, NOT a commutative shortcut. -/
def nativeGK4ARTwistedMatrix (v : NativeGK4ADValue) : NativeGK4AHMatrix :=
  nativeGK4AHMul (nativeGK4ARBaseMatrix v)
    nativeGK4ARArithmeticTwister

theorem nativeGK4ARBaseMatrix_AQ (v : NativeGK4ADValue) :
    nativeGK4AQLowerLinked v (nativeGK4ARBaseMatrix v) := by
  refine ⟨⟨?_, ⟨0, ?_⟩⟩, ⟨0, ?_⟩⟩
  · refine ⟨?_, ⟨nativeGK4APOldUpperResidue v *
      (v.1.2 : Int), ?_⟩, ⟨(v.1.2 : Int), ?_⟩, ⟨0, ?_⟩⟩
    · simp [nativeGK4AODet, nativeGK4ARBaseMatrix]
      ring
    · simp [nativeGK4ARBaseMatrix]
      ring
    · simp [nativeGK4ARBaseMatrix]
    · simp [nativeGK4ARBaseMatrix]
  · simp [nativeGK4ARBaseMatrix]
  · simp [nativeGK4ARBaseMatrix]

theorem nativeGK4ARArithmeticTwister_AQ :
    nativeGK4AQLowerLinked nativeGK4ADZero
      nativeGK4ARArithmeticTwister := by
  refine ⟨⟨?_, ⟨1, ?_⟩⟩, ⟨1, ?_⟩⟩
  · exact ⟨by decide, ⟨1, by decide⟩,
      ⟨4, by decide⟩, ⟨3, by decide⟩⟩
  · decide
  · decide

theorem nativeGK4ARTwistedMatrix_AQ (v : NativeGK4ADValue) :
    nativeGK4AQLowerLinked v (nativeGK4ARTwistedMatrix v) := by
  have h := nativeGK4AQLowerLinked_mul
    v nativeGK4ADZero
    (nativeGK4ARBaseMatrix v) nativeGK4ARArithmeticTwister
    (nativeGK4ARBaseMatrix_AQ v) nativeGK4ARArithmeticTwister_AQ
  change nativeGK4AQLowerLinked
    (nativeGK4ADCombine v nativeGK4ADZero)
    (nativeGK4ARTwistedMatrix v) at h
  rw [nativeGK4ADCombine_rightUnit] at h
  exact h

/-- Exact gap is 4 modulo 16, independently of charge and beta. -/
theorem nativeGK4ARTwistedMatrix_diagonal_gap (v : NativeGK4ADValue) :
    (nativeGK4ARTwistedMatrix v).1.1 =
      (nativeGK4ARBaseMatrix v).1.1 + 4 +
      16 * (nativeGK4APOldUpperResidue v *
        ((v.1.2 : Int) + 1)) := by
  simp [nativeGK4ARTwistedMatrix, nativeGK4ARBaseMatrix,
    nativeGK4ARArithmeticTwister, nativeGK4AHMul]
  ring

/-- Both old-AQ-admissible matrices CANNOT obey the newly required
same fixed old orderedMoment upper-left residue modulo 16. -/
theorem nativeGK4ARBaseTwist_not_both (v : NativeGK4ADValue) :
    ¬ (nativeGK4ARDiagonalLinked v (nativeGK4ARBaseMatrix v) ∧
       nativeGK4ARDiagonalLinked v (nativeGK4ARTwistedMatrix v)) := by
  rintro ⟨hbase, htwist⟩
  rcases hbase.2 with ⟨tb, hb⟩
  rcases htwist.2 with ⟨tt, ht⟩
  have hg := nativeGK4ARTwistedMatrix_diagonal_gap v
  rw [hb, ht] at hg
  omega

section RealFixedOldFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Actual fixed-old-q AR arithmetic slice; includes ALL previous
AQ/AP/AO constraints AND the new orderedMoment diagonal congruence. -/
def nativeGK4ARFiberArithmeticSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  {M | nativeGK4ARDiagonalLinked
      ((nativeGK4AGKernelValue first last target).1.2) M}

theorem nativeGK4ARSlice_subset_AQ
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ARFiberArithmeticSlice first last target ⊆
      nativeGK4AQFiberArithmeticSlice first last target := by
  intro M h
  exact h.1

/-- Actual attained second matrices over ANY typed old q inherit
the orderedMoment diagonal constraint without phantom Q cells. -/
theorem nativeGK4ARAttained_subset_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      nativeGK4ARFiberArithmeticSlice first last target := by
  intro M h
  rcases h with ⟨z, rfl⟩
  exact nativeGK4ARFiber_sound first last target z

/-- Two actual K_AI points in one fixed q-fiber have the SAME
upper-left diagonal residue modulo sixteen. -/
theorem nativeGK4ARSameFiber_diagonal_residue
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (x y : nativeGK4AJOldFiber first last target) :
    ∃ t : Int,
      (nativeGK4AJFiberMatrix first last target x).1.1 =
        (nativeGK4AJFiberMatrix first last target y).1.1 + 16 * t := by
  rcases (nativeGK4ARFiber_sound first last target x).2 with ⟨tx, hx⟩
  rcases (nativeGK4ARFiber_sound first last target y).2 with ⟨ty, hy⟩
  refine ⟨tx - ty, ?_⟩
  rw [hx, hy]
  ring

/-- The q-dependent AR slice is STRICTLY SMALLER than the PREVIOUS
AQ slice for EVERY genuine old K_AG class q. A definite witness
is chosen by inspecting whether Base obeys the new diagonal law. -/
theorem nativeGK4ARStrictInsideAQ
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ARFiberArithmeticSlice first last target ⊆
      nativeGK4AQFiberArithmeticSlice first last target ∧
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4AQFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4ARFiberArithmeticSlice first last target := by
  refine ⟨nativeGK4ARSlice_subset_AQ first last target, ?_⟩
  let v := (nativeGK4AGKernelValue first last target).1.2
  by_cases hbase : nativeGK4ARDiagonalLinked v (nativeGK4ARBaseMatrix v)
  · refine ⟨nativeGK4ARTwistedMatrix v,
      nativeGK4ARTwistedMatrix_AQ v, ?_⟩
    intro htwist
    exact nativeGK4ARBaseTwist_not_both v ⟨hbase, htwist⟩
  · exact ⟨nativeGK4ARBaseMatrix v, nativeGK4ARBaseMatrix_AQ v, hbase⟩

/-- Stronger explicit EXISTENCE of an old AQ-slice matrix which is
UNATTAINABLE in this same fixed genuine old q-fiber. -/
theorem nativeGK4ARUnattainableInsideAQ
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4AQFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4ALAttainedMatrixSet first last target := by
  rcases (nativeGK4ARStrictInsideAQ first last target).2 with
    ⟨M, hAQ, hnotAR⟩
  exact ⟨M, hAQ, fun h => hnotAR
    (nativeGK4ARAttained_subset_slice first last target h)⟩

/-- Genuine dependent fiber injection into the finer arithmetic
target; no assumption that every arithmetic candidate is attainable. -/
def nativeGK4ARRestrictedFiberEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪
      {M : NativeGK4AHMatrix //
        M ∈ nativeGK4ARFiberArithmeticSlice first last target} where
  toFun z := ⟨nativeGK4AJFiberMatrix first last target z,
    nativeGK4ARFiber_sound first last target z⟩
  inj' := by
    intro x y h
    apply nativeGK4AJFiberMatrix_injective first last target
    exact congrArg Subtype.val h

/-- Exact attained-image normal form WITHIN new AR arithmetic slice.
Not an equivalence with all arithmetic matrices in that slice. -/
def nativeGK4ARRestrictedAttainedEquiv
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {M : {N : NativeGK4AHMatrix //
        N ∈ nativeGK4ARFiberArithmeticSlice first last target} //
        M ∈ Set.range (nativeGK4ARRestrictedFiberEmbedding first last target)} :=
  Equiv.ofBijective
    (fun z => ⟨nativeGK4ARRestrictedFiberEmbedding first last target z,
      ⟨z, rfl⟩⟩)
    ⟨(by
       intro x y h
       apply (nativeGK4ARRestrictedFiberEmbedding first last target).injective
       exact congrArg Subtype.val h),
     (by
       rintro ⟨M, ⟨z, hz⟩⟩
       refine ⟨z, ?_⟩
       exact Subtype.ext hz)⟩

end RealFixedOldFibers

#print axioms nativeGK4ARBaseMatrix
#print axioms nativeGK4ARArithmeticTwister
#print axioms nativeGK4ARTwistedMatrix
#print axioms nativeGK4ARBaseMatrix_AQ
#print axioms nativeGK4ARArithmeticTwister_AQ
#print axioms nativeGK4ARTwistedMatrix_AQ
#print axioms nativeGK4ARTwistedMatrix_diagonal_gap
#print axioms nativeGK4ARBaseTwist_not_both
#print axioms nativeGK4ARFiberArithmeticSlice
#print axioms nativeGK4ARSlice_subset_AQ
#print axioms nativeGK4ARAttained_subset_slice
#print axioms nativeGK4ARSameFiber_diagonal_residue
#print axioms nativeGK4ARStrictInsideAQ
#print axioms nativeGK4ARUnattainableInsideAQ
#print axioms nativeGK4ARRestrictedFiberEmbedding
#print axioms nativeGK4ARRestrictedAttainedEquiv

end
end Kuu.F112.Physical
