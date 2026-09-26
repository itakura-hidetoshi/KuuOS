import KUOS.DependentOriginationStageIIExactFractalCertificateV4_40
import Mathlib.Analysis.Real.OfDigits
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Set.Finite.Lattice
import Mathlib.Data.Set.Finite.Range
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib

namespace KUOS.DependentOriginationStageIIFiniteApproxDimensionV4_41

open MeasureTheory
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIICantorMetricConvergenceV4_31

set_option autoImplicit false

noncomputable section

/-!
# Finite Stage-II approximants have Hausdorff dimension zero v4.41

v4.31 defines the depth-n Cantor partial sum by summing the first n ternary
digit terms of mathlib's canonical Cantor coding.  The formal point of this
unit is to expose, inside Lean, that this partial sum factors through a finite
prefix carrier.

We use the deliberately generous finite code type

  Fin n → Fin 3.

The actual Cantor digits are only 0 or 2, but that sharper restriction is not
needed for finiteness.  The factorization is exact: the range-n sum in v4.31 is
identified with the corresponding sum over Fin n using
Fin.sum_univ_eq_sum_range and the defining formula for Real.ofDigitsTerm.

Consequently:

* the range of stageIICantorPartial n is finite;
* every translated depth-n geometric fiber is finite;
* the global union over the eight Stage-II branch indices is finite;
* every such finite approximant has Hausdorff dimension zero by
  Set.Finite.dimH_zero.

No informal cardinality argument is used.
-/

/-- The length-n ternary prefix read from mathlib's canonical Cantor coding. -/
def stageIICantorPrefix
    (n : Nat) (t : ℝ) :
    Fin n → Fin 3 :=
  fun i => cantorToTernary t i

/-- Evaluate a finite ternary prefix as the same positional sum used by
Real.ofDigitsTerm.  This is defined on a finite domain of prefix codes. -/
noncomputable def stageIICantorPartialOfPrefix
    (n : Nat) (a : Fin n → Fin 3) : ℝ :=
  ∑ i : Fin n,
    ((a i : Nat) : ℝ) * ((3 : ℝ) ^ ((i : Nat) + 1))⁻¹

/-- Exact factorization of the v4.31 partial sum through the finite prefix
carrier Fin n → Fin 3. -/
theorem stageIICantorPartial_eq_partialOfPrefix
    (n : Nat) (t : ℝ) :
    stageIICantorPartial n t =
      stageIICantorPartialOfPrefix n (stageIICantorPrefix n t) := by
  simpa [stageIICantorPartial, stageIICantorPartialOfPrefix,
    stageIICantorPrefix, Real.ofDigitsTerm] using
    (Fin.sum_univ_eq_sum_range
      (fun i : Nat => Real.ofDigitsTerm (cantorToTernary t) i)
      n).symm

/-- Equal finite ternary prefixes give equal depth-n partial sums. -/
theorem stageIICantorPartial_eq_of_prefix_eq
    {n : Nat} {t u : ℝ}
    (h :
      stageIICantorPrefix n t =
        stageIICantorPrefix n u) :
    stageIICantorPartial n t =
      stageIICantorPartial n u := by
  rw [stageIICantorPartial_eq_partialOfPrefix,
    stageIICantorPartial_eq_partialOfPrefix, h]

/-- The range of the depth-n Cantor partial-sum map is finite because it is
contained in the range of a function whose domain Fin n → Fin 3 is finite. -/
theorem range_stageIICantorPartial_finite
    (n : Nat) :
    (Set.range (stageIICantorPartial n)).Finite := by
  refine
    (Set.finite_range (stageIICantorPartialOfPrefix n)).subset ?_
  rintro y ⟨t, rfl⟩
  refine ⟨stageIICantorPrefix n t, ?_⟩
  exact (stageIICantorPartial_eq_partialOfPrefix n t).symm

/-- One translated geometric approximant fiber is contained in the finite
range obtained by translating all finite prefix values. -/
theorem stageIIGeometricApproxFiber_subset_prefixRange
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) :
    stageIIGeometricApproxFiber n x ⊆
      Set.range
        (fun a : Fin n → Fin 3 =>
          stageIICurrentBranchOffset x +
            stageIICantorPartialOfPrefix n a) := by
  intro y hy
  change
    y ∈ stageIIGeometricApproxPoint n x '' cantorSet
      at hy
  rcases hy with ⟨t, ht, rfl⟩
  refine ⟨stageIICantorPrefix n t, ?_⟩
  unfold stageIIGeometricApproxPoint
  exact
    congrArg
      (fun s : ℝ => stageIICurrentBranchOffset x + s)
      (stageIICantorPartial_eq_partialOfPrefix n t).symm

/-- Every depth-n geometric approximant fiber is finite. -/
theorem stageIIGeometricApproxFiber_finite
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) :
    (stageIIGeometricApproxFiber n x).Finite := by
  exact
    (Set.finite_range
      (fun a : Fin n → Fin 3 =>
        stageIICurrentBranchOffset x +
          stageIICantorPartialOfPrefix n a)).subset
      (stageIIGeometricApproxFiber_subset_prefixRange n x)

/-- The global depth-n Stage-II geometric approximant is finite because the
branch index type is finite and every branch fiber is finite. -/
theorem XInfinityGeometricApprox_finite
    (n : Nat) :
    (XInfinityGeometricApprox n).Finite := by
  unfold XInfinityGeometricApprox
  exact
    Set.finite_iUnion
      (fun x : StageIIFiniteDepthInverseLimit =>
        stageIIGeometricApproxFiber_finite n x)

/-- Every finite-depth translated approximant fiber has Hausdorff dimension
zero. -/
theorem dimH_stageIIGeometricApproxFiber_eq_zero
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) :
    dimH (stageIIGeometricApproxFiber n x) = 0 := by
  exact (stageIIGeometricApproxFiber_finite n x).dimH_zero

/-- Main v4.41 theorem: every global finite-depth approximant has Hausdorff
dimension zero. -/
theorem dimH_XInfinityGeometricApprox_eq_zero
    (n : Nat) :
    dimH (XInfinityGeometricApprox n) = 0 := by
  exact (XInfinityGeometricApprox_finite n).dimH_zero

/-!
## Boundary after v4.41

The finite-depth side of the Stage-II geometric construction is now exact.

For every n:

  stageIIGeometricApproxFiber n x

and

  XInfinityGeometricApprox n

are finite sets, because their values factor through finite ternary prefix
codes.  Therefore both have Hausdorff dimension zero.

Together with v4.31 and v4.39, the next theorem unit can now state the concrete
Hausdorff-limit dimension jump:

* every approximant has dimH = 0;
* d_H(X_n, X_infinity) <= 3^{-n};
* d_H(X_n, X_infinity) -> 0;
* dimH(X_infinity) = log 2 / log 3 > 0.

That is the intended v4.42 synthesis.
-/

end

end KUOS.DependentOriginationStageIIFiniteApproxDimensionV4_41
