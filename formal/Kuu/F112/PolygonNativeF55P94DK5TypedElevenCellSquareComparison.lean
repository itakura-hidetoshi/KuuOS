import Kuu.F112.PolygonNativeF55P94DK5TenCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AH — source-typed ELEVEN-cell coherence

The conservative ELEVEN-cell syntax compares genuinely dependent,
ORIGINAL Type-valued TEN-cell witnesses at their exact NINE-cell
source/target. Its primitive rules include:
 * the 10D groupoid relations (associativity, units, inverse laws);
 * left/right 10D composition congruence and 10D symmetry congruence;
 * 9D left/right whiskerings and inversion congruence;
 * original 8D left/right whiskerings and inversion congruence.

Complete structural induction shows all of its generators preserve
both the selected FREE-GROUP 10D history and abelian exchange count.
For the genuinely adjoined 10D squareExchange, the two 10D paths
have distinct history and no conservative ELEVEN-cell comparison.

A new INDEPENDENT Type-valued ELEVEN-cell squareExchange is adjoined
at those exact dependent boundaries, with 10D/9D/8D congruence
closures. It conserves the coarser integer count.

These are relative results for explicitly stated presentations,
NOT universal high-dimensional no-go, automatic global coherence,
old P92B descent, global strict 3/n, or (∞,3)-hyperdescent.
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

/-- Conservative source-dependent ELEVEN-cell, exactly typed on
two original parallel TEN-cell witnesses. -/
inductive NativeK5CoreElevenCell (p : Polygon) :
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
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d},
      NativeK5StructuralTenCell p q t →
      NativeK5StructuralTenCell p q t →
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
      {q t : NativeK5StructuralNineCell p e d}
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5CoreElevenCell p P P
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
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p Q P
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) (K : NativeK5CoreElevenCell p Q R) :
      NativeK5CoreElevenCell p P R
  | tenAssoc
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
      {q t j l : NativeK5StructuralNineCell p e d}
      (P : NativeK5StructuralTenCell p q t)
      (Q : NativeK5StructuralTenCell p t j)
      (R : NativeK5StructuralTenCell p j l) :
      NativeK5CoreElevenCell p (.trans (.trans P Q) R) (.trans P (.trans Q R))
  | tenLeftUnit
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
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5CoreElevenCell p (.trans (.core (.refl q)) P) P
  | tenRightUnit
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
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5CoreElevenCell p (.trans P (.core (.refl t))) P
  | tenInverseLeft
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
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5CoreElevenCell p (.trans P (.symm P)) (.core (.refl q))
  | tenInverseRight
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
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5CoreElevenCell p (.trans (.symm P) P) (.core (.refl t))
  | tenVerticalLeft
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
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5CoreElevenCell p (.trans P suffix) (.trans Q suffix)
  | tenVerticalRight
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
      {q t j : NativeK5StructuralNineCell p e d}
      (prior : NativeK5StructuralTenCell p q t)
      {P Q : NativeK5StructuralTenCell p t j}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.trans prior P) (.trans prior Q)
  | tenSymmRespect
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
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.symm P) (.symm Q)
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
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5CoreElevenCell p (.nineVerticalLeft P suffix) (.nineVerticalLeft Q suffix)
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
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p d j}
      (prior : NativeK5StructuralNineCell p e d)
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.nineVerticalRight prior P) (.nineVerticalRight prior Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.nineSymmRespect P) (.nineSymmRespect Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreElevenCell p (.eightVerticalLeft P suffix) (.eightVerticalLeft Q suffix)
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
      {q t : NativeK5StructuralNineCell p e d}
      (prior : NativeK5StructuralEightCell p h k)
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.eightVerticalRight prior P) (.eightVerticalRight prior Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5CoreElevenCell p (.eightInverseRespect P) (.eightInverseRespect Q)

/-- Soundness of every conservative 11D constructor for the
noncommutative FREE-GROUP history of genuine 10D proof terms. -/
theorem NativeK5CoreElevenCell.historyWord_sound
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
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    (H : NativeK5CoreElevenCell p P Q) :
    P.historyWord = Q.historyWord := by
  induction H with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | tenAssoc P Q R =>
      change (P.historyWord * Q.historyWord) * R.historyWord =
        P.historyWord * (Q.historyWord * R.historyWord)
      exact mul_assoc _ _ _
  | tenLeftUnit P =>
      change (1 : NativeK5TenHistoryWord) * P.historyWord = P.historyWord
      exact one_mul _
  | tenRightUnit P =>
      change P.historyWord * (1 : NativeK5TenHistoryWord) = P.historyWord
      exact mul_one _
  | tenInverseLeft P =>
      change P.historyWord * P.historyWord⁻¹ = (1 : NativeK5TenHistoryWord)
      exact mul_inv_cancel _
  | tenInverseRight P =>
      change P.historyWord⁻¹ * P.historyWord = (1 : NativeK5TenHistoryWord)
      exact inv_mul_cancel _
  | tenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : NativeK5TenHistoryWord =>
        x * suffix.historyWord) ih
  | tenVerticalRight prior _ ih =>
      exact congrArg (fun x : NativeK5TenHistoryWord =>
        prior.historyWord * x) ih
  | tenSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5TenHistoryWord => x⁻¹) ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5TenHistoryWord =>
        nativeK5TenInverseFrame * x * nativeK5TenInverseFrame⁻¹) ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- All conservative 11D constructors also conserve signed
