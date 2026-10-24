import Kuu.F112.PolygonNativeF55P94DK5NineCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AG — genuine dependent TEN-cell comparisons

The source-typed conservative TEN-cell presentation relates parallel
genuine NINE-cell evidence on exactly the same dependent EIGHT-cell
boundaries. Its basic constructors are: reflexivity, symmetry,
composition, nine-cell associativity, units and inverses, left and
right 9D vertical congruence, 9D inverse congruence, 8D left/right
whiskering and original 8D inversion congruence.

Prove BOTH the universal noncommutative NINE-cell history word and
signed integer diamond count are conserved by every conservative
10D constructor.  The authentic unitDiamond 9-cell yields two raw
9D pastings with distinct free-group histories and NO 10D filler in
this specified core.

A NEW independent Type-valued 10D squareExchange generator is
adjoined at their exact dependent 9D boundaries. The new syntax is
closed under both 9D and 8D congruences. Coarse diamond count
survives. This is a RELATIVE mathematical result for named
presentations, not a universal 10D no-go or old P92B descent.
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

inductive NativeK5CoreTenCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k},
      NativeK5StructuralNineCell p e d →
      NativeK5StructuralNineCell p e d →
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
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5CoreTenCell p q q
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
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      (H : NativeK5CoreTenCell p q t) :
      NativeK5CoreTenCell p t q
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
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t s : NativeK5StructuralNineCell p e d}
      (H : NativeK5CoreTenCell p q t) (K : NativeK5CoreTenCell p t s) :
      NativeK5CoreTenCell p q s
  | nineAssoc
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
      {e d t x : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) (z : NativeK5StructuralNineCell p d t) (y : NativeK5StructuralNineCell p t x) :
      NativeK5CoreTenCell p (.trans (.trans q z) y) (.trans q (.trans z y))
  | nineLeftUnit
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
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5CoreTenCell p (.trans (.core (.refl e)) q) q
  | nineRightUnit
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
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5CoreTenCell p (.trans q (.core (.refl d))) q
  | nineInverseLeft
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
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5CoreTenCell p (.trans q (.symm q)) (.core (.refl e))
  | nineInverseRight
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
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5CoreTenCell p (.trans (.symm q) q) (.core (.refl d))
  | nineVerticalLeft
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
      {e d t : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d}
      (H : NativeK5CoreTenCell p q z) (suffix : NativeK5StructuralNineCell p d t) :
      NativeK5CoreTenCell p (.trans q suffix) (.trans z suffix)
  | nineVerticalRight
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
      {e d t : NativeK5StructuralEightCell p h k}
      (prior : NativeK5StructuralNineCell p e d)
      {q z : NativeK5StructuralNineCell p d t} (H : NativeK5CoreTenCell p q z) :
      NativeK5CoreTenCell p (.trans prior q) (.trans prior z)
  | nineSymmRespect
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5CoreTenCell p q z) :
      NativeK5CoreTenCell p (.symm q) (.symm z)
  | eightVerticalLeft
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5CoreTenCell p q z)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreTenCell p (.verticalLeft q suffix) (.verticalLeft z suffix)
  | eightVerticalRight
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
      {e d : NativeK5StructuralEightCell p k l}
      (prior : NativeK5StructuralEightCell p h k)
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5CoreTenCell p q z) :
      NativeK5CoreTenCell p (.verticalRight prior q) (.verticalRight prior z)
  | eightInverseRespect
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5CoreTenCell p q z) :
      NativeK5CoreTenCell p (.inverseRespect q) (.inverseRespect z)

