import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVPolynomialInvariant
import Mathlib.Algebra.Polynomial.Degree.Lemmas
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Tactic

/-!
F112-P94D3GK4AV — evaluation, SL₂(Z[X]) determinant and true
backwardCount bounds of the original F54 typed polynomial observer.
Every entry has natDegree ≤ original GK4AD backwardCount. This is
proved for real rotation edges, intermediate trees, all five original
route constructors, and separately for Q and independent S.
Evaluation is EXACTLY the GK4AU family at every integer t, including
the genuine previous AF/AH observations t=1,4.

natDegree bound is an upper bound, not an equality for every path;
nothing implies a source 3-cell from a polynomial identity.
No assumption that the full polynomial observer descends to the
existing two-evaluation K_AI quotient. No original Q category laws.
Append-only / tighten-only / same public roots107. Protected #1558.
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

/-- Evaluate each polynomial at the same actual integer parameter. -/
def nativeGK4AVPolyEval (t : Int) (M : NativeGK4AVValue) :
    NativeGK4AHMatrix :=
  ((M.1.1.eval t, M.1.2.eval t),
   (M.2.1.eval t, M.2.2.eval t))

theorem nativeGK4AVPolyEval_mul (t : Int)
    (A B : NativeGK4AVValue) :
    nativeGK4AVPolyEval t (nativeGK4AVMul A B) =
      nativeGK4AHMul (nativeGK4AVPolyEval t A)
        (nativeGK4AVPolyEval t B) := by
  rcases A with ⟨⟨a, b⟩, ⟨c, d⟩⟩
  rcases B with ⟨⟨e, f⟩, ⟨g, h⟩⟩
  simp [nativeGK4AVPolyEval, nativeGK4AVMul, nativeGK4AHMul]

theorem nativeGK4AVPolyEval_one (t : Int) :
    nativeGK4AVPolyEval t nativeGK4AVOne = nativeGK4AHOne := by
  simp [nativeGK4AVPolyEval, nativeGK4AVOne, nativeGK4AHOne]

theorem nativeGK4AVPolyEval_cast (t : Int) :
    nativeGK4AVPolyEval t nativeGK4AVCast = nativeGK4AHCast := by
  simp [nativeGK4AVPolyEval, nativeGK4AVCast, nativeGK4AHCast]

theorem nativeGK4AVPolyEval_forward (t : Int) :
    nativeGK4AVPolyEval t nativeGK4AVForward = nativeGK4AHForward := by
  simp [nativeGK4AVPolyEval, nativeGK4AVForward, nativeGK4AHForward]

theorem nativeGK4AVPolyEval_backward (t : Int) :
    nativeGK4AVPolyEval t nativeGK4AVBackward =
      nativeGK4AUBackward t := by
  simp [nativeGK4AVPolyEval, nativeGK4AVBackward, nativeGK4AUBackward]

/-- Determinant inside the polynomial ring (not only after evaluation). -/
def nativeGK4AVPolyDet (M : NativeGK4AVValue) : Polynomial Int :=
  M.1.1 * M.2.2 - M.1.2 * M.2.1

theorem nativeGK4AVPolyDet_mul (A B : NativeGK4AVValue) :
    nativeGK4AVPolyDet (nativeGK4AVMul A B) =
      nativeGK4AVPolyDet A * nativeGK4AVPolyDet B := by
  rcases A with ⟨⟨a,b⟩,⟨c,d⟩⟩
  rcases B with ⟨⟨e,f⟩,⟨g,h⟩⟩
  simp only [nativeGK4AVPolyDet, nativeGK4AVMul]
  ring

theorem nativeGK4AVPolyDet_one :
    nativeGK4AVPolyDet nativeGK4AVOne = 1 := by
  simp [nativeGK4AVPolyDet, nativeGK4AVOne]

theorem nativeGK4AVPolyDet_cast :
    nativeGK4AVPolyDet nativeGK4AVCast = 1 := by
  simp [nativeGK4AVPolyDet, nativeGK4AVCast]

