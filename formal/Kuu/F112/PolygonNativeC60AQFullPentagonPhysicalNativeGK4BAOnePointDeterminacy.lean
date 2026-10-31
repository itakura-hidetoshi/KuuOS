import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAIntegerWordAction
import Mathlib.Tactic

/-!
F112-P94D3GK4BA — GK4AZ's PROVED free-product injection implies
that the single ACTUAL old GK4AH parameter t=4 determines the entire
GK4AV polynomial matrix of every genuine F54 dependent route.

The proof is NOT an unsupported Sanov axiom: every source path has
an actual two-cyclic free-product word. Its integer action equals
the rescaled matrix P_r(4) on the even horizontal sublattice,
and since the integer action is additive this lattice determines
the whole permutation. GK4AZ ping-pong injectivity then recovers
the free-product word, whose universal polynomial action recovers
all four entries P_r(X). This holds separately on existing P92B Q
and independent S by proven original quotient descents.

This does NOT imply original source Type-valued path equality,
source 3-cells, old Q category laws, or full historical typed
equivalence. Append-only, tighten-only, same public roots107,
strict 空 central; independent Kuu one presentation, no Gray.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/OPEN/unmerged.
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

section GenuineF54OnePoint
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Even-horizontal lattice equality is enough for these SPECIFIC
additive word permutations: doubling all coordinates lets us
cancel the integer factor 2. -/
theorem nativeGK4BAIntegerRoutes_sameWord
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (h4 :
      nativeGK4AVPolyEval 4 u.gk4avPolynomial =
        nativeGK4AVPolyEval 4 v.gk4avPolynomial) :
    u.gk4baWord = v.gk4baWord := by
  apply nativeGK4BAIntegerWordAction_injective
  intro z
  have hu := nativeGK4BAIntegerRoute_action u z.1 (2*z.2)
  have hv := nativeGK4BAIntegerRoute_action v z.1 (2*z.2)
  have heven :
      nativeGK4BAIntegerWordAction u.gk4baWord (2*z.1, 2*z.2) =
        nativeGK4BAIntegerWordAction v.gk4baWord (2*z.1, 2*z.2) := by
    calc
      _ = nativeGK4BARescaledVec
          (nativeGK4AVPolyEval 4 u.gk4avPolynomial)
          z.1 (2*z.2) := hu
      _ = nativeGK4BARescaledVec
          (nativeGK4AVPolyEval 4 v.gk4avPolynomial)
          z.1 (2*z.2) := by rw [h4]
      _ = _ := hv.symm
  rw [nativeGK4BAIntegerWordAction_double u.gk4baWord z,
    nativeGK4BAIntegerWordAction_double v.gk4baWord z] at heven
  apply Prod.ext
  · have h := congrArg Prod.fst heven
    omega
  · have h := congrArg Prod.snd heven
    omega

/-- FULL, all-degree polynomial-matrix equality from one actual
old AH evaluation at t=4, for ALL true F54 dependent paths. -/
theorem nativeGK4BARoute_onePoint_determines
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (h4 :
      nativeGK4AVPolyEval 4 u.gk4avPolynomial =
        nativeGK4AVPolyEval 4 v.gk4avPolynomial) :
    u.gk4avPolynomial = v.gk4avPolynomial :=
  nativeGK4BAWord_eq_implies_polynomial u v
    (nativeGK4BAIntegerRoutes_sameWord u v h4)

/-- Exact iff: the universal polynomial family carries no additional
route-distinguishing information beyond the ORIGINAL AH t=4 matrix. -/
theorem nativeGK4BARoute_polynomial_eq_iff_four
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    u.gk4avPolynomial = v.gk4avPolynomial ↔
      nativeGK4AVPolyEval 4 u.gk4avPolynomial =
        nativeGK4AVPolyEval 4 v.gk4avPolynomial := by
  constructor
  · intro h
    exact congrArg (nativeGK4AVPolyEval 4) h
  · exact nativeGK4BARoute_onePoint_determines u v

