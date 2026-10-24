import Kuu.F112.PolygonNativeF55P94DK5SevenCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AE — genuine dependent 8D comparison and relative obstruction

Define the conservative source-typed EIGHT-cell syntax on raw 7D
proof witnesses: 7D groupoid laws, congruence in both 7D composition
variables, and the original 6D/5D congruences and 3D whiskerings.
Each constructor conserves the chosen S₃-valued 7D history.
A genuine target-square 7D double-whiskering diamond violates that
history, hence it admits no core 8D filler.

Adjoin a NEW INDEPENDENT source-typed 8D squareExchange comparison,
not a raw 7D equality. This fills the particular diamond by an
actual Type-valued 8-cell. Nonexistence remains relative to the
listed conservative 8D syntax; no universal no-go is claimed.
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

/-- Explicit conservative 8D comparison between genuine parallel
7D evidence on the same EXACT six-cell source and target. -/
inductive NativeK5CoreEightCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z},
      NativeK5StructuralSevenCell p u v →
      NativeK5StructuralSevenCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5CoreEightCell p h h
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p k h
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) (d : NativeK5CoreEightCell p k l) :
      NativeK5CoreEightCell p h l
  | sevenAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v q t : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v)
      (k : NativeK5StructuralSevenCell p v q)
      (l : NativeK5StructuralSevenCell p q t) :
      NativeK5CoreEightCell p (.trans (.trans h k) l) (.trans h (.trans k l))
  | sevenLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5CoreEightCell p (.trans (.core (.refl u)) h) h
  | sevenRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5CoreEightCell p (.trans h (.core (.refl v))) h
  | sevenInverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5CoreEightCell p (.trans h (.symm h)) (.core (.refl u))
  | sevenInverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5CoreEightCell p (.trans (.symm h) h) (.core (.refl v))
  | sevenVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v q t : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k)
      (suffix : NativeK5StructuralSevenCell p v q) :
      NativeK5CoreEightCell p (.trans h suffix) (.trans k suffix)
  | sevenVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v q : NativeK5StructuralSixCell p w z}
      (prior : NativeK5StructuralSevenCell p u v)
      {h k : NativeK5StructuralSevenCell p v q}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.trans prior h) (.trans prior k)
  | sevenSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.symm h) (.symm k)
  | sixVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k)
      (suffix : NativeK5StructuralSixCell p z q) :
      NativeK5CoreEightCell p (.verticalLeft h suffix) (.verticalLeft k suffix)
  | sixVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      (prior : NativeK5StructuralSixCell p w z)
      {u v : NativeK5StructuralSixCell p z q}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.verticalRight prior h) (.verticalRight prior k)
  | sixInverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.inverseRespect h) (.inverseRespect k)
  | fiveVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k)
      (suffix : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5CoreEightCell p (.fiveVerticalLeft h suffix) (.fiveVerticalLeft k suffix)
  | fiveVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p beta gamma}
      (prior : NativeK5StructuralFiveCell p alpha beta)
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.fiveVerticalRight prior h) (.fiveVerticalRight prior k)
  | fiveInverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.fiveInverseRespect h) (.fiveInverseRespect k)
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p s t}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (prior : NativeF55StructuralComparison p r s)
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5CoreEightCell p (.precompose prior h) (.precompose prior k)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5CoreEightCell p (.postcompose h suffix) (.postcompose k suffix)