theorem nativeGK4AVPolyDet_forward :
    nativeGK4AVPolyDet nativeGK4AVForward = 1 := by
  simp [nativeGK4AVPolyDet, nativeGK4AVForward]

theorem nativeGK4AVPolyDet_backward :
    nativeGK4AVPolyDet nativeGK4AVBackward = 1 := by
  simp [nativeGK4AVPolyDet, nativeGK4AVBackward]

/-- All four polynomial degrees are bounded by an original Nat count. -/
def nativeGK4AVDegreeBound (b : Nat) (M : NativeGK4AVValue) : Prop :=
  M.1.1.natDegree ≤ b ∧ M.1.2.natDegree ≤ b ∧
  M.2.1.natDegree ≤ b ∧ M.2.2.natDegree ≤ b

/-- Algebraic stability of degree under exact matrix multiplication. -/
theorem nativeGK4AVDegreeBound_mul
    (A B : NativeGK4AVValue) (m n : Nat)
    (hA : nativeGK4AVDegreeBound m A)
    (hB : nativeGK4AVDegreeBound n B) :
    nativeGK4AVDegreeBound (m + n) (nativeGK4AVMul A B) := by
  rcases hA with ⟨ha, hb, hc, hd⟩
  rcases hB with ⟨he, hf, hg, hh⟩
  change
    (A.1.1 * B.1.1 + A.1.2 * B.2.1).natDegree ≤ m + n ∧
    (A.1.1 * B.1.2 + A.1.2 * B.2.2).natDegree ≤ m + n ∧
    (A.2.1 * B.1.1 + A.2.2 * B.2.1).natDegree ≤ m + n ∧
    (A.2.1 * B.1.2 + A.2.2 * B.2.2).natDegree ≤ m + n
  exact ⟨
    Polynomial.natDegree_add_le_of_degree_le
      (Polynomial.natDegree_mul_le_of_le ha he)
      (Polynomial.natDegree_mul_le_of_le hb hg),
    Polynomial.natDegree_add_le_of_degree_le
      (Polynomial.natDegree_mul_le_of_le ha hf)
      (Polynomial.natDegree_mul_le_of_le hb hh),
    Polynomial.natDegree_add_le_of_degree_le
      (Polynomial.natDegree_mul_le_of_le hc he)
      (Polynomial.natDegree_mul_le_of_le hd hg),
    Polynomial.natDegree_add_le_of_degree_le
      (Polynomial.natDegree_mul_le_of_le hc hf)
      (Polynomial.natDegree_mul_le_of_le hd hh)⟩

theorem nativeGK4AVDegreeBound_one :
    nativeGK4AVDegreeBound 0 nativeGK4AVOne := by
  simp [nativeGK4AVDegreeBound, nativeGK4AVOne]

theorem nativeGK4AVDegreeBound_cast :
    nativeGK4AVDegreeBound 0 nativeGK4AVCast := by
  simp [nativeGK4AVDegreeBound, nativeGK4AVCast]

theorem nativeGK4AVDegreeBound_forward :
    nativeGK4AVDegreeBound 0 nativeGK4AVForward := by
  simp [nativeGK4AVDegreeBound, nativeGK4AVForward]

theorem nativeGK4AVDegreeBound_backward :
    nativeGK4AVDegreeBound 1 nativeGK4AVBackward := by
  simp [nativeGK4AVDegreeBound, nativeGK4AVBackward]

section GenuineOriginalDependentSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4AVEdge_eval
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after)
    (t : Int) :
    nativeGK4AVPolyEval t edge.gk4avPolynomial = edge.gk4auFamily t := by
  cases edge with
  | forward _ => exact nativeGK4AVPolyEval_forward t
  | backward _ => exact nativeGK4AVPolyEval_backward t

