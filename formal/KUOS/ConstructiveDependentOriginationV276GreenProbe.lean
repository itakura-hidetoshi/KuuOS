import KUOS.DependentOriginationBoundedLossFiltrationV2_76

namespace KUOS.DependentOriginationBoundedLossFiltrationV2_76

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

universe u
variable {D : Type u} {F : ObstructionFiltration D}

example
    (O : LossyUnaryOperation F)
    {d : D} (hd : F.Flat d) :
    F.Flat (O.op d) :=
  O.flat_map hd

example
    (O : LossyUnaryOperation F)
    {d : D} (hd : F.Flat d)
    (k : Nat) :
    F.Flat ((O.op^[k]) d) :=
  O.flat_iterate hd k

example
    (O : LossyBinaryOperation F)
    {a b : D} (ha : F.Flat a) (hb : F.Flat b) :
    F.Flat (O.op a b) :=
  O.flat_map ha hb

end KUOS.DependentOriginationBoundedLossFiltrationV2_76
