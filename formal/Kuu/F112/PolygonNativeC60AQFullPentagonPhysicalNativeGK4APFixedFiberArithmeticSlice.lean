import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4APLinkedObserverResidue
import Mathlib.Tactic

/-!
F112-P94D3GK4AP — a STRICTLY STRONGER fiber-relative arithmetic
image restriction INSIDE the already proved Γ₁(4) necessary domain.
For any actual old K_AG class q with old AD charge c_q and backward
count b_q, every genuinely attained second GK4AH matrix satisfies
  M.1.2 ≡ c_q + b_q (mod 4).
Thus ALL two points in a fixed forgetful fiber have congruent
upper-right entries, not only lower-left/diagonal congruences.

A fully explicit q-dependent unipotent matrix
  N(q) = [[1, c_q + b_q + 1],[0,1]]
HAS det=1 and satisfies all GK4AO Gamma_1(4) congruences, yet is
PROVABLY UNATTAINABLE in the actual fiber above q. Every old q
therefore has a proper arithmetic slice of Gamma_1(4).
The exact genuine fiber embeds into that q-dependent slice, with
an Equiv ONLY to its actually attained image. This does not prove
full image classification, fixed infinite fibers, new Type-cells,
original Q category laws, S global faithfulness, Gray or hyperdescent.
Append-only/tighten-only/same-root107; strict 空 central, independent
Kuu one presentation, protected #1558 stays Draft/open/unmerged.
Lean v4.30.0-rc2 and pinned mathlib
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

/-- An explicit Γ₁(4)-admissible matrix with the WRONG upper-right
residue for the given old charge/backwardCount presentation. -/
def nativeGK4APForbiddenUpperMatrix (v : NativeGK4ADValue) :
    NativeGK4AHMatrix :=
  ((1, nativeGK4APOldUpperResidue v + 1), (0, 1))

theorem nativeGK4APForbiddenUpperMatrix_gamma (v : NativeGK4ADValue) :
    nativeGK4AOIntegralCongruence (nativeGK4APForbiddenUpperMatrix v) := by
  refine ⟨?_, ⟨0, ?_⟩, ⟨0, ?_⟩, ⟨0, ?_⟩⟩
  · simp [nativeGK4AODet, nativeGK4APForbiddenUpperMatrix]
  · simp [nativeGK4APForbiddenUpperMatrix]
  · simp [nativeGK4APForbiddenUpperMatrix]
  · simp [nativeGK4APForbiddenUpperMatrix]

/-- Stronger than GK4AO's previous SL₂ obstruction:
this impossible matrix STILL BELONGS to Γ₁(4). -/
theorem nativeGK4APForbiddenUpperMatrix_not_linked (v : NativeGK4ADValue) :
    ¬ nativeGK4APLinked v (nativeGK4APForbiddenUpperMatrix v) := by
  rintro ⟨_, t, ht⟩
  change nativeGK4APOldUpperResidue v + 1 =
    nativeGK4APOldUpperResidue v + 4 * t at ht
  omega

section ActualOldTargetFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The q-dependent proper arithmetic slice of Γ₁(4), based on
the ACTUAL old K_AG value, not a chosen untyped F54 representative. -/
def nativeGK4APFiberArithmeticSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  {M | nativeGK4APLinked
    ((nativeGK4AGKernelValue first last target).1.2) M}

/-- Every q-dependent slice is inside Γ₁(4), a previously proved
necessary congruence domain of second observation matrices. -/
theorem nativeGK4APFiberSlice_subset_gamma
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4APFiberArithmeticSlice first last target ⊆
      {M | nativeGK4AOIntegralCongruence M} := by
  intro M hM
  exact hM.1

/-- The TRUE GK4AL attained matrix image is in this STRONGER
fixed-q arithmetic slice. No syntactic word is silently identified. -/
theorem nativeGK4APAttained_subset_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      nativeGK4APFiberArithmeticSlice first last target := by
  intro M hM
  rcases hM with ⟨z, rfl⟩
  exact nativeGK4APFiber_sound first last target z

