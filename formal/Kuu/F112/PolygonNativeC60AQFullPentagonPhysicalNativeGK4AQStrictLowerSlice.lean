import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQLowerLeftResidue
import Mathlib.Tactic

/-!
F112-P94D3GK4AQ — for EVERY actual old K_AG class q, a STRICT
new arithmetic restriction INSIDE GK4AP's q-dependent Γ₁(4) slice.
The previous q-slice fixes upper-right M.1.2 modulo 4 using old
charge+backwardCount. The NEW smaller q-slice also fixes
  M.2.1 ≡ 4 * backwardCount(q) (mod 16).
This compatibility comes from ORIGINAL dependent F54 histories,
not from arbitrary matrices or fictitious Type-valued 3-cells.

For every q, explicitly construct a matrix N(q) in the OLD
GK4AP q-slice with determinant 1, diagonal 1 mod4 and correct upper
right residue, but with lower-left = 4*(backwardCount(q)+1).
It lies in Γ₁(4)^(q) yet cannot belong to the new GK4AQ slice,
and therefore cannot be an actually attained second matrix in
the same fixed q-fiber. Real fibers embed into their narrow arithmetic
slice, and are equivalent ONLY to the actually attained values there.
No assertion of fixed infinite fiber, full arithmetic-slice
surjectivity, source Q category laws, global S faithfulness,
Gray or hyperdescent. Append-only/tighten-only/same-root107;
strict 空 central, independent Kuu a presentation, protect #1558.
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

/-- For each old AD value v, this integral matrix has EXACTLY the
old AP upper-right residue yet violates lower-left mod16 by 4. -/
def nativeGK4AQForbiddenLowerMatrix (v : NativeGK4ADValue) :
    NativeGK4AHMatrix :=
  ((1, nativeGK4APOldUpperResidue v),
   (4 * ((v.1.2 : Int) + 1),
    1 + 4 * ((v.1.2 : Int) + 1) * nativeGK4APOldUpperResidue v))

/-- This explicit obstruction is still a legal element of the
previous GK4AO Γ₁(4) group: determinant 1 and all three congruences. -/
theorem nativeGK4AQForbiddenLowerMatrix_gamma (v : NativeGK4ADValue) :
    nativeGK4AOIntegralCongruence
      (nativeGK4AQForbiddenLowerMatrix v) := by
  refine ⟨?_, ⟨0, ?_⟩, ⟨(v.1.2 : Int) + 1, ?_⟩,
    ⟨((v.1.2 : Int) + 1) * nativeGK4APOldUpperResidue v, ?_⟩⟩
  · simp [nativeGK4AODet, nativeGK4AQForbiddenLowerMatrix]
    ring
  · simp [nativeGK4AQForbiddenLowerMatrix]
  · simp [nativeGK4AQForbiddenLowerMatrix]
  · simp [nativeGK4AQForbiddenLowerMatrix] <;> ring

/-- The matrix is also legal in the PREVIOUS stronger GK4AP
q-dependent slice, with exactly the required upper-right residue. -/
theorem nativeGK4AQForbiddenLowerMatrix_AP (v : NativeGK4ADValue) :
    nativeGK4APLinked v (nativeGK4AQForbiddenLowerMatrix v) := by
  refine ⟨nativeGK4AQForbiddenLowerMatrix_gamma v, ⟨0, ?_⟩⟩
  simp [nativeGK4AQForbiddenLowerMatrix]

/-- But it is impossible at the NEW fixed-q lower-left residue.
4*(b+1)=4*b+16*t has no integral solution. -/
theorem nativeGK4AQForbiddenLowerMatrix_not_linked (v : NativeGK4ADValue) :
    ¬ nativeGK4AQLowerLinked v
      (nativeGK4AQForbiddenLowerMatrix v) := by
  rintro ⟨_, t, ht⟩
  change 4 * ((v.1.2 : Int) + 1) =
    4 * (v.1.2 : Int) + 16 * t at ht
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

/-- Exact NEW q-dependent arithmetic slice, tightening GK4AP.
The underlying K_AG q and actual original F45 typed Hom are fixed. -/
def nativeGK4AQFiberArithmeticSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  {M | nativeGK4AQLowerLinked
    ((nativeGK4AGKernelValue first last target).1.2) M}

/-- Every new q-slice is contained in the PREVIOUS GK4AP slice,
retaining all prior determinant and right-upper conditions. -/
theorem nativeGK4AQSlice_subset_AP
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AQFiberArithmeticSlice first last target ⊆
      nativeGK4APFiberArithmeticSlice first last target := by
  intro M h
  exact h.1

/-- The exact GK4AL actual attained second-matrix image inside
the genuine fixed q-fiber satisfies the stronger congruence. -/
theorem nativeGK4AQAttained_subset_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      nativeGK4AQFiberArithmeticSlice first last target := by
  intro M h
  rcases h with ⟨z, rfl⟩
  exact nativeGK4AQFiber_sound first last target z

