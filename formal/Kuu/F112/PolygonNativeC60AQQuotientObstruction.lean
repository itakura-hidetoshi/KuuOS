import Kuu.F112.PolygonNativeC60AQFullPentagonKernelComparison

/-!
F112-P94D3DY — exact quotient obstruction and equality detection.
The obstruction is a kernel of a canonical quotient map, not an
asserted new geometric 19D filler. No new axioms or sorry.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section
universe u
variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A concrete quotient comparison obtained from the already proved
normal-kernel inclusion, without assuming that the kernels coincide. -/
def nativeC60DYComparisonMap (word : List Bool) :
    NativeC60DWContextPentagonQuotient S F word →*
      NativeC60DXFullClosedPentagonQuotient S F :=
  QuotientGroup.map (nativeC60DXImageKernel_le_full S F word)

/-- The canonical comparison is onto; any loss is entirely in its kernel. -/
theorem nativeC60DYComparisonMap_surjective (word : List Bool) :
    Function.Surjective (nativeC60DYComparisonMap S F word) := by
  intro q
  induction q using QuotientGroup.induction_on with
  | _ x =>
    exact ⟨(QuotientGroup.mk'
      (nativeC60DWContextPentagonNormalClosure S F word)) x, rfl⟩

end
#print axioms nativeC60DYComparisonMap
#print axioms nativeC60DYComparisonMap_surjective
end Kuu.F112.Physical
