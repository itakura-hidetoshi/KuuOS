import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVDegreeEvaluation
import Mathlib.Algebra.Polynomial.Degree.Lemmas
import Mathlib.Tactic

/-!
F112-P94D3GK4AW — EXACT higher-coefficient vanishing and genuinely
attained sharp polynomial degree, on the ORIGINAL F54 dependent source.

GK4AV proves every entry of the genuine SL₂(Z[X]) history has
natDegree bounded by the ORIGINAL GK4AD backwardCount. We turn that
bound into a certificate that EVERY coefficient above the bound is
zero, separately for original F54 routes, P92B Q, and structural S.

The actual LocalRotation forward/backward original Type-valued
backtrack has polynomial matrix
  [[1-X,-1],[X,1]]
and backwardCount=1, with lower-left natDegree=1. Thus the universal
GK4AV degree bound is attained, although not on every route.
The C60 physical north example is unconditional.

No extra Type-valued 3-cells are inferred from observer equality.
No existing K_AI full-polynomial descent or original Q category laws
are assumed. Append-only, tighten-only, same-root107; preserve #1558.
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

/-- Every entry's coefficients above the original backwardCount bound vanish. -/
def nativeGK4AWAboveBoundZero (b : Nat) (M : NativeGK4AVValue) : Prop :=
  ∀ n : Nat, b < n →
    M.1.1.coeff n = 0 ∧ M.1.2.coeff n = 0 ∧
    M.2.1.coeff n = 0 ∧ M.2.2.coeff n = 0

/-- The pinned mathlib degree characterization supplies all four
coefficient equations, including the zero-polynomial case. -/
theorem nativeGK4AWAboveBoundZero_of_degree
    (b : Nat) (M : NativeGK4AVValue)
    (h : nativeGK4AVDegreeBound b M) :
    nativeGK4AWAboveBoundZero b M := by
  intro n hn
  rcases h with ⟨h11, h12, h21, h22⟩
  exact ⟨
    (Polynomial.natDegree_le_iff_coeff_eq_zero.mp h11) n hn,
    (Polynomial.natDegree_le_iff_coeff_eq_zero.mp h12) n hn,
    (Polynomial.natDegree_le_iff_coeff_eq_zero.mp h21) n hn,
    (Polynomial.natDegree_le_iff_coeff_eq_zero.mp h22) n hn⟩

section ActualOriginalDependentSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4AWRoute_coeff_zero
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4AWAboveBoundZero route.gk4adValue.1.2
      route.gk4avPolynomial :=
  nativeGK4AWAboveBoundZero_of_degree _ _ (nativeGK4AVRoute_degree route)

end ActualOriginalDependentSource

section ActualOriginalQuotients
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

theorem nativeGK4AWP92_coeff_zero
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AWAboveBoundZero
      (nativeGK4ADP92Value first last q).1.2
      (nativeGK4AVP92Value first last q) :=
  nativeGK4AWAboveBoundZero_of_degree _ _
    (nativeGK4AVP92_degree first last q)

theorem nativeGK4AWStructural_coeff_zero
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AWAboveBoundZero
      (nativeGK4ADStructuralValue first last s).1.2
      (nativeGK4AVStructuralValue first last s) :=
  nativeGK4AWAboveBoundZero_of_degree _ _
    (nativeGK4AVStructural_degree first last s)

end ActualOriginalQuotients

section GenuineBacktrackDegreeSharpness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

include rot

/-- The real two-edge original typed F54 LocalRotation round trip,
not a synthetic free-monoid word. -/
theorem nativeGK4AWBacktrack_polynomial :
    (nativeGK4FBacktrack rot).gk4avPolynomial =
      (((1 : Polynomial Int) - Polynomial.X, (-1 : Polynomial Int)),
       (Polynomial.X, (1 : Polynomial Int))) := by
  change nativeGK4AVMul
    (nativeGK4AVMul nativeGK4AVOne nativeGK4AVForward)
    nativeGK4AVBackward = _
  rw [nativeGK4AVMul_leftUnit]
  simp [nativeGK4AVMul, nativeGK4AVForward,
    nativeGK4AVBackward, sub_eq_add_neg]

/-- One actual original backwards rotation in the round trip. -/
theorem nativeGK4AWBacktrack_backwardCount :
    (nativeGK4FBacktrack rot).gk4adValue.1.2 = 1 := by
  rfl

/-- The lower-left coefficient retains the actual formal variable X. -/
theorem nativeGK4AWBacktrack_lowerLeft_natDegree :
    ((nativeGK4FBacktrack rot).gk4avPolynomial).2.1.natDegree = 1 := by
  rw [nativeGK4AWBacktrack_polynomial rot]
  simp

/-- The upper bound from GK4AV is sharp for an actual original
Type-valued backtrack, without claiming equality for every route. -/
theorem nativeGK4AWBacktrack_degree_sharp :
    ((nativeGK4FBacktrack rot).gk4avPolynomial).2.1.natDegree =
      (nativeGK4FBacktrack rot).gk4adValue.1.2 := by
  rw [nativeGK4AWBacktrack_lowerLeft_natDegree rot,
    nativeGK4AWBacktrack_backwardCount rot]

end GenuineBacktrackDegreeSharpness

/-- Physical north C60 supplies a genuine unconditional witness. -/
theorem nativeGK4AWPhysicalNorth_degree_sharp :
    ((nativeGK4FBacktrack northHexagonNativeLeftRotation).gk4avPolynomial).2.1.natDegree =
      (nativeGK4FBacktrack northHexagonNativeLeftRotation).gk4adValue.1.2 :=
  nativeGK4AWBacktrack_degree_sharp northHexagonNativeLeftRotation

#print axioms nativeGK4AWAboveBoundZero
#print axioms nativeGK4AWAboveBoundZero_of_degree
#print axioms nativeGK4AWRoute_coeff_zero
#print axioms nativeGK4AWP92_coeff_zero
#print axioms nativeGK4AWStructural_coeff_zero
#print axioms nativeGK4AWBacktrack_polynomial
#print axioms nativeGK4AWBacktrack_backwardCount
#print axioms nativeGK4AWBacktrack_lowerLeft_natDegree
#print axioms nativeGK4AWBacktrack_degree_sharp
#print axioms nativeGK4AWPhysicalNorth_degree_sharp

end
end Kuu.F112.Physical
