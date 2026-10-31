import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4OPrimitiveSeamTransportCriterion

/-!
GK4P compiler contracts, before implementation. These must fail because
GK4P is not implemented yet; no new axiom or proof hole is introduced.
The completed module will retain these same contract examples.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
universe uD vD uE vE

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OBooleanFamily p D E) :=
  nativeGK4P_boolean_kernel

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) :=
  nativeGK4P_option_kernel

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) ∧
      ¬ NativeGK4OGlobalFactors (nativeGK4OOptionFamily p D E) :=
  nativeGK4P_option_kernel_without_descent tree

end Kuu.F112.Physical
