import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AKParametricPhysicalWords
import Mathlib.Tactic

/-!
F112-P94D3GK4AK — arbitrary finite lower bounds for genuine
attained K_AI -> K_AG fibers. For every k construct an actual
old class q_k and an embedding Fin(k+1) into its SAME typed fiber.
The witnesses are original F54 W(j,k-j)=B^(6j) C B^(12(k-j)) C B^(6j),
not abstract observer tuples or invented Type-valued source cells.
The linear second-matrix decoder 8-192*(k-j) recovers the index.
The old target itself is attained, with O_AE=(decide(k=0),2-24k,
12k,12k-144k^2) and M_AF=C^2. Different k give different old targets.
Hence fiber sizes have no uniform finite upper bound; NO single
fixed fiber is asserted infinite, and S->K_AI global faithfulness
is neither assumed nor established. No Q category axioms, Gray,
historical full equivalence, fillers or hyperdescent.
Append-only/same-root107; strict 空 central; independent Kuu one
presentation; protected PR #1558 Draft/open/unmerged.
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

section GenuineFiniteFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Actual independent structural S classes, retaining original source. -/
def nativeGK4AKStructuralFamily (k : Nat) (i : Fin (k + 1)) :
    NativeGK4EStructuralRouteClasses before before :=
  nativeGK4EStructuralRouteClass before before
    (nativeGK4AKWord rot i.val (k - i.val))

/-- The real comparison into the genuine SECOND K_AI quotient. -/
def nativeGK4AKClass (k : Nat) (i : Fin (k + 1)) :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before (nativeGK4AKStructuralFamily rot k i)

/-- The old target is ATTAINED by a genuine original F54 route. -/
def nativeGK4AKOldTarget (k : Nat) :
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) before before :=
  nativeGK4AGComparison before before
    (nativeGK4EStructuralRouteClass before before (nativeGK4AKWord rot 0 k))

/-- All k+1 classes have one and the SAME true old K_AG target. -/
theorem nativeGK4AKClass_forget (k : Nat) (i : Fin (k + 1)) :
    nativeGK4AIForgetMatrix before before (nativeGK4AKClass rot k i) =
      nativeGK4AKOldTarget rot k := by
  change nativeGK4AIForgetMatrix before before
      (nativeGK4AIComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4AKWord rot i.val (k - i.val)))) =
    nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AKWord rot 0 k))
  rw [nativeGK4AIForgetMatrix_comparison]
  apply (nativeGK4AGComparison_eq_iff before before _ _).mpr
  have hi := i.isLt
  have hsum : i.val + (k - i.val) = k := by omega
  simp only [nativeGK4AKWord_oldValue, hsum, Nat.zero_add]

/-- Exact decoder from a genuinely attained K_AI class. -/
theorem nativeGK4AKClass_decoder (k : Nat) (i : Fin (k + 1)) :
    nativeGK4AKDecoder
        (nativeGK4AIKernelValue before before (nativeGK4AKClass rot k i)).2 =
      8 - 192 * ((k - i.val : Nat) : Int) := by
  change nativeGK4AKDecoder
    (nativeGK4AKWord rot i.val (k - i.val)).gk4ahMatrix = _
  exact nativeGK4AKWord_decoder rot i.val (k - i.val)

/-- Index recovery proves pairwise separation for ALL finite k,
not just a computed finite sample of words or matrices. -/
theorem nativeGK4AKClass_injective (k : Nat) :
    Function.Injective (nativeGK4AKClass rot k) := by
  intro i j h
  have hm := congrArg
    (fun z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before =>
      nativeGK4AKDecoder (nativeGK4AIKernelValue before before z).2) h
  change nativeGK4AKDecoder
      (nativeGK4AIKernelValue before before (nativeGK4AKClass rot k i)).2 =
    nativeGK4AKDecoder
      (nativeGK4AIKernelValue before before (nativeGK4AKClass rot k j)).2 at hm
  rw [nativeGK4AKClass_decoder rot k i, nativeGK4AKClass_decoder rot k j] at hm
  apply Fin.ext
  have hi := i.isLt
  have hj := j.isLt
  omega

