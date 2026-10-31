import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4APFixedFiberArithmeticSlice
import Mathlib.Tactic

/-!
F112-P94D3GK4AQ — a STRICT NEW lower-left congruence of the actual
second GK4AH matrix linked to ORIGINAL F54 backwardCount:
  M_AH(r).2.1 = 4 * backwardCount_AD(r) + 16 * t.
This does not follow from the bare Gamma_1(4) condition, and unlike
an abstract matrix constraint it is grounded in real fully dependent
F54 RotationEdge/RotationChain/all FIVE DepthRotationRoute constructors.

The combined invariant RETAINS the previously proven GK4AP
charge+backwardCount upper-right residue and full GK4AO det=1 and
Gamma_1(4) diagonal/lower-left congruences. Multiplication respects
the original noncommutative AD and AH products. Descend to the true
original P92B Q and independently presented structural S, then the
attained K_AI quotient and EVERY fixed old K_AG forgetful fiber.
Original F55 9, P92B 9, structural seams 14, extended comparison 3
Type-valued witnesses are inherited via their previously proven
observer soundness. Never infer a Type-valued source 3-cell from an
observed numerical equality. No Q category axioms, global faithfulness,
fixed infinite fiber, Gray or hyperdescent.
Append-only/tighten-only/same-root107, strict 空 central, independent
Kuu one presentation. Protect PR #1558 Draft/OPEN/unmerged.
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

/-- New linkage of OLD backwardCount and the exact second integer
matrix's lower-left entry modulo 16. The full AP invariant stays. -/
def nativeGK4AQLowerLinked (v : NativeGK4ADValue)
    (M : NativeGK4AHMatrix) : Prop :=
  nativeGK4APLinked v M ∧
  ∃ t : Int, M.2.1 = 4 * (v.1.2 : Int) + 16 * t

/-- True noncommutative multiplication preserves BOTH old-charge
upper-right mod 4 and the stronger lower-left mod 16 condition.
The lower-left equation uses B_11=1 mod4 and A_22=1 mod4 from
the genuine prior GK4AO source proof, not unverified matrix APIs. -/
theorem nativeGK4AQLowerLinked_mul
    (u v : NativeGK4ADValue) (A B : NativeGK4AHMatrix)
    (hu : nativeGK4AQLowerLinked u A)
    (hv : nativeGK4AQLowerLinked v B) :
    nativeGK4AQLowerLinked (nativeGK4ADCombine u v)
      (nativeGK4AHMul A B) := by
  refine ⟨nativeGK4APLinked_mul u v A B hu.1 hv.1, ?_⟩
  rcases hu with ⟨hapu, ⟨tu, htu⟩⟩
  rcases hv with ⟨hapv, ⟨tv, htv⟩⟩
  rcases hapu.1 with ⟨_, _, _, ⟨du, hdu⟩⟩
  rcases hapv.1 with ⟨_, ⟨av, hav⟩, _, _⟩
  refine ⟨tu + tv + (u.1.2 : Int) * av + du * (v.1.2 : Int) +
    4 * (tu * av + du * tv), ?_⟩
  change A.2.1 * B.1.1 + A.2.2 * B.2.1 =
    4 * ((u.1.2 + v.1.2 : Nat) : Int) +
    16 * (tu + tv + (u.1.2 : Int) * av + du * (v.1.2 : Int) +
      4 * (tu * av + du * tv))
  rw [htu, htv, hdu, hav]
  push_cast
  ring

theorem nativeGK4AQLowerLinked_one :
    nativeGK4AQLowerLinked nativeGK4ADZero nativeGK4AHOne := by
  refine ⟨nativeGK4APLinked_one, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4AQLowerLinked_cast :
    nativeGK4AQLowerLinked nativeGK4ADCast nativeGK4AHCast := by
  refine ⟨nativeGK4APLinked_cast, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4AQLowerLinked_forward :
    nativeGK4AQLowerLinked nativeGK4ADForward nativeGK4AHForward := by
  refine ⟨nativeGK4APLinked_forward, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4AQLowerLinked_backward :
    nativeGK4AQLowerLinked nativeGK4ADBackward nativeGK4AHBackward := by
  refine ⟨nativeGK4APLinked_backward, ⟨0, ?_⟩⟩
  decide

