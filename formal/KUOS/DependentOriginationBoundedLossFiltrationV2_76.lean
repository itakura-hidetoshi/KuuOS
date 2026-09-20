import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationBoundedLossFiltrationV2_76

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

universe u

/-!
# Bounded-loss filtration algebra v2.76

Operations used during transport, composition, or realization may consume a
fixed finite amount of obstruction order. This module records that loss
explicitly and proves that flat defects remain flat under any fixed finite
application of such operations.
-/

/-- A unary operation that consumes a fixed amount of filtration order. -/
structure LossyUnaryOperation
    {D : Type u} (F : ObstructionFiltration D) where
  op : D → D
  loss : ℕ
  map_order :
    ∀ n d,
      F.OrderAtLeast (n + loss) d →
      F.OrderAtLeast n (op d)

/-- A binary operation that consumes a fixed amount of filtration order from
both inputs. -/
structure LossyBinaryOperation
    {D : Type u} (F : ObstructionFiltration D) where
  op : D → D → D
  loss : ℕ
  map_order :
    ∀ n a b,
      F.OrderAtLeast (n + loss) a →
      F.OrderAtLeast (n + loss) b →
      F.OrderAtLeast n (op a b)

namespace LossyUnaryOperation

variable {D : Type u} {F : ObstructionFiltration D}

/-- Flatness absorbs any fixed unary filtration loss. -/
theorem flat_map
    (O : LossyUnaryOperation F) {d : D}
    (hd : F.Flat d) :
    F.Flat (O.op d) := by
  intro n
  exact O.map_order n d (hd (n + O.loss))

/-- Every explicitly finite iterate of a fixed-loss unary operation preserves
flatness. This is not an infinite-iteration or convergence theorem. -/
theorem flat_iterate
    (O : LossyUnaryOperation F) {d : D}
    (hd : F.Flat d) (k : ℕ) :
    F.Flat ((O.op^[k]) d) := by
  induction k generalizing d with
  | zero =>
      simpa using hd
  | succ k ih =>
      rw [Function.iterate_succ_apply]
      exact ih (O.flat_map hd)

end LossyUnaryOperation

namespace LossyBinaryOperation

variable {D : Type u} {F : ObstructionFiltration D}

/-- Flatness absorbs any fixed binary filtration loss. -/
theorem flat_map
    (O : LossyBinaryOperation F) {a b : D}
    (ha : F.Flat a) (hb : F.Flat b) :
    F.Flat (O.op a b) := by
  intro n
  exact O.map_order n a b
    (ha (n + O.loss))
    (hb (n + O.loss))

end LossyBinaryOperation

end KUOS.DependentOriginationBoundedLossFiltrationV2_76