10D square-exchange count, an abelianized observation. -/
theorem NativeK5CoreElevenCell.exchangeCount_sound
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
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    (H : NativeK5CoreElevenCell p P Q) :
    P.exchangeCount = Q.exchangeCount := by
  induction H with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | tenAssoc P Q R =>
      change (P.exchangeCount + Q.exchangeCount) + R.exchangeCount =
        P.exchangeCount + (Q.exchangeCount + R.exchangeCount)
      exact add_assoc _ _ _
  | tenLeftUnit P =>
      change (0 : ℤ) + P.exchangeCount = P.exchangeCount
      exact zero_add _
  | tenRightUnit P =>
      change P.exchangeCount + (0 : ℤ) = P.exchangeCount
      exact add_zero _
  | tenInverseLeft P =>
      change P.exchangeCount + -P.exchangeCount = (0 : ℤ)
      exact add_neg_cancel _
  | tenInverseRight P =>
      change -P.exchangeCount + P.exchangeCount = (0 : ℤ)
      exact neg_add_cancel _
  | tenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.exchangeCount) ih
  | tenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.exchangeCount + x) ih
  | tenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- Independently adjoined source-dependent Type-valued 11D
square exchange and complete low-dimensional congruence closure. -/
inductive NativeK5StructuralElevenCell (p : Polygon) :
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
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d},
      NativeK5StructuralTenCell p q t →
      NativeK5StructuralTenCell p q t →
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5CoreElevenCell p P Q) :
      NativeK5StructuralElevenCell p P Q
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
      {q t : NativeK5StructuralNineCell p e d}
      (P : NativeK5StructuralTenCell p q t) :
      NativeK5StructuralElevenCell p (nativeK5TenPastingLeftThenRight P)
        (nativeK5TenPastingRightThenLeft P)
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
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p Q P
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) (K : NativeK5StructuralElevenCell p Q R) :
      NativeK5StructuralElevenCell p P R
  | tenVerticalLeft
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
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5StructuralElevenCell p (.trans P suffix) (.trans Q suffix)
  | tenVerticalRight
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
      {q t j : NativeK5StructuralNineCell p e d}
      (prior : NativeK5StructuralTenCell p q t)
      {P Q : NativeK5StructuralTenCell p t j}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.trans prior P) (.trans prior Q)
  | tenSymmRespect
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
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.symm P) (.symm Q)
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
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5StructuralElevenCell p (.nineVerticalLeft P suffix) (.nineVerticalLeft Q suffix)
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
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p d j}
      (prior : NativeK5StructuralNineCell p e d)
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.nineVerticalRight prior P) (.nineVerticalRight prior Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.nineSymmRespect P) (.nineSymmRespect Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralElevenCell p (.eightVerticalLeft P suffix) (.eightVerticalLeft Q suffix)
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
      {q t : NativeK5StructuralNineCell p e d}
      (prior : NativeK5StructuralEightCell p h k)
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.eightVerticalRight prior P) (.eightVerticalRight prior Q)
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
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralElevenCell p (.eightInverseRespect P) (.eightInverseRespect Q)

