import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AWPolynomialCoeffSharp
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Tactic

/-!
F112-P94D3GK4AX — finite-sample determinacy of genuine polynomial
matrix histories with exact original GK4AD backwardCount bounds.

Using pinned mathlib Polynomial.eq_of_natDegree_lt_card_of_eval_eq,
any two genuine F54 original dependent routes with backward counts
b,c are polynomially identical when they have identical evaluations
at more than max(b,c) pairwise distinct integer parameters.
The same assertion is established SEPARATELY on original P92B Q
and independent original structural S.

In particular the TWO historical AF and AH evaluations (1,4)
are sufficient if BOTH actual backwardCounts are at most one.
Any hypothetical collision of these two observations with unequal
polynomial histories therefore requires max backwardCount >= 2.
This is a proved necessary condition, NOT an existence assertion.

No full one-point t=4 faithfulness is claimed: extending beyond
bounded finite interpolation requires an additional Sanov/ping-pong
free-subgroup theorem and a source-word transfer, not just
polynomial root counting. No extra original Type-valued cells,
existing K_AI family descent, or Q category laws are assumed.

Append-only/tighten-only, unchanged public 107 roots and protected
PR #1558 Draft/OPEN/unmerged. Strict 空 central; independent Kuu
one presentation; no Gray reintroduction.
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
universe uD vD uE vE uI

/-- The pinned mathlib finite-root bound, with the ORIGINAL GK4AV
degree certificates as hypotheses. -/
theorem nativeGK4AXEntry_eq_of_samples
    {ι : Type uI} [Fintype ι] (sample : ι → Int)
    (hinj : Function.Injective sample)
    (b c : Nat) (p q : Polynomial Int)
    (hp : p.natDegree ≤ b) (hq : q.natDegree ≤ c)
    (hcard : max b c < Fintype.card ι)
    (heval : ∀ i : ι, p.eval (sample i) = q.eval (sample i)) :
    p = q := by
  apply Polynomial.eq_of_natDegree_lt_card_of_eval_eq p q hinj heval
  exact lt_of_le_of_lt (max_le_max hp hq) hcard

/-- Full polynomial 2x2 matrix determinacy from finitely many
DISTINCT integer parameters; all four entries, not merely traces. -/
theorem nativeGK4AXMatrix_eq_of_samples
    {ι : Type uI} [Fintype ι] (sample : ι → Int)
    (hinj : Function.Injective sample)
    (b c : Nat) (M N : NativeGK4AVValue)
    (hM : nativeGK4AVDegreeBound b M)
    (hN : nativeGK4AVDegreeBound c N)
    (hcard : max b c < Fintype.card ι)
    (heval : ∀ i : ι,
      nativeGK4AVPolyEval (sample i) M =
        nativeGK4AVPolyEval (sample i) N) : M = N := by
  rcases M with ⟨⟨a, b₁⟩, ⟨c₁, d⟩⟩
  rcases N with ⟨⟨e, f⟩, ⟨g, h⟩⟩
  rcases hM with ⟨ha, hb, hc, hd⟩
  rcases hN with ⟨he, hf, hg, hh⟩
  have h11 : ∀ i : ι, a.eval (sample i) = e.eval (sample i) := by
    intro i
    exact congrArg (fun T : NativeGK4AHMatrix => T.1.1) (heval i)
  have h12 : ∀ i : ι, b₁.eval (sample i) = f.eval (sample i) := by
    intro i
    exact congrArg (fun T : NativeGK4AHMatrix => T.1.2) (heval i)
  have h21 : ∀ i : ι, c₁.eval (sample i) = g.eval (sample i) := by
    intro i
    exact congrArg (fun T : NativeGK4AHMatrix => T.2.1) (heval i)
  have h22 : ∀ i : ι, d.eval (sample i) = h.eval (sample i) := by
    intro i
    exact congrArg (fun T : NativeGK4AHMatrix => T.2.2) (heval i)
  exact Prod.ext
    (Prod.ext
      (nativeGK4AXEntry_eq_of_samples sample hinj _ _ _ _ ha he hcard h11)
      (nativeGK4AXEntry_eq_of_samples sample hinj _ _ _ _ hb hf hcard h12))
    (Prod.ext
      (nativeGK4AXEntry_eq_of_samples sample hinj _ _ _ _ hc hg hcard h21)
      (nativeGK4AXEntry_eq_of_samples sample hinj _ _ _ _ hd hh hcard h22))