/-- A single OLD AH observation already determines all polynomial
coefficients for two original fully typed F54 routes. -/
theorem nativeGK4BARoute_AH_determines
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hAH : u.gk4ahMatrix = v.gk4ahMatrix) :
    u.gk4avPolynomial = v.gk4avPolynomial := by
  apply nativeGK4BARoute_onePoint_determines u v
  calc
    nativeGK4AVPolyEval 4 u.gk4avPolynomial = u.gk4auFamily 4 :=
      nativeGK4AVRoute_eval u 4
    _ = u.gk4ahMatrix := (nativeGK4AURoute_specialize u).2
    _ = v.gk4ahMatrix := hAH
    _ = v.gk4auFamily 4 := (nativeGK4AURoute_specialize v).2.symm
    _ = nativeGK4AVPolyEval 4 v.gk4avPolynomial :=
      (nativeGK4AVRoute_eval v 4).symm

/-- Consequently no ORIGINAL F54 typed pair can have equal AF and
AH matrix observations but DISTINCT polynomial matrices.
This refutes the earlier proposed candidate, without adding an
extra source 3-cell or asserting equality of original routes. -/
theorem nativeGK4BA_no_twoEval_polynomial_collision
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ (u.gk4afMatrix = v.gk4afMatrix ∧
      u.gk4ahMatrix = v.gk4ahMatrix ∧
      u.gk4avPolynomial ≠ v.gk4avPolynomial) := by
  rintro ⟨_, hAH, hne⟩
  exact hne (nativeGK4BARoute_AH_determines u v hAH)

end GenuineF54OnePoint

section ExistingOriginalQuotients
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Existing P92B witness-existence Q, WITHOUT assuming Q's missing
associativity and unit laws, has the SAME one-point exact criterion. -/
theorem nativeGK4BAP92_onePoint_determines
    (q r : NativeF55P92AssocRouteClasses first last)
    (h4 :
      nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last q) =
        nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last r)) :
    nativeGK4AVP92Value first last q =
      nativeGK4AVP92Value first last r := by
  refine _root_.Quotient.inductionOn₂ q r ?_
  intro u v
  exact nativeGK4BARoute_onePoint_determines u v

theorem nativeGK4BAP92_AH_determines
    (q r : NativeF55P92AssocRouteClasses first last)
    (hAH : nativeGK4AHP92Value first last q =
      nativeGK4AHP92Value first last r) :
    nativeGK4AVP92Value first last q =
      nativeGK4AVP92Value first last r := by
  apply nativeGK4BAP92_onePoint_determines first last q r
  calc
    nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last q) =
      nativeGK4AHP92Value first last q := (nativeGK4AVP92_recover first last q).2
    _ = nativeGK4AHP92Value first last r := hAH
    _ = nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last r) :=
      (nativeGK4AVP92_recover first last r).2.symm

/-- Independent structural S: separate real quotient descent,
not identification of Q and S. -/
theorem nativeGK4BAStructural_onePoint_determines
    (q r : NativeGK4EStructuralRouteClasses first last)
    (h4 :
      nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last q) =
        nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last r)) :
    nativeGK4AVStructuralValue first last q =
      nativeGK4AVStructuralValue first last r := by
  refine _root_.Quotient.inductionOn₂ q r ?_
  intro u v
  exact nativeGK4BARoute_onePoint_determines u v

theorem nativeGK4BAStructural_AH_determines
    (q r : NativeGK4EStructuralRouteClasses first last)
    (hAH : nativeGK4AHStructuralValue first last q =
      nativeGK4AHStructuralValue first last r) :
    nativeGK4AVStructuralValue first last q =
      nativeGK4AVStructuralValue first last r := by
  apply nativeGK4BAStructural_onePoint_determines first last q r
  calc
    nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last q) =
      nativeGK4AHStructuralValue first last q :=
        (nativeGK4AVStructural_recover first last q).2
    _ = nativeGK4AHStructuralValue first last r := hAH
    _ = nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last r) :=
      (nativeGK4AVStructural_recover first last r).2.symm

end ExistingOriginalQuotients

#print axioms nativeGK4BAIntegerRoutes_sameWord
#print axioms nativeGK4BARoute_onePoint_determines
#print axioms nativeGK4BARoute_polynomial_eq_iff_four
#print axioms nativeGK4BARoute_AH_determines
#print axioms nativeGK4BA_no_twoEval_polynomial_collision
#print axioms nativeGK4BAP92_onePoint_determines
#print axioms nativeGK4BAP92_AH_determines
#print axioms nativeGK4BAStructural_onePoint_determines
#print axioms nativeGK4BAStructural_AH_determines

end
end Kuu.F112.Physical