section OriginalTypedF54
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- A real oriented original F54 Type-valued rotation edge. -/
theorem nativeGK4AQEdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4AQLowerLinked edge.gk4adValue edge.gk4ahMatrix := by
  cases edge with
  | forward _ => exact nativeGK4AQLowerLinked_forward
  | backward _ => exact nativeGK4AQLowerLinked_backward

/-- Original intermediate-tree dependent F54 rotation chain, including
its zero-edge constructor. No abstract untyped word is substituted. -/
theorem nativeGK4AQChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4AQLowerLinked chain.gk4adValue chain.gk4ahMatrix := by
  induction chain with
  | refl => exact nativeGK4AQLowerLinked_one
  | snoc path edge ih =>
      change nativeGK4AQLowerLinked
        (nativeGK4ADCombine path.gk4adValue edge.gk4adValue)
        (nativeGK4AHMul path.gk4ahMatrix edge.gk4ahMatrix)
      exact nativeGK4AQLowerLinked_mul _ _ _ _
        ih (nativeGK4AQEdge_sound edge)

/-- All FIVE genuinely typed original F54 route constructors, with
no quotient category or guessed source comparison used. -/
theorem nativeGK4AQRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4AQLowerLinked route.gk4adValue route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4AQChain_sound path
  | castDepths _ _ _ => exact nativeGK4AQLowerLinked_cast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4AQLowerLinked_mul _ _ _ _ ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end OriginalTypedF54

section ActualOriginalQuotientsAndFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Actual original P92B proof-existence quotient. All nine genuine
F55 and P92B Type-valued comparisons are inherited from GK4AD/AH. -/
theorem nativeGK4AQP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AQLowerLinked (nativeGK4ADP92Value first last q)
      (nativeGK4AHP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4AQLowerLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4AQRoute_sound raw

/-- Independently generated structural S: fourteen original seams
already independently certified, NOT a synthetic P92B 3-cell. -/
theorem nativeGK4AQStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AQLowerLinked (nativeGK4ADStructuralValue first last s)
      (nativeGK4AHStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change nativeGK4AQLowerLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4AQRoute_sound raw

/-- Second quotient K_AI, constructed from the original Q and actual
observer image, not arbitrary freely chosen integer matrices. -/
theorem nativeGK4AQKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4AQLowerLinked
      ((nativeGK4AIKernelValue first last z).1.1.2)
      ((nativeGK4AIKernelValue first last z).2) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4AQLowerLinked
    (nativeGK4ADP92Value first last q)
    (nativeGK4AHP92Value first last q)
  exact nativeGK4AQP92_sound first last q

/-- Every REAL dependent fiber over any fixed old K_AG target q has
one common lower-left residue modulo 16, forced by backwardCount(q). -/
theorem nativeGK4AQFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4AQLowerLinked
      ((nativeGK4AGKernelValue first last target).1.2)
      (nativeGK4AJFiberMatrix first last target z) := by
  have hz := nativeGK4AQKernel_sound first last z.1
  have hvalue := nativeGK4AIForgetMatrix_value first last z.1
  rw [z.2] at hvalue
  have hAD := congrArg
    (fun value : NativeGK4AGValue => value.1.2) hvalue
  change (nativeGK4AGKernelValue first last target).1.2 =
    (nativeGK4AIKernelValue first last z.1).1.1.2 at hAD
  change nativeGK4AQLowerLinked
    ((nativeGK4AGKernelValue first last target).1.2)
    ((nativeGK4AIKernelValue first last z.1).2)
  rw [hAD]
  exact hz

#print axioms nativeGK4AQLowerLinked
#print axioms nativeGK4AQLowerLinked_mul
#print axioms nativeGK4AQLowerLinked_one
#print axioms nativeGK4AQLowerLinked_cast
#print axioms nativeGK4AQLowerLinked_forward
#print axioms nativeGK4AQLowerLinked_backward
#print axioms nativeGK4AQEdge_sound
#print axioms nativeGK4AQChain_sound
#print axioms nativeGK4AQRoute_sound
#print axioms nativeGK4AQP92_sound
#print axioms nativeGK4AQStructural_sound
#print axioms nativeGK4AQKernel_sound
#print axioms nativeGK4AQFiber_sound

end ActualOriginalQuotientsAndFiber

end
end Kuu.F112.Physical