/-- Original F54 histories: sample equality is assumed only on
the ACTUAL GK4AU integer family, not on an untyped word model. -/
theorem nativeGK4AXRoute_eq_of_samples
    {ι : Type uI} [Fintype ι] (sample : ι → Int)
    (hinj : Function.Injective sample)
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hcard : max u.gk4adValue.1.2 v.gk4adValue.1.2 < Fintype.card ι)
    (heval : ∀ i : ι, u.gk4auFamily (sample i) = v.gk4auFamily (sample i)) :
    u.gk4avPolynomial = v.gk4avPolynomial := by
  apply nativeGK4AXMatrix_eq_of_samples sample hinj _ _ _ _
    (nativeGK4AVRoute_degree u) (nativeGK4AVRoute_degree v) hcard
  intro i
  exact (nativeGK4AVRoute_eval u (sample i)).trans
    ((heval i).trans (nativeGK4AVRoute_eval v (sample i)).symm)

/-- The ORIGINAL P92B witness-existence quotient Q descends
independently, without assuming its category laws. -/
theorem nativeGK4AXP92_eq_of_samples
    {ι : Type uI} [Fintype ι] (sample : ι → Int)
    (hinj : Function.Injective sample)
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (q r : NativeF55P92AssocRouteClasses first last)
    (hcard :
      max (nativeGK4ADP92Value first last q).1.2
          (nativeGK4ADP92Value first last r).1.2 < Fintype.card ι)
    (heval : ∀ i : ι,
      nativeGK4AUP92Value first last q (sample i) =
        nativeGK4AUP92Value first last r (sample i)) :
    nativeGK4AVP92Value first last q =
      nativeGK4AVP92Value first last r := by
  apply nativeGK4AXMatrix_eq_of_samples sample hinj _ _ _ _
    (nativeGK4AVP92_degree first last q)
    (nativeGK4AVP92_degree first last r) hcard
  intro i
  exact (nativeGK4AVP92_eval first last q (sample i)).trans
    ((heval i).trans (nativeGK4AVP92_eval first last r (sample i)).symm)

/-- The INDEPENDENT original structural quotient S obeys the
same sample-determinacy theorem via its OWN polynomial descent. -/
theorem nativeGK4AXStructural_eq_of_samples
    {ι : Type uI} [Fintype ι] (sample : ι → Int)
    (hinj : Function.Injective sample)
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (q r : NativeGK4EStructuralRouteClasses first last)
    (hcard :
      max (nativeGK4ADStructuralValue first last q).1.2
          (nativeGK4ADStructuralValue first last r).1.2 < Fintype.card ι)
    (heval : ∀ i : ι,
      nativeGK4AUStructuralValue first last q (sample i) =
        nativeGK4AUStructuralValue first last r (sample i)) :
    nativeGK4AVStructuralValue first last q =
      nativeGK4AVStructuralValue first last r := by
  apply nativeGK4AXMatrix_eq_of_samples sample hinj _ _ _ _
    (nativeGK4AVStructural_degree first last q)
    (nativeGK4AVStructural_degree first last r) hcard
  intro i
  exact (nativeGK4AVStructural_eval first last q (sample i)).trans
    ((heval i).trans (nativeGK4AVStructural_eval first last r (sample i)).symm)

/-- The two actual old parameters, indexed without collapsing 1 and 4. -/
def nativeGK4AXTwoSamples (i : Fin 2) : Int :=
  if i = 0 then 1 else 4