/-- The new 11D grammar preserves total signed 10D exchange
charge; it does NOT identify raw 10D terms by definitional equality. -/
theorem NativeK5StructuralElevenCell.exchangeCount_sound
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
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    (H : NativeK5StructuralElevenCell p P Q) :
    P.exchangeCount = Q.exchangeCount := by
  induction H with
  | core witness => exact witness.exchangeCount_sound
  | squareExchange witness =>
      exact nativeK5TenPasting_integerBlind witness
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | tenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.exchangeCount) ih
  | tenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.exchangeCount + x) ih
  | tenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- Exact relative necessity: genuine eleven-cell comparison
in the extended grammar, no witness in the conservative grammar. -/
theorem nativeK5TenExchange_elevenRelativeNecessity
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
    (q : NativeK5StructuralNineCell p e d) :
    Nonempty (NativeK5StructuralElevenCell p (nativeK5TenPastingLeftThenRight (NativeK5StructuralTenCell.squareExchange q)) (nativeK5TenPastingRightThenLeft (NativeK5StructuralTenCell.squareExchange q))) ∧
    ¬ Nonempty (NativeK5CoreElevenCell p (nativeK5TenPastingLeftThenRight (NativeK5StructuralTenCell.squareExchange q)) (nativeK5TenPastingRightThenLeft (NativeK5StructuralTenCell.squareExchange q))) := by
  constructor
  · exact ⟨.squareExchange (NativeK5StructuralTenCell.squareExchange q)⟩
  · rintro ⟨H⟩
    exact nativeK5TenSquareExchange_pastingWord_ne q H.historyWord_sound

/-- No boundary-preserving map from this independently added
11-cell comparison into the specified conservative 11D core. -/
theorem nativeK5TenExchange_elevenNoCoreRetraction
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
    (q : NativeK5StructuralNineCell p e d) :
    ¬ Nonempty
      (NativeK5StructuralElevenCell p (nativeK5TenPastingLeftThenRight (NativeK5StructuralTenCell.squareExchange q)) (nativeK5TenPastingRightThenLeft (NativeK5StructuralTenCell.squareExchange q)) →
       NativeK5CoreElevenCell p (nativeK5TenPastingLeftThenRight (NativeK5StructuralTenCell.squareExchange q)) (nativeK5TenPastingRightThenLeft (NativeK5StructuralTenCell.squareExchange q))) := by
  rintro ⟨transport⟩
  obtain ⟨⟨new11⟩, noCore⟩ :=
    nativeK5TenExchange_elevenRelativeNecessity q
  exact noCore ⟨transport new11⟩

#print axioms NativeK5CoreElevenCell
#print axioms NativeK5CoreElevenCell.historyWord_sound
#print axioms NativeK5CoreElevenCell.exchangeCount_sound
#print axioms NativeK5StructuralElevenCell
#print axioms NativeK5StructuralElevenCell.exchangeCount_sound
#print axioms nativeK5TenExchange_elevenRelativeNecessity
#print axioms nativeK5TenExchange_elevenNoCoreRetraction

end
end Kuu.F112.Physical
