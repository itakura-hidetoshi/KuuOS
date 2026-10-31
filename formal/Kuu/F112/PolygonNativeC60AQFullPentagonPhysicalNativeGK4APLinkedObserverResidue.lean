import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AORestrictedMatrixImage
import Mathlib.Tactic

/-!
F112-P94D3GK4AP — a NEW cross-observer arithmetic compatibility
condition inside the actual Γ₁(4) second-matrix image:
  M_AH(r).1.2 = charge_AD(r) + backwardCount_AD(r) + 4*t.
The old GK4AD charge and backwardCount are the REAL original F54
ordered Type-valued observations; unlike a standalone matrix modulus,
this congruence fixes the residue of M_AH's upper-right entry
as soon as the OLD K_AG target q is fixed.

We verify all genuine original F54 edge/chain/five route constructors,
the actual P92B quotient, independently generated structural S, true
attained second quotient K_AI, and every dependent forgetful fiber.
The multiplicative law uses the exact noncommutative GK4ADCombine and
GK4AH matrix multiplication, plus already-proved GK4AO diagonal
congruences. The original F55 9/P92B 9/seam 14/extended 3 Type-valued
soundness witnesses are inherited, NOT manufactured by equality.
No global S faithfulness, no fixed infinite fiber, no false Γ₁(4)
surjectivity, no Q category laws, Gray or hyperdescent.
Append-only/tighten-only/same-root107, strict 空 central, independent
Kuu one presentation, protected PR #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, pinned mathlib
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

/-- The old GK4AD measured total charge plus genuine backwardCount.
The cast to Int is necessary: count belongs to Nat, charge to Int. -/
def nativeGK4APOldUpperResidue (v : NativeGK4ADValue) : Int :=
  v.1.1 + (v.1.2 : Int)

/-- The NEW exact compatibility between two already sound original
observers. Full Gamma_1(4) arithmetic is retained, not weakened. -/
def nativeGK4APLinked (v : NativeGK4ADValue)
    (M : NativeGK4AHMatrix) : Prop :=
  nativeGK4AOIntegralCongruence M ∧
  ∃ t : Int, M.1.2 = nativeGK4APOldUpperResidue v + 4 * t

/-- Both original observers are compatible under their exact
NONCOMMUTATIVE products, not a fictional commutative word-count. -/
theorem nativeGK4APLinked_mul
    (u v : NativeGK4ADValue) (A B : NativeGK4AHMatrix)
    (hu : nativeGK4APLinked u A)
    (hv : nativeGK4APLinked v B) :
    nativeGK4APLinked (nativeGK4ADCombine u v)
      (nativeGK4AHMul A B) := by
  refine ⟨nativeGK4AOIntegralCongruence_mul A B hu.1 hv.1, ?_⟩
  rcases hu with ⟨⟨_, ⟨au, hau⟩, _, _⟩, ⟨tu, htu⟩⟩
  rcases hv with ⟨⟨_, _, _, ⟨dv, hdv⟩⟩, ⟨tv, htv⟩⟩
  refine ⟨tu + tv + au * B.1.2 + A.1.2 * dv, ?_⟩
  change A.1.1 * B.1.2 + A.1.2 * B.2.2 =
    (u.1.1 + v.1.1) + (((u.1.2 + v.1.2 : Nat) : Int)) +
      4 * (tu + tv + au * B.1.2 + A.1.2 * dv)
  rw [hau, hdv, htu, htv]
  push_cast
  ring

theorem nativeGK4APLinked_one :
    nativeGK4APLinked nativeGK4ADZero nativeGK4AHOne := by
  refine ⟨nativeGK4AOIntegralCongruence_one, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4APLinked_cast :
    nativeGK4APLinked nativeGK4ADCast nativeGK4AHCast := by
  refine ⟨nativeGK4AOIntegralCongruence_cast, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4APLinked_forward :
    nativeGK4APLinked nativeGK4ADForward nativeGK4AHForward := by
  refine ⟨nativeGK4AOIntegralCongruence_forward, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4APLinked_backward :
    nativeGK4APLinked nativeGK4ADBackward nativeGK4AHBackward := by
  refine ⟨nativeGK4AOIntegralCongruence_backward, ⟨0, ?_⟩⟩
  decide

