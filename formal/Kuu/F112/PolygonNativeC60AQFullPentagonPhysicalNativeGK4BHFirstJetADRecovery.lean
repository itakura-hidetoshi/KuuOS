import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BGResidualAEFiber
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Tactic

/-!
F112-P94D3GK4BH — genuine F54 ordered Heisenberg history
is the FIRST JET of the original polynomial matrix at X=0.

For every genuine, fully typed original F54 DepthRotationRoute, the
constant upper-right coefficient reads its old signed cast charge,
the first lower-left coefficient reads the actual backward count,
and the first upper-left coefficient reads its noncommutative ordered
GK4AD moment. This is proven for every genuine generator, all
typed chains, casts, dependent contexts and composition.

Thus original AH evaluation at t=4 (which determines the entire
polynomial matrix by GK4BA) determines the ENTIRE GK4AD invariant
on genuine F54 routes and the existing original K_AI quotient.

This is not source Type-valued equality, faithfulness of original Q,
new 3-cells, any fabricated witness, Gray or hyperdescent.
Append-only / tighten-only / same public root107.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect validation-only #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- The exact first-jet correspondence between genuine old ordered
F54 history and the full original polynomial-matrix observer. -/
def nativeGK4BHJetLinked
    (d : NativeGK4ADValue) (M : NativeGK4AVValue) : Prop :=
  M.1.1.coeff 0 = 1 ∧
  M.1.2.coeff 0 = d.1.1 ∧
  M.2.1.coeff 0 = 0 ∧
  M.2.2.coeff 0 = 1 ∧
  M.1.1.coeff 1 = d.2 ∧
  M.2.1.coeff 1 = (d.1.2 : Int)

/-- The first jet of a genuine ordered product obeys precisely the
original GK4AD Heisenberg law, including its charge-before-backward
cross-term. Pinned mathlib's 'mul_coeff_zero/one' are used directly. -/
theorem nativeGK4BHJetLinked_mul
    (d e : NativeGK4ADValue) (A B : NativeGK4AVValue)
    (hA : nativeGK4BHJetLinked d A)
    (hB : nativeGK4BHJetLinked e B) :
    nativeGK4BHJetLinked
      (nativeGK4ADCombine d e) (nativeGK4AVMul A B) := by
  rcases hA with ⟨ha11, ha12, ha21, ha22, ha11one, ha21one⟩
  rcases hB with ⟨hb11, hb12, hb21, hb22, hb11one, hb21one⟩
  change
    (A.1.1 * B.1.1 + A.1.2 * B.2.1).coeff 0 = 1 ∧
    (A.1.1 * B.1.2 + A.1.2 * B.2.2).coeff 0 =
      d.1.1 + e.1.1 ∧
    (A.2.1 * B.1.1 + A.2.2 * B.2.1).coeff 0 = 0 ∧
    (A.2.1 * B.1.2 + A.2.2 * B.2.2).coeff 0 = 1 ∧
    (A.1.1 * B.1.1 + A.1.2 * B.2.1).coeff 1 =
      d.2 + e.2 + d.1.1 * (e.1.2 : Int) ∧
    (A.2.1 * B.1.1 + A.2.2 * B.2.1).coeff 1 =
      (((d.1.2 + e.1.2 : Nat) : Int))
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals
    simp only [Polynomial.coeff_add,
      Polynomial.mul_coeff_zero, Polynomial.mul_coeff_one,
      ha11, ha12, ha21, ha22, ha11one, ha21one,
      hb11, hb12, hb21, hb22, hb11one, hb21one]
    push_cast
    ring

theorem nativeGK4BHJetLinked_one :
    nativeGK4BHJetLinked nativeGK4ADZero nativeGK4AVOne := by
  simp [nativeGK4BHJetLinked, nativeGK4ADZero, nativeGK4AVOne]

theorem nativeGK4BHJetLinked_cast :
    nativeGK4BHJetLinked nativeGK4ADCast nativeGK4AVCast := by
  simp [nativeGK4BHJetLinked, nativeGK4ADCast, nativeGK4AVCast]

theorem nativeGK4BHJetLinked_forward :
    nativeGK4BHJetLinked nativeGK4ADForward nativeGK4AVForward := by
  simp [nativeGK4BHJetLinked, nativeGK4ADForward, nativeGK4AVForward]

theorem nativeGK4BHJetLinked_backward :
    nativeGK4BHJetLinked nativeGK4ADBackward nativeGK4AVBackward := by
  simp [nativeGK4BHJetLinked, nativeGK4ADBackward, nativeGK4AVBackward]