/-- Soundness of EVERY core 10D constructor for the chosen
universal FREE GROUP history on genuine 9D witnesses. -/
theorem NativeK5CoreTenCell.historyWord_sound
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
    {e d : NativeK5StructuralEightCell p h k}
    {q z : NativeK5StructuralNineCell p e d}
    (H : NativeK5CoreTenCell p q z) :
    q.historyWord = z.historyWord := by
  induction H with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | nineAssoc q z y =>
      change (q.historyWord * z.historyWord) * y.historyWord =
        q.historyWord * (z.historyWord * y.historyWord)
      exact mul_assoc _ _ _
  | nineLeftUnit q =>
      change (1 : NativeK5NineHistoryWord) * q.historyWord = q.historyWord
      exact one_mul _
  | nineRightUnit q =>
      change q.historyWord * (1 : NativeK5NineHistoryWord) = q.historyWord
      exact mul_one _
  | nineInverseLeft q =>
      change q.historyWord * q.historyWord⁻¹ = (1 : NativeK5NineHistoryWord)
      exact mul_inv_cancel _
  | nineInverseRight q =>
      change q.historyWord⁻¹ * q.historyWord = (1 : NativeK5NineHistoryWord)
      exact inv_mul_cancel _
  | nineVerticalLeft _ suffix ih =>
      exact congrArg (fun t : NativeK5NineHistoryWord =>
        t * suffix.historyWord) ih
  | nineVerticalRight prior _ ih =>
      exact congrArg (fun t : NativeK5NineHistoryWord =>
        prior.historyWord * t) ih
  | nineSymmRespect _ ih =>
      exact congrArg (fun t : NativeK5NineHistoryWord => t⁻¹) ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih =>
      exact congrArg (fun t : NativeK5NineHistoryWord =>
        nativeK5NineFrameLetter * t * nativeK5NineFrameLetter⁻¹) ih

/-- Signed count is also invariant in the conservative grammar. -/
theorem NativeK5CoreTenCell.diamondCount_sound
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
    {e d : NativeK5StructuralEightCell p h k}
    {q z : NativeK5StructuralNineCell p e d}
    (H : NativeK5CoreTenCell p q z) :
    q.diamondCount = z.diamondCount := by
  induction H with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | nineAssoc q z y =>
      change (q.diamondCount + z.diamondCount) + y.diamondCount =
        q.diamondCount + (z.diamondCount + y.diamondCount)
      exact add_assoc _ _ _
  | nineLeftUnit q =>
      change (0 : ℤ) + q.diamondCount = q.diamondCount
      exact zero_add _
  | nineRightUnit q =>
      change q.diamondCount + (0 : ℤ) = q.diamondCount
      exact add_zero _
  | nineInverseLeft q =>
      change q.diamondCount + -q.diamondCount = (0 : ℤ)
      exact add_neg_cancel _
  | nineInverseRight q =>
      change -q.diamondCount + q.diamondCount = (0 : ℤ)
      exact neg_add_cancel _
  | nineVerticalLeft _ suffix ih =>
      exact congrArg (fun t : ℤ => t + suffix.diamondCount) ih
  | nineVerticalRight prior _ ih =>
      exact congrArg (fun t : ℤ => prior.diamondCount + t) ih
  | nineSymmRespect _ ih =>
      exact congrArg (fun t : ℤ => -t) ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- New Type-valued TEN-cell grammar, with INDEPENDENT
source-typed 9D square exchange, not raw equality of 9D witnesses. -/
inductive NativeK5StructuralTenCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k},
      NativeK5StructuralNineCell p e d →
      NativeK5StructuralNineCell p e d →
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5CoreTenCell p q z) :
      NativeK5StructuralTenCell p q z
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
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5StructuralTenCell p (nativeK5NinePastingLeftThenRight q)
        (nativeK5NinePastingRightThenLeft q)
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z) :
      NativeK5StructuralTenCell p z q
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
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q z y : NativeK5StructuralNineCell p e d}
      (H : NativeK5StructuralTenCell p q z) (K : NativeK5StructuralTenCell p z y) :
      NativeK5StructuralTenCell p q y
  | nineVerticalLeft
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
      {e d t : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z)
      (suffix : NativeK5StructuralNineCell p d t) :
      NativeK5StructuralTenCell p (.trans q suffix) (.trans z suffix)
  | nineVerticalRight
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
      {e d t : NativeK5StructuralEightCell p h k}
      (prior : NativeK5StructuralNineCell p e d)
      {q z : NativeK5StructuralNineCell p d t} (H : NativeK5StructuralTenCell p q z) :
      NativeK5StructuralTenCell p (.trans prior q) (.trans prior z)
  | nineSymmRespect
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z) :
      NativeK5StructuralTenCell p (.symm q) (.symm z)
  | eightVerticalLeft
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralTenCell p (.verticalLeft q suffix) (.verticalLeft z suffix)
  | eightVerticalRight
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
      {e d : NativeK5StructuralEightCell p k l}
      (prior : NativeK5StructuralEightCell p h k)
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z) :
      NativeK5StructuralTenCell p (.verticalRight prior q) (.verticalRight prior z)
  | eightInverseRespect
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
      {e d : NativeK5StructuralEightCell p h k}
      {q z : NativeK5StructuralNineCell p e d} (H : NativeK5StructuralTenCell p q z) :
      NativeK5StructuralTenCell p (.inverseRespect q) (.inverseRespect z)

