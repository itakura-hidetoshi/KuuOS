import Kuu.F112.PolygonNativeC60AQFullPentagonRecursiveGeneratorReflection

/-!
# F112-P94D3FI — regression goals for complete dependent reflection

These checks use the genuine original and separately context-closed
18D alphabets. No frame injectivity or 19D filler is postulated.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
noncomputable section
universe u

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

example (word : List Bool) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) ↔
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word) :=
  nativeC60FICompleteCode_injective_iff_context S F word

example (word : List Bool) :
    Function.Injective (nativeC60DVFullWordTransport S F word) ↔
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word) :=
  nativeC60FIFullFree_injective_iff_context S F word

example : Function.Injective (nativeC60DVFullWordTransport S F []) :=
  nativeC60FIFullFree_nil_injective S F

example :
    (∀ word : List Bool,
      Function.Injective (nativeC60DVFullWordTransport S F word)) ↔
      Function.Injective ((nativeC60DRSeventeenFrame S F false).mapTotal) ∧
      Function.Injective ((nativeC60DRSeventeenFrame S F true).mapTotal) :=
  nativeC60FIAllFullFree_injective_iff_singletons S F

end
end Kuu.F112.Physical