section ActualOriginalF54
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- True oriented LocalRotation edges, including the ORIGINAL
backwards orientation (not an invented inverse Hom). -/
theorem nativeGK4BHJet_edge
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4BHJetLinked edge.gk4adValue edge.gk4avPolynomial := by
  cases edge with
  | forward _ => exact nativeGK4BHJetLinked_forward
  | backward _ => exact nativeGK4BHJetLinked_backward

/-- Every intermediate-tree-preserving original F54 rotation chain. -/
theorem nativeGK4BHJet_chain
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4BHJetLinked chain.gk4adValue chain.gk4avPolynomial := by
  induction chain with
  | refl => exact nativeGK4BHJetLinked_one
  | snoc path edge ih =>
      change nativeGK4BHJetLinked
        (nativeGK4ADCombine path.gk4adValue edge.gk4adValue)
        (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial)
      exact nativeGK4BHJetLinked_mul _ _ _ _ ih (nativeGK4BHJet_edge edge)

/-- Every REAL original F54 route constructor, including genuine
double-Nat casts and both original dependent contexts. -/
theorem nativeGK4BHJet_route
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4BHJetLinked route.gk4adValue route.gk4avPolynomial := by
  induction route with
  | chain path => exact nativeGK4BHJet_chain path
  | castDepths _ _ _ => exact nativeGK4BHJetLinked_cast
  | trans u v ihU ihV =>
      change nativeGK4BHJetLinked
        (nativeGK4ADCombine u.gk4adValue v.gk4adValue)
        (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial)
      exact nativeGK4BHJetLinked_mul _ _ _ _ ihU ihV
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

/-- The ENTIRE original ordered GK4AD history is forced by the
coefficients of its full GK4AV polynomial, not just its charge. -/
theorem nativeGK4BHAD_eq_of_polynomial_eq
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hP : u.gk4avPolynomial = v.gk4avPolynomial) :
    u.gk4adValue = v.gk4adValue := by
  obtain ⟨_, huc, _, _, hum, hub⟩ := nativeGK4BHJet_route u
  obtain ⟨_, hvc, _, _, hvm, hvb⟩ := nativeGK4BHJet_route v
  apply Prod.ext
  · apply Prod.ext
    · exact huc.symm.trans
        ((congrArg (fun M : NativeGK4AVValue => M.1.2.coeff 0) hP).trans hvc)
    · have hb : (u.gk4adValue.1.2 : Int) =
          (v.gk4adValue.1.2 : Int) :=
        hub.symm.trans
          ((congrArg (fun M : NativeGK4AVValue => M.2.1.coeff 1) hP).trans hvb)
      exact_mod_cast hb
  · exact hum.symm.trans
      ((congrArg (fun M : NativeGK4AVValue => M.1.1.coeff 1) hP).trans hvm)

/-- GK4BA's full-original free-product one-point determinacy now
forces ALSO the old ordered noncommutative AD history. -/
theorem nativeGK4BHRoute_AH_determines_AD
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hAH : u.gk4ahMatrix = v.gk4ahMatrix) :
    u.gk4adValue = v.gk4adValue :=
  nativeGK4BHAD_eq_of_polynomial_eq u v
    (nativeGK4BARoute_AH_determines u v hAH)

end ActualOriginalF54

section ActualKAIKernel
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Complete original GK4AD ordered data is AH-determined on the
EXISTING second-kernel K_AI, not only on the raw F54 source. -/
theorem nativeGK4BHKernel_AH_determines_AD
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (hAH : (nativeGK4AIKernelValue first last u).2 =
      (nativeGK4AIKernelValue first last v).2) :
    (nativeGK4AIKernelValue first last u).1.1.2 =
      (nativeGK4AIKernelValue first last v).1.1.2 := by
  revert hAH
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r hAH
  revert hAH
  refine _root_.Quotient.inductionOn₂ q r ?_
  intro rawU rawV hAH
  change rawU.gk4ahMatrix = rawV.gk4ahMatrix at hAH
  change rawU.gk4adValue = rawV.gk4adValue
  exact nativeGK4BHRoute_AH_determines_AD rawU rawV hAH

end ActualKAIKernel

#print axioms nativeGK4BHJetLinked
#print axioms nativeGK4BHJetLinked_mul
#print axioms nativeGK4BHJetLinked_one
#print axioms nativeGK4BHJetLinked_cast
#print axioms nativeGK4BHJetLinked_forward
#print axioms nativeGK4BHJetLinked_backward
#print axioms nativeGK4BHJet_edge
#print axioms nativeGK4BHJet_chain
#print axioms nativeGK4BHJet_route
#print axioms nativeGK4BHAD_eq_of_polynomial_eq
#print axioms nativeGK4BHRoute_AH_determines_AD
#print axioms nativeGK4BHKernel_AH_determines_AD

end
end Kuu.F112.Physical