theorem nativeGK4AVChain_eval
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after)
    (t : Int) :
    nativeGK4AVPolyEval t chain.gk4avPolynomial = chain.gk4auFamily t := by
  induction chain with
  | refl => exact nativeGK4AVPolyEval_one t
  | snoc path edge ih =>
      change nativeGK4AVPolyEval t
        (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial) =
          nativeGK4AHMul (path.gk4auFamily t) (edge.gk4auFamily t)
      rw [nativeGK4AVPolyEval_mul, ih, nativeGK4AVEdge_eval edge t]

theorem nativeGK4AVRoute_eval
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (t : Int) :
    nativeGK4AVPolyEval t route.gk4avPolynomial = route.gk4auFamily t := by
  induction route with
  | chain path => exact nativeGK4AVChain_eval path t
  | castDepths _ _ _ => exact nativeGK4AVPolyEval_cast t
  | trans u v ihu ihv =>
      change nativeGK4AVPolyEval t
        (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial) =
          nativeGK4AHMul (u.gk4auFamily t) (v.gk4auFamily t)
      rw [nativeGK4AVPolyEval_mul, ihu, ihv]
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AVEdge_det
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4AVPolyDet edge.gk4avPolynomial = 1 := by
  cases edge with
  | forward _ => exact nativeGK4AVPolyDet_forward
  | backward _ => exact nativeGK4AVPolyDet_backward

theorem nativeGK4AVChain_det
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4AVPolyDet chain.gk4avPolynomial = 1 := by
  induction chain with
  | refl => exact nativeGK4AVPolyDet_one
  | snoc path edge ih =>
      change nativeGK4AVPolyDet
        (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial) = 1
      rw [nativeGK4AVPolyDet_mul, ih, nativeGK4AVEdge_det edge, mul_one]

theorem nativeGK4AVRoute_det
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4AVPolyDet route.gk4avPolynomial = 1 := by
  induction route with
  | chain path => exact nativeGK4AVChain_det path
  | castDepths _ _ _ => exact nativeGK4AVPolyDet_cast
  | trans u v ihu ihv =>
      change nativeGK4AVPolyDet
        (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial) = 1
      rw [nativeGK4AVPolyDet_mul, ihu, ihv, mul_one]
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AVEdge_degree
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4AVDegreeBound edge.gk4adValue.1.2 edge.gk4avPolynomial := by
  cases edge with
  | forward _ => exact nativeGK4AVDegreeBound_forward
  | backward _ => exact nativeGK4AVDegreeBound_backward

theorem nativeGK4AVChain_degree
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4AVDegreeBound chain.gk4adValue.1.2 chain.gk4avPolynomial := by
  induction chain with
  | refl => exact nativeGK4AVDegreeBound_one
  | snoc path edge ih =>
      change nativeGK4AVDegreeBound
        (path.gk4adValue.1.2 + edge.gk4adValue.1.2)
        (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial)
      exact nativeGK4AVDegreeBound_mul _ _ _ _ ih (nativeGK4AVEdge_degree edge)

theorem nativeGK4AVRoute_degree
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4AVDegreeBound route.gk4adValue.1.2 route.gk4avPolynomial := by
  induction route with
  | chain path => exact nativeGK4AVChain_degree path
  | castDepths _ _ _ => exact nativeGK4AVDegreeBound_cast
  | trans u v ihu ihv =>
      change nativeGK4AVDegreeBound
        (u.gk4adValue.1.2 + v.gk4adValue.1.2)
        (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial)
      exact nativeGK4AVDegreeBound_mul _ _ _ _ ihu ihv
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end GenuineOriginalDependentSource

section ActualOriginalQuotients
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

theorem nativeGK4AVP92_eval
    (q : NativeF55P92AssocRouteClasses first last) (t : Int) :
    nativeGK4AVPolyEval t (nativeGK4AVP92Value first last q) =
      nativeGK4AUP92Value first last q t := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AVRoute_eval raw t

