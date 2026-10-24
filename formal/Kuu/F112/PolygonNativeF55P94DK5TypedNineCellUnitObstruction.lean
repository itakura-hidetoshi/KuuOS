import Kuu.F112.PolygonNativeF55P94DK5EightCellUnitCriticalPair
import Mathlib.Tactic

/-!
# F112-P94D3AF — conservative typed 9D grammar and universal-word obstruction

The ORIGINAL P94D3AE full eight-cell proof terms (not just their
FreeGroup shadows) are compared by explicit source-dependent 9-cells.
The conservative core contains EIGHT-cell groupoid coherence and
both-sided EIGHT-cell vertical congruence, but not the critical
left/right 7D unit-normalization interchange.

Every constructor preserves the universal FREE-GROUP word on
independent left/right 7D unit-reduction symbols. A finite S₃
representation only certifies that the two free words are unequal.

The extended 9D grammar ADJOINS a genuine independent Type-valued
unitDiamond comparison at exactly the two original 8D paths.
It includes source-typed 8D vertical congruences, inverse respect,
composition, symmetry. This is a new presentation generator,
not a derivation of all arbitrary 8D pastings.
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

/-- A conservative source-typed NINE-cell between two genuinely
dependent, original eight-cell proof witnesses. -/
inductive NativeK5CoreNineCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v},
      NativeK5StructuralEightCell p h k →
      NativeK5StructuralEightCell p h k →
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
      (e : NativeK5StructuralEightCell p h k) :
      NativeK5CoreNineCell p e e
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
      (q : NativeK5CoreNineCell p e d) :
      NativeK5CoreNineCell p d e
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
      {e d t : NativeK5StructuralEightCell p h k}
      (q : NativeK5CoreNineCell p e d)
      (q' : NativeK5CoreNineCell p d t) :
      NativeK5CoreNineCell p e t
  | eightAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l q : NativeK5StructuralSevenCell p u v}
      (e : NativeK5StructuralEightCell p h k)
      (d : NativeK5StructuralEightCell p k l)
      (t : NativeK5StructuralEightCell p l q) :
      NativeK5CoreNineCell p (.trans (.trans e d) t) (.trans e (.trans d t))
  | eightLeftUnit
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
      NativeK5CoreNineCell p (.trans (.core (.refl h)) e) e
  | eightRightUnit
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
      NativeK5CoreNineCell p (.trans e (.core (.refl k))) e
  | eightInverseLeft
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
      NativeK5CoreNineCell p (.trans e (.symm e)) (.core (.refl h))
  | eightInverseRight
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
      NativeK5CoreNineCell p (.trans (.symm e) e) (.core (.refl k))
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
      (q : NativeK5CoreNineCell p e d)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreNineCell p (.trans e suffix) (.trans d suffix)
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
      (prior : NativeK5StructuralEightCell p h k)
      {e d : NativeK5StructuralEightCell p k l}
      (q : NativeK5CoreNineCell p e d) :
      NativeK5CoreNineCell p (.trans prior e) (.trans prior d)
  | eightSymmRespect
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
      (q : NativeK5CoreNineCell p e d) :
      NativeK5CoreNineCell p (.symm e) (.symm d)

/-- The universal free word is preserved by EVERY conservative
9D constructor, including 8D inverse and vertical congruence. -/
theorem NativeK5CoreNineCell.unitWord_sound
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
    (q : NativeK5CoreNineCell p e d) :
    e.unitWord = d.unitWord := by
  induction q with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | eightAssoc e d t =>
      change (e.unitWord * d.unitWord) * t.unitWord =
        e.unitWord * (d.unitWord * t.unitWord)
      exact mul_assoc _ _ _
  | eightLeftUnit e =>
      change (1 : NativeK5EightUnitWord) * e.unitWord = e.unitWord
      exact one_mul _
  | eightRightUnit e =>
      change e.unitWord * (1 : NativeK5EightUnitWord) = e.unitWord
      exact mul_one _
  | eightInverseLeft e =>
      change e.unitWord * e.unitWord⁻¹ = (1 : NativeK5EightUnitWord)
      exact mul_inv_cancel _
  | eightInverseRight e =>
      change e.unitWord⁻¹ * e.unitWord = (1 : NativeK5EightUnitWord)
      exact inv_mul_cancel _
  | eightVerticalLeft _ suffix ih =>
      exact congrArg (fun t : NativeK5EightUnitWord => t * suffix.unitWord) ih
  | eightVerticalRight prior _ ih =>
      exact congrArg (fun t : NativeK5EightUnitWord => prior.unitWord * t) ih
  | eightSymmRespect _ ih =>
      exact congrArg (fun t : NativeK5EightUnitWord => t⁻¹) ih