/-- Integer diamond count remains invariant under all NEW
10-cell constructors, including independent squareExchange. -/
theorem NativeK5StructuralTenCell.diamondCount_sound
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
    {e d : NativeK5StructuralEightCell p h k}
    {q z : NativeK5StructuralNineCell p e d}
    (H : NativeK5StructuralTenCell p q z) :
    q.diamondCount = z.diamondCount := by
  induction H with
  | core witness => exact witness.diamondCount_sound
  | squareExchange witness =>
      exact nativeK5NinePasting_integerBlind witness
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | nineVerticalLeft _ suffix ih =>
      exact congrArg (fun t : ℤ => t + suffix.diamondCount) ih
  | nineVerticalRight prior _ ih =>
      exact congrArg (fun t : ℤ => prior.diamondCount + t) ih
  | nineSymmRespect _ ih =>
      exact congrArg (fun t : ℤ => -t) ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- Genuine 10D filler exists in the NEW presentation but cannot
exist in the stated conservative syntax; relative to selected
free-group history and the exact Type-valued 9D boundary. -/
theorem nativeK5NineUnitDiamond_tenRelativeNecessity
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
    Nonempty (NativeK5StructuralTenCell p (nativeK5NinePastingLeftThenRight (NativeK5StructuralNineCell.unitDiamond h)) (nativeK5NinePastingRightThenLeft (NativeK5StructuralNineCell.unitDiamond h))) ∧
    ¬ Nonempty (NativeK5CoreTenCell p (nativeK5NinePastingLeftThenRight (NativeK5StructuralNineCell.unitDiamond h)) (nativeK5NinePastingRightThenLeft (NativeK5StructuralNineCell.unitDiamond h))) := by
  constructor
  · exact ⟨.squareExchange (NativeK5StructuralNineCell.unitDiamond h)⟩
  · rintro ⟨core⟩
    exact nativeK5NineUnitDiamond_pastingWord_ne h core.historyWord_sound

/-- No boundary-preserving retraction from independently adjoined
10D comparison into the explicitly conservative 10D core. -/
theorem nativeK5NineUnitDiamond_tenNoCoreRetraction
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
    ¬ Nonempty
      (NativeK5StructuralTenCell p (nativeK5NinePastingLeftThenRight (NativeK5StructuralNineCell.unitDiamond h)) (nativeK5NinePastingRightThenLeft (NativeK5StructuralNineCell.unitDiamond h)) →
       NativeK5CoreTenCell p (nativeK5NinePastingLeftThenRight (NativeK5StructuralNineCell.unitDiamond h)) (nativeK5NinePastingRightThenLeft (NativeK5StructuralNineCell.unitDiamond h))) := by
  rintro ⟨transport⟩
  obtain ⟨⟨newWitness⟩, noCore⟩ :=
    nativeK5NineUnitDiamond_tenRelativeNecessity h
  exact noCore ⟨transport newWitness⟩

#print axioms NativeK5CoreTenCell
#print axioms NativeK5CoreTenCell.historyWord_sound
#print axioms NativeK5CoreTenCell.diamondCount_sound
#print axioms NativeK5StructuralTenCell
#print axioms NativeK5StructuralTenCell.diamondCount_sound
#print axioms nativeK5NineUnitDiamond_tenRelativeNecessity
#print axioms nativeK5NineUnitDiamond_tenNoCoreRetraction

end
end Kuu.F112.Physical