section OriginalTypedF54
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- An actual original dependent LocalRotation forward/backward edge. -/
theorem nativeGK4APEdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4APLinked edge.gk4adValue edge.gk4ahMatrix := by
  cases edge with
  | forward _ => exact nativeGK4APLinked_forward
  | backward _ => exact nativeGK4APLinked_backward

/-- Original intermediate-tree-dependent true rotation chain. -/
theorem nativeGK4APChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4APLinked chain.gk4adValue chain.gk4ahMatrix := by
  induction chain with
  | refl => exact nativeGK4APLinked_one
  | snoc path edge ih =>
      change nativeGK4APLinked
        (nativeGK4ADCombine path.gk4adValue edge.gk4adValue)
        (nativeGK4AHMul path.gk4ahMatrix edge.gk4ahMatrix)
      exact nativeGK4APLinked_mul _ _ _ _
        ih (nativeGK4APEdge_sound edge)

/-- The REAL original F54 DepthRotationRoute: all FIVE constructors
preserve BOTH old AD and second AH arithmetic linkage. -/
theorem nativeGK4APRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4APLinked route.gk4adValue route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4APChain_sound path
  | castDepths _ _ _ => exact nativeGK4APLinked_cast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4APLinked_mul _ _ _ _ ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end OriginalTypedF54

section OriginalQuotientsAndKernel
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Original P92B existence quotient Q with its TRUE F55/P92B cells.
Do not infer a new comparison from congruence alone. -/
theorem nativeGK4APP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4APLinked (nativeGK4ADP92Value first last q)
      (nativeGK4AHP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4APLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4APRoute_sound raw

/-- Original independently presented structural S uses its OWN
actual real Type-valued seam comparisons, no Q category laws. -/
theorem nativeGK4APStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4APLinked (nativeGK4ADStructuralValue first last s)
      (nativeGK4AHStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change nativeGK4APLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4APRoute_sound raw

/-- The TRUE attained K_AI quotient simultaneously remembers the
old charge/backwardCount and the new matrix upper-right residue. -/
theorem nativeGK4APKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4APLinked
      ((nativeGK4AIKernelValue first last z).1.1.2)
      ((nativeGK4AIKernelValue first last z).2) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4APLinked
    (nativeGK4ADP92Value first last q)
    (nativeGK4AHP92Value first last q)
  exact nativeGK4APP92_sound first last q

/-- For an ACTUAL fixed old K_AG target q the residue is fixed by
the old class q, not merely by a raw F54 route chosen ad hoc. -/
theorem nativeGK4APFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4APLinked
      ((nativeGK4AGKernelValue first last target).1.2)
      (nativeGK4AJFiberMatrix first last target z) := by
  have hz := nativeGK4APKernel_sound first last z.1
  have hvalue := nativeGK4AIForgetMatrix_value first last z.1
  rw [z.2] at hvalue
  have hcharge := congrArg
    (fun v : NativeGK4AGValue => v.1.2) hvalue
  change nativeGK4APLinked
    ((nativeGK4AGKernelValue first last target).1.2)
    ((nativeGK4AIKernelValue first last z.1).2)
  rw [hcharge]
  exact hz

#print axioms nativeGK4APOldUpperResidue
#print axioms nativeGK4APLinked
#print axioms nativeGK4APLinked_mul
#print axioms nativeGK4APLinked_one
#print axioms nativeGK4APLinked_cast
#print axioms nativeGK4APLinked_forward
#print axioms nativeGK4APLinked_backward
#print axioms nativeGK4APEdge_sound
#print axioms nativeGK4APChain_sound
#print axioms nativeGK4APRoute_sound
#print axioms nativeGK4APP92_sound
#print axioms nativeGK4APStructural_sound
#print axioms nativeGK4APKernel_sound
#print axioms nativeGK4APFiber_sound

end OriginalQuotientsAndKernel

end
end Kuu.F112.Physical