theorem nativeGK4AVStructural_eval
    (s : NativeGK4EStructuralRouteClasses first last) (t : Int) :
    nativeGK4AVPolyEval t (nativeGK4AVStructuralValue first last s) =
      nativeGK4AUStructuralValue first last s t := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  exact nativeGK4AVRoute_eval raw t

theorem nativeGK4AVP92_det
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AVPolyDet (nativeGK4AVP92Value first last q) = 1 := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AVRoute_det raw

theorem nativeGK4AVStructural_det
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AVPolyDet (nativeGK4AVStructuralValue first last s) = 1 := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  exact nativeGK4AVRoute_det raw

theorem nativeGK4AVP92_degree
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AVDegreeBound
      (nativeGK4ADP92Value first last q).1.2
      (nativeGK4AVP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AVRoute_degree raw

theorem nativeGK4AVStructural_degree
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AVDegreeBound
      (nativeGK4ADStructuralValue first last s).1.2
      (nativeGK4AVStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  exact nativeGK4AVRoute_degree raw

/-- Exact evaluations at the two OLD genuine matrix observations. -/
theorem nativeGK4AVP92_recover
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AVPolyEval 1 (nativeGK4AVP92Value first last q) =
      nativeGK4AFP92Value first last q ∧
    nativeGK4AVPolyEval 4 (nativeGK4AVP92Value first last q) =
      nativeGK4AHP92Value first last q := by
  rw [nativeGK4AVP92_eval, nativeGK4AVP92_eval]
  exact nativeGK4AUP92_specialize first last q

theorem nativeGK4AVStructural_recover
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AVPolyEval 1 (nativeGK4AVStructuralValue first last s) =
      nativeGK4AFStructuralValue first last s ∧
    nativeGK4AVPolyEval 4 (nativeGK4AVStructuralValue first last s) =
      nativeGK4AHStructuralValue first last s := by
  rw [nativeGK4AVStructural_eval, nativeGK4AVStructural_eval]
  exact nativeGK4AUStructural_specialize first last s

end ActualOriginalQuotients

#print axioms nativeGK4AVPolyEval
#print axioms nativeGK4AVPolyEval_mul
#print axioms nativeGK4AVPolyEval_one
#print axioms nativeGK4AVPolyEval_cast
#print axioms nativeGK4AVPolyEval_forward
#print axioms nativeGK4AVPolyEval_backward
#print axioms nativeGK4AVPolyDet
#print axioms nativeGK4AVPolyDet_mul
#print axioms nativeGK4AVPolyDet_one
#print axioms nativeGK4AVPolyDet_cast
#print axioms nativeGK4AVPolyDet_forward
#print axioms nativeGK4AVPolyDet_backward
#print axioms nativeGK4AVDegreeBound
#print axioms nativeGK4AVDegreeBound_mul
#print axioms nativeGK4AVDegreeBound_one
#print axioms nativeGK4AVDegreeBound_cast
#print axioms nativeGK4AVDegreeBound_forward
#print axioms nativeGK4AVDegreeBound_backward
#print axioms nativeGK4AVEdge_eval
#print axioms nativeGK4AVChain_eval
#print axioms nativeGK4AVRoute_eval
#print axioms nativeGK4AVEdge_det
#print axioms nativeGK4AVChain_det
#print axioms nativeGK4AVRoute_det
#print axioms nativeGK4AVEdge_degree
#print axioms nativeGK4AVChain_degree
#print axioms nativeGK4AVRoute_degree
#print axioms nativeGK4AVP92_eval
#print axioms nativeGK4AVStructural_eval
#print axioms nativeGK4AVP92_det
#print axioms nativeGK4AVStructural_det
#print axioms nativeGK4AVP92_degree
#print axioms nativeGK4AVStructural_degree
#print axioms nativeGK4AVP92_recover
#print axioms nativeGK4AVStructural_recover

end
end Kuu.F112.Physical
