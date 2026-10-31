import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANShiftedOddFamily
import Mathlib.Tactic

/-!
F112-P94D3GK4AO — arithmetic OBSTRUCTION for the actual second
integer 2x2 observation M_AH of ORIGINAL F54 dependent typed paths.
Every actual source matrix has determinant exactly 1 and belongs
to the congruence subgroup with diagonal entries 1 mod 4 and
bottom-left entry 0 mod 4. These are algebraic NECESSARY conditions,
not a characterization of all matrices that occur on any Hom.

Prove the multiplicative invariant on the exact GK4AH generators
C, F, R4, the original intermediate-tree RotationChain and all
five actual original DepthRotationRoute constructors, then descend
SEPARATELY through the original P92B Q and independent structural S.
GK4AH already proved preservation of real F55/P92B 9, fourteen
seams and three extended comparison constructors; NO new Type cell
is produced by integer equality. Transfer to actual K_AI and
every dependent forgetful fiber. No original Q category axioms,
no fixed infinite fiber, no Gray/hyperdescent or global faithfulness.
Append-only/tighten-only/same-root107. Strict 空 central; independent
Kuu one presentation. PR #1558 protected Draft/OPEN/unmerged.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- The ACTUAL determinant of the full ordered GK4AH integer matrix. -/
def nativeGK4AODet (M : NativeGK4AHMatrix) : Int :=
  M.1.1 * M.2.2 - M.1.2 * M.2.1

/-- The three exact integral congruence conditions of the genuine
Gamma_1(4) image, written without an unverified Mathlib API. -/
def nativeGK4AOIntegralCongruence (M : NativeGK4AHMatrix) : Prop :=
  nativeGK4AODet M = 1 ∧
  (∃ a : Int, M.1.1 = 1 + 4 * a) ∧
  (∃ c : Int, M.2.1 = 4 * c) ∧
  (∃ d : Int, M.2.2 = 1 + 4 * d)

/-- Determinant multiplicativity for the genuine ordered matrix
product: an unrestricted, directly checked integral polynomial law. -/
theorem nativeGK4AODet_mul (u v : NativeGK4AHMatrix) :
    nativeGK4AODet (nativeGK4AHMul u v) =
      nativeGK4AODet u * nativeGK4AODet v := by
  rcases u with ⟨⟨a, b⟩, ⟨c, d⟩⟩
  rcases v with ⟨⟨e, f⟩, ⟨g, h⟩⟩
  simp [nativeGK4AODet, nativeGK4AHMul]
  ring