/-- The actual original independent S classes are distinct as well.
This is restricted to the constructed family, not global faithfulness. -/
theorem nativeGK4AKStructuralFamily_injective (k : Nat) :
    Function.Injective (nativeGK4AKStructuralFamily rot k) := by
  intro i j h
  apply nativeGK4AKClass_injective rot k
  exact congrArg (nativeGK4AIComparison before before) h

/-- Genuine elements of the original typed fiber over the fixed q_k. -/
def nativeGK4AKFiberPoint (k : Nat) (i : Fin (k + 1)) :
    nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) :=
  ⟨nativeGK4AKClass rot k i, nativeGK4AKClass_forget rot k i⟩

/-- MAIN CONSTRUCTION: Fin(k+1) embeds into one genuinely attained
K_AI->K_AG fiber. The target depends on k, not on the finite index. -/
def nativeGK4AKFiberEmbedding (k : Nat) :
    Fin (k + 1) ↪ nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) where
  toFun := nativeGK4AKFiberPoint rot k
  inj' := by
    intro i j h
    exact nativeGK4AKClass_injective rot k (congrArg Subtype.val h)

/-- Explicit old observed target: the positive k case has false grade,
while k=0 is the honest zero-rotation two-cast word. -/
theorem nativeGK4AKOldTarget_value (k : Nat) :
    nativeGK4AGKernelValue before before (nativeGK4AKOldTarget rot k) =
      nativeGK4AKOldValue k := by
  change nativeGK4AGKernelValue before before
    (nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AKWord rot 0 k))) = _
  rw [nativeGK4AGComparison_value]
  simpa only [Nat.zero_add] using (nativeGK4AKWord_oldValue rot 0 k)

/-- Different k use different old targets; unbounded finite lower
bounds do not assert infinitude of any one fixed fiber. -/
theorem nativeGK4AKOldTarget_injective :
    Function.Injective (nativeGK4AKOldTarget rot) := by
  intro k l h
  have hv := congrArg
    (fun q : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) before before =>
      (nativeGK4AGKernelValue before before q).1.2.1.2) h
  change (nativeGK4AGKernelValue before before (nativeGK4AKOldTarget rot k)).1.2.1.2 =
    (nativeGK4AGKernelValue before before (nativeGK4AKOldTarget rot l)).1.2.1.2 at hv
  rw [nativeGK4AKOldTarget_value rot k, nativeGK4AKOldTarget_value rot l] at hv
  change 12 * k = 12 * l at hv
  omega

/-- Every finite lower bound is realized by a true fixed attained fiber.
The genuine LocalRotation hypothesis is explicit, never silently dropped. -/
theorem nativeGK4AK_arbitrary_finite_fiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) before before,
      Nonempty (Fin (k + 1) ↪ nativeGK4AJOldFiber before before q) := by
  exact ⟨nativeGK4AKOldTarget rot k, ⟨nativeGK4AKFiberEmbedding rot k⟩⟩

end GenuineFiniteFibers

/-- Actual C60 north, for EVERY k: no synthetic local source generator. -/
theorem nativeGK4AKPhysicalNorth_arbitrary_finite_fiber (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      Nonempty (Fin (k + 1) ↪ nativeGK4AJOldFiber
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) := by
  exact nativeGK4AK_arbitrary_finite_fiber northHexagonNativeLeftRotation k

#print axioms nativeGK4AKStructuralFamily
#print axioms nativeGK4AKClass
#print axioms nativeGK4AKOldTarget
#print axioms nativeGK4AKClass_forget
#print axioms nativeGK4AKClass_decoder
#print axioms nativeGK4AKClass_injective
#print axioms nativeGK4AKStructuralFamily_injective
#print axioms nativeGK4AKFiberPoint
#print axioms nativeGK4AKFiberEmbedding
#print axioms nativeGK4AKOldTarget_value
#print axioms nativeGK4AKOldTarget_injective
#print axioms nativeGK4AK_arbitrary_finite_fiber
#print axioms nativeGK4AKPhysicalNorth_arbitrary_finite_fiber

end
end Kuu.F112.Physical
