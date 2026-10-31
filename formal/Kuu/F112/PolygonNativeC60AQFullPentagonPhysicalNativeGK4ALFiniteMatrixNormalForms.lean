import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALCountableFibers
import Mathlib.Tactic

/-!
F112-P94D3GK4AL — exact and limited finite-family matrix codes
for the original F54 words W_k(j)=B^(6j);C;B^(12(k-j));C;B^(6j).
There are k+1 genuinely distinct second matrices inside one
attained q_k fiber, and every such fiber is countable.
A k-indexed family exhausts its entire fiber IFF its matrix
codes cover all attained matrices there. The consequent finite
normal form is strictly conditional: coverage is NOT assumed.
No assertion of fixed infinite fiber, exact cardinality of all
q_k fibers, global faithfulness of S -> K_AI or arbitrary matrix
attainability. Original Q is not presumed to be a category.
Append-only and same-root107. Strict 空 central. Gray not restored.
Protected Lean-4.31 validation-only PR #1558 remains unmerged.
Pinned Lean v4.30.0-rc2 / mathlib
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

section GenuineFiniteMatrixFamilies
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The attained second matrix of the i-th true source path in
the fixed old K_AG fiber of the previously established q_k. -/
def nativeGK4ALFiniteFamilyMatrix (k : Nat) (i : Fin (k + 1)) :
    NativeGK4AHMatrix :=
  nativeGK4AJFiberMatrix before before (nativeGK4AKOldTarget rot k)
    (nativeGK4AKFiberPoint rot k i)

/-- Exact integer decoder for each attained finite-family matrix.
It recovers k-i; the full proof is already in original F54 words. -/
theorem nativeGK4ALFiniteFamilyMatrix_decoder (k : Nat)
    (i : Fin (k + 1)) :
    nativeGK4AKDecoder (nativeGK4ALFiniteFamilyMatrix rot k i) =
      8 - 192 * ((k - i.val : Nat) : Int) :=
  nativeGK4AKClass_decoder rot k i

/-- Explicit honest matrix injection of Fin(k+1), not a numeric
enumeration or a claimed exhaustive normal form. -/
def nativeGK4ALFiniteFamilyMatrixEmbedding (k : Nat) :
    Fin (k + 1) ↪ NativeGK4AHMatrix where
  toFun := nativeGK4ALFiniteFamilyMatrix rot k
  inj' := by
    intro i j hij
    apply (nativeGK4AKFiberEmbedding rot k).injective
    apply nativeGK4AJFiberMatrix_injective before before
      (nativeGK4AKOldTarget rot k)
    exact hij

/-- The specifically constructed k+1 attained matrix values are
equivalent to the original finite index set, with no surjectivity
claim onto all attained matrices above q_k. -/
def nativeGK4ALFiniteFamilyMatrixNormalForm (k : Nat) :
    Fin (k + 1) ≃
      {M : NativeGK4AHMatrix //
        M ∈ Set.range (nativeGK4ALFiniteFamilyMatrix rot k)} :=
  Equiv.ofBijective
    (fun i => ⟨nativeGK4ALFiniteFamilyMatrix rot k i, ⟨i, rfl⟩⟩)
    ⟨(by
       intro i j hij
       exact (nativeGK4ALFiniteFamilyMatrixEmbedding rot k).injective
         (congrArg Subtype.val hij)),
     (by
       rintro ⟨M, ⟨i, hi⟩⟩
       exact ⟨i, Subtype.ext hi⟩)⟩

/-- Stronger *extra* property not established by the main theorem:
that the explicitly constructed source family fills the whole
actual K_AI -> K_AG dependent fiber above q_k. -/
def nativeGK4ALFamilyCovers (k : Nat) : Prop :=
  Function.Surjective (nativeGK4AKFiberPoint rot k)

/-- The precise obstruction to a complete finite normal form:
coverage by physical source words is EQUIVALENT to coverage by
their actual attained second matrices. Faithful fiber coding is
the only ingredient; coverage itself is NOT inferred. -/
theorem nativeGK4ALFamilyCovers_iff_matrixCover (k : Nat) :
    nativeGK4ALFamilyCovers rot k ↔
      ∀ z : nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k),
        ∃ i : Fin (k + 1),
          nativeGK4AJFiberMatrix before before
              (nativeGK4AKOldTarget rot k) z =
            nativeGK4ALFiniteFamilyMatrix rot k i := by
  constructor
  · intro h z
    obtain ⟨i, hi⟩ := h z
    refine ⟨i, ?_⟩
    change nativeGK4AJFiberMatrix before before
      (nativeGK4AKOldTarget rot k) z =
      nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4AKFiberPoint rot k i)
    rw [hi]
  · intro h z
    obtain ⟨i, hi⟩ := h z
    refine ⟨i, ?_⟩
    apply nativeGK4AJFiberMatrix_injective before before
      (nativeGK4AKOldTarget rot k)
    exact hi.symm

/-- CONDITIONAL exact finite normal form of the entire actual
fiber, available only after a future proof of its full coverage. -/
def nativeGK4ALExactFiniteFiberEquivOfCover (k : Nat)
    (h : nativeGK4ALFamilyCovers rot k) :
    Fin (k + 1) ≃
      nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) :=
  Equiv.ofBijective (nativeGK4AKFiberPoint rot k)
    ⟨(nativeGK4AKFiberEmbedding rot k).injective, h⟩

/-- For every k, the very same truly attained fiber has k+1
distinct classes AND is countable, simultaneously. -/
theorem nativeGK4AL_arbitrary_finite_countable_fiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E)
        before before,
      Countable (nativeGK4AJOldFiber before before q) ∧
        Nonempty (Fin (k + 1) ↪ nativeGK4AJOldFiber before before q) := by
  exact ⟨nativeGK4AKOldTarget rot k,
    nativeGK4ALFiberCountable before before (nativeGK4AKOldTarget rot k),
    ⟨nativeGK4AKFiberEmbedding rot k⟩⟩

end GenuineFiniteMatrixFamilies

/-- Unconditional actual physical C60 north specialization:
arbitrarily large finite witnessed subsets in countable fibers. -/
theorem nativeGK4ALPhysicalNorth_arbitrary_finite_countable_fiber (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      Countable (nativeGK4AJOldFiber nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple q) ∧
      Nonempty (Fin (k + 1) ↪ nativeGK4AJOldFiber
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) := by
  exact nativeGK4AL_arbitrary_finite_countable_fiber
    northHexagonNativeLeftRotation k

#print axioms nativeGK4ALFiniteFamilyMatrix
#print axioms nativeGK4ALFiniteFamilyMatrix_decoder
#print axioms nativeGK4ALFiniteFamilyMatrixEmbedding
#print axioms nativeGK4ALFiniteFamilyMatrixNormalForm
#print axioms nativeGK4ALFamilyCovers
#print axioms nativeGK4ALFamilyCovers_iff_matrixCover
#print axioms nativeGK4ALExactFiniteFiberEquivOfCover
#print axioms nativeGK4AL_arbitrary_finite_countable_fiber
#print axioms nativeGK4ALPhysicalNorth_arbitrary_finite_countable_fiber

end
end Kuu.F112.Physical
