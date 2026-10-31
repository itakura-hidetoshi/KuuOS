import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AKUnboundedFiniteFibers
import Mathlib.Tactic

/-!
F112-P94D3GK4AL — every actual typed K_AI -> K_AG forgetful fiber
is countable, with a faithful matrix code and exact equivalence to
the *attained* set of second integer 2x2 matrices.
The result applies to arbitrary original F45 source/target trees,
without a LocalRotation or any choice of a particular attained q_k.
Combines the already-proved genuine AJ fiber-matrix injectivity and
the actual countability of ((Int x Int) x (Int x Int)).
It does not assert that every integer matrix is attained, that any
one fiber is infinite, or that original S -> K_AI is faithful.
No original P92B Q category axioms, Gray, fillers or hyperdescent.
Append-only, same-root107. Strict 空 central; independent Kuu is
one presentation. Validation-only PR #1558 remains draft/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
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

section AllTypedFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- True injection of a fixed original typed fiber into the full
second 2x2 integer matrix carrier; no abstract Hom is substituted. -/
def nativeGK4ALFiberMatrixEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪ NativeGK4AHMatrix where
  toFun := nativeGK4AJFiberMatrix first last target
  inj' := nativeGK4AJFiberMatrix_injective first last target

/-- Every actual forgotten fiber is at most countable, even without
a physical LocalRotation. Countability follows from an exact
within-fiber matrix injection, not source syntax counting. -/
theorem nativeGK4ALFiberCountable
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    Countable (nativeGK4AJOldFiber first last target) := by
  exact (nativeGK4AJFiberMatrix_injective first last target).countable

/-- Canonical carrier of actual attained matrix values above q.
This is generally a proper subset of all integer matrices. -/
def nativeGK4ALAttainedMatrixSet
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  Set.range (nativeGK4AJFiberMatrix first last target)

/-- An exact normal form *relative to attained values*: a real
fiber element is equivalent to its unique attained second matrix. -/
def nativeGK4ALFiberAttainedMatrixEquiv
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {M : NativeGK4AHMatrix // M ∈ nativeGK4ALAttainedMatrixSet first last target} :=
  nativeGK4AJFiberMatrixImageEquiv first last target

/-- The full new second kernel on each original typed Hom is itself
countable: its genuine full joint observation is injective. -/
theorem nativeGK4ALKernelHomCountable :
    Countable (NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) := by
  exact (nativeGK4AIKernelValue_injective first last).countable

end AllTypedFibers

#print axioms nativeGK4ALFiberMatrixEmbedding
#print axioms nativeGK4ALFiberCountable
#print axioms nativeGK4ALAttainedMatrixSet
#print axioms nativeGK4ALFiberAttainedMatrixEquiv
#print axioms nativeGK4ALKernelHomCountable

end
end Kuu.F112.Physical
