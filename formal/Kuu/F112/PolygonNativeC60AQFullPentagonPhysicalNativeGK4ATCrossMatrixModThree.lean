import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ASForcedLowerDiagonal
import Mathlib.Data.Int.ModEq
import Mathlib.Tactic

/-!
F112-P94D3GK4AT — a NEW compatibility between two EXISTING genuine
noncommutative source observations: M_AF(r) = M_AH(r) entrywise mod3.
The actual C and F matrices agree exactly; the backward generators
have lower-left entries 1 and 4, which agree mod3. Use the pinned
Mathlib Int.ModEq addition/multiplication laws, then inspect the real
F54 RotationEdge/RotationChain and all five DepthRotationRoute
constructors. Descend separately to original P92B Q and independent
structural S, genuine K_AI and EVERY fixed old K_AG fiber.

The old K_AG target retains the WHOLE AF matrix, not merely AD data.
Thus this uses previously retained information without adding any
source generator or fabricating a Type-valued comparison cell.
The following module proves this condition is independent of AS/AR.
No original Q category laws, fixed infinite fiber, all-slice
reachability, Gray, global strict or hyperdescent asserted.
Append-only/tighten-only/same-root107; strict empty presentation
central, independent Kuu one presentation; protect #1558 unmerged.
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

/-- All FOUR entries of the original AF and AH matrix observations
agree modulo three. Both matrices are still kept as integers. -/
def nativeGK4ATModThree (P : NativeGK4AFMatrix)
    (M : NativeGK4AHMatrix) : Prop :=
  Int.ModEq 3 P.1.1 M.1.1 ∧ Int.ModEq 3 P.1.2 M.1.2 ∧
  Int.ModEq 3 P.2.1 M.2.1 ∧ Int.ModEq 3 P.2.2 M.2.2

/-- Compatibility with the two REAL ordered matrix products.
No commuting or reordering of original Type-valued histories. -/
theorem nativeGK4ATModThree_mul
    (P Q : NativeGK4AFMatrix) (A B : NativeGK4AHMatrix)
    (hA : nativeGK4ATModThree P A)
    (hB : nativeGK4ATModThree Q B) :
    nativeGK4ATModThree (nativeGK4AFMul P Q) (nativeGK4AHMul A B) := by
  rcases hA with ⟨ha, hb, hc, hd⟩
  rcases hB with ⟨he, hf, hg, hh⟩
  exact ⟨(ha.mul he).add (hb.mul hg), (ha.mul hf).add (hb.mul hh),
    (hc.mul he).add (hd.mul hg), (hc.mul hf).add (hd.mul hh)⟩

theorem nativeGK4ATModThree_one :
    nativeGK4ATModThree nativeGK4AFOne nativeGK4AHOne := by decide

theorem nativeGK4ATModThree_cast :
    nativeGK4ATModThree nativeGK4AFCast nativeGK4AHCast := by decide

theorem nativeGK4ATModThree_forward :
    nativeGK4ATModThree nativeGK4AFForward nativeGK4AHForward := by decide

/-- The essential original-generator compatibility: 1 = 4 mod3. -/
theorem nativeGK4ATModThree_backward :
    nativeGK4ATModThree nativeGK4AFBackward nativeGK4AHBackward := by decide

section GenuineOriginalDependentSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4ATEdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4ATModThree edge.gk4afMatrix edge.gk4ahMatrix := by
  cases edge with
  | forward _ => exact nativeGK4ATModThree_forward
  | backward _ => exact nativeGK4ATModThree_backward

theorem nativeGK4ATChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4ATModThree chain.gk4afMatrix chain.gk4ahMatrix := by
  induction chain with
  | refl => exact nativeGK4ATModThree_one
  | snoc path edge ih =>
      exact nativeGK4ATModThree_mul _ _ _ _ ih (nativeGK4ATEdge_sound edge)

/-- All original five dependent route constructors, not abstract
untyped words or freely chosen matrix pairs. -/
theorem nativeGK4ATRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4ATModThree route.gk4afMatrix route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4ATChain_sound path
  | castDepths _ _ _ => exact nativeGK4ATModThree_cast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4ATModThree_mul _ _ _ _ ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end GenuineOriginalDependentSource

section GenuineQuotientsAndFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Original Q descent uses the PREVIOUSLY certified original
F55/P92B soundness of each observer; no reverse inference to cells. -/
theorem nativeGK4ATP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4ATModThree (nativeGK4AFP92Value first last q)
      (nativeGK4AHP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4ATModThree raw.gk4afMatrix raw.gk4ahMatrix
  exact nativeGK4ATRoute_sound raw

/-- Independent structural S descent retains its own real seams. -/
theorem nativeGK4ATStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4ATModThree (nativeGK4AFStructuralValue first last s)
      (nativeGK4AHStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change nativeGK4ATModThree raw.gk4afMatrix raw.gk4ahMatrix
  exact nativeGK4ATRoute_sound raw

/-- Two genuine matrix components of the actual K_AI observer. -/
theorem nativeGK4ATKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4ATModThree ((nativeGK4AIKernelValue first last z).1.2)
      ((nativeGK4AIKernelValue first last z).2) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4ATModThree (nativeGK4AFP92Value first last q)
    (nativeGK4AHP92Value first last q)
  exact nativeGK4ATP92_sound first last q

/-- Fixing the old K_AG class fixes the old AF WHOLE matrix, hence
fixes all four residues of the AH matrix modulo three. -/
theorem nativeGK4ATFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4ATModThree ((nativeGK4AGKernelValue first last target).2)
      (nativeGK4AJFiberMatrix first last target z) := by
  have hz := nativeGK4ATKernel_sound first last z.1
  have hvalue := nativeGK4AIForgetMatrix_value first last z.1
  rw [z.2] at hvalue
  have hAF := congrArg (fun value : NativeGK4AGValue => value.2) hvalue
  change (nativeGK4AGKernelValue first last target).2 =
    (nativeGK4AIKernelValue first last z.1).1.2 at hAF
  change nativeGK4ATModThree ((nativeGK4AGKernelValue first last target).2)
    ((nativeGK4AIKernelValue first last z.1).2)
  rw [hAF]
  exact hz

end GenuineQuotientsAndFibers

#print axioms nativeGK4ATModThree
#print axioms nativeGK4ATModThree_mul
#print axioms nativeGK4ATModThree_one
#print axioms nativeGK4ATModThree_cast
#print axioms nativeGK4ATModThree_forward
#print axioms nativeGK4ATModThree_backward
#print axioms nativeGK4ATEdge_sound
#print axioms nativeGK4ATChain_sound
#print axioms nativeGK4ATRoute_sound
#print axioms nativeGK4ATP92_sound
#print axioms nativeGK4ATStructural_sound
#print axioms nativeGK4ATKernel_sound
#print axioms nativeGK4ATFiber_sound

end
end Kuu.F112.Physical