theorem nativeGK4AXTwoSamples_injective :
    Function.Injective nativeGK4AXTwoSamples := by
  intro i j hij
  fin_cases i <;> fin_cases j <;>
    simp_all [nativeGK4AXTwoSamples]

/-- TWO evaluations suffice for any full matrix pair whose proven
degrees are each bounded by one. -/
theorem nativeGK4AXMatrix_eq_of_one_four
    (b c : Nat) (M N : NativeGK4AVValue)
    (hM : nativeGK4AVDegreeBound b M)
    (hN : nativeGK4AVDegreeBound c N)
    (hcard : max b c < 2)
    (h1 : nativeGK4AVPolyEval 1 M = nativeGK4AVPolyEval 1 N)
    (h4 : nativeGK4AVPolyEval 4 M = nativeGK4AVPolyEval 4 N) : M = N := by
  apply nativeGK4AXMatrix_eq_of_samples nativeGK4AXTwoSamples
    nativeGK4AXTwoSamples_injective b c M N hM hN
  · simpa using hcard
  · intro i
    fin_cases i
    · simpa [nativeGK4AXTwoSamples] using h1
    · simpa [nativeGK4AXTwoSamples] using h4

section TwoHistoricalObservations
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Real F54: old AF and AH matrices determine the polynomial
matrix whenever both true original backward counts are at most 1. -/
theorem nativeGK4AXRoute_twoEval_determines
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hcard : max u.gk4adValue.1.2 v.gk4adValue.1.2 < 2)
    (hAF : u.gk4afMatrix = v.gk4afMatrix)
    (hAH : u.gk4ahMatrix = v.gk4ahMatrix) :
    u.gk4avPolynomial = v.gk4avPolynomial := by
  apply nativeGK4AXMatrix_eq_of_one_four _ _ _ _
    (nativeGK4AVRoute_degree u) (nativeGK4AVRoute_degree v)
    hcard
  · calc
      nativeGK4AVPolyEval 1 u.gk4avPolynomial = u.gk4auFamily 1 :=
        nativeGK4AVRoute_eval u 1
      _ = u.gk4afMatrix := (nativeGK4AURoute_specialize u).1
      _ = v.gk4afMatrix := hAF
      _ = v.gk4auFamily 1 := (nativeGK4AURoute_specialize v).1.symm
      _ = nativeGK4AVPolyEval 1 v.gk4avPolynomial :=
        (nativeGK4AVRoute_eval v 1).symm
  · calc
      nativeGK4AVPolyEval 4 u.gk4avPolynomial = u.gk4auFamily 4 :=
        nativeGK4AVRoute_eval u 4
      _ = u.gk4ahMatrix := (nativeGK4AURoute_specialize u).2
      _ = v.gk4ahMatrix := hAH
      _ = v.gk4auFamily 4 := (nativeGK4AURoute_specialize v).2.symm
      _ = nativeGK4AVPolyEval 4 v.gk4avPolynomial :=
        (nativeGK4AVRoute_eval v 4).symm

/-- Non-identical polynomial histories with equal old two matrices
NECESSARILY require at least two backwards edges in one route. -/
theorem nativeGK4AXRoute_collision_requires_two
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hAF : u.gk4afMatrix = v.gk4afMatrix)
    (hAH : u.gk4ahMatrix = v.gk4ahMatrix)
    (hne : u.gk4avPolynomial ≠ v.gk4avPolynomial) :
    2 ≤ max u.gk4adValue.1.2 v.gk4adValue.1.2 := by
  by_contra hlt
  have hcard : max u.gk4adValue.1.2 v.gk4adValue.1.2 < 2 :=
    Nat.lt_of_not_ge hlt
  exact hne (nativeGK4AXRoute_twoEval_determines u v hcard hAF hAH)

end TwoHistoricalObservations