/-- Every old conservative 8D constructor is sound for the
noncommutative 7D history model, including the conjugation
automorphism along original six-cell inverse respect. -/
theorem NativeK5CoreEightCell.historyGroup_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    (e : NativeK5CoreEightCell p h k) :
    h.historyGroup = k.historyGroup := by
  induction e with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | sevenAssoc h k l =>
      change (h.historyGroup * k.historyGroup) * l.historyGroup =
        h.historyGroup * (k.historyGroup * l.historyGroup)
      exact mul_assoc _ _ _
  | sevenLeftUnit h =>
      change (1 : NativeK5SevenHistoryGroup) * h.historyGroup = h.historyGroup
      exact one_mul _
  | sevenRightUnit h =>
      change h.historyGroup * (1 : NativeK5SevenHistoryGroup) = h.historyGroup
      exact mul_one _
  | sevenInverseLeft h =>
      change h.historyGroup * h.historyGroup⁻¹ = (1 : NativeK5SevenHistoryGroup)
      exact mul_inv_cancel _
  | sevenInverseRight h =>
      change h.historyGroup⁻¹ * h.historyGroup = (1 : NativeK5SevenHistoryGroup)
      exact inv_mul_cancel _
  | sevenVerticalLeft _ suffix ih =>
      exact congrArg (fun g : NativeK5SevenHistoryGroup => g * suffix.historyGroup) ih
  | sevenVerticalRight prior _ ih =>
      exact congrArg (fun g : NativeK5SevenHistoryGroup => prior.historyGroup * g) ih
  | sevenSymmRespect _ ih =>
      exact congrArg (fun g : NativeK5SevenHistoryGroup => g⁻¹) ih
  | sixVerticalLeft _ suffix ih => exact ih
  | sixVerticalRight prior _ ih => exact ih
  | sixInverseRespect _ ih =>
      exact congrArg
        (fun g : NativeK5SevenHistoryGroup =>
          nativeK5SevenSourceHistoryGenerator * g *
            nativeK5SevenSourceHistoryGenerator⁻¹) ih
  | fiveVerticalLeft _ suffix ih => exact ih
  | fiveVerticalRight prior _ ih => exact ih
  | fiveInverseRespect _ ih => exact ih
  | precompose prior _ ih => exact ih
  | postcompose _ suffix ih => exact ih

/-- Genuine source-typed 8D extension: the independent interchange
generator is ADJOINED, not claimed to be derivable from core 8D laws. -/
inductive NativeK5StructuralEightCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z},
      NativeK5StructuralSevenCell p u v →
      NativeK5StructuralSevenCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | core
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5CoreEightCell p h k) :
      NativeK5StructuralEightCell p h k
  | squareExchange
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralEightCell p
        (nativeK5SevenPastingLeftThenRight h)
        (nativeK5SevenPastingRightThenLeft h)
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      (e : NativeK5StructuralEightCell p h k) :
      NativeK5StructuralEightCell p k h
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      (e : NativeK5StructuralEightCell p h k)
      (d : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralEightCell p h l

/-- A primitive target-comparison square creates a genuine 8D
boundary that the specified conservative 8D grammar cannot fill,
although the extended grammar contains a source-typed comparison. -/
theorem nativeK5TargetEightSquare_relativeNecessity
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
    Nonempty (NativeK5StructuralEightCell p
      (nativeK5SevenPastingLeftThenRight (NativeK5StructuralSevenCell.targetComparison w v)) (nativeK5SevenPastingRightThenLeft (NativeK5StructuralSevenCell.targetComparison w v))) ∧
    ¬ Nonempty (NativeK5CoreEightCell p
      (nativeK5SevenPastingLeftThenRight (NativeK5StructuralSevenCell.targetComparison w v)) (nativeK5SevenPastingRightThenLeft (NativeK5StructuralSevenCell.targetComparison w v))) := by
  constructor
  · exact ⟨.squareExchange (NativeK5StructuralSevenCell.targetComparison w v)⟩
  · rintro ⟨e⟩
    exact nativeK5TargetSevenPasting_history_ne w v e.historyGroup_sound

/-- A boundary-preserving map BACK into the specified core 8D
grammar would contradict the noncommutative history obstruction.
No statement is made about the still-unbuilt P92B 8D carrier. -/
theorem nativeK5TargetEightSquare_coreNoRetraction
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
    ¬ Nonempty
      (NativeK5StructuralEightCell p (nativeK5SevenPastingLeftThenRight (NativeK5StructuralSevenCell.targetComparison w v)) (nativeK5SevenPastingRightThenLeft (NativeK5StructuralSevenCell.targetComparison w v)) →
        NativeK5CoreEightCell p (nativeK5SevenPastingLeftThenRight (NativeK5StructuralSevenCell.targetComparison w v)) (nativeK5SevenPastingRightThenLeft (NativeK5StructuralSevenCell.targetComparison w v))) := by
  rintro ⟨transport⟩
  obtain ⟨⟨exchange⟩, noCore⟩ :=
    nativeK5TargetEightSquare_relativeNecessity w v
  exact noCore ⟨transport exchange⟩

#print axioms NativeK5CoreEightCell
#print axioms NativeK5CoreEightCell.historyGroup_sound
#print axioms NativeK5StructuralEightCell
#print axioms nativeK5TargetEightSquare_relativeNecessity
#print axioms nativeK5TargetEightSquare_coreNoRetraction

end
end Kuu.F112.Physical
