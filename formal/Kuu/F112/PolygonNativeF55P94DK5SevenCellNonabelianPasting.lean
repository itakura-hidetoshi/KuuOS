import Kuu.F112.PolygonNativeF55P94DK5PentagonatorSevenCellNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AE — two authentic 7-cell pasting orders and nonabelian history

The original P94D3AD dependent seven-cell syntax has two different
pasting orders for h : u ⇒ v and its six-cell-inversion whisker.
Both paths relate the EXACT same original dependent six-cell boundaries
  (u · u⁻¹) ⇒ (v · v⁻¹).
They are NOT definitionally the same seven-cell witness.

Interpret 7D constructor histories in the noncommutative S₃ group.
The primitive target/source comparisons have generators (01)/(12);
seven-cell symmetry and composition map to group inverse/product.
The original 6D inverse-respect whiskering acts by the involutive
inner automorphism induced by (12). Other 6D/5D whiskerings
retain the history. This is an explicit, intentionally selected
source-dependent *syntactic model* for testing a specified 8D
presentation, not an intrinsic unique holonomy nor a theorem
about arbitrary 8D presentations or old P92B.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Nonabelian group of source-typed seven-cell histories. -/
abbrev NativeK5SevenHistoryGroup := Equiv.Perm (Fin 3)

def nativeK5SevenTargetHistoryGenerator : NativeK5SevenHistoryGroup :=
  Equiv.swap (0 : Fin 3) 1

def nativeK5SevenSourceHistoryGenerator : NativeK5SevenHistoryGroup :=
  Equiv.swap (1 : Fin 3) 2

/-- Recursive observer on EXACT Type-valued seven-cell witnesses.
Inversion of the old six-cell boundary acts by conjugation with
a transposition, hence preserves the noncommutative group law. -/
def NativeK5StructuralSevenCell.historyGroup
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) : NativeK5SevenHistoryGroup :=
  match h with
  | .core _ => 1
  | .targetComparison _ _ => nativeK5SevenTargetHistoryGenerator
  | .sourceComparison _ _ => nativeK5SevenSourceHistoryGenerator
  | .symm h => h.historyGroup⁻¹
  | .trans h k => h.historyGroup * k.historyGroup
  | .verticalLeft h _ => h.historyGroup
  | .verticalRight _ h => h.historyGroup
  | .inverseRespect h =>
      nativeK5SevenSourceHistoryGenerator * h.historyGroup *
        nativeK5SevenSourceHistoryGenerator⁻¹
  | .fiveVerticalLeft h _ => h.historyGroup
  | .fiveVerticalRight _ h => h.historyGroup
  | .fiveInverseRespect h => h.historyGroup
  | .precompose _ h => h.historyGroup
  | .postcompose h _ => h.historyGroup

/-- Whisker first along the original six-cell, then along its
inversion: both steps are genuine new SEVEN-cell proofs. -/
def nativeK5SevenPastingLeftThenRight
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    NativeK5StructuralSevenCell p
      (.trans u (.symm u)) (.trans v (.symm v)) :=
  .trans (.verticalLeft h (.symm u))
    (.verticalRight v (.inverseRespect h))

/-- Perform the same two independent whiskerings in the opposite
order. Their dependent six-cell source AND target coincide with
the preceding pasting path, but the raw seven-cell terms do not. -/
def nativeK5SevenPastingRightThenLeft
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    NativeK5StructuralSevenCell p
      (.trans u (.symm u)) (.trans v (.symm v)) :=
  .trans (.verticalRight u (.inverseRespect h))
    (.verticalLeft h (.symm v))

/-- Exact ordered seven-cell history of the first pasting path. -/
theorem nativeK5SevenPastingLeft_history
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5SevenPastingLeftThenRight h).historyGroup =
      h.historyGroup *
        (nativeK5SevenSourceHistoryGenerator * h.historyGroup *
          nativeK5SevenSourceHistoryGenerator⁻¹) := rfl

/-- Exact reversed history, with the SAME genuine 6D endpoints. -/
theorem nativeK5SevenPastingRight_history
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5SevenPastingRightThenLeft h).historyGroup =
      (nativeK5SevenSourceHistoryGenerator * h.historyGroup *
          nativeK5SevenSourceHistoryGenerator⁻¹) * h.historyGroup := rfl

/-- Conjugation by (12) sends (01) to a distinct noncommuting
transposition. This is stronger than a signed integer observer. -/
theorem nativeK5SevenTarget_conjugate_noncommute :
    nativeK5SevenTargetHistoryGenerator *
        (nativeK5SevenSourceHistoryGenerator *
          nativeK5SevenTargetHistoryGenerator *
          nativeK5SevenSourceHistoryGenerator⁻¹) ≠
      (nativeK5SevenSourceHistoryGenerator *
          nativeK5SevenTargetHistoryGenerator *
          nativeK5SevenSourceHistoryGenerator⁻¹) *
        nativeK5SevenTargetHistoryGenerator := by
  unfold nativeK5SevenTargetHistoryGenerator nativeK5SevenSourceHistoryGenerator
  decide

/-- An ACTUAL primitive target-square 7-cell yields two pasting
paths with the exact same dependent 6D boundaries and distinct
noncommutative group histories. In particular, they cannot be
identified as raw Type-valued 7D proof terms. -/
theorem nativeK5TargetSevenPasting_history_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    (nativeK5SevenPastingLeftThenRight
      (NativeK5StructuralSevenCell.targetComparison w v)).historyGroup ≠
    (nativeK5SevenPastingRightThenLeft
      (NativeK5StructuralSevenCell.targetComparison w v)).historyGroup := by
  change nativeK5SevenTargetHistoryGenerator *
        (nativeK5SevenSourceHistoryGenerator *
          nativeK5SevenTargetHistoryGenerator *
          nativeK5SevenSourceHistoryGenerator⁻¹) ≠
      (nativeK5SevenSourceHistoryGenerator *
          nativeK5SevenTargetHistoryGenerator *
          nativeK5SevenSourceHistoryGenerator⁻¹) *
        nativeK5SevenTargetHistoryGenerator
  exact nativeK5SevenTarget_conjugate_noncommute

theorem nativeK5TargetSevenPasting_raw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    nativeK5SevenPastingLeftThenRight
      (NativeK5StructuralSevenCell.targetComparison w v) ≠
    nativeK5SevenPastingRightThenLeft
      (NativeK5StructuralSevenCell.targetComparison w v) := by
  intro heq
  exact nativeK5TargetSevenPasting_history_ne w v (congrArg
    NativeK5StructuralSevenCell.historyGroup heq)

#print axioms NativeK5StructuralSevenCell.historyGroup
#print axioms nativeK5SevenPastingLeftThenRight
#print axioms nativeK5SevenPastingRightThenLeft
#print axioms nativeK5SevenPastingLeft_history
#print axioms nativeK5SevenPastingRight_history
#print axioms nativeK5SevenTarget_conjugate_noncommute
#print axioms nativeK5TargetSevenPasting_history_ne
#print axioms nativeK5TargetSevenPasting_raw_ne

end
end Kuu.F112.Physical