section TwoHistoricalQuotients
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Original P92B Q: exact AF/AH two-evaluation determinacy
at max backwardCount < 2, without any Q category axioms. -/
theorem nativeGK4AXP92_twoEval_determines
    (q r : NativeF55P92AssocRouteClasses first last)
    (hcard :
      max (nativeGK4ADP92Value first last q).1.2
          (nativeGK4ADP92Value first last r).1.2 < 2)
    (hAF : nativeGK4AFP92Value first last q = nativeGK4AFP92Value first last r)
    (hAH : nativeGK4AHP92Value first last q = nativeGK4AHP92Value first last r) :
    nativeGK4AVP92Value first last q =
      nativeGK4AVP92Value first last r := by
  apply nativeGK4AXMatrix_eq_of_one_four _ _ _ _
    (nativeGK4AVP92_degree first last q)
    (nativeGK4AVP92_degree first last r) hcard
  · calc
      nativeGK4AVPolyEval 1 (nativeGK4AVP92Value first last q) =
          nativeGK4AFP92Value first last q := (nativeGK4AVP92_recover first last q).1
      _ = nativeGK4AFP92Value first last r := hAF
      _ = nativeGK4AVPolyEval 1 (nativeGK4AVP92Value first last r) :=
        (nativeGK4AVP92_recover first last r).1.symm
  · calc
      nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last q) =
          nativeGK4AHP92Value first last q := (nativeGK4AVP92_recover first last q).2
      _ = nativeGK4AHP92Value first last r := hAH
      _ = nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last r) :=
        (nativeGK4AVP92_recover first last r).2.symm

/-- Independent structural S has its own two-evaluation theorem. -/
theorem nativeGK4AXStructural_twoEval_determines
    (q r : NativeGK4EStructuralRouteClasses first last)
    (hcard :
      max (nativeGK4ADStructuralValue first last q).1.2
          (nativeGK4ADStructuralValue first last r).1.2 < 2)
    (hAF :
      nativeGK4AFStructuralValue first last q = nativeGK4AFStructuralValue first last r)
    (hAH :
      nativeGK4AHStructuralValue first last q = nativeGK4AHStructuralValue first last r) :
    nativeGK4AVStructuralValue first last q =
      nativeGK4AVStructuralValue first last r := by
  apply nativeGK4AXMatrix_eq_of_one_four _ _ _ _
    (nativeGK4AVStructural_degree first last q)
    (nativeGK4AVStructural_degree first last r) hcard
  · calc
      nativeGK4AVPolyEval 1 (nativeGK4AVStructuralValue first last q) =
          nativeGK4AFStructuralValue first last q :=
        (nativeGK4AVStructural_recover first last q).1
      _ = nativeGK4AFStructuralValue first last r := hAF
      _ = nativeGK4AVPolyEval 1 (nativeGK4AVStructuralValue first last r) :=
        (nativeGK4AVStructural_recover first last r).1.symm
  · calc
      nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last q) =
          nativeGK4AHStructuralValue first last q :=
        (nativeGK4AVStructural_recover first last q).2
      _ = nativeGK4AHStructuralValue first last r := hAH
      _ = nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last r) :=
        (nativeGK4AVStructural_recover first last r).2.symm

end TwoHistoricalQuotients

#print axioms nativeGK4AXEntry_eq_of_samples
#print axioms nativeGK4AXMatrix_eq_of_samples
#print axioms nativeGK4AXRoute_eq_of_samples
#print axioms nativeGK4AXP92_eq_of_samples
#print axioms nativeGK4AXStructural_eq_of_samples
#print axioms nativeGK4AXTwoSamples
#print axioms nativeGK4AXTwoSamples_injective
#print axioms nativeGK4AXMatrix_eq_of_one_four
#print axioms nativeGK4AXRoute_twoEval_determines
#print axioms nativeGK4AXRoute_collision_requires_two
#print axioms nativeGK4AXP92_twoEval_determines
#print axioms nativeGK4AXStructural_twoEval_determines

end
end Kuu.F112.Physical