/-- The left-lower second matrix entries of ALL two actual
K_AI classes over one q coincide modulo SIXTEEN. -/
theorem nativeGK4AQSameFiber_lower_residue
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (x y : nativeGK4AJOldFiber first last target) :
    ∃ t : Int,
      (nativeGK4AJFiberMatrix first last target x).2.1 =
        (nativeGK4AJFiberMatrix first last target y).2.1 + 16 * t := by
  rcases (nativeGK4AQFiber_sound first last target x).2 with ⟨tx, hx⟩
  rcases (nativeGK4AQFiber_sound first last target y).2 with ⟨ty, hy⟩
  refine ⟨tx - ty, ?_⟩
  rw [hx, hy]
  ring

/-- This matrix genuinely lies IN the earlier AP q-slice, not merely
inside all determinant-one matrices or all Γ₁(4). -/
theorem nativeGK4AQForbiddenMatrix_in_AP
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AQForbiddenLowerMatrix
      ((nativeGK4AGKernelValue first last target).1.2) ∈
        nativeGK4APFiberArithmeticSlice first last target := by
  exact nativeGK4AQForbiddenLowerMatrix_AP
    ((nativeGK4AGKernelValue first last target).1.2)

/-- However the same explicit q-dependent matrix is NOT in the
new smaller arithmetic slice, by the genuine backwardCount mod16. -/
theorem nativeGK4AQForbiddenMatrix_not_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AQForbiddenLowerMatrix
      ((nativeGK4AGKernelValue first last target).1.2) ∉
        nativeGK4AQFiberArithmeticSlice first last target := by
  intro h
  exact nativeGK4AQForbiddenLowerMatrix_not_linked
    ((nativeGK4AGKernelValue first last target).1.2) h

/-- MAIN STRICTNESS: for EVERY old q, the new arithmetic slice is
a proper subset of the previously established AP q-slice. -/
theorem nativeGK4AQStrictInsideAP
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AQFiberArithmeticSlice first last target ⊆
      nativeGK4APFiberArithmeticSlice first last target ∧
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4APFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4AQFiberArithmeticSlice first last target := by
  exact ⟨nativeGK4AQSlice_subset_AP first last target,
    nativeGK4AQForbiddenLowerMatrix
      ((nativeGK4AGKernelValue first last target).1.2),
    nativeGK4AQForbiddenMatrix_in_AP first last target,
    nativeGK4AQForbiddenMatrix_not_slice first last target⟩

/-- This stronger AP-admissible matrix is still not ATTAINED above q.
Never mistake a necessary congruence for an actual source route. -/
theorem nativeGK4AQForbiddenMatrix_unattainable
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AQForbiddenLowerMatrix
      ((nativeGK4AGKernelValue first last target).1.2) ∉
        nativeGK4ALAttainedMatrixSet first last target := by
  intro h
  exact nativeGK4AQForbiddenMatrix_not_slice first last target
    (nativeGK4AQAttained_subset_slice first last target h)

/-- The actual dependent fiber embeds into the NEW strictly narrower
arithmetic slice, using the existing exact within-fiber matrix code. -/
def nativeGK4AQRestrictedFiberEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪
      {M : NativeGK4AHMatrix //
        M ∈ nativeGK4AQFiberArithmeticSlice first last target} where
  toFun z := ⟨nativeGK4AJFiberMatrix first last target z,
    nativeGK4AQFiber_sound first last target z⟩
  inj' := by
    intro x y h
    apply nativeGK4AJFiberMatrix_injective first last target
    exact congrArg Subtype.val h

/-- Exact normal form ONLY relative to the genuine attained matrix
values INSIDE the q-specific smaller arithmetic slice. -/
def nativeGK4AQRestrictedAttainedEquiv
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {M : {N : NativeGK4AHMatrix //
        N ∈ nativeGK4AQFiberArithmeticSlice first last target} //
        M ∈ Set.range (nativeGK4AQRestrictedFiberEmbedding first last target)} :=
  Equiv.ofBijective
    (fun z => ⟨nativeGK4AQRestrictedFiberEmbedding first last target z,
      ⟨z, rfl⟩⟩)
    ⟨(by
       intro x y h
       apply (nativeGK4AQRestrictedFiberEmbedding first last target).injective
       exact congrArg Subtype.val h),
     (by
       rintro ⟨M, ⟨z, hz⟩⟩
       refine ⟨z, ?_⟩
       exact Subtype.ext hz)⟩

end RealFixedOldFibers

#print axioms nativeGK4AQForbiddenLowerMatrix
#print axioms nativeGK4AQForbiddenLowerMatrix_gamma
#print axioms nativeGK4AQForbiddenLowerMatrix_AP
#print axioms nativeGK4AQForbiddenLowerMatrix_not_linked
#print axioms nativeGK4AQFiberArithmeticSlice
#print axioms nativeGK4AQSlice_subset_AP
#print axioms nativeGK4AQAttained_subset_slice
#print axioms nativeGK4AQSameFiber_lower_residue
#print axioms nativeGK4AQForbiddenMatrix_in_AP
#print axioms nativeGK4AQForbiddenMatrix_not_slice
#print axioms nativeGK4AQStrictInsideAP
#print axioms nativeGK4AQForbiddenMatrix_unattainable
#print axioms nativeGK4AQRestrictedFiberEmbedding
#print axioms nativeGK4AQRestrictedAttainedEquiv

end
end Kuu.F112.Physical
