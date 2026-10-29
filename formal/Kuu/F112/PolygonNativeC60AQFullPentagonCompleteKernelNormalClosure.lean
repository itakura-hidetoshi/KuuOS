import Kuu.F112.PolygonNativeC60AQFullPentagonOldNewTypedFaithfulnessComparison

/-! F112-P94D3FO: regression obligations before the exact kernel implementation.
No placeholder axioms or admitted proofs. The baseline must fail because these
new declarations are not yet implemented. Copyright Hidetoshi Itakura. -/
namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
universe u v

example {A : Type u} {B : Type v} (f : A → B) :
    (FreeGroup.map f).ker = nativeC60DTNormalClosure
      {pair : FreeGroup A × FreeGroup A |
        ∃ a b : A, f a = f b ∧ pair = (FreeGroup.of a, FreeGroup.of b)} :=
  nativeC60FOFreeMap_ker_eq_normalClosure f

#check nativeC60FOFullTransport_kernel_eq_normalClosure
#check nativeC60FOReceiver_descends_iff_code_fibers
end Kuu.F112.Physical