/-- Every two actual independent K_AI classes in ONE fixed old
q-fiber have equal upper-right second-matrix residues modulo 4. -/
theorem nativeGK4APSameFiber_upper_residue
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (x y : nativeGK4AJOldFiber first last target) :
    ∃ t : Int,
      (nativeGK4AJFiberMatrix first last target x).1.2 =
      (nativeGK4AJFiberMatrix first last target y).1.2 + 4 * t := by
  rcases (nativeGK4APFiber_sound first last target x).2 with ⟨tx, hx⟩
  rcases (nativeGK4APFiber_sound first last target y).2 with ⟨ty, hy⟩
  refine ⟨tx - ty, ?_⟩
  rw [hx, hy]
  ring

/-- An explicit Gamma_1(4) matrix NEVER in this fixed q-slice:
the obstruction is the known old AD charge and backward count. -/
theorem nativeGK4APForbiddenMatrix_not_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4APForbiddenUpperMatrix
      ((nativeGK4AGKernelValue first last target).1.2) ∉
        nativeGK4APFiberArithmeticSlice first last target := by
  intro h
  exact nativeGK4APForbiddenUpperMatrix_not_linked
    ((nativeGK4AGKernelValue first last target).1.2) h

/-- The Γ₁(4) boundary is STRICT FOR EVERY OLD q:
a q-dependent determinant-one and Gamma-admissible integer matrix
does not lie in the actually attained second matrix image. -/
theorem nativeGK4APStrictGammaSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    ∃ M : NativeGK4AHMatrix,
      nativeGK4AOIntegralCongruence M ∧
      M ∉ nativeGK4ALAttainedMatrixSet first last target := by
  let v := (nativeGK4AGKernelValue first last target).1.2
  refine ⟨nativeGK4APForbiddenUpperMatrix v,
    nativeGK4APForbiddenUpperMatrix_gamma v, ?_⟩
  intro h
  exact nativeGK4APForbiddenMatrix_not_slice first last target
    (nativeGK4APAttained_subset_slice first last target h)

/-- A faithful genuine typed fiber code into ONLY its own
q-dependent arithmetic slice, stronger than prior full Γ₁(4). -/
def nativeGK4APRestrictedFiberEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪
      {M : NativeGK4AHMatrix //
        M ∈ nativeGK4APFiberArithmeticSlice first last target} where
  toFun z := ⟨nativeGK4AJFiberMatrix first last target z,
    nativeGK4APFiber_sound first last target z⟩
  inj' := by
    intro x y h
    apply nativeGK4AJFiberMatrix_injective first last target
    exact congrArg Subtype.val h

/-- Exactly the actually ATTAINED portion of the q-slice:
the equivalence does not claim any Γ₁(4) or q-slice surjectivity. -/
def nativeGK4APRestrictedAttainedEquiv
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {M : {N : NativeGK4AHMatrix //
        N ∈ nativeGK4APFiberArithmeticSlice first last target} //
        M ∈ Set.range (nativeGK4APRestrictedFiberEmbedding first last target)} :=
  Equiv.ofBijective
    (fun z => ⟨nativeGK4APRestrictedFiberEmbedding first last target z,
      ⟨z, rfl⟩⟩)
    ⟨(by
       intro x y h
       apply (nativeGK4APRestrictedFiberEmbedding first last target).injective
       exact congrArg Subtype.val h),
     (by
       rintro ⟨M, ⟨z, hz⟩⟩
       refine ⟨z, ?_⟩
       exact Subtype.ext hz)⟩

end ActualOldTargetFibers

#print axioms nativeGK4APForbiddenUpperMatrix
#print axioms nativeGK4APForbiddenUpperMatrix_gamma
#print axioms nativeGK4APForbiddenUpperMatrix_not_linked
#print axioms nativeGK4APFiberArithmeticSlice
#print axioms nativeGK4APFiberSlice_subset_gamma
#print axioms nativeGK4APAttained_subset_slice
#print axioms nativeGK4APSameFiber_upper_residue
#print axioms nativeGK4APForbiddenMatrix_not_slice
#print axioms nativeGK4APStrictGammaSlice
#print axioms nativeGK4APRestrictedFiberEmbedding
#print axioms nativeGK4APRestrictedAttainedEquiv

end
end Kuu.F112.Physical