/-- Even the abelian integer count is invariant under every
conservative 9D constructor (and will survive the new 9D generator). -/
theorem NativeK5CoreNineCell.unitCount_sound
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
    (q : NativeK5CoreNineCell p e d) :
    e.unitCount = d.unitCount := by
  induction q with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | eightAssoc e d t =>
      change (e.unitCount + d.unitCount) + t.unitCount =
        e.unitCount + (d.unitCount + t.unitCount)
      exact add_assoc _ _ _
  | eightLeftUnit e =>
      change (0 : ℤ) + e.unitCount = e.unitCount
      exact zero_add _
  | eightRightUnit e =>
      change e.unitCount + (0 : ℤ) = e.unitCount
      exact add_zero _
  | eightInverseLeft e =>
      change e.unitCount + -e.unitCount = (0 : ℤ)
      exact add_neg_cancel _
  | eightInverseRight e =>
      change -e.unitCount + e.unitCount = (0 : ℤ)
      exact neg_add_cancel _
  | eightVerticalLeft _ suffix ih =>
      exact congrArg (fun t : ℤ => t + suffix.unitCount) ih
  | eightVerticalRight prior _ ih =>
      exact congrArg (fun t : ℤ => prior.unitCount + t) ih
  | eightSymmRespect _ ih =>
      exact congrArg (fun t : ℤ => -t) ih

/-- The two typed 8D unit-normalization paths exhibit a
relative nonexistence of a 9D filler in the explicit core.
This is not a universal no-go for all higher presentations. -/
theorem nativeK5EightUnitPair_noCoreNine
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h0 : NativeK5StructuralSevenCell p u v) :
    ¬ Nonempty (NativeK5CoreNineCell p
      (nativeK5EightUnitLeftFirst h0)
      (nativeK5EightUnitRightFirst h0)) := by
  rintro ⟨q⟩
  exact nativeK5EightUnitPair_word_ne h0 q.unitWord_sound

/-- An independently ADJOINED Type-valued 9D comparison at the
exact original 8D source/target, closed under the fundamental
9D groupoid and vertical 8D congruences. -/
inductive NativeK5StructuralNineCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v},
      NativeK5StructuralEightCell p h k →
      NativeK5StructuralEightCell p h k →
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
      (q : NativeK5CoreNineCell p e d) :
      NativeK5StructuralNineCell p e d
  | unitDiamond
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
      NativeK5StructuralNineCell p (nativeK5EightUnitLeftFirst h)
        (nativeK5EightUnitRightFirst h)
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
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5StructuralNineCell p d e
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
      {e d t : NativeK5StructuralEightCell p h k}
      (q : NativeK5StructuralNineCell p e d)
      (q' : NativeK5StructuralNineCell p d t) :
      NativeK5StructuralNineCell p e t
  | verticalLeft
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
      (q : NativeK5StructuralNineCell p e d)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralNineCell p (.trans e suffix) (.trans d suffix)
  | verticalRight
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
      (prior : NativeK5StructuralEightCell p h k)
      {e d : NativeK5StructuralEightCell p k l}
      (q : NativeK5StructuralNineCell p e d) :
      NativeK5StructuralNineCell p (.trans prior e) (.trans prior d)
  | inverseRespect
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
      NativeK5StructuralNineCell p (.symm e) (.symm d)

/-- Integer unit count persists even after adjoining the new 9D
comparison; it cannot detect the old free-word obstruction. -/
theorem NativeK5StructuralNineCell.unitCount_sound
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
    e.unitCount = d.unitCount := by
  induction q with
  | core w => exact w.unitCount_sound
  | unitDiamond h =>
      obtain ⟨hl, hr⟩ := nativeK5EightUnitPair_sameInteger h
      exact hl.trans hr.symm
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft _ suffix ih =>
      exact congrArg (fun t : ℤ => t + suffix.unitCount) ih
  | verticalRight prior _ ih =>
      exact congrArg (fun t : ℤ => prior.unitCount + t) ih
  | inverseRespect _ ih =>
      exact congrArg (fun t : ℤ => -t) ih

/-- The new 9D unitDiamond exists between the genuinely distinct
eight-cell paths, precisely where the conservative core is blocked. -/
theorem nativeK5EightUnitPair_nineRelativeNecessity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h0 : NativeK5StructuralSevenCell p u v) :
    Nonempty (NativeK5StructuralNineCell p
      (nativeK5EightUnitLeftFirst h0)
      (nativeK5EightUnitRightFirst h0)) ∧
    ¬ Nonempty (NativeK5CoreNineCell p
      (nativeK5EightUnitLeftFirst h0)
      (nativeK5EightUnitRightFirst h0)) := by
  exact ⟨⟨.unitDiamond h0⟩, nativeK5EightUnitPair_noCoreNine h0⟩

#print axioms NativeK5CoreNineCell
#print axioms NativeK5CoreNineCell.unitWord_sound
#print axioms NativeK5CoreNineCell.unitCount_sound
#print axioms nativeK5EightUnitPair_noCoreNine
#print axioms NativeK5StructuralNineCell
#print axioms NativeK5StructuralNineCell.unitCount_sound
#print axioms nativeK5EightUnitPair_nineRelativeNecessity

end
end Kuu.F112.Physical