/-- Gamma_1(4) congruences AND determinant 1 are closed under the
exact matrix product. Both integral witnesses are constructed. -/
theorem nativeGK4AOIntegralCongruence_mul (u v : NativeGK4AHMatrix)
    (hu : nativeGK4AOIntegralCongruence u)
    (hv : nativeGK4AOIntegralCongruence v) :
    nativeGK4AOIntegralCongruence (nativeGK4AHMul u v) := by
  rcases hu with ⟨hdu, ⟨au, hau⟩, ⟨cu, hcu⟩, ⟨du, hdu'⟩⟩
  rcases hv with ⟨hdv, ⟨av, hav⟩, ⟨cv, hcv⟩, ⟨dv, hdv'⟩⟩
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [nativeGK4AODet_mul, hdu, hdv]
    norm_num
  · refine ⟨au + av + 4 * au * av + u.1.2 * cv, ?_⟩
    change u.1.1 * v.1.1 + u.1.2 * v.2.1 =
      1 + 4 * (au + av + 4 * au * av + u.1.2 * cv)
    rw [hau, hav, hcv]
    ring
  · refine ⟨cu + cv + 4 * cu * av + 4 * du * cv, ?_⟩
    change u.2.1 * v.1.1 + u.2.2 * v.2.1 =
      4 * (cu + cv + 4 * cu * av + 4 * du * cv)
    rw [hcu, hav, hdu', hcv]
    ring
  · refine ⟨du + dv + 4 * du * dv + cu * v.1.2, ?_⟩
    change u.2.1 * v.1.2 + u.2.2 * v.2.2 =
      1 + 4 * (du + dv + 4 * du * dv + cu * v.1.2)
    rw [hcu, hdu', hdv']
    ring

/-- Unit and the three ORIGINAL F54 source-generator evaluations
really lie in the integral congruence monoid. -/
theorem nativeGK4AOIntegralCongruence_one :
    nativeGK4AOIntegralCongruence nativeGK4AHOne := by
  exact ⟨by decide, ⟨0, by decide⟩, ⟨0, by decide⟩, ⟨0, by decide⟩⟩

theorem nativeGK4AOIntegralCongruence_cast :
    nativeGK4AOIntegralCongruence nativeGK4AHCast := by
  exact ⟨by decide, ⟨0, by decide⟩, ⟨0, by decide⟩, ⟨0, by decide⟩⟩

theorem nativeGK4AOIntegralCongruence_forward :
    nativeGK4AOIntegralCongruence nativeGK4AHForward := by
  exact ⟨by decide, ⟨0, by decide⟩, ⟨0, by decide⟩, ⟨0, by decide⟩⟩

theorem nativeGK4AOIntegralCongruence_backward :
    nativeGK4AOIntegralCongruence nativeGK4AHBackward := by
  exact ⟨by decide, ⟨0, by decide⟩, ⟨1, by decide⟩, ⟨0, by decide⟩⟩

section ActualOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- Original Type-valued forward/backward rotation edge: not a new
untyped letter or a matrix chosen independently from the source. -/
theorem nativeGK4AORotationEdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4AOIntegralCongruence edge.gk4ahMatrix := by
  cases edge with
  | forward _ => exact nativeGK4AOIntegralCongruence_forward
  | backward _ => exact nativeGK4AOIntegralCongruence_backward

/-- The original intermediate-tree RotationChain is sound, even
without assuming an edge exists between arbitrary input trees. -/
theorem nativeGK4AORotationChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4AOIntegralCongruence chain.gk4ahMatrix := by
  induction chain with
  | refl => exact nativeGK4AOIntegralCongruence_one
  | snoc path edge ih =>
      change nativeGK4AOIntegralCongruence
        (nativeGK4AHMul path.gk4ahMatrix edge.gk4ahMatrix)
      exact nativeGK4AOIntegralCongruence_mul _ _
        ih (nativeGK4AORotationEdge_sound edge)

/-- All FIVE genuine original F54 dependent route constructors:
chain/cast/trans/leftContext/rightContext. No original comparison
cell, Q law, Gray interchange or synthetic matrix-only path. -/
theorem nativeGK4AODepthRotationRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4AOIntegralCongruence route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4AORotationChain_sound path
  | castDepths _ _ _ => exact nativeGK4AOIntegralCongruence_cast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4AOIntegralCongruence_mul _ _ ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end ActualOriginalSource

section ExactTypedDescent
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- ACTUAL original P92B Q existence quotient: the pre-existing
Type-valued F55/P92B comparison soundness supports this descent. -/
theorem nativeGK4AOP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AOIntegralCongruence (nativeGK4AHP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4AOIntegralCongruence raw.gk4ahMatrix
  exact nativeGK4AODepthRotationRoute_sound raw

/-- Separately constructed independent structural S: already
certified GK4AH seam soundness, never equality -> Type-cell. -/
theorem nativeGK4AOStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AOIntegralCongruence (nativeGK4AHStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change nativeGK4AOIntegralCongruence raw.gk4ahMatrix
  exact nativeGK4AODepthRotationRoute_sound raw

/-- Genuine attained second P92B kernel K_AI on ANY original fully
typed F45 Hom satisfies Gamma_1(4) and determinant 1. -/
theorem nativeGK4AOKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4AOIntegralCongruence
      ((nativeGK4AIKernelValue first last z).2) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4AOIntegralCongruence (nativeGK4AHP92Value first last q)
  exact nativeGK4AOP92_sound first last q

/-- ALL actual dependent fibers over any prior old class q inherit
these necessary restrictions on their second integer matrices. -/
theorem nativeGK4AOFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4AOIntegralCongruence
      (nativeGK4AJFiberMatrix first last target z) :=
  nativeGK4AOKernel_sound first last z.1

/-- The exact GK4AL attained-image normal form lies INSIDE the
proper congruence submonoid, never all integer 2x2 matrices. -/
theorem nativeGK4AOAttainedMatrix_subset
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      {M : NativeGK4AHMatrix | nativeGK4AOIntegralCongruence M} := by
  intro M hM
  rcases hM with ⟨z, rfl⟩
  exact nativeGK4AOFiber_sound first last target z

/-- Any matrix that violates even ONE congruence or determinant
constraint is rigorously impossible above this actual old target. -/
theorem nativeGK4AOUnattainable_of_not_congruence
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (M : NativeGK4AHMatrix) (hM : ¬ nativeGK4AOIntegralCongruence M) :
    M ∉ nativeGK4ALAttainedMatrixSet first last target := by
  intro h
  exact hM (nativeGK4AOAttainedMatrix_subset first last target h)

end ExactTypedDescent

#print axioms nativeGK4AODet
#print axioms nativeGK4AOIntegralCongruence
#print axioms nativeGK4AODet_mul
#print axioms nativeGK4AOIntegralCongruence_mul
#print axioms nativeGK4AOIntegralCongruence_one
#print axioms nativeGK4AOIntegralCongruence_cast
#print axioms nativeGK4AOIntegralCongruence_forward
#print axioms nativeGK4AOIntegralCongruence_backward
#print axioms nativeGK4AORotationEdge_sound
#print axioms nativeGK4AORotationChain_sound
#print axioms nativeGK4AODepthRotationRoute_sound
#print axioms nativeGK4AOP92_sound
#print axioms nativeGK4AOStructural_sound
#print axioms nativeGK4AOKernel_sound
#print axioms nativeGK4AOFiber_sound
#print axioms nativeGK4AOAttainedMatrix_subset
#print axioms nativeGK4AOUnattainable_of_not_congruence

end
end Kuu.F112.Physical
